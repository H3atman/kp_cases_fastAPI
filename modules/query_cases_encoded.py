import streamlit as st
from config.database import api_endpoint
import requests
from datetime import datetime
from time import sleep

def search_cases(mps_cps):
    cases = []
    entry_search = st.text_input("Input Entry Number")
    if st.button("Search Entry", use_container_width=True, type="primary", key="search_button"):
        st.session_state.clear
        if entry_search:
            response = requests.get(f"{api_endpoint}/search_case", params={"entry_number": entry_search, "mps_cps": mps_cps})
            
            if response.status_code == 200:
                st.session_state.cases = response.json()
            elif response.status_code == 404:
                st.error("Cases not found")
                st.session_state.cases = []
            else:
                st.error(f"An error occurred: {response.status_code}")
                st.session_state.cases = []
        else:
            st.warning("Please enter an entry number")
            st.session_state.cases = []
        #     if response.status_code == 200:
        #         cases = response.json()
        #     elif response.status_code == 404:
        #         st.error("Cases not found")
        #         cases = []
        #     else:
        #         st.error(f"An error occurred: {response.status_code}")
        #         cases = []
        # else:
        #     st.warning("Please enter an entry number")
        #     cases = []

    return cases

# Function to display cases
def display_cases(mps_cps):
    if "cases" in st.session_state and st.session_state.cases:
        for case in st.session_state.cases:
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**:red[ENTRY NUMBER:]** {case['entry_number']}")
                    st.write(f":blue-background[**STATION:**] {case['mps_cps']}")
                    st.write(f":blue-background[**OFFENSE:**] {case['offense']}")
                    date_encoded = datetime.fromisoformat(case['date_encoded']).strftime("%m/%d/%Y %I:%M %p")
                    st.write(f":blue-background[**DATE ENCODED:**] {date_encoded}")
                with col2:
                    st.write(f":blue-background[**VICTIM:**] {case['victim_details']}")
                    st.write(f":blue-background[**SUSPECT:**] {case['suspect_details']}")


                if st.button(f"Edit Entry {case['entry_number']}", use_container_width=True, key=f"edit_{case['entry_number']}"):
                    if mps_cps == case['mps_cps']:
                        # Store the entry number to be edited in session state
                        st.session_state.current_entry_number = case['entry_number']
                        # If the entry number does not exist, proceed with creating a new entry
                        response = requests.post(f"{api_endpoint}/temp-edit-entries/", json={"entry_number": st.session_state.current_entry_number})
                        if response.status_code == 200:
                            st.session_state.current_entry_number = response.json()["id"]
                            print(st.session_state.combined_value)
                            st.cache_data.clear
                            st.switch_page("pages/edit_form.py")
                            # st.switch_page("pages/entry_form.py")
                        else:
                            st.error("Failed to store the entry")
                        
                        # st.switch_page("pages/testpage.py")
                    else:
                        st.error("You do not have permission to edit Entry")
                        st.cache_data.clear()
                        st.session_state.clear()
