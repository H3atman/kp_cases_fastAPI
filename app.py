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
        user['username']: {"name": user['username'], "password": user['password']}
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

if st.session_state['authentication_status'] is None:
    st.title("Welcome to Encoding of KP Cases Details")

    user_action = st.selectbox("Please select Action", options=["LOGIN", "REGISTER"])

    if user_action == "LOGIN":
        st.title("User Login")
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

    else:
        st.title("User Registration")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            response = requests.post("http://127.0.0.1:8000/register/", json={"username": username, "password": password})
            if response.status_code == 200:
                st.success("Registration successful!")
            else:
                st.error("Registration failed: " + response.json().get("detail", "Unknown error"))
else:
    authenticator.logout("Logout", "main")
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
