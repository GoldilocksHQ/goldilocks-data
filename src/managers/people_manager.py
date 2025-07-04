from src.managers.base_manager import BaseManager
from src.services import people_services
from src.models import people as people_models
from src.managers.organisation_manager import OrganisationManager
from typing import Dict, Any, Optional
from datetime import datetime, date
import json


class PeopleManager(BaseManager):
    """
    Manages the processing and persistence of people-related data.
    Orchestrates calls to the OrganisationManager when company data is found.
    """

    def __init__(self, org_manager: OrganisationManager):
        super().__init__()
        self.org_manager = org_manager
        # Initialize all people services
        self.identity_service = people_services.IdentityService()
        self.profile_service = people_services.ProfileService()
        self.gender_service = people_services.GenderService()
        self.social_link_service = people_services.SocialLinkService()
        self.status_service = people_services.StatusService()
        self.email_service = people_services.EmailService()
        self.phone_service = people_services.PhoneService()
        self.address_service = people_services.AddressService()
        self.experience_service = people_services.ExperienceService()
        self.job_title_detail_service = people_services.JobTitleDetailService()
        self.job_function_service = people_services.JobFunctionService()
        self.job_seniority_service = people_services.JobSeniorityService()
        self.education_service = people_services.EducationService()
        self.certification_service = people_services.CertificationService()
        self.membership_service = people_services.MembershipService()
        self.publication_service = people_services.PublicationService()
        self.patent_service = people_services.PatentService()
        self.award_service = people_services.AwardService()

    def _to_date(self, date_str: str) -> Optional[date]:
        """
        Safely converts a date string (in various formats) to a date object.
        """
        if not date_str:
            return None
        try:
            return datetime.strptime(str(date_str).split(" ")[0], "%Y-%m-%d").date()
        except (ValueError, AttributeError):
            return None

    def process_people_from_file(self, file_path: str) -> tuple[int, int]:
        """
        Processes a file containing a list of person records.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            tuple[int, int]: A tuple containing the success count and failure count.
        """
        success_count = 0
        failure_count = 0
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self._log_error(f"Could not read or parse file {file_path}: {e}")
            # If the file is invalid, all its records are considered failures.
            try:
                # Attempt to count records if possible, otherwise return 0,0
                with open(file_path, "r") as f:
                    # A crude way to estimate line count for malformed JSON
                    num_records = len(f.readlines())
                return 0, num_records
            except Exception:
                return 0, 0  # Cannot even open the file

        profiles = data.get("results", [])
        if not profiles:
            self._log_error(f"No 'results' key found or list is empty in {file_path}.")
            return 0, 0

        for person_record in profiles:
            try:
                self.process_person_data(person_record)
                success_count += 1
            except Exception as e:
                self._log_error(f"Failed to process person record: {e}", exc_info=True)
                failure_count += 1

        return success_count, failure_count

    def process_person_data(self, person_record: Dict[str, Any]):
        """
        Processes and persists a single person's data from the API response.
        This is the main entry point for processing a person.
        """
        try:
            profile_data = person_record.get("profile_data", {})
            resume_data = person_record.get("resume_data", {})

            if not profile_data:
                self._log_error("No 'profile_data' found, skipping record.")
                return

            # Check for existing person by neuron360_profile_id
            neuron_id = profile_data.get("profile_id")
            if neuron_id:
                existing_identity = self.identity_service.get_by_neuron_id(neuron_id)
                if existing_identity:
                    self.logger.info(
                        f"Skipping existing Person with neuron_id: {neuron_id}"
                    )
                    return

            self.logger.info(
                f"Processing person: {profile_data.get('profile_full_name')}"
            )

            # 1. Create Identity
            identity_model = people_models.Identity(
                neuron360_profile_id=profile_data.get("profile_id"),
                first_name=profile_data.get("profile_first_name"),
                last_name=profile_data.get("profile_last_name"),
                full_name=profile_data.get("profile_full_name"),
                picture_url=profile_data.get("profile_picture", {}).get("url"),
                last_modified_date=profile_data.get("profile_last_modified_date"),
                last_seen_date=profile_data.get("profile_last_seen_date"),
            )
            created_identity = self.identity_service.create(identity_model)
            if not created_identity:
                self._log_error(
                    "Failed to create identity, aborting processing for this person."
                )
                return

            people_id = created_identity.people_id
            self._log_success(f"Created Identity with people_id: {people_id}")

            # 2. Create Profile and related sub-tables
            self._process_profile_details(profile_data, people_id)

            # 3. Process resume data, which includes experiences, educations, etc.
            if resume_data:
                self._process_resume_items(resume_data, people_id)

            self._log_success(
                f"Successfully processed all data for people_id: {people_id}"
            )

        except Exception as e:
            self._log_error(
                f"An error occurred during person data processing: {e}", exc_info=True
            )

    def _process_profile_details(self, data: Dict[str, Any], people_id: Any):
        # Create main profile
        profile_details = {
            "summary": data.get("profile_summary"),
            "languages": data.get("profile_languages"),
            "expertises": data.get("profile_expertises"),
            "tags": data.get("profile_tags"),
            "prior_industries": data.get("profile_prior_industries"),
            "raw_location": data.get("raw_location"),
            "headline": data.get("profile_headline"),
        }
        profile = people_models.Profile(people_id=people_id, **profile_details)
        created_profile = self.profile_service.create(profile)

        # CRITICAL: Check if profile was created before proceeding
        if not created_profile:
            self._log_error(
                "Failed to create profile for people_id: %s. "
                "Aborting further profile-dependent inserts.",
                people_id,
            )
            # We raise an exception to stop the processing for this person
            raise Exception(f"Profile creation failed for people_id: {people_id}")

        # Other direct profile relations
        if data.get("profile_gender"):
            gender_data = data.get("profile_gender")
            gender = people_models.Gender(
                people_id=people_id,
                gender=gender_data.get("gender"),
                confidence_score=gender_data.get("confidence_score"),
            )
            self.gender_service.create(gender)

        if data.get("profile_social_links"):
            for link in data["profile_social_links"]:
                s_link = people_models.SocialLink(people_id=people_id, **link)
                self.social_link_service.create(s_link)

        if data.get("profile_status"):
            status_data = data.get("profile_status")
            status = people_models.Status(
                people_id=people_id, status=status_data.get("status")
            )
            self.status_service.create(status)

        if data.get("profile_emails"):
            for email_data in data["profile_emails"]:
                em = people_models.Email(people_id=people_id, **email_data)
                self.email_service.create(em)

        if data.get("profile_phones"):
            for phone_data in data["profile_phones"]:
                ph = people_models.Phone(people_id=people_id, **phone_data)
                self.phone_service.create(ph)

        if data.get("profile_address"):
            address = people_models.Address(
                people_id=people_id, **data["profile_address"]
            )
            self.address_service.create(address)

    def _process_experience(self, exp_data: Dict[str, Any], people_id: Any):
        """
        Processes a single experience record, its related details,
        and triggers the organisation manager to process the associated company.
        """
        # 1. Trigger OrganisationManager to process company data first
        # This ensures the organisation exists before we link it to an experience
        self.org_manager.process_organisation_data(exp_data)

        # 2. Create the Experience record
        exp_model = people_models.Experience(
            people_id=people_id,
            job_title=exp_data.get("job_title"),
            start_date=self._to_date(exp_data.get("start_date")),
            end_date=self._to_date(exp_data.get("end_date")),
            summary=exp_data.get("summary"),
            current=exp_data.get("current"),
            priority=exp_data.get("priority"),
            raw_location=exp_data.get("raw_location"),
        )
        created_exp = self.experience_service.create(exp_model)

        if created_exp and created_exp.id:
            exp_id = created_exp.id

            # 3. Process nested details for the experience
            job_title_details_data = exp_data.get("job_title_details")
            if job_title_details_data:
                raw_title_data = job_title_details_data.get("raw_job_title", {})
                translated_title_data = job_title_details_data.get(
                    "raw_translated_job_title", {}
                )
                normalized_title_data = job_title_details_data.get(
                    "normalized_job_title", {}
                )

                processed_jtd = {
                    "raw_job_title": raw_title_data.get("job_title"),
                    "raw_job_title_language_code": raw_title_data.get("language_code"),
                    "raw_job_title_language_detection_confidence_score": raw_title_data.get(
                        "language_detection_confidence_score"
                    ),
                    "raw_translated_job_title": translated_title_data.get("job_title"),
                    "raw_translated_job_title_language_code": translated_title_data.get(
                        "language_code"
                    ),
                    "normalized_job_title_id": normalized_title_data.get("id"),
                    "normalized_job_title": normalized_title_data.get("job_title"),
                }
                processed_jtd = {
                    k: v for k, v in processed_jtd.items() if v is not None
                }
                if processed_jtd:
                    jtd = people_models.JobTitleDetail(
                        experience_id=exp_id, **processed_jtd
                    )
                    self.job_title_detail_service.create(jtd)

            job_functions_data = exp_data.get("job_functions", [])
            for jf_data in job_functions_data:
                level1_data = jf_data.get("level1", {}) or {}
                level2_data = jf_data.get("level2", {}) or {}
                level3_data = jf_data.get("level3", {}) or {}

                job_function_payload = {
                    "experience_id": exp_id,
                    "priority": jf_data.get("priority"),
                    "level1_code": level1_data.get("code"),
                    "level1_name": level1_data.get("name"),
                    "level1_confidence_score": level1_data.get("confidence_score"),
                    "level2_code": level2_data.get("code"),
                    "level2_name": level2_data.get("name"),
                    "level2_confidence_score": level2_data.get("confidence_score"),
                    "level3_code": level3_data.get("code"),
                    "level3_name": level3_data.get("name"),
                    "level3_confidence_score": level3_data.get("confidence_score"),
                }
                jf = people_models.JobFunction(**job_function_payload)
                self.job_function_service.create(jf)

            job_seniority_data = exp_data.get("job_seniority")
            if job_seniority_data:
                js = people_models.JobSeniority(
                    experience_id=exp_id, **job_seniority_data
                )
                self.job_seniority_service.create(js)

    def _process_resume_items(self, resume_data: Dict[str, Any], people_id: Any):
        """
        Processes all lists of items within the resume_data object.
        """
        # Process Experiences
        for exp_data in resume_data.get("experiences", []):
            self._process_experience(exp_data, people_id)

        # Process Educations
        if "educations" in resume_data:
            for edu_data in resume_data.get("educations", []):
                web_address_data = edu_data.pop(
                    "educational_establishment_web_address", {}
                )
                edu_model = people_models.Education(
                    people_id=people_id,
                    educational_establishment=edu_data.get("educational_establishment"),
                    diploma=edu_data.get("diploma"),
                    specialization=edu_data.get("specialization"),
                    start_date=self._to_date(edu_data.get("start_date")),
                    end_date=self._to_date(edu_data.get("end_date")),
                    priority=edu_data.get("priority"),
                    web_address_url=web_address_data.get("url"),
                    web_address_rank=web_address_data.get("rank"),
                )
                self.education_service.create(edu_model)

        # Process Certifications
        if "certifications" in resume_data:
            certifications_data = resume_data.get("certifications", [])
            for cert_data in certifications_data:
                web_address_data = cert_data.pop("web_address", {})
                cert_payload = {
                    "people_id": people_id,
                    "name": cert_data.get("name"),
                    "url": cert_data.get("url"),
                    "start_date": cert_data.get("start_date"),
                    "end_date": cert_data.get("end_date"),
                    "authority": cert_data.get("authority"),
                    "raw_name": cert_data.get("raw_name"),
                    "web_address_url": web_address_data.get("url"),
                    "web_address_rank": web_address_data.get("rank"),
                }
                cert = people_models.Certification(**cert_payload)
                self.certification_service.create(cert)

        # Process Memberships
        if "memberships" in resume_data:
            memberships_data = resume_data.get("memberships", [])
            for mem_data in memberships_data:
                web_address_data = mem_data.pop("web_address", {})
                mem_model = people_models.Membership(
                    people_id=people_id,
                    title=mem_data.get("title"),
                    description=mem_data.get("description"),
                    reference=mem_data.get("reference"),
                    name=mem_data.get("name"),
                    start_date=mem_data.get("start_date"),
                    end_date=mem_data.get("end_date"),
                    location=mem_data.get("location"),
                    priority=mem_data.get("priority"),
                    web_address_url=web_address_data.get("url"),
                    web_address_rank=web_address_data.get("rank"),
                )
                self.membership_service.create(mem_model)

        # Process Publications
        if "publications" in resume_data:
            publications_data = resume_data.get("publications", [])
            for pub_data in publications_data:
                web_address_data = pub_data.pop("web_address", {})
                pub_payload = {
                    "people_id": people_id,
                    "name": pub_data.get("name"),
                    "date": pub_data.get("date"),
                    "description": pub_data.get("description"),
                    "publisher": pub_data.get("publisher"),
                    "url": pub_data.get("url"),
                    "web_address_url": web_address_data.get("url"),
                    "web_address_rank": web_address_data.get("rank"),
                }
                pub = people_models.Publication(**pub_payload)
                self.publication_service.create(pub)

        # Process Patents
        if "patents" in resume_data:
            for pat_data in resume_data.get("patents", []):
                web_address_data = pat_data.pop("web_address", {})
                pat_model = people_models.Patent(
                    people_id=people_id,
                    name=pat_data.get("name"),
                    issue=pat_data.get("issue"),
                    number=pat_data.get("number"),
                    start_date=self._to_date(pat_data.get("start_date")),
                    end_date=self._to_date(pat_data.get("end_date")),
                    priority=pat_data.get("priority"),
                    web_address_url=web_address_data.get("url"),
                    web_address_rank=web_address_data.get("rank"),
                )
                self.patent_service.create(pat_model)

        # Process Awards
        if "awards" in resume_data:
            awards_data = resume_data.get("awards", [])
            for award_data in awards_data:
                award_payload = {
                    "people_id": people_id,
                    "name": award_data.get("name"),
                    "description": award_data.get("description"),
                    "issue": award_data.get("issue"),
                    "date": award_data.get("date"),
                    "priority": award_data.get("priority"),
                }
                self.logger.debug(
                    f"Attempting to create Award with payload: {award_payload}"
                )
                award_model = people_models.Award(**award_payload)
                self.award_service.create(award_model)
