from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional

class VictimData_Validation(BaseModel):
    vic_fname: str = Field(..., min_length=1, description="First name is required")
    vic_midname: Optional[str] = None
    vic_lname: str = Field(..., min_length=1, description="Last name is required")
    vic_qlfr: Optional[str] = None
    vic_alias: Optional[str] = None
    vic_gndr: str = Field(..., description="Gender is required")
    vic_age: int = Field(..., ge=0, description="Age must be a non-negative integer")
    vic_distprov: str = Field(..., description="District/Province is required")
    vic_cityMun: str = Field(..., description="City/Municipality is required")
    vic_brgy: str = Field(..., description="Barangay is required")
    vic_strName: Optional[str] = None

    @field_validator('vic_gndr')
    def gender_must_be_valid(cls, gender):
        if gender not in ("Male", "Female"):
            raise ValueError('Gender must be either "Male" or "Female"')
        return gender
    
