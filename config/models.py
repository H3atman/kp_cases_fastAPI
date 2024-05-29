from sqlalchemy import Boolean, Column, Integer, String
from config.database import Base

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