from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, Time, ForeignKey, func, TIMESTAMP
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
    date_encoded = Column(TIMESTAMP(timezone=True), server_default=func.now())
    entry_number = Column(String, index=True, nullable=False)
    pro = Column(String, nullable=True)
    ppo_cpo = Column(String, nullable=True)
    mps_cps = Column(String, nullable=True)
    offense = Column(String, nullable=False)
    offense_class = Column(String, nullable=False)
    case_status = Column(String, nullable=False)
    check = Column(Boolean, nullable=False)
    narrative = Column(String, nullable=True)
    date_reported = Column(Date, nullable=False)
    time_reported = Column(Time, nullable=True)
    date_committed = Column(Date, nullable=True)
    time_committed = Column(Time, nullable=True)

    victims = relationship("Victim_Details", back_populates="case")
    suspects = relationship("Suspect_Details", back_populates="case")


class Victim_Details(Base):
    __tablename__ = 'victim_details'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_encoded = Column(TIMESTAMP(timezone=True), server_default=func.now())
    # entry_number = Column(String, index=True)
    entry_number = Column(String, ForeignKey('case_details.entry_number'), index=True)
    pro = Column(String)
    ppo_cpo = Column(String)
    mps_cps = Column(String)
    vic_fname = Column(String)
    vic_midname = Column(String)
    vic_lname = Column(String)
    vic_qlfr = Column(String)
    vic_alias = Column(String)
    vic_gndr = Column(String)
    vic_age = Column(Integer)
    vic_distprov = Column(String)
    vic_cityMun = Column(String)
    vic_brgy = Column(String)
    vic_strName = Column(String)

    case = relationship("CaseDetails", back_populates="victims")


class Suspect_Details(Base):
    __tablename__ = 'suspect_details'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_encoded = Column(TIMESTAMP(timezone=True), server_default=func.now())
    # entry_number = Column(String, index=True)
    entry_number = Column(String, ForeignKey('case_details.entry_number'), index=True)
    pro = Column(String)
    ppo_cpo = Column(String)
    mps_cps = Column(String)
    sus_fname = Column(String)
    sus_midname = Column(String)
    sus_lname = Column(String)
    sus_qlfr = Column(String)
    sus_alias = Column(String)
    sus_gndr = Column(String)
    sus_age = Column(Integer)
    sus_distprov = Column(String)
    sus_cityMun = Column(String)
    sus_brgy = Column(String)
    sus_strName = Column(String)

    case = relationship("CaseDetails", back_populates="suspects")