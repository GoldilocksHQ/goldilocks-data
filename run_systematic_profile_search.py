import logging
import time
import json
import threading
import queue
from math import ceil
import argparse

from src.managers.profile_search_manager import ProfileSearchManager
from src.utils.progress_tracker import ProgressTracker
from src.utils.parameter_provider import ParameterProvider
from src.utils.failed_request_logger import setup_failed_request_logger
from src.utils.file_utils import save_json_response
import src.config.extraction_config as config
from src.config.path_config import UK_PROFILES_DIR

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Constants ---
MAX_PROFILES_PER_QUERY = 10000
PAGE_SIZE = 100
REQUEST_DELAY_SECONDS = 0.00

# --- Global Components ---
FAILED_REQUEST_LOGGER = setup_failed_request_logger()
OUTPUT_DIR = UK_PROFILES_DIR
TRACKER = ProgressTracker()
# Main thread manager for initial checks
MAIN_THREAD_MANAGER = ProfileSearchManager(output_dir=OUTPUT_DIR)
PARAMETER_PROVIDER = ParameterProvider()
IS_DRY_RUN = False


def mass_request_pages(
    params: dict,
    total_profiles: int,
    results_queue: queue.Queue,
    progress_queue: queue.Queue,
):
    """
    Fetches all pages for a single workable parameter set.
    This function is executed by a worker thread from the pool.
    """
    # Each thread needs its own manager instance for thread safety
    thread_manager = ProfileSearchManager(output_dir=OUTPUT_DIR)

    last_page = min(ceil(total_profiles / PAGE_SIZE), 100)
    progress = TRACKER.get_progress(params)
    start_page = int(progress.get("last_completed_page", 0)) + 1

    logging.info(
        (
            f"Starting mass request for {total_profiles} profiles across "
            f"{last_page} pages. Starting from page {start_page}."
        )
    )

    for page_num in range(start_page, last_page + 1):
        try:
            current_page_size = PAGE_SIZE
            if page_num == last_page:
                last_page_size = total_profiles % PAGE_SIZE
                if last_page_size == 0:
                    last_page_size = PAGE_SIZE
                current_page_size = last_page_size

            time.sleep(REQUEST_DELAY_SECONDS)
            response_data = thread_manager.search(
                page_number=page_num,
                page_size=current_page_size,
                parameters=params,
            )
            # Put data and progress updates onto queues
            if response_data:
                results_queue.put((response_data, params))
                logging.info(
                    f"[Downloader] Queued page {page_num} for writing. Params: {params}"
                )
            progress_queue.put(("PAGE_UPDATE", params, {"page_number": page_num}))

        except Exception as e:
            logging.error(
                "A non-retryable error occurred during mass request for "
                f"{params} on page {page_num}: {e}"
            )
            FAILED_REQUEST_LOGGER.error(
                f"Failed mass request: PARAMS={params}, PAGE={page_num}, ERROR={e}"
            )
            progress_queue.put(("FAILED", params, {"failed_at_page": page_num}))
            return  # Exit for this parameter set on failure

    progress_queue.put(("COMPLETED", params, {}))
    logging.info(f"Successfully queued all pages for parameter set: {params}")


