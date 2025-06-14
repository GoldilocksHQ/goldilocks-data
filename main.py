import json
from src.managers.people_manager import PeopleManager
from src.managers.organisation_manager import OrganisationManager
from src.utils.logging import logger


def main():
    """
    Main function to run the data processing pipeline.
    This function loads the example data, initializes the managers,
    and processes the data for both people and organisations.
    """
    logger.info("Starting data processing pipeline...")

    # Load example data
    file_path = "data_schema/example/search_profile_response_full_eg3.json"
    try:
        with open(file_path, "r") as f:
            example_data = json.load(f)
        logger.info("Successfully loaded example data.")
    except FileNotFoundError:
        logger.error(f"The data file was not found at the specified path: {file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from the file: {file_path}")
        return

    # Initialize managers
    try:
        org_manager = OrganisationManager()
        people_manager = PeopleManager(org_manager)
        logger.info("Managers initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize managers: {e}", exc_info=True)
        return

    # Process each person record from the 'results' field of the example data
    results = example_data.get("results", [])
    if not results:
        logger.warning(
            "No person records found in the 'results' field of the data file."
        )
        return

    for person_record in results:
        people_manager.process_person_data(person_record)

    logger.info("Data processing pipeline finished.")


if __name__ == "__main__":
    main()
