import streamlit as st
from config.database import api_endpoint
import requests
from datetime import datetime

def search_cases(mps_cps):
    entry_search = st.text_input("Input Entry Number")
    if st.button("Search Entry", use_container_width=True, type="primary"):
        if entry_search:
            response = requests.get(f"{api_endpoint}/search_case", params={"entry_number": entry_search, "mps_cps": mps_cps})
            
            if response.status_code == 200:
                cases = response.json()
                for case in cases:
                    with st.container(border=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**:red[ENTRY NUMBER:]** {case['entry_number']}")
                            st.write(f":blue-background[**STATION:**] {case['mps_cps']}")
                            st.write(f":blue-background[**OFFENSE:**] {case['offense']}")
                            # Parse the date
                            date_encoded = datetime.fromisoformat(case['date_encoded']).strftime("%m/%d/%Y %I:%M %p")
                            st.write(f":blue-background[**DATE ENCODED:**] {date_encoded}")
                        with col2:
                            st.write(f":blue-background[**VICTIM:**] {case['victim_details']}")
                            st.write(f":blue-background[**SUSPECT:**]: {case['suspect_details']}")

                        st.button("Edit Entry",use_container_width=True,key={case['entry_number']})

            elif response.status_code == 404:
                st.error("Cases not found")
            else:
                st.error(f"An error occurred: {response.status_code}")
        else:
            st.warning("Please enter an entry number")

# Assuming you provide mps_cps as an argument or set it somewhere
# search_cases()