def process_layer(current_params: dict, layer_index: int, work_queue: queue.Queue):
    """
    Recursively processes each layer of the parameter hierarchy. (Producer)
    """
    if layer_index >= len(config.PARAMETER_HIERARCHY):
        logging.info("Reached the bottom of the hierarchy.")
        return

    layer_name = config.PARAMETER_HIERARCHY[layer_index]
    values_for_layer = PARAMETER_PROVIDER.get_values_for_layer(
        layer_name, current_params
    )

    for value in values_for_layer:
        new_params = current_params.copy()
        new_params[layer_name] = [value] if not isinstance(value, list) else value

        log_msg = (
            f"--- Processing Layer: {layer_name} | Params: {json.dumps(new_params)} ---"
        )
        logging.info(log_msg)

        progress = TRACKER.get_progress(new_params)
        if progress:
            status = progress.get("status")
            if status == "COMPLETED":
                logging.info(
                    "This parameter set is already marked as COMPLETED. Skipping."
                )
                continue
            elif status == "SKIPPED_NO_RESULT":
                logging.info(
                    "Query previously returned 0 results. Pruning this branch."
                )
                continue
            elif status in ["IN_PROGRESS", "PENDING", "FAILED"]:
                logging.info(f"Resuming/Retrying {status} parameter set.")
                if not IS_DRY_RUN:
                    work_queue.put((new_params, int(progress["total_profiles"])))
                continue
            elif status == "SKIPPED_TOO_LARGE":
                logging.info(
                    "Query previously deemed not workable (too large). Descending to next layer."
                )
                process_layer(new_params, layer_index + 1, work_queue)
                continue

        try:
            time.sleep(REQUEST_DELAY_SECONDS)
            check_response = MAIN_THREAD_MANAGER.search(
                page_size=1, parameters=new_params
            )
            total_profiles = MAIN_THREAD_MANAGER.get_total_profiles(check_response)

            logging.info(f"Check result: {total_profiles} profiles for {new_params}")

            if 0 < total_profiles < MAX_PROFILES_PER_QUERY:
                TRACKER.log_check(new_params, total_profiles, is_workable=True)
                logging.info("Query is workable. Submitting for mass request.")
                if not IS_DRY_RUN:
                    logging.info(f"[Producer] ADDING to work_queue: {new_params}")
                    work_queue.put((new_params, total_profiles))

            elif total_profiles == 0:
                TRACKER.log_check(new_params, total_profiles, is_workable=False)
                logging.info("Query returned 0 results. Pruning this branch.")
                continue

            else:  # total_profiles >= MAX_PROFILES_PER_QUERY
                is_last_layer = layer_index == len(config.PARAMETER_HIERARCHY) - 1
                TRACKER.log_check(new_params, total_profiles, is_workable=False)
                if is_last_layer:
                    logging.warning(
                        "Query too large at the last layer. Proceeding with mass request."
                    )
                    if not IS_DRY_RUN:
                        logging.info(
                            f"[Producer] ADDING to work_queue (MAX_PROFILES): {new_params}"
                        )
                        work_queue.put((new_params, MAX_PROFILES_PER_QUERY))
                else:
                    logging.info("Query too large. Descending to next layer.")
                    process_layer(new_params, layer_index + 1, work_queue)

        except Exception as e:
            logging.error(
                f"Initial check failed for {new_params}. Error: {e}. Skipping."
            )
            FAILED_REQUEST_LOGGER.error(
                f"Initial check failed: PARAMS={new_params}, ERROR={e}"
            )
            TRACKER.mark_failed(new_params)
            continue


def producer_worker(work_queue: queue.Queue):
    """The producer thread's target. Runs the recursive layer processing."""
    try:
        logging.info("[Producer] Starting parameter space exploration.")
        base_params = {"countries": [config.STATIC_COUNTRY]}
        process_layer(base_params, layer_index=0, work_queue=work_queue)
        logging.info("[Producer] Finished parameter space exploration.")
    except Exception as e:
        logging.critical(
            f"[Producer] The main producer thread encountered a fatal error: {e}",
            exc_info=True,
        )
    finally:
        # This signals to the main thread that production is done.
        logging.info("[Producer] Signaling work production is complete.")


def file_writer_worker(results_queue: queue.Queue):
    """Worker to write responses from a queue to files."""
    while True:
        try:
            item = results_queue.get()
            if item is None:
                logging.info("[Writer] Received sentinel. Exiting.")
                break
            response_data, params = item
            save_json_response(response_data, OUTPUT_DIR)
            logging.info(f"[Writer] Successfully saved data for {params}")
        except Exception as e:
            logging.error(
                f"[file_writer_worker] Error processing item: {e}", exc_info=True
            )
        finally:
            if item is not None:
                results_queue.task_done()


def progress_logger_worker(progress_queue: queue.Queue):
    """Worker to log progress updates from a queue."""
    while True:
        try:
            item = progress_queue.get()
            if item is None:
                logging.info("Progress logger thread received sentinel. Exiting.")
                break
            event_type, params, data = item
            if event_type == "PAGE_UPDATE":
                TRACKER.update_page_progress(params, data["page_number"])
            elif event_type == "COMPLETED":
                TRACKER.mark_completed(params)
            elif event_type == "FAILED":
                TRACKER.mark_failed(params, data)
        except Exception as e:
            logging.error(
                f"[progress_logger_worker] Error processing item: {e}", exc_info=True
            )
        finally:
            if item is not None:
                progress_queue.task_done()


