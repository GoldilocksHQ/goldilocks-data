from src.services.base_service import BaseService
from src.models import organisation as organisation_models


class IdentityService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.identities", model=organisation_models.Identity
        )


class WebAddressService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.web_addresses",
            model=organisation_models.WebAddress,
        )


class EmployeeService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.employees", model=organisation_models.Employee
        )


class SocialLinkService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.social_links", model=organisation_models.SocialLink
        )


class IndustryService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.industries", model=organisation_models.Industry
        )


class PhoneService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.phones", model=organisation_models.Phone
        )


class OfficeService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.offices", model=organisation_models.Office
        )


class OfficeAddressService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.office_addresses",
            model=organisation_models.OfficeAddress,
        )


class OfficeIndustryService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="organisation.office_industries",
            model=organisation_models.OfficeIndustry,
        )
