import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager
import jwt

st.set_page_config("KP Cases Detailed Entry")

css = '''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

# Function to check login status
def check_login():
    token = st.session_state.get('access_token', None)
    if token:
        response = requests.get("http://127.0.0.1:8000/users/me", headers={"Authorization": f"Bearer {token}"})
        return response.status_code == 200
    return False

# Function to log in
def login(username, password):
    response = requests.post("http://127.0.0.1:8000/token", data={"username": username, "password": password})
    if response.status_code == 200:
        data = response.json()
        st.session_state['access_token'] = data['access_token']
        return True
    else:
        return False

# Display login form if not authenticated
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = check_login()

if st.session_state['authentication_status']:
    st.title(f"Welcome {st.session_state.get('username', 'User')}")
    if st.button('Logout'):
        st.session_state['authentication_status'] = False
        st.session_state['access_token'] = None
        st.session_state['username'] = None
else:
    st.title("KP Cases Detailed Encoding")
    with st.form("login_form"):
        st.subheader("User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if login(username, password):
                st.session_state['username'] = username
                st.session_state['authentication_status'] = True
                st.experimental_rerun()
            else:
                st.error('Invalid username or password')
