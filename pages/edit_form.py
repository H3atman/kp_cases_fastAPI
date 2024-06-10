import streamlit as st
from modules.auth_utils import fetch_users, prepare_credentials, initialize_authenticator
from modules.get_data import get_victim_data
from edit_data_forms import offenses, victims, suspects, caseDetails

def show_error(message):
    st.error(message)

def edit_form(entry_number, mps_cps):
    hide_sidebar_css = '''
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    '''
    st.markdown(hide_sidebar_css, unsafe_allow_html=True)

    users_data = fetch_users()
    credentials = prepare_credentials(users_data)
    authenticator = initialize_authenticator(credentials)
    authenticator.login(fields={'Form name': 'PRO 12 KP Cases Details Encoding User\'s Login'})

    if st.session_state["authentication_status"]:
        st.session_state['username'] = st.session_state["name"]
        username = st.session_state['username']
        user_info = credentials["usernames"].get(username, {})
        pro = "PRO 12"
        ppo_cpo = user_info.get("ppo_cpo", "")

        vic_data = get_victim_data(entry_number, mps_cps)
        if vic_data is None:
            return

        st.title('Edit Entry Katarungang Pambarangay Cases Detailed Report')
        st.text_input("Entry Number", value=entry_number, disabled=True)

        complainant, suspect, caseDetail, offense = st.tabs(["Complainant / Victim's Profile", "Suspect/s Profile", "Case Detail", "Offense"])

        with complainant:
            st.subheader("Victim's Profile")
            victims.editVictim(vic_data)

        with suspect:
            st.subheader("Suspect's Profile")

        with caseDetail:
            st.subheader("Case Details")

        with offense:
            st.subheader("Offense")

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')

    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

query_params = st.experimental_get_query_params()
if "entry_number" in query_params and "mps_cps" in query_params:
    edit_form(query_params["entry_number"][0], query_params["mps_cps"][0])
