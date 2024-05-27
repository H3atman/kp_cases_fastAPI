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
