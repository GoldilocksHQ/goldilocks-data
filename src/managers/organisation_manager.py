from src.managers.base_manager import BaseManager
from src.services import organisation_services
from src.models import organisation as org_models
from typing import Dict, Any


class OrganisationManager(BaseManager):
    """
    Manages the processing and persistence of organisation-related data.
    """

    def __init__(self):
        super().__init__()
        # Initialize all organisation services
        self.identity_service = organisation_services.IdentityService()
        self.web_address_service = organisation_services.WebAddressService()
        self.employee_service = organisation_services.EmployeeService()
        self.social_link_service = organisation_services.SocialLinkService()
        self.industry_service = organisation_services.IndustryService()
        self.phone_service = organisation_services.PhoneService()
        self.office_service = organisation_services.OfficeService()
        self.office_address_service = organisation_services.OfficeAddressService()
        self.office_industry_service = organisation_services.OfficeIndustryService()

    def process_organisation_data(self, exp_data: Dict[str, Any]):
        """
        Processes and persists a single organisation's data from an experience entry.
        It creates the organisation identity and all related sub-records.
        """
        try:
            neuron_id = exp_data.get("company_id")
            if not neuron_id:
                # self.logger.warning("Skipping organisation processing: 'company_id' is missing.")
                return

            # Check if an organisation with this neuron360_company_id already exists
            existing_identity = self.identity_service.get_by_neuron_id(neuron_id)
            if existing_identity:
                self._log_success(
                    f"Skipping existing Organisation with neuron_id: {neuron_id}"
                )
                return

            # 1. Create Organisation Identity
            identity_model = org_models.Identity(
                neuron360_company_id=neuron_id,
                name=exp_data.get("company_name"),
                domain=exp_data.get("company_domain"),
                logo_url=exp_data.get("company_logo_url"),
                industry=exp_data.get("company_industry"),
            )
            created_identity = self.identity_service.create(identity_model)

            if not created_identity:
                self._log_error(
                    f"Failed to create organisation identity for neuron_id: {neuron_id}."
                )
                return

            org_id = created_identity.organisation_id
            self._log_success(f"Created new Organisation with ID: {org_id}")

            # 2. Process related organisation data
            self._process_organisation_details(exp_data, org_id)

            # 3. Process Office data
            if exp_data.get("office_id"):
                self._process_office(exp_data, org_id)

        except Exception as e:
            self._log_error(
                f"An error occurred during organisation data processing: {e}",
                exc_info=True,
            )

    def _process_organisation_details(
        self, company_details: Dict[str, Any], org_id: Any
    ):
        if company_details.get("company_web_address"):
            web_addr = org_models.WebAddress(
                organisation_id=org_id, **company_details["company_web_address"]
            )
            self.web_address_service.create(web_addr)

        if company_details.get("company_employees"):
            emp = org_models.Employee(
                organisation_id=org_id, **company_details["company_employees"]
            )
            self.employee_service.create(emp)

        if company_details.get("company_social_links"):
            social_links_data = {
                f"{key}_url": value.get("url")
                for key, value in company_details["company_social_links"].items()
                if value and "url" in value
            }
            sl = org_models.SocialLink(organisation_id=org_id, **social_links_data)
            self.social_link_service.create(sl)

        if company_details.get("company_industries"):
            for industry_data in company_details["company_industries"]:
                ind_data = industry_data.copy()
                if "id" in ind_data:
                    ind_data["industry_id"] = ind_data.pop("id")
                for key, value in ind_data.items():
                    if key.startswith("code") and value is not None:
                        ind_data[key] = str(value)
                ind = org_models.Industry(organisation_id=org_id, **ind_data)
                self.industry_service.create(ind)

        if company_details.get("company_phones"):
            for phone_data in company_details["company_phones"]:
                phone = org_models.Phone(organisation_id=org_id, **phone_data)
                self.phone_service.create(phone)

    def _process_office(self, office_details: Dict[str, Any], org_id: Any):
        office_data = {
            "organisation_id": org_id,
            "neuron360_office_id": office_details.get("office_id"),
            "name": office_details.get("office_name"),
            "type": office_details.get("office_type"),
            "is_hq": office_details.get("is_hq"),
            "is_active": office_details.get("is_active"),
        }
        office_model = org_models.Office(
            **{k: v for k, v in office_data.items() if v is not None}
        )

        # Check if office exists before creating
        existing_office = self.office_service.get_by_neuron_id(
            office_model.neuron360_office_id
        )
        if existing_office:
            office_id = existing_office.office_id
        else:
            created_office = self.office_service.create(office_model)
            if not created_office:
                self._log_error(
                    f"Failed to create office for neuron_id: {office_model.neuron360_office_id}"
                )
                return
            office_id = created_office.office_id

        self._log_success(f"Processed Office with ID: {office_id}")

        if office_details.get("office_address"):
            addr = org_models.OfficeAddress(
                office_id=office_id, **office_details["office_address"]
            )
            self.office_address_service.create(addr)

        if office_details.get("office_phones"):
            for phone_data in office_details["office_phones"]:
                phone = org_models.Phone(organisation_id=org_id, **phone_data)
                self.phone_service.create(phone)

        if office_details.get("office_industries"):
            for industry in office_details["office_industries"]:
                ind_data = industry.copy()
                if "id" in ind_data:
                    ind_data["industry_id"] = ind_data.pop("id")
                for key, value in ind_data.items():
                    if key.startswith("code") and value is not None:
                        ind_data[key] = str(value)
                oi = org_models.OfficeIndustry(office_id=office_id, **ind_data)
                self.office_industry_service.create(oi)
