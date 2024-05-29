from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
from uuid import UUID, uuid4
import bcrypt
from typing import List
import config.models as models
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

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
        orm_mode = True

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
def read_station_by_mps_cps(mps_cps: str, db: Session = Depends(get_db)):
    station_sequence = db.execute(select(models.Station_Sequence).where(models.Station_Sequence.mps_cps == mps_cps)).scalars().all()
    
    if not station_sequence:
        raise HTTPException(status_code=404, detail="Station sequence not found")

    return station_sequence
