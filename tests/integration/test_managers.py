import pytest
from unittest.mock import MagicMock
from src.managers.people_manager import PeopleManager
from src.managers.organisation_manager import OrganisationManager
from src.models import people as people_models
from src.models import organisation as org_models
import uuid


@pytest.fixture
def mock_people_services(mocker):
    """
    Mocks all services used by the PeopleManager.
    """
    mock_identity_service = MagicMock()
    mock_identity = people_models.Identity(people_id=uuid.uuid4(), first_name="John")
    mock_identity_service.create.return_value = mock_identity

    mocker.patch(
        "src.managers.people_manager.people_services.IdentityService",
        return_value=mock_identity_service,
    )
    # Add mocks for all other services used in PeopleManager
    mocker.patch("src.managers.people_manager.people_services.ProfileService")
    mocker.patch("src.managers.people_manager.people_services.GenderService")
    mocker.patch("src.managers.people_manager.people_services.SocialLinkService")
    mocker.patch("src.managers.people_manager.people_services.StatusService")
    mocker.patch("src.managers.people_manager.people_services.EmailService")
    mocker.patch("src.managers.people_manager.people_services.PhoneService")
    mocker.patch("src.managers.people_manager.people_services.AddressService")
    mocker.patch("src.managers.people_manager.people_services.ExperienceService")
    mocker.patch("src.managers.people_manager.people_services.JobTitleDetailService")
    mocker.patch("src.managers.people_manager.people_services.JobFunctionService")
    mocker.patch("src.managers.people_manager.people_services.JobSeniorityService")
    mocker.patch("src.managers.people_manager.people_services.EducationService")
    mocker.patch(
        "src.managers.people_manager.people_services.EducationWebAddressService"
    )
    mocker.patch("src.managers.people_manager.people_services.CertificationService")
    mocker.patch(
        "src.managers.people_manager.people_services.CertificationWebAddressService"
    )
    mocker.patch("src.managers.people_manager.people_services.MembershipService")
    mocker.patch(
        "src.managers.people_manager.people_services.MembershipWebAddressService"
    )
    mocker.patch("src.managers.people_manager.people_services.PublicationService")
    mocker.patch(
        "src.managers.people_manager.people_services.PublicationWebAddressService"
    )
    mocker.patch("src.managers.people_manager.people_services.PatentService")
    mocker.patch("src.managers.people_manager.people_services.PatentWebAddressService")
    mocker.patch("src.managers.people_manager.people_services.AwardService")

    return {"identity_service": mock_identity_service}


def test_people_manager_processing(single_profile_record, mock_people_services):
    """
    Tests the main processing logic of the PeopleManager.
    """
    people_manager = PeopleManager()

    people_manager.process_person_data(single_profile_record["profile_data"])

    mock_people_services["identity_service"].create.assert_called_once()


@pytest.fixture
def mock_org_services(mocker):
    """
    Mocks all services used by the OrganisationManager.
    """
    mock_identity_service = MagicMock()
    mock_identity = org_models.Identity(organisation_id=uuid.uuid4(), name="TestCorp")
    mock_identity_service.upsert.return_value = mock_identity

    mocker.patch(
        "src.managers.organisation_manager.organisation_services.IdentityService",
        return_value=mock_identity_service,
    )
    mocker.patch(
        "src.managers.organisation_manager.organisation_services.WebAddressService"
    )
    mocker.patch(
        "src.managers.organisation_manager.organisation_services.EmployeeService"
    )
    mocker.patch(
        "src.managers.organisation_manager.organisation_services.SocialLinkService"
    )
    mocker.patch(
        "src.managers.organisation_manager.organisation_services.IndustryService"
    )
    mocker.patch("src.managers.organisation_manager.organisation_services.PhoneService")
    mocker.patch(
        "src.managers.organisation_manager.organisation_services.OfficeService"
    )
    mocker.patch(
        "src.managers.organisation_manager.organisation_services.OfficeAddressService"
    )
    mocker.patch(
        "src.managers.organisation_manager.organisation_services.OfficeIndustryService"
    )

    return {"identity_service": mock_identity_service}


def test_organisation_manager_processing(single_profile_record, mock_org_services):
    """
    Tests the main processing logic of the OrganisationManager.
    """
    org_manager = OrganisationManager()

    experience_data = single_profile_record["contact_data"][
        "contact_current_experiences"
    ][0]
    org_manager.process_organisation_data(experience_data)

    mock_org_services["identity_service"].upsert.assert_called_once()
