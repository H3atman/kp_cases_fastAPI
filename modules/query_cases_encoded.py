import streamlit as st
from config.database import api_endpoint
import requests
from datetime import datetime
# def container(entry_number, station, offense, date_encoded):
def container():
    with st.container(border=True):
        entry_number = "Test"
        offense = "Test"
        date_encoded = "Test"
        station = "Test"
        st.write(f"<h3>{entry_number}</h3>",unsafe_allow_html=True)
        st.write(station)
        st.write(offense)
        st.write(date_encoded)


def search_cases(mps_cps):
    entry_search = st.text_input("Input Entry Number")
    if st.button("Search Entry", use_container_width=True, type="primary"):
        if entry_search:
            response = requests.get(f"{api_endpoint}/search_case", params={"entry_number": entry_search, "mps_cps": mps_cps})
            
            if response.status_code == 200:
                cases = response.json()
                for case in cases:
                    st.write(f"Entry Number: {case['entry_number']}")
                    st.write(f"Station: {case['mps_cps']}")
                    st.write(f"Offense: {case['offense']}")
                    # Parse the date
                    date_encoded = datetime.fromisoformat(case['date_encoded']).strftime("%m/%d/%Y %I:%M %p")
                    st.write(f"Date Encoded: {date_encoded}")
                    st.write("---")
            elif response.status_code == 404:
                st.error("Cases not found")
            else:
                st.error(f"An error occurred: {response.status_code}")
        else:
            st.warning("Please enter an entry number")
    container()

# Assuming you provide mps_cps as an argument or set it somewhere
# search_cases()
