import streamlit as st
from modules.auth_utils import fetch_users, prepare_credentials, initialize_authenticator
import requests
import time
from forms import offenses, victims, suspects, caseDetails
from modules.dataValidation import Entry_Number_Validation
from pydantic import ValidationError



# Define the FastAPI base URL
API_URL = "http://127.0.0.1:8000"

@st.cache_data(ttl="60m")
def fetch_combined_value_and_id(api_url):
    response = requests.get(f"{api_url}/temp-entries/")
    if response.status_code == 200:
        temp_entries = response.json()
        if temp_entries:
            latest_entry = temp_entries[-1]
            combined_value = latest_entry['combined_value']
            entry_id = latest_entry['id']
        else:
            combined_value = None
            entry_id = None
    else:
        st.error("Failed to fetch the combined value")
        combined_value = None
        entry_id = None
    return combined_value, entry_id

def entryForm():

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
        
        # Fetch the combined_value and its ID using the cached function
        combined_value, entry_id = fetch_combined_value_and_id(API_URL)
        
        # Redirect to home page if combined_value is None
        if combined_value is None:
            st.warning("No combined value found. Redirecting to home page.")
            time.sleep(3)
            st.switch_page('app.py')

        if st.button("Home"):
            if entry_id is not None:
                response = requests.delete(f"{API_URL}/temp-entries/{entry_id}")
                if response.status_code == 200:
                    st.success("Successfully deleted the entry")
                else:
                    st.error("Failed to delete the entry")
            st.switch_page('app.py')

        username = st.session_state['username']
        user_info = credentials["usernames"].get(username, {})
        mps_cps = user_info.get("mps_cps", "")
        ppo_cpo = user_info.get("ppo_cpo", "")
        
        #====================================
        # Display entry form
        #====================================
        st.title('Katarungang Pambarangay Cases Detailed Report Encoding')
        st.text_input("Entry Number", value=combined_value, disabled=True)

        complainant, suspect, caseDetail, offense = st.tabs(["Complainant / Victim's Profile", "Suspect/s Profile", "Case Detail", "Offense"])

        with complainant:
            st.subheader("Victims's Profile")
            victim_data = victims.addVictim(mps_cps)


        with suspect:
            st.subheader("Suspect's Profile")
            suspect_data = suspects.addSuspect(mps_cps)


        with caseDetail:
            st.subheader("Case Details")
            case_detail = caseDetails.case_Details()
        
        with offense:
            st.subheader("Offense :red[#]")
            offense_detail = offenses.addOffense()


    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


    data = {
        "entry_number": combined_value,
    }

    # Validate the data using Pydantic
    combined_value_data = ""
    try:
        combined_value_data = Entry_Number_Validation(**data)
        # Data is valid, proceed with database operations
        return combined_value_data
    except ValidationError as e:
        st.error(e)
    finally:
        st.write(combined_value_data)


# Call the entryForm function
entryForm()
