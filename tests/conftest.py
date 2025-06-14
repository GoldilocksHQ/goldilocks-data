import pytest
import json
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_path() -> Path:
    """
    Returns the path to the test data directory.
    """
    return Path(__file__).parent.parent / "data_schema" / "example"


@pytest.fixture(scope="session")
def search_profile_response_full_eg1(test_data_path: Path) -> dict:
    """
    Loads the first example of a full search profile response.
    """
    file_path = test_data_path / "search_profile_response_full_eg1.json"
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def single_profile_record(search_profile_response_full_eg1: dict) -> dict:
    """
    Provides a single profile record from the example data.
    """
    return search_profile_response_full_eg1["results"][0]
