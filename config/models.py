from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

class UserBase(Base):
    __tablename__ = 'userbase'

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_logged_in = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    mps_cps = Column(String)
    ppo_cpo = Column(String)


class Station_Sequence(Base):
    __tablename__ = 'station_sequene'

    seq = Column(String,primary_key=True, index=True)
    mps_cps = Column(String)
    ppo_cpo = Column(String)

class Barangay(Base):
    __tablename__ = 'regionxii_brgy'

    id = Column(Integer, primary_key=True, index=True)
    province = Column(String)
    mun_city = Column(String)
    mps_cps = Column(String)
    ppo_cpo = Column(String)
    brgy = Column(String)

class TempEntry(Base):
    __tablename__ = 'temp_entries'

    id = Column(Integer, primary_key=True, index=True)
    combined_value = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Province_Brgy_Details(Base):
    __tablename__ = 'regionxii_brgy'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    province = Column(String)
    mun_city = Column(String)
    ppo_cpo = Column(String)
    mps_cps = Column(String)
    brgy = Column(String)

class Offense(Base):
    __tablename__ = 'offense_class'

    id = Column(Integer, primary_key=True, index=True)
    incidents = Column(String)
    classification = Column(String)



# =====================================================

class CaseDetails(Base):
    __tablename__ = 'case_details'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_number = Column(String, index=True)
    offense = Column(String)
    offense_class = Column(String)
    case_status = Column(String)
    check = Column(Boolean)


    narrative = Column(String)
    date_reported = Column(Date)
    time_reported = Column(Time)
    date_committed = Column(Date)
    time_committed = Column(Time)