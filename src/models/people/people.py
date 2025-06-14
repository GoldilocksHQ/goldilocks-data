import uuid
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field
from src.models.base_model import CustomBaseModel

# PEOPLE SCHEMA


# identities table
class Identity(CustomBaseModel):
    people_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    neuron360_profile_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    picture_url: Optional[str] = None
    last_modified_date: Optional[datetime] = None
    last_seen_date: Optional[datetime] = None


# profiles table
class Profile(CustomBaseModel):
    people_id: uuid.UUID
    summary: Optional[str] = None
    languages: Optional[List[str]] = None
    expertises: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    prior_industries: Optional[List[str]] = None
    raw_location: Optional[str] = None
    headline: Optional[str] = None


# genders table
class Gender(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    gender: Optional[str] = None
    confidence_score: Optional[float] = None


# social_links table
class SocialLink(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    name: Optional[str] = None
    url: Optional[str] = None


# statuses table
class Status(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    status: Optional[str] = None


# emails table
class Email(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    email: Optional[str] = None
    priority: Optional[int] = None


# phones table
class Phone(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    phone: Optional[str] = None
    ddi: Optional[bool] = None
    dnc: Optional[bool] = None
    type: Optional[str] = None
    carrier: Optional[str] = None
    priority: Optional[int] = None


# addresses table
class Address(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    last_modified_date: Optional[datetime] = None
    formatted_address: Optional[str] = None
    street_address: Optional[str] = None
    place_id: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    accuracy: Optional[str] = None
    confidence_score: Optional[float] = None
    quality: Optional[str] = None
    administrative_area_level_1: Optional[str] = None
    administrative_area_level_2: Optional[str] = None
    administrative_area_level_3: Optional[str] = None
    administrative_area_level_4: Optional[str] = None
    administrative_area_level_5: Optional[str] = None
    continent: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    establishment: Optional[str] = None
    locality: Optional[str] = None
    postal_code: Optional[str] = None
    postal_town: Optional[str] = None
    premise: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    sublocality: Optional[str] = None
    subpremise: Optional[str] = None
    score: Optional[float] = None


# experiences table
class Experience(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    job_title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    summary: Optional[str] = None
    current: Optional[bool] = None
    priority: Optional[int] = None
    raw_location: Optional[str] = None


# job_title_details table
class JobTitleDetail(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    experience_id: uuid.UUID
    raw_job_title: Optional[str] = None
    raw_job_title_language_code: Optional[str] = None
    raw_job_title_language_detection_confidence_score: Optional[float] = None
    raw_translated_job_title: Optional[str] = None
    raw_translated_job_title_language_code: Optional[str] = None
    normalized_job_title_id: Optional[int] = None
    normalized_job_title: Optional[str] = None


# job_functions table
class JobFunction(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    experience_id: uuid.UUID
    level1_code: Optional[str] = None
    level1_name: Optional[str] = None
    level1_confidence_score: Optional[float] = None
    level2_code: Optional[str] = None
    level2_name: Optional[str] = None
    level2_confidence_score: Optional[float] = None
    level3_code: Optional[str] = None
    level3_name: Optional[str] = None
    level3_confidence_score: Optional[float] = None
    priority: Optional[int] = None


# job_seniority table
class JobSeniority(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    experience_id: uuid.UUID
    job_level: Optional[str] = None


# educations table
class Education(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    educational_establishment: Optional[str] = None
    diploma: Optional[str] = None
    specialization: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    priority: Optional[int] = None


# education_web_addresses table
class EducationWebAddress(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    education_id: uuid.UUID
    url: Optional[str] = None
    rank: Optional[int] = None


# certifications table
class Certification(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    name: Optional[str] = None
    description: Optional[str] = None
    authority: Optional[str] = None
    reference: Optional[str] = None
    date: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    priority: Optional[int] = None


# certification_web_addresses table
class CertificationWebAddress(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    certification_id: uuid.UUID
    url: Optional[str] = None
    rank: Optional[int] = None


# memberships table
class Membership(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    title: Optional[str] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    priority: Optional[int] = None


# membership_web_addresses table
class MembershipWebAddress(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    membership_id: uuid.UUID
    url: Optional[str] = None
    rank: Optional[int] = None


# publications table
class Publication(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    name: Optional[str] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    issue: Optional[str] = None
    date: Optional[str] = None
    priority: Optional[int] = None


# publication_web_addresses table
class PublicationWebAddress(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    publication_id: uuid.UUID
    url: Optional[str] = None
    rank: Optional[int] = None


# patents table
class Patent(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    name: Optional[str] = None
    issue: Optional[str] = None
    number: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    priority: Optional[int] = None


# patent_web_addresses table
class PatentWebAddress(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    patent_id: uuid.UUID
    url: Optional[str] = None
    rank: Optional[int] = None


# awards table
class Award(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    people_id: uuid.UUID
    name: Optional[str] = None
    description: Optional[str] = None
    issue: Optional[str] = None
    date: Optional[str] = None
    priority: Optional[int] = None
