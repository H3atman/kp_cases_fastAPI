import streamlit as st
import streamlit_authenticator as stauth
import requests
from fastapi import HTTPException

# Function to fetch users from FastAPI
def fetch_users():
    response = requests.get("http://127.0.0.1:8000/users/")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch users")
    return response.json()

# Fetch users from FastAPI
users_data = fetch_users()

# Prepare data for streamlit-authenticator
credentials = {
    "usernames": {
        user['username']: {
            "name": user['username'],
            "password": user['password'],
            "mps_cps": user.get('mps_cps', ''),  # Include mps_cps, defaulting to an empty string if not present
            "ppo_cpo": user.get('ppo_cpo', '')   # Include ppo_cpo, defaulting to an empty string if not present
        }
        for user in users_data
    }
}

# Initialize authenticator
authenticator = stauth.Authenticate(
    credentials,
    "my_app",
    "auth_cookie_name",
    cookie_expiry_days=30
)

# Check if user is authenticated
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# Display login widget if not authenticated
if st.session_state['authentication_status'] is None:
    login_slot = st.empty()
    login_slot.title("User Login")
    authenticator.login()

# Process authentication result
if st.session_state["authentication_status"]:
    login_slot = st.empty()
    login_slot.empty()  # Remove login title
    st.session_state['username'] = st.session_state["name"]  # Store username in session state
    authenticator.logout()  # Logout after storing username
    username = st.session_state['username']  # Retrieve username from session state
    user_info = credentials["usernames"].get(username, {})
    mps_cps = user_info.get("mps_cps", "")
    ppo_cpo = user_info.get("ppo_cpo", "")
    st.title(f'Welcome *{ppo_cpo}*, *{mps_cps}*')
else:
    st.warning('Please enter your username and password')
