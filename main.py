from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated,  List, Optional
from uuid import UUID
import bcrypt
import config.models as models
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import date, time
from modules import dataValidation as dv
import pandas as pd

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# ============================================
# Pydantic Classes
# ============================================
class UserBaseModel(BaseModel):
    id: UUID
    username: str
    password: str
    is_logged_in: bool = False
    failed_login_attempts: int

class UserLoginModel(BaseModel):
    username: str
    password: str

# Pydantic schema for Station_Sequence model
class StationSequence(BaseModel):
    seq: str
    mps_cps: str
    ppo_cpo: str

    class Config:
        from_attributes = True

# Pydantic model for TempEntry
class TempEntryCreate(BaseModel):
    combined_value: str

class TempEntryResponse(BaseModel):
    id: int
    combined_value: str

    class Config:
        from_attributes = True

class Brgy_Value(BaseModel):
    id: int
    brgy: str

class City_Mun_Value(BaseModel):
    id: int
    city_mun: str

class Province_Value(BaseModel):
    id: int
    province: str

class Province_City_Mun_Value_ResponseModel(BaseModel):
    brgy_values: List[Brgy_Value]
    city_mun_value: Optional[City_Mun_Value]
    province_value: Optional[Province_Value]


class Offense_Classification(BaseModel):
    id: int
    incidents: str
    classification: str



class CaseDetailsModel(BaseModel):
    entry_number: str
    offense: str
    offense_class: str
    case_status: str
    check: bool

    narrative: str
    date_reported: date
    time_reported: Optional[time] = None
    date_committed: Optional[date] = None
    time_committed: Optional[time] = None

# Define the Pydantic model for the response data
class CaseData(BaseModel):
    entry_number: str
    offense: str
    case_status: str
    date_reported: date
    time_reported: time
    date_committed: date
    time_committed: time
    victim_details: str
    suspect_details: str





# ============================================
# END of Pydantic Classes
# ============================================


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Get all USERS
@app.get("/users/")
async def get_users(db: db_dependency):
    users = db.query(models.UserBase).all()
    return users

@app.post("/login/")
async def login(user: UserLoginModel, db: db_dependency):
    db_user = db.query(models.UserBase).filter(models.UserBase.username == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verify_password(user.password, db_user.password):
        db_user.failed_login_attempts += 1
        db.add(db_user)
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    db_user.is_logged_in = True
    db_user.failed_login_attempts = 0  # Reset on successful login
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "Login successful", "user": db_user}


# Endpoint to fetch `seq` by `mps_cps`
@app.get("/stations/{mps_cps}", response_model=List[StationSequence])
async def read_station_by_mps_cps(mps_cps: str, db: Session = Depends(get_db)):
    station_sequence = db.execute(select(models.Station_Sequence).where(models.Station_Sequence.mps_cps == mps_cps)).scalars().all()
    
    if not station_sequence:
        raise HTTPException(status_code=404, detail="Station sequence not found")

    return station_sequence



# Endpoint to store a new temp entry
@app.post("/temp-entries/", response_model=TempEntryResponse)
async def create_temp_entry(entry: TempEntryCreate, db: Session = Depends(get_db)):
    db_entry = models.TempEntry(combined_value=entry.combined_value)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# Endpoint to delete a temp entry
@app.delete("/temp-entries/{entry_id}", response_model=TempEntryResponse)
async def delete_temp_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = db.query(models.TempEntry).filter(models.TempEntry.id == entry_id).first()
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(db_entry)
    db.commit()
    return db_entry

# Endpoint to get all temp entries (optional, for debugging)
@app.get("/temp-entries/", response_model=List[TempEntryResponse])
async def get_temp_entries(db: Session = Depends(get_db)):
    return db.query(models.TempEntry).all()


# Endpoint to get Brgy_Value and City_Mun_Value based on mps_cps
@app.get("/brgy-city-mun/{mps_cps}", response_model=Province_City_Mun_Value_ResponseModel)
async def get_brgy_city_mun(mps_cps: str, db: db_dependency):

    # Query to get Brgy_Value
    brgy_query = select(
        models.Province_Brgy_Details.id,
        models.Province_Brgy_Details.brgy
    ).where(models.Province_Brgy_Details.mps_cps == mps_cps)
    
    brgy_results = db.execute(brgy_query).fetchall()
    brgy_values = [Brgy_Value(id=row[0], brgy=row[1]) for row in brgy_results]

    # Query to get the first City_Mun_Value
    city_mun_query = select(
        models.Province_Brgy_Details.id,
        models.Province_Brgy_Details.mun_city
    ).where(models.Province_Brgy_Details.mps_cps == mps_cps).limit(1)

    city_mun_result = db.execute(city_mun_query).first()

    city_mun_value = None
    if city_mun_result:
        city_mun_value = City_Mun_Value(id=city_mun_result[0], city_mun=city_mun_result[1])

    # Query to get the first Province
    province_query = select(
        models.Province_Brgy_Details.id,
        models.Province_Brgy_Details.province
    ).where(models.Province_Brgy_Details.mps_cps == mps_cps).limit(1)

    province_result = db.execute(province_query).first()

    province_value = None
    if province_result:
        province_value = Province_Value(id=province_result[0], province=province_result[1])

    # Return the results as a dictionary
    return {
        "brgy_values": brgy_values,
        "city_mun_value": city_mun_value,
        "province_value": province_value
    }


