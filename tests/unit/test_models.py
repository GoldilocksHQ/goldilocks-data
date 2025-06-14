import pytest
from src.models import people as people_models
from src.models import organisation as org_models
import uuid


def test_people_identity_model(single_profile_record):
    """
    Tests the instantiation of the people.Identity model.
    """
    profile_data = single_profile_record["profile_data"]
    identity = people_models.Identity(
        neuron360_profile_id=profile_data.get("profile_id"),
        first_name=profile_data.get("profile_first_name"),
        last_name=profile_data.get("profile_last_name"),
    )
    assert identity.neuron360_profile_id == "prof-shli-1894231214f1c24499892b455cca9e58"
    assert identity.first_name == "Soner"
    assert isinstance(identity.people_id, uuid.UUID)


def test_organisation_identity_model(single_profile_record):
    """
    Tests the instantiation of the organisation.Identity model.
    """
    exp_data = single_profile_record["contact_data"]["contact_current_experiences"][0]
    identity = org_models.Identity(
        neuron360_company_id=exp_data.get("company_id"),
        name=exp_data.get("company_name"),
        domain=exp_data.get("company_domain"),
    )
    assert identity.name == "Makerscafe - Live Laser Engravers For Events"
    assert identity.domain == "makerscafe.com"
    assert isinstance(identity.organisation_id, uuid.UUID)


def test_experience_model(single_profile_record):
    """
    Tests the instantiation of the people.Experience model.
    """
    exp_data = single_profile_record["contact_data"]["contact_current_experiences"][0]
    # A people_id is required for foreign key relation
    dummy_people_id = uuid.uuid4()
    experience = people_models.Experience(people_id=dummy_people_id, **exp_data)

    assert experience.job_title == "Founder"
    assert experience.current is True
    assert experience.people_id == dummy_people_id
