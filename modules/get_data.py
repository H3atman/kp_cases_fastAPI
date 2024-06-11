import streamlit as st
from config.database import api_endpoint
import requests
import json


def get_victim_data(entry_number):
    response = requests.get(f"{api_endpoint}/get_victim_details", params={"entry_number": entry_number})
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list):
            victim = data[0]
            
            victim_data = {
                "id": victim.get("id"),
                "pro": victim.get("pro"),
                "mps_cps": victim.get("mps_cps"),
                "vic_midname": victim.get("vic_midname"),
                "vic_qlfr": victim.get("vic_qlfr"),
                "vic_gndr": victim.get("vic_gndr"),
                "vic_distprov": victim.get("vic_distprov"),
                "vic_brgy": victim.get("vic_brgy"),
                "date_encoded": victim.get("date_encoded"),
                "entry_number": victim.get("entry_number"),
                "ppo_cpo": victim.get("ppo_cpo"),
                "vic_fname": victim.get("vic_fname"),
                "vic_lname": victim.get("vic_lname"),
                "vic_alias": victim.get("vic_alias"),
                "vic_age": victim.get("vic_age"),
                "vic_cityMun": victim.get("vic_cityMun"),
                "vic_strName": victim.get("vic_strName")
            }
            
            return victim_data
        else:
            print("Unexpected JSON structure")
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