# Endpoint to get offense classifications
@app.get("/offense_classifications")
async def get_offense_classifications(db: Session = Depends(get_db)):
    offenses = db.query(models.Offense).all()
    return [{"incidents": offense.incidents, "classification": offense.classification} for offense in offenses]




@app.post("/case-details/")
async def create_case_details(case_details: CaseDetailsModel, db: Session = Depends(get_db)):
    # Create a new database object
    db_case_details = models.CaseDetails(
        entry_number=case_details.entry_number,
        offense=case_details.offense,
        offense_class=case_details.offense_class,
        case_status=case_details.case_status,
        check=case_details.check,
        narrative=case_details.narrative,
        date_reported=case_details.date_reported,
        time_reported=case_details.time_reported,
        date_committed=case_details.date_committed,
        time_committed=case_details.time_committed
    )

    # Add it to the database
    db.add(db_case_details)
    db.commit()
    db.refresh(db_case_details)

    return db_case_details


@app.post("/victim-new-entry/", response_model=dv.New_Entry_VictimData_Validation)
async def enter_victim(victim: dv.New_Entry_VictimData_Validation, db: Session = Depends(get_db)):
    db_victim = models.Victim_Details(**victim.model_dump())
    db.add(db_victim)
    db.commit()
    db.refresh(db_victim)
    return db_victim


@app.post("/suspect-new-entry/", response_model=dv.New_Entry_SuspectData_Validation)
async def enter_victim(suspect: dv.New_Entry_SuspectData_Validation, db: Session = Depends(get_db)):
    db_suspect = models.Suspect_Details(**suspect.model_dump())
    db.add(db_suspect)
    db.commit()
    db.refresh(db_suspect)
    return db_suspect


# Define the endpoint
@app.get('/cases')
def get_cases(db: Session = Depends(get_db)):
    # Create a query
    query = (
        select(
            models.CaseDetails.entry_number,
            models.CaseDetails.offense,
            models.CaseDetails.case_status,
            models.CaseDetails.date_reported,
            models.CaseDetails.time_reported,
            models.CaseDetails.date_committed,
            models.CaseDetails.time_committed,
            models.Victim_Details.vic_fname,
            models.Victim_Details.vic_midname,
            models.Victim_Details.vic_lname,
            models.Victim_Details.vic_qlfr,
            models.Victim_Details.vic_alias,
            models.Victim_Details.vic_age,
            models.Victim_Details.vic_gndr,
            models.Suspect_Details.sus_fname,
            models.Suspect_Details.sus_midname,
            models.Suspect_Details.sus_lname,
            models.Suspect_Details.sus_qlfr,
            models.Suspect_Details.sus_alias,
            models.Suspect_Details.sus_age,
            models.Suspect_Details.sus_gndr,
        )
        .select_from(models.CaseDetails)
        .join(models.Victim_Details, models.CaseDetails.entry_number == models.Victim_Details.entry_number)
        .join(models.Suspect_Details, models.CaseDetails.entry_number == models.Suspect_Details.entry_number)
    )

    # Execute the query
    result = db.execute(query)

    # Fetch all the rows
    rows = result.fetchall()

    # Convert the rows to a DataFrame
    df = pd.DataFrame(rows, columns=[
        "entry_number",
        "offense",
        "case_status",
        "date_reported",
        "time_reported",
        "date_committed",
        "time_committed",
        "vic_fname",
        "vic_midname",
        "vic_lname",
        "vic_qlfr",
        "vic_alias",
        "vic_age",
        "vic_gndr",
        "sus_fname",
        "sus_midname",
        "sus_lname",
        "sus_qlfr",
        "sus_alias",
        "sus_age",
        "sus_gndr",
    ])

    # Add the victim_details and suspect_details columns
    df["victim_details"] = df.apply(lambda row: f"{row.vic_fname} {row.vic_midname} {row.vic_lname} {row.vic_qlfr} {row.vic_alias} ({row.vic_age}/{row.vic_gndr})", axis=1)
    df["suspect_details"] = df.apply(lambda row: f"{row.sus_fname} {row.sus_midname} {row.sus_lname} {row.sus_qlfr} {row.sus_alias} ({row.sus_age}/{row.sus_gndr})", axis=1)

    # Drop the individual victim and suspect details columns
    df = df.drop(columns=[
        "time_reported",
        "time_committed",
        "vic_fname",
        "vic_midname",
        "vic_lname",
        "vic_qlfr",
        "vic_alias",
        "vic_age",
        "vic_gndr",
        "sus_fname",
        "sus_midname",
        "sus_lname",
        "sus_qlfr",
        "sus_alias",
        "sus_age",
        "sus_gndr",
    ])

        # Rename columns if needed
    df = df.rename(columns={
        "entry_number": "Entry Number",
        "offense": "Offense",
        "case_status": "Case Status",
        "date_reported": "Date Reported",
        "date_committed": "Date Committed",
        "victim_details": "Victim Details",
        "suspect_details": "Suspect Details"
    })

    # Return the DataFrame as a JSON response
    return df