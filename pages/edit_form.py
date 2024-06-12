from time import sleep
import streamlit as st
from modules.auth_utils import fetch_users, prepare_credentials, initialize_authenticator
import requests
from edit_data_forms import edit_caseDetails, edit_offenses, edit_suspects, edit_victims
from modules.updateEntry_functions import *
from config.database import api_endpoint
from modules.get_data import get_victim_data, get_suspect_data, get_case_data
import concurrent.futures


def process_offense(offense, offense_class, otherOffense, case_status, check):
    if offense is None:
        offense = otherOffense

    return {
        "offense": offense,
        "offense_class": offense_class,
        "case_status": case_status,
        "check": check
    }

# Define the FastAPI base URL
API_URL = api_endpoint

@st.cache_data(ttl="60m")
def get_entry_number(api_url):
    response = requests.get(f"{api_url}/temp-edit-entries/")
    if response.status_code == 200:
        temp_entries = response.json()
        if temp_entries:
            latest_entry = temp_entries[-1]
            combined_value = latest_entry['entry_number']
            entry_id = latest_entry['id']
        else:
            combined_value = None
            entry_id = None
    else:
        st.error("Failed to fetch the combined value")
        combined_value = None
        entry_id = None
    return combined_value, entry_id



# Define a function to show error messages for incomplete data
def show_error(message):
    st.error(message)



def editForm():

    # Set page configuration
    # st.set_page_config(page_title="Edit KP Cases Detailed Entry")

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
        entry_number, entry_id = get_entry_number(API_URL)
        
        # Redirect to home page if combined_value is None
        if entry_number is None:
            st.warning("No combined value found. Redirecting to home page.")
            sleep(3)
            st.switch_page('app.py')

        if st.button("Home"):
            if entry_id is not None:
                requests.delete(f"{API_URL}/temp-edit-entries/{entry_id}")
            st.cache_data.clear()
            st.session_state.clear()
            st.switch_page('app.py')
            

        username = st.session_state['username']
        user_info = credentials["usernames"].get(username, {})
        pro = "PRO 12"
        mps_cps = user_info.get("mps_cps", "") # THERE IS A POSSIBILITY THAT I WILL BE DELETING THIS
        ppo_cpo = user_info.get("ppo_cpo", "") # THERE IS A POSSIBILITY THAT I WILL BE DELETING THIS
        
        #====================================
        # Display entry form
        #====================================
        st.title(':blue-background[Update] Katarungang Pambarangay Cases Detailed Report')
        st.text_input("Entry Number", value=entry_number, disabled=True)

        complainant, suspect, caseDetail, offense = st.tabs(["Complainant / Victim's Profile", "Suspect/s Profile", "Case Detail", "Offense"])

        with complainant:
            st.subheader("Victims's Profile")
            # Query the victims data and return the nessesary variables
            vicdetails = get_victim_data(entry_number)
            victim_data = edit_victims.editVictim(vicdetails)


        with suspect:
            st.subheader("Suspect's Profile")
            susdetails = get_suspect_data(entry_number)
            suspect_data = edit_suspects.editSuspect(susdetails)


        with caseDetail:
            st.subheader("Case Details")
            casedata = get_case_data(entry_number)
            case_detail = edit_caseDetails.edit_case_Details(casedata)
        
        with offense:
            st.subheader("Offense :red[#]")
            offense_detail = edit_offenses.editOffense(casedata)


    # Check completeness of case detail and offense detail
    case_detail_complete = case_detail is not None and offense_detail is not None and hasattr(offense_detail, 'offense')
    if not case_detail_complete:
        show_error("Please Complete the Required Entries in Case Detail and Offense Tab")

    # Check completeness of victim data
    victim_data_complete = victim_data is not None
    if not victim_data_complete:
        show_error("Please Complete the Required Entries in Victim's Profile Tab")

    # Check completeness of suspect data
    suspect_data_complete = suspect_data is not None
    if not suspect_data_complete:
        show_error("Please Complete the Required Entries in Suspect's Profile Tab")

    # Add submit button if all required data is complete
    if case_detail_complete and victim_data_complete and suspect_data_complete:
        if st.button("Update Entry", type="primary", use_container_width=True):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                futures.append(executor.submit(update_case_details, entry_number, case_detail, offense_detail, API_URL))
                futures.append(executor.submit(update_victim_details, entry_number, victim_data, API_URL))
                futures.append(executor.submit(update_suspect_details, entry_number, suspect_data, API_URL))

                # Wait for all futures to complete
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()  # Get the result to raise any exceptions
                    except Exception as e:
                        show_error(f"An error occurred: {e}")
            #  Delete temp-entry and go back to main page
            st.warning(f"Entry Number {entry_number} succesfuly updated")
            sleep(3)
            requests.delete(f"{API_URL}/temp-edit-entries/{entry_id}")
            st.session_state.clear()
            st.cache_data.clear()
            st.switch_page('app.py')




    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


# Call the entryForm function
editForm()