import streamlit as st
from modules.auth_utils import fetch_users, prepare_credentials, initialize_authenticator
from modules.newEntry_comp import newEntry  # Import custom component for new entries

# Check if 'combined_value' is in the session state
if "combined_value" not in st.session_state:
    st.session_state.combined_value = None

if st.session_state.combined_value is None:
    st.switch_page('app.py')
else:
    entryNumber = st.session_state.combined_value

def entryForm(entryNumber):
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
        if st.button("Home"):
            st.switch_page('app.py')
        username = st.session_state['username']
        user_info = credentials["usernames"].get(username, {})
        mps_cps = user_info.get("mps_cps", "")
        ppo_cpo = user_info.get("ppo_cpo", "")
        # Display entry form
        st.text_input("Entry Number", value=entryNumber, disabled=True)
        st.write(f"You are now encoding the {mps_cps} which is part of {ppo_cpo}")


    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

# Call the entryForm function with default values
entryForm(entryNumber)
