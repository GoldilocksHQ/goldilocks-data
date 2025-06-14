import uuid
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from src.models.base_model import CustomBaseModel

# ORGANISATION SCHEMA


# identities table
class Identity(CustomBaseModel):
    organisation_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    neuron360_company_id: Optional[str] = None
    name: Optional[str] = None
    domain: Optional[str] = None
    logo_url: Optional[str] = None
    industry: Optional[str] = None


# web_addresses table
class WebAddress(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    organisation_id: uuid.UUID
    url: Optional[str] = None
    rank: Optional[int] = None


# employees table
class Employee(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    organisation_id: uuid.UUID
    number_of_employees: Optional[int] = None
    number_of_employees_code: Optional[str] = None
    number_of_employees_min: Optional[int] = None
    number_of_employees_max: Optional[int] = None


# social_links table
class SocialLink(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    organisation_id: uuid.UUID
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None
    crunchbase_url: Optional[str] = None
    yelp_url: Optional[str] = None


# industries table
class Industry(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    organisation_id: uuid.UUID
    industry_id: Optional[str] = None
    code2: Optional[str] = None
    name2: Optional[str] = None
    code3: Optional[str] = None
    name3: Optional[str] = None
    code4: Optional[str] = None
    name4: Optional[str] = None
    code5: Optional[str] = None
    name5: Optional[str] = None
    code6: Optional[str] = None
    name6: Optional[str] = None
    standard: Optional[str] = None
    activity_priority: Optional[int] = None
    priority: Optional[int] = None


# phones table
class Phone(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    organisation_id: uuid.UUID
    phone: Optional[str] = None
    ddi: Optional[bool] = None
    dnc: Optional[bool] = None
    type: Optional[str] = None
    carrier: Optional[str] = None
    priority: Optional[int] = None


# offices table
class Office(CustomBaseModel):
    office_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    organisation_id: uuid.UUID
    neuron360_office_id: Optional[str] = None


# office_addresses table
class OfficeAddress(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    office_id: uuid.UUID
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


# office_industries table
class OfficeIndustry(CustomBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    office_id: uuid.UUID
    industry_id: Optional[str] = None
    code2: Optional[str] = None
    name2: Optional[str] = None
    code3: Optional[str] = None
    name3: Optional[str] = None
    code4: Optional[str] = None
    name4: Optional[str] = None
    code5: Optional[str] = None
    name5: Optional[str] = None
    code6: Optional[str] = None
    name6: Optional[str] = None
    standard: Optional[str] = None
    activity_priority: Optional[int] = None
    priority: Optional[int] = None
