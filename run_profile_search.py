import logging
import time
from src.managers.profile_search_manager import ProfileSearchManager

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """
    Main function to run a paginated profile search.
    """
    logging.info("Initializing ProfileSearchManager...")
    manager = ProfileSearchManager()

    logging.info("Defining search criteria...")
    search_parameters = {
        "completion_score": [{"value": "0.7", "operator": "greater than"}],
        "last_modified_date": [{"value": "2024-12-12", "operator": "since"}],
        "current_job_titles": [{"value": ["engineer"], "operator": "is one of"}],
        "expertises": [{"value": ["strategy"], "operator": "is one of"}],
        "countries": [{"value": ["United Kingdom"], "operator": "is one of"}],
    }

    logging.info(f"Starting profile search with criteria: {search_parameters}")

    page_number = 1
    page_size = 10
    total_profiles = -1
    last_page = 1  # Initialize to 1 to start the loop

    while page_number <= last_page:
        logging.info(
            f"Fetching page {page_number} of "
            f"{last_page if total_profiles != -1 else 'unknown'}..."
        )
        response = manager.search(
            page_number=page_number,
            page_size=page_size,
            parameters=search_parameters,
        )

        if not response:
            logging.error(
                f"Search failed for page {page_number}. " f"Stopping pagination."
            )
            break

        if total_profiles == -1:
            total_profiles = manager.get_total_profiles(response)
            if total_profiles == 0:
                logging.info("No profiles found matching the criteria.")
                break
            # Calculate the last page, respecting the API's max page limit
            last_page = min((total_profiles + page_size - 1) // page_size, 100)
            logging.info(
                f"Total profiles: {total_profiles}. "
                f"Total pages to fetch: {last_page}"
            )

        page_number += 1
        time.sleep(1)  # Be respectful to the API server

    logging.info("Finished fetching all pages.")


if __name__ == "__main__":
    main()
