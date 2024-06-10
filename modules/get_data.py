import streamlit as st
from config.database import api_endpoint
import requests
import json


def get_victim_data(entry_number, mps_cps):
    with st.spinner("Fetching case count..."):
        response = requests.get(f"{api_endpoint}/get_victim_details", params={"entry_number": entry_number,"mps_cps": mps_cps})
        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                st.error("Error decoding JSON from response")
                return
            finally:
                data
        else:
            st.error(f"Failed to fetch victim data: Received status code {response.status_code}")
