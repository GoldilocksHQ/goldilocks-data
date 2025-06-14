from src.services.base_service import BaseService
from src.models import people as people_models


class IdentityService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.identities", model=people_models.Identity)


class ProfileService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.profiles", model=people_models.Profile)


class GenderService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.genders", model=people_models.Gender)


class SocialLinkService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.social_links", model=people_models.SocialLink
        )


class StatusService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.statuses", model=people_models.Status)


class EmailService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.emails", model=people_models.Email)


class PhoneService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.phones", model=people_models.Phone)


class AddressService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.addresses", model=people_models.Address)


class ExperienceService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.experiences", model=people_models.Experience
        )


class JobTitleDetailService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.job_title_details", model=people_models.JobTitleDetail
        )


class JobFunctionService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.job_functions", model=people_models.JobFunction
        )


class JobSeniorityService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.job_seniority", model=people_models.JobSeniority
        )


class EducationService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.educations", model=people_models.Education)


class EducationWebAddressService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.education_web_addresses",
            model=people_models.EducationWebAddress,
        )


class CertificationService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.certifications", model=people_models.Certification
        )


class CertificationWebAddressService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.certification_web_addresses",
            model=people_models.CertificationWebAddress,
        )


class MembershipService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.memberships", model=people_models.Membership
        )


class MembershipWebAddressService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.membership_web_addresses",
            model=people_models.MembershipWebAddress,
        )


class PublicationService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.publications", model=people_models.Publication
        )


class PublicationWebAddressService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.publication_web_addresses",
            model=people_models.PublicationWebAddress,
        )


class PatentService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.patents", model=people_models.Patent)


class PatentWebAddressService(BaseService):
    def __init__(self):
        super().__init__(
            table_name="people.patent_web_addresses",
            model=people_models.PatentWebAddress,
        )


class AwardService(BaseService):
    def __init__(self):
        super().__init__(table_name="people.awards", model=people_models.Award)
