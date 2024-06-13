import requests
from fastapi import HTTPException
import streamlit as st
import streamlit_authenticator as stauth
from config.database import api_endpoint


@st.cache_data(ttl="60m")
def fetch_users():
    response = requests.get(f"{api_endpoint}/users/")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch users")
    return response.json()

def prepare_credentials(users_data):
    credentials = {
        "usernames": {
            user['username']: {
                "name": user['username'],
                "password": user['password'],
                "mps_cps": user.get('mps_cps', ''),  # Include mps_cps, defaulting to an empty string if not present
                "ppo_cpo": user.get('ppo_cpo', ''),   # Include ppo_cpo, defaulting to an empty string if not present
                "role": user.get('role','')
            }
            for user in users_data
        }
    }
    return credentials

def initialize_authenticator(credentials):
    authenticator = stauth.Authenticate(
        credentials,
        "my_app",
        "auth_cookie_name",
        cookie_expiry_days=30
    )
    return authenticator
