from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field, field_serializer, field_validator
from typing import Literal, Optional
from datetime import datetime

class NotificationPreferences(BaseModel):
    """Represents notification preferences for a student."""
    email_alerts_grades: bool = True
    email_alerts_receipts: bool = True
    sms_alerts_schedule: bool = False

class Sponsor(Document):
    """Represents the financial sponsor for a student, with fields for contact details."""
    title: str
    full_name: str
    email: Indexed(EmailStr, unique=True) # type: ignore
    phone_number: str
    full_address: str
    organization: Optional[str] = None
    relationship_to_student: Optional[str] = None
    
    class Settings:
        name = "sponsors"

class ParentGuardian(Document):
    """Represents the parent or guardian of a student, with fields for contact details."""
    title: str
    full_name: str
    email: Indexed(EmailStr, unique=True) # type: ignore
    phone_number: str
    full_address: str
    relationship_to_student: Optional[str] = None
    
    class Settings:
        name = "parents_guardians"

class NextOfKin(Document):
    """Represents the next of kin for a student, with fields for contact details."""
    title: str
    full_name: str
    email: Indexed(EmailStr, unique=True) # type: ignore
    phone_number: str
    full_address: str
    relationship_to_student: Optional[str] = None
    
    class Settings:
        name = "next_of_kin"


class Student(Document):
    """Represents a student in the system, with fields for personal information and authentication details."""
    student_id: Indexed(str, unique=True) # type: ignore
    
    first_name: str
    last_name: str
    email: Indexed(EmailStr, unique=True) # type: ignore
    middle_name: Optional[str] = None
    hashed_password: str
    
    # Updated Literals to accept 'NA'
    enroled_track: Literal['A', 'T', 'NA'] = Field(default='NA')
    study_mode: Literal['O', 'S', 'NA'] = Field(default='NA') 
    hardware_requirement: Literal['Y', 'N', 'NA'] = Field(default='NA') 
    
    sex: Literal['M', 'F']
    phone_number: str
    street_address: str
    city: str
    state: str
    country: str
    
    # Fixed Missing Type Annotations (str)
    secondary_school: str = Field(default='NA') 
    graduation_year: str = Field(default='NA') 
    highest_qualification: str = Field(default='NA') 
    
    core_strength: Optional[str] = None
    areas_of_improvement: Optional[str] = None
    date_of_birth: datetime
    
    required_accommodations: Optional[str] = None
    
    passport_photo_url: Optional[str] = None
    id_card_photo_url: Optional[str] = None
    academic_reference_letter_url: Optional[str] = None
    o_level_result_url: Optional[str] = None
    
    preferences: NotificationPreferences = Field(default_factory=NotificationPreferences)
    
    requires_high_contrast: bool = False
    
    sponsor: Optional[Link[Sponsor]] = None
    parent_guardian: Optional[Link[ParentGuardian]] = None
    next_of_kin: Optional[Link[NextOfKin]] = None

    @field_validator('sex', mode='before')
    @classmethod
    def normalize_sex(cls, value: str) -> str:
        """
        Normalizes the sex value to a consistent format (e.g., 'M' or 'F').
        """
        if not isinstance(value, str):
            raise ValueError('Sex must be provided as a string value.')

        normalized = value.strip().lower()
        mapping = {
            'm': 'M',
            'male': 'M',
            'f': 'F',
            'female': 'F',
        }

        if normalized not in mapping:
            raise ValueError("Sex must be one of: 'M', 'F', 'male', or 'female'.")

        return mapping[normalized]

    @field_validator('enroled_track', mode='before')
    @classmethod
    def normalize_enroled_track(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError('Enrolled track must be provided as a string value.')

        normalized = value.strip().lower()
        mapping = {
            'a': 'A',
            'academic': 'A',
            'academic track': 'A',
            't': 'T',
            'tech': 'T',
            'tech innovation': 'T',
            'tech innovation track': 'T',
        }

        if normalized not in mapping:
            raise ValueError(
                "Enrolled track must be one of: 'A', 'T', 'Academic Track', or 'Tech Innovation Track'."
            )

        return mapping[normalized]

    @field_validator('study_mode', mode='before')
    @classmethod
    def normalize_study_mode(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError('Study mode must be provided as a string value.')

        normalized = value.strip().lower()
        mapping = {
            'o': 'O',
            'online': 'O',
            's': 'S',
            'onsite': 'S',
        }

        if normalized not in mapping:
            raise ValueError("Study mode must be one of: 'O', 'S', 'Online', or 'Onsite'.")

        return mapping[normalized]

    @field_serializer('sex', when_used='json')
    def serialize_sex_human_readable(self, value: Literal['M', 'F']) -> str:
        return 'male' if value == 'M' else 'female'

    @field_serializer('enroled_track', when_used='json')
    def serialize_enroled_track_human_readable(self, value: Literal['A', 'T']) -> str:
        return 'Academic Track' if value == 'A' else 'Tech Innovation Track'

    @field_serializer('study_mode', when_used='json')
    def serialize_study_mode_human_readable(self, value: Literal['O', 'S']) -> str:
        return 'Online' if value == 'O' else 'Onsite'
    
    class Collection:
        name = 'students'