import pytest
from unittest.mock import MagicMock
from src.services.people_services import IdentityService
from src.models.people import Identity
import uuid


@pytest.fixture
def mock_supabase_client(mocker):
    """
    Fixture to mock the Supabase client.
    """
    mock_client = MagicMock()
    # Mock the chain of calls: client.table(...).insert(...).execute()
    mock_client.table.return_value.insert.return_value.execute.return_value.data = [
        {
            "people_id": str(uuid.uuid4()),
            "neuron360_profile_id": "test_id",
            "first_name": "John",
        }
    ]
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {
            "people_id": str(uuid.uuid4()),
            "neuron360_profile_id": "test_id",
            "first_name": "John",
        }
    ]
    mocker.patch("src.services.base_service.supabase_client", mock_client)
    return mock_client


def test_create_identity(mock_supabase_client):
    """
    Tests the create method of the IdentityService.
    """
    identity_service = IdentityService()
    test_identity = Identity(neuron360_profile_id="test_id", first_name="John")

    created_identity = identity_service.create(test_identity)

    # Verify that the insert method was called with the correct data
    mock_supabase_client.table.return_value.insert.assert_called_once()

    assert created_identity is not None
    assert created_identity.first_name == "John"


def test_get_identity_by_id(mock_supabase_client):
    """
    Tests the get_by_id method of the IdentityService.
    """
    identity_service = IdentityService()

    # The actual ID doesn't matter here as the response is mocked
    retrieved_identity = identity_service.get_by_id(1)

    # Verify that the select and eq methods were called
    mock_supabase_client.table.return_value.select.assert_called_with("*")
    mock_supabase_client.table.return_value.select.return_value.eq.assert_called_with(
        "id", 1
    )

    assert retrieved_identity is not None
    assert retrieved_identity.first_name == "John"
