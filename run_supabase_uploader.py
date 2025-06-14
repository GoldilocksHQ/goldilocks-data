import argparse
import os
import time
import json
import shutil
import concurrent.futures
from functools import partial

from src.utils.logging import logger
from src.utils.progress_logger import ProgressLogger
from src.managers.people_manager import PeopleManager
from src.managers.organisation_manager import OrganisationManager

# Configure basic logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )

# --- Constants ---
SOURCE_DIR = "data/neuron360/systematic_search_results"
FAILED_DIR = "data/neuron360/failed_uploads"
PROGRESS_CSV_PATH = "data/supabase_upload_progress.csv"


def process_file(file_path: str, progress_logger: ProgressLogger):
    """
    Worker function to process a single JSON file.
    Instantiates its own managers to ensure thread safety.
    """
    logger.info(f"Processing file: {file_path}")
    start_time = time.time()

    # Instantiate managers within the thread for thread safety
    org_manager = OrganisationManager()
    people_manager = PeopleManager(org_manager=org_manager)

    profile_count = 0
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        profile_count = len(data.get("results", []))

        if profile_count == 0:
            logger.warning(f"No profiles found in {file_path}. Deleting empty file.")
            os.remove(file_path)
            return

        progress_logger.log_start(file_path, profile_count)
        success_count, failure_count = people_manager.process_people_from_file(
            file_path
        )

        duration = time.time() - start_time
        if failure_count > 0:
            # Move to failed directory if any record fails
            os.makedirs(FAILED_DIR, exist_ok=True)
            shutil.move(
                file_path, os.path.join(FAILED_DIR, os.path.basename(file_path))
            )
            progress_logger.log_end(
                file_path, success_count, failure_count, duration, "FAILED"
            )
            logger.error(
                "Moved %s to failed directory due to %s processing errors.",
                file_path,
                failure_count,
            )
        else:
            # Delete file on full success
            os.remove(file_path)
            progress_logger.log_end(
                file_path, success_count, failure_count, duration, "COMPLETED"
            )
            logger.info(f"Successfully processed and deleted {file_path}.")

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Critical error processing {file_path}: {e}", exc_info=True)
        os.makedirs(FAILED_DIR, exist_ok=True)
        shutil.move(file_path, os.path.join(FAILED_DIR, os.path.basename(file_path)))
        # Log failure for the whole file
        progress_logger.log_end(
            file_path, 0, profile_count, duration, "CRITICAL_FAILURE"
        )


def main(args):
    """
    Main function to orchestrate the processing and uploading of profile data.
    """
    logger.info(f"Starting Supabase uploader with {args.workers} workers.")
    progress_logger = ProgressLogger(PROGRESS_CSV_PATH)
    os.makedirs(SOURCE_DIR, exist_ok=True)

    while True:
        try:
            files_to_process = [
                os.path.join(SOURCE_DIR, f)
                for f in os.listdir(SOURCE_DIR)
                if f.endswith(".json")
            ]

            if not files_to_process:
                logger.info("No new files found. Exiting.")
                break

            logger.info(
                f"Found {len(files_to_process)} files to process in this cycle."
            )

            # We use a partial function to pass the progress_logger to the worker
            worker_func = partial(process_file, progress_logger=progress_logger)

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=args.workers
            ) as executor:
                # map() is lazy, so we wrap it in a list to ensure all tasks are submitted and complete
                list(executor.map(worker_func, files_to_process))

            logger.info("Processing cycle complete. Checking for new files.")

        except Exception as e:
            logger.critical(
                "An unexpected error occurred in the main loop: %s", e, exc_info=True
            )
            time.sleep(60)  # Wait a minute before retrying


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the concurrent Supabase uploader."
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=50,
        help="Number of concurrent threads to use for processing files.",
    )
    args = parser.parse_args()
    main(args)
