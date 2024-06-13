import streamlit as st
from modules.newEntry_comp import newEntry
from modules.auth_utils import fetch_users, prepare_credentials, initialize_authenticator
from modules.encoded_data import encoded_data_mps, encoded_data_ppo, encoded_data_pro
from modules.query_cases_encoded import search_cases, display_cases

# Set page configuration
st.set_page_config(page_title="KP Cases Dashboard")

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
    st.session_state['username'] = st.session_state["name"]
    authenticator.logout()
    username = st.session_state['username']
    user_info = credentials["usernames"].get(username, {})
    mps_cps = user_info.get("mps_cps", "")
    ppo_cpo = user_info.get("ppo_cpo", "")
    pro = user_info.get("pro","")
    role = user_info.get("role","")
    st.title(f'Welcome *{mps_cps}*, *{ppo_cpo}*')

    # Manage navigation between pages
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        if role == "encoder":
            # Create tabs for navigation
            tab1, tab2, tab3, tab4 = st.tabs(["New Entry", "Encoded Data", "Search and Edit Entry", "Change Password"])

            with tab1:
                st.subheader("New Entry")
                entryCode = newEntry(mps_cps)

            with tab2:
                encoded_data_mps(mps_cps)

            with tab3:
                st.subheader("You can search and edit your entries here")
                search_cases(mps_cps)
                display_cases()

            with tab4:
                st.subheader("You can change your password here")
                st.write(":red[Under Development]")

        if role == "viewer":
            # Create tabs for navigation
            tab1, tab2, tab3 = st.tabs(["Encoded Data", "Extract Report", "Change Password"])

            with tab1:
                encoded_data_ppo(ppo_cpo)

            with tab2:
                st.subheader("You can extract report here in Detailed Crime Analysis Report Format")
                st.write(":red[Under Development]")
                # search_cases(mps_cps)
                # display_cases()

            with tab3:
                st.subheader("You can change your password here")
                st.write(":red[Under Development]")

        if role == "administrator":
            # Create tabs for navigation
            tab1, tab2, tab3 = st.tabs(["Encoded Data", "Extract Report", "Change Password"])

            with tab1:
                encoded_data_pro(pro)

            with tab2:
                st.subheader("You can extract report here in Detailed Crime Analysis Report Format")
                st.write(":red[Under Development]")
                # search_cases(mps_cps)
                # display_cases()

            with tab3:
                st.subheader("You can change your password here")
                st.write(":red[Under Development]")



elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
