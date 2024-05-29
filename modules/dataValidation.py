from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from typing import Optional
from datetime import date, time

class VictimData_Validation(BaseModel):
    vic_fname: str = Field(..., min_length=1, description="First name is required")
    vic_midname: Optional[str] = None
    vic_lname: str = Field(..., min_length=1, description="Last name is required")
    vic_qlfr: Optional[str] = None
    vic_alias: Optional[str] = None
    vic_gndr: str = Field(..., description="Gender is required")
    vic_age: Optional[int] = Field(..., ge=0, description="Age must be a non-negative integer")
    vic_distprov: str = Field(..., description="District/Province is required")
    vic_cityMun: str = Field(..., description="City/Municipality is required")
    vic_brgy: str = Field(..., description="Barangay is required")
    vic_strName: Optional[str] = None

    @field_validator('vic_alias')
    def check_alias(cls, value):
        if not value:
            return "alias Unknown"
        return value
    
    @field_validator('vic_age')
    def check_age(cls, value):
        if not value:
            return 0
        return value

    @field_validator('vic_gndr')
    def gender_must_be_valid(cls, gender):
        if gender is not None and gender not in ("Male", "Female"):
            return None
        return gender

class SuspectData_Validation(BaseModel):
    sus_fname: Optional[str] = None
    sus_midname: Optional[str] = None
    sus_lname: Optional[str] = None
    sus_qlfr: Optional[str] = None
    sus_alias: Optional[str] = None
    sus_gndr: Optional[str] = Field(None, description="Gender is required")
    sus_age: Optional[int] = Field(0, ge=0, description="Age must be a non-negative integer")
    sus_distprov: Optional[str] = Field(None, description="District/Province is required")
    sus_cityMun: Optional[str] = Field(None, description="City/Municipality is required")
    sus_brgy: Optional[str] = Field(None, description="Barangay is required")
    sus_strName: Optional[str] = None

    @field_validator('sus_fname', 'sus_midname', 'sus_lname')
    def check_names(cls, value):
        if not value:
            return "Unidentified"
        return value
    
    @field_validator('sus_alias')
    def check_alias(cls, value):
        if not value:
            return "alias Unknown"
        return value
    
    @field_validator('sus_age')
    def check_age(cls, value):
        if not value:
            return 0
        return value

    @field_validator('sus_gndr')
    def gender_must_be_valid(cls, gender):
        if gender is not None and gender not in ("Male", "Female"):
            return None
        return gender
    
    @field_validator('sus_brgy')
    def check_brgy(cls, value):
        if not value:
            return "Unidentified"
        return value
    

class Case_Detail_Validation(BaseModel):
    det_narrative: Optional[str] = Field(..., description="Narrative description of the case")
    dt_reported: date = Field(..., description="Date Reported")
    time_reported: Optional[time] = Field(None, description="Time Reported")
    dt_committed: Optional[date] = Field(..., description="Date Committed")
    time_committed: Optional[time] = Field(None, description="Time Committed")

    @field_validator('dt_reported')
    def check_dt_reported(cls, value):
        if value == date.today():
            raise ValueError("Please change the Date Reported")
        return value