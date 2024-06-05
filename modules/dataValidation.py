from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, time

class VictimData_Validation(BaseModel):
    pro: str
    ppo_cpo: str
    mps_cps: str
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
            return "Unidentified"
        return gender

class SuspectData_Validation(BaseModel):
    pro: str
    ppo_cpo: str
    mps_cps: str
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
            return "Unidentified"
        return gender
    
    @field_validator('sus_brgy')
    def check_brgy(cls, value):
        if not value:
            return "Unidentified"
        return value
    

# Pydantic model for case details validation
class Case_Detail_Validation(BaseModel):
    pro: str
    ppo_cpo: str
    mps_cps: str
    det_narrative: Optional[str] = Field(None, description="Narrative description of the case")
    dt_reported: date = Field(..., description="Date Reported")
    time_reported: Optional[time]
    dt_committed: Optional[date]
    time_committed: Optional[time]

    @field_validator('dt_reported')
    def check_dt_reported(cls, value):
        if value == date.today():
            raise ValueError("Please change the Date Reported")
        return value
    

class Offense_Validation(BaseModel):
    offense: Optional[str] = None
    offense_class: str
    case_status: str = None
    check: bool

    @field_validator('offense')
    def check_names(cls, value):
        if not value:
            return None
        return value
    
    @field_validator('case_status')
    def check_dt_reported(cls, value):
        if not value:
            raise ValueError("Please Select a Case Status")
        return value
    
class Entry_Number_Validation(BaseModel):
    entryNumber: str  = Field(..., alias="entry_number")



# ==============================================
class New_Entry_CaseDetails_Validation(BaseModel):
    pro: Optional[str]
    ppo_cpo: Optional[str]
    mps_cps: Optional[str]
    det_narrative: Optional[str] = Field(None, description="Narrative description of the case")
    dt_reported: date = Field(..., description="Date Reported")
    time_reported: Optional[time]
    dt_committed: Optional[date]
    time_committed: Optional[time]

    offense: str
    offense_class: str
    case_status: str
    check: bool



class New_Entry_VictimData_Validation(BaseModel):
    entry_number: str  = Field(..., alias="entry_number")
    pro: str
    ppo_cpo: str
    mps_cps: str
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


class New_Entry_SuspectData_Validation(BaseModel):
    entry_number: str  = Field(..., alias="entry_number")
    pro: str
    ppo_cpo: str
    mps_cps: str
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