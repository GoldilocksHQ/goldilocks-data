import logging
import time
import json
from math import ceil
import argparse

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
REQUEST_DELAY_SECONDS = 0.07

# --- Global Components ---
FAILED_REQUEST_LOGGER = setup_failed_request_logger()
OUTPUT_DIR = "data/neuron360/systematic_search_results"
TRACKER = ProgressTracker()
MANAGER = ProfileSearchManager(output_dir=OUTPUT_DIR)
PARAMETER_PROVIDER = ParameterProvider()
IS_DRY_RUN = False


def mass_request_pages(params: dict, total_profiles: int):
    """Fetches all pages for a workable parameter set."""
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
            time.sleep(REQUEST_DELAY_SECONDS)
            logging.debug(
                f"Requesting page {page_num}/{last_page} for params: {params}"
            )
            MANAGER.search(page_number=page_num, page_size=PAGE_SIZE, parameters=params)
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


def process_layer(current_params: dict, layer_index: int):
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
                mass_request_pages(new_params, int(progress["total_profiles"]))
                continue
            elif progress.get("is_workable") == "False":
                logging.info(
                    "Query previously deemed not workable. Descending to next layer."
                )
                process_layer(new_params, layer_index + 1)
                continue

        # Perform the initial check request
        try:
            time.sleep(REQUEST_DELAY_SECONDS)
            check_response = MANAGER.search(page_size=1, parameters=new_params)
            total_profiles = MANAGER.get_total_profiles(check_response)
            is_workable = total_profiles < MAX_PROFILES_PER_QUERY

            TRACKER.log_check(new_params, total_profiles, is_workable)
            logging.info(
                f"Check result: {total_profiles} profiles. Workable: {is_workable}"
            )

            if is_workable:
                if IS_DRY_RUN:
                    logging.info(
                        f"[DRY RUN] Would execute mass request for: {new_params}"
                    )
                else:
                    mass_request_pages(new_params, total_profiles)
            elif layer_index == len(config.PARAMETER_HIERARCHY) - 1:
                logging.warning(
                    "Query not workable at the last layer. Proceeding with mass "
                    f"request for first {MAX_PROFILES_PER_QUERY} results."
                )
                if IS_DRY_RUN:
                    logging.info(
                        f"[DRY RUN] Would execute mass request for: {new_params}"
                    )
                else:
                    mass_request_pages(new_params, total_profiles)
            else:
                logging.info("Query not workable. Descending to next layer.")
                process_layer(new_params, layer_index + 1)

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


def main(is_dry_run: bool):
    """
    Main function to orchestrate the systematic data extraction.
    """
    global IS_DRY_RUN
    IS_DRY_RUN = is_dry_run

    logging.info("--- Starting Systematic Profile Search (Top-Down) ---")
    if IS_DRY_RUN:
        logging.info("****** DRY RUN MODE ENABLED ******")

    TRACKER.load_progress()

    # Start the recursive process from the top layer (index 0)
    base_params = {"countries": [config.STATIC_COUNTRY]}
    process_layer(base_params, layer_index=0)

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
    args = parser.parse_args()

    main(is_dry_run=args.dry_run)
