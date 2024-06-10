import streamlit as st
from config.database import api_endpoint
import requests
from datetime import datetime

def search_cases(mps_cps):
    entry_search = st.text_input("Input Entry Number")
    if st.button("Search Entry", use_container_width=True, type="primary", key="test"):
        if entry_search:
            response = requests.get(f"{api_endpoint}/search_case", params={"entry_number": entry_search, "mps_cps": mps_cps})
            
            if response.status_code == 200:
                cases = response.json()
                for case in cases:
                    with st.container():
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
                            st.experimental_set_query_params(entry_number=case['entry_number'], mps_cps=case['mps_cps'])
                            st.experimental_rerun()

            elif response.status_code == 404:
                st.error("Cases not found")
            else:
                st.error(f"An error occurred: {response.status_code}")
        else:
            st.warning("Please enter an entry number")