def downloader_worker(
    work_queue: queue.Queue, results_queue: queue.Queue, progress_queue: queue.Queue
):
    """Worker to download profiles based on work items from a queue."""
    while True:
        try:
            item = work_queue.get()
            if item is None:
                logging.info("Downloader thread received sentinel. Exiting.")
                break
            params, total_profiles = item
            mass_request_pages(params, total_profiles, results_queue, progress_queue)
        except Exception as e:
            logging.error(
                f"[downloader_worker] Unhandled error processing item: {item}. Error: {e}",
                exc_info=True,
            )
        finally:
            if item is not None:
                work_queue.task_done()


def main(args):
    """Main function to orchestrate the systematic data extraction."""
    global IS_DRY_RUN
    IS_DRY_RUN = args.dry_run
    num_downloader_threads = args.threads

    logging.info("--- Starting Systematic Profile Search ---")
    if IS_DRY_RUN:
        logging.info("****** DRY RUN MODE ENABLED ******")

    # CRITICAL FIX: Load all progress from ledgers BEFORE starting any work.
    # This prevents a race condition where the producer starts before the state is known.
    logging.info("Loading previous progress from all ledger files...")
    TRACKER.load_progress()
    logging.info("Progress loading complete.")

    work_queue = queue.Queue(maxsize=1000)
    results_queue = queue.Queue(maxsize=50)
    progress_queue = queue.Queue()

    threads = []

    # Start IO workers
    file_writer = threading.Thread(target=file_writer_worker, args=(results_queue,))
    threads.append(file_writer)
    progress_logger = threading.Thread(
        target=progress_logger_worker, args=(progress_queue,)
    )
    threads.append(progress_logger)

    # Start downloader workers
    for _ in range(num_downloader_threads):
        downloader = threading.Thread(
            target=downloader_worker, args=(work_queue, results_queue, progress_queue)
        )
        threads.append(downloader)

    # Start producer thread
    producer_thread = threading.Thread(target=producer_worker, args=(work_queue,))

    # Start all threads. The main change is that load_progress() is now guaranteed
    # to be finished before the producer thread starts.
    for t in threads:
        t.start()
    producer_thread.start()

    try:
        # Monitor thread health and queue sizes
        while producer_thread.is_alive():
            logging.info(
                f"[Monitor] Queues - Work: {work_queue.qsize()}, "
                f"Results: {results_queue.qsize()}, "
                f"Progress: {progress_queue.qsize()}"
            )
            producer_thread.join(timeout=15)

        logging.info("[Main] Producer thread has finished.")

        # Wait for the downloader queue to be emptied by the downloaders
        logging.info("[Main] Waiting for download queue to empty...")
        work_queue.join()
        logging.info("[Main] Download queue is empty.")

    except KeyboardInterrupt:
        logging.info(
            "\n[Main] KeyboardInterrupt received. Initiating graceful shutdown..."
        )

    finally:
        logging.info("[Main] Starting shutdown sequence.")

        # STAGE 1: Wait for all work to be produced and processed by downloaders.
        # This ensures no data is lost if a downloader has an item but hasn't
        # yet put the result onto the results_queue.
        logging.info("[Main] Waiting for producer and download queue to empty...")
        producer_thread.join()  # Wait for the producer to finish its work.
        work_queue.join()  # Wait for all items in the work queue to be processed.
        logging.info("[Main] All download work has been completed.")

        # STAGE 2: Wait for all results to be written to disk and progress to be logged.
        logging.info("[Main] Waiting for final IO queues to empty...")
        results_queue.join()
        progress_queue.join()
        logging.info("[Main] All IO operations have been completed.")

        # STAGE 3: Now that all work is done, signal all threads to stop.
        logging.info(
            f"[Main] Signaling {num_downloader_threads} downloader threads to stop."
        )
        for _ in range(num_downloader_threads):
            work_queue.put(None)

        logging.info("[Main] Signaling IO threads to stop.")
        results_queue.put(None)
        progress_queue.put(None)

        # Wait for all threads to terminate.
        logging.info("[Main] Waiting for all threads to terminate...")
        all_threads = threads + [producer_thread]
        for t in all_threads:
            if t.is_alive():
                t.join(timeout=10)
        logging.info("[Main] All threads have terminated.")

        # Final state save.
        TRACKER.save_progress()
        logging.info("[Main] Final progress saved.")
        logging.info("--- Systematic Profile Search Finished ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the systematic Neuron360 profile data extraction script."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run. The script will not perform mass page requests.",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=5,
        help="Number of concurrent worker threads for mass requesting data.",
    )
    args = parser.parse_args()
    main(args)
