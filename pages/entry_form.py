from time import sleep
import streamlit as st
from modules.auth_utils import fetch_users, prepare_credentials, initialize_authenticator
import requests
from forms import offenses, victims, suspects, caseDetails
from modules.newEntry_functions import *
from pydantic import ValidationError
import concurrent.futures
from config.database import api_endpoint


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



# Define a function to show error messages for incomplete data
def show_error(message):
    st.error(message)



def entryForm():

    # Set page configuration
    # st.set_page_config(page_title="KP Cases Detailed Entry")

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
            sleep(3)
            st.switch_page('app.py')

        if st.button("Home"):
            if entry_id is not None:
                requests.delete(f"{API_URL}/temp-entries/{entry_id}")
                # if response.status_code == 200:
                #     st.success("Successfully deleted the entry")
                # else:
                #     st.error("Failed to delete the entry")
            st.switch_page('app.py')

        username = st.session_state['username']
        user_info = credentials["usernames"].get(username, {})
        pro = "PRO 12"
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
            victim_data = victims.addVictim(mps_cps,ppo_cpo,pro)


        with suspect:
            st.subheader("Suspect's Profile")
            suspect_data = suspects.addSuspect(mps_cps,ppo_cpo,pro)


        with caseDetail:
            st.subheader("Case Details")
            case_detail = caseDetails.case_Details(mps_cps,ppo_cpo,pro)
        
        with offense:
            st.subheader("Offense :red[#]")
            offense_detail = offenses.addOffense()


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
        if st.button("Submit Entry", type="primary", use_container_width=True):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                futures.append(executor.submit(dataEntry_caseDetails, combined_value, case_detail, offense_detail, API_URL))
                futures.append(executor.submit(dataEntry_victimDetails, combined_value, victim_data, API_URL))
                futures.append(executor.submit(dataEntry_suspectDetails, combined_value, suspect_data, API_URL))

                # Wait for all futures to complete
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()  # Get the result to raise any exceptions
                    except Exception as e:
                        show_error(f"An error occurred: {e}")
            #  Delete temp-entry and go back to main page
            st.success(f"Entry Number {combined_value} succesfuly submitted")
            sleep(3)
            requests.delete(f"{API_URL}/temp-entries/{entry_id}")
            st.switch_page('app.py')




    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


# Call the entryForm function
entryForm()


