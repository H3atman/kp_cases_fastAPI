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
names = []
usernames = []
hashed_passwords = []

for user in users_data:
    names.append(user['username'])  # Assuming username is used as the name
    usernames.append(user['username'])
    hashed_passwords.append(user['password'])  # Ensure these are hashed

credentials = {
    "usernames": {
        username: {"name": name, "password": hashed_password}
        for name, username, hashed_password in zip(names, usernames, hashed_passwords)
    }
}

# Initialize authenticator
authenticator = stauth.Authenticate(
    credentials,
    "my_app",
    "auth_cookie_name",
    cookie_expiry_days=30
)

# Login widget
authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')