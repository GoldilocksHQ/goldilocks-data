import logging
import time
import json
from math import ceil
import argparse
import concurrent.futures

from src.managers.profile_search_manager import ProfileSearchManager
from src.utils.progress_tracker import ProgressTracker
from src.utils.parameter_provider import ParameterProvider
from src.utils.failed_request_logger import setup_failed_request_logger
import src.config.extraction_config as config

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
OUTPUT_DIR = "/Volumes/PSSD/goldilocks/data/neuron360/profile_search_uk_results"
TRACKER = ProgressTracker()
MANAGER = ProfileSearchManager(output_dir=OUTPUT_DIR)
PARAMETER_PROVIDER = ParameterProvider()
IS_DRY_RUN = False


def mass_request_pages(params: dict, total_profiles: int):
    """
    Fetches all pages for a workable parameter set.
    This function is executed by a worker thread.
    """
    # Each thread needs its own manager instance for thread safety
    manager = ProfileSearchManager(output_dir=OUTPUT_DIR)

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
                # Calculate the exact size for the last page to avoid over-fetching
                last_page_size = total_profiles % PAGE_SIZE
                if last_page_size == 0:
                    last_page_size = PAGE_SIZE
                current_page_size = last_page_size

            time.sleep(REQUEST_DELAY_SECONDS)
            logging.debug(
                f"Requesting page {page_num}/{last_page} with size {current_page_size} for params: {params}"
            )
            manager.search(
                page_number=page_num,
                page_size=current_page_size,
                parameters=params,
            )
            TRACKER.update_page_progress(params, page_num)
        except Exception as e:
            logging.error(
                "A non-retryable error occurred during mass request for "
                f"{params} on page {page_num}: {e}"
            )
            FAILED_REQUEST_LOGGER.error(
                f"Failed mass request: PARAMS={params}, PAGE={page_num}, ERROR={e}"
            )
            TRACKER.mark_failed(params)
            break
    else:
        TRACKER.mark_completed(params)
        logging.info(f"Successfully completed all pages for parameter set: {params}")


def process_layer(current_params: dict, layer_index: int, executor):
    """
    Recursively processes each layer of the parameter hierarchy.
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
            elif status == "IN_PROGRESS":
                logging.info("Resuming IN_PROGRESS parameter set.")
                executor.submit(
                    mass_request_pages, new_params, int(progress["total_profiles"])
                )
                continue
            elif not progress.get("is_workable"):
                logging.info(
                    "Query previously deemed not workable. Descending to next layer."
                )
                process_layer(new_params, layer_index + 1, executor)
                continue

        # Perform the initial check request
        try:
            time.sleep(REQUEST_DELAY_SECONDS)
            check_response = MANAGER.search(page_size=1, parameters=new_params)
            total_profiles = MANAGER.get_total_profiles(check_response)

            logging.info(f"Check result: {total_profiles} profiles for {new_params}")

            # Case 1: Workable number of profiles
            if 0 < total_profiles < MAX_PROFILES_PER_QUERY:
                TRACKER.log_check(new_params, total_profiles, is_workable=True)
                logging.info("Query is workable. Submitting for mass request.")
                if IS_DRY_RUN:
                    logging.info(
                        f"[DRY RUN] Would execute mass request for: {new_params}"
                    )
                else:
                    executor.submit(mass_request_pages, new_params, total_profiles)

            # Case 2: Zero profiles found
            elif total_profiles == 0:
                TRACKER.log_check(
                    new_params,
                    total_profiles,
                    is_workable=False,
                    status="SKIPPED_NO_RESULT",
                )
                logging.info("Query returned 0 results. Pruning this branch.")
                continue

            # Case 3: Too many profiles (or exactly 10k)
            else:  # total_profiles >= MAX_PROFILES_PER_QUERY
                is_last_layer = layer_index == len(config.PARAMETER_HIERARCHY) - 1
                TRACKER.log_check(
                    new_params,
                    total_profiles,
                    is_workable=False,
                    status="SKIPPED_TOO_LARGE",
                )

                if is_last_layer:
                    logging.warning(
                        "Query too large at the last layer. Proceeding with mass "
                        f"request for first {MAX_PROFILES_PER_QUERY} results."
                    )
                    if IS_DRY_RUN:
                        logging.info(
                            f"[DRY RUN] Would execute mass request for: {new_params}"
                        )
                    else:
                        executor.submit(
                            mass_request_pages, new_params, MAX_PROFILES_PER_QUERY
                        )
                else:
                    logging.info("Query too large. Descending to next layer.")
                    process_layer(new_params, layer_index + 1, executor)

        except Exception as e:
            logging.error(
                f"Initial check failed for parameter set {new_params}. "
                f"Error: {e}. Skipping."
            )
            FAILED_REQUEST_LOGGER.error(
                f"Initial check failed: PARAMS={new_params}, ERROR={e}"
            )
            TRACKER.mark_failed(new_params)
            continue


def main(args):
    """
    Main function to orchestrate the systematic data extraction.
    """
    global IS_DRY_RUN
    IS_DRY_RUN = args.dry_run

    logging.info("--- Starting Systematic Profile Search (Top-Down) ---")
    if IS_DRY_RUN:
        logging.info("****** DRY RUN MODE ENABLED ******")

    TRACKER.load_progress()

    # Start the recursive process from the top layer (index 0)
    base_params = {"countries": [config.STATIC_COUNTRY]}

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        process_layer(base_params, layer_index=0, executor=executor)
        logging.info(
            "All parameter combinations have been explored. Waiting for running downloads to complete..."
        )
        # The 'with' block will implicitly call executor.shutdown(wait=True)

    logging.info("--- Systematic Profile Search Finished ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the systematic Neuron360 profile data extraction script."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Perform a dry run. The script will execute all checks but will not "
            "perform mass page requests."
        ),
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=5,
        help="Number of concurrent worker threads for mass requesting data.",
    )
    args = parser.parse_args()

    main(args)
