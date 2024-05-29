import streamlit as st
from modules.newEntry_comp import newEntry  # Import custom component for new entries
from modules.auth_utils import fetch_users, prepare_credentials, initialize_authenticator  # Import authentication utilities

# Set page configuration
st.set_page_config(page_title="KP Cases Detailed Entry")

# Hide the sidebar with custom CSS
hide_sidebar_css = '''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(hide_sidebar_css, unsafe_allow_html=True)

# Fetch users from FastAPI and prepare credentials
users_data = fetch_users()
credentials = prepare_credentials(users_data)

# Initialize the authenticator
authenticator = initialize_authenticator(credentials)

authenticator.login(fields={'Form name': 'PRO 12 KP Cases Details Encoding User\'s Login'})

if st.session_state["authentication_status"]:
    # If authenticated, store and retrieve username
    st.session_state['username'] = st.session_state["name"]
    authenticator.logout()  # Provide logout functionality
    username = st.session_state['username']
    user_info = credentials["usernames"].get(username, {})
    mps_cps = user_info.get("mps_cps", "")
    ppo_cpo = user_info.get("ppo_cpo", "")
    st.title(f'Welcome *{mps_cps}*, *{ppo_cpo}*')

    # Create tabs for navigation
    tab1, tab2, tab3 = st.tabs(["New Entry", "Encoded Data", "Change Password"])
    
    with tab1:
        st.subheader("New Entry")
        entryCode = newEntry(mps_cps)

    with tab2:
        st.subheader("Show Encoded Data")

    with tab3:
        st.subheader("You can change your password here")

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


