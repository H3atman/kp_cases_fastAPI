from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import streamlit as st

# Get the PostgreSQL connection details from the secrets
pg_conn = st.secrets["connections"]["postgresql"]


DATABASE_URL = f"postgresql://{pg_conn['username']}:{pg_conn['password']}@{pg_conn['host']}:{pg_conn['port']}/{pg_conn['database']}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# API Endpoint
api = st.secrets["url"]

api_endpoint = f"{api['ip']}"