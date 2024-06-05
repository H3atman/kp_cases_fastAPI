import requests
from config.models import CaseDetails
import streamlit as st
from datetime import date, time
import json

# import json

def dataEntry_caseDetails(entry_number, case_detail, offense_detail, api_url):
    # Convert date and time objects to strings
    def serialize_datetime(obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        return obj

    # Check if offense_detail has an offense attribute
    if not hasattr(offense_detail, 'offense'):
        raise ValueError("offense_detail does not have an 'offense' attribute")

    # Create the data dictionary
    data = {
        "entry_number": entry_number,
        "pro":case_detail.pro,
        "ppo_cpo":case_detail.ppo_cpo,
        "mps_cps":case_detail.mps_cps,
        "offense": offense_detail.offense,
        "offense_class": offense_detail.offense_class,
        "case_status": offense_detail.case_status,
        "check": offense_detail.check,
        "narrative": case_detail.det_narrative,
        "date_reported": serialize_datetime(case_detail.dt_reported)
    }

    # Add optional fields if they are not None
    if case_detail.time_reported is not None:
        data["time_reported"] = serialize_datetime(case_detail.time_reported)
    if case_detail.dt_committed is not None:
        data["date_committed"] = serialize_datetime(case_detail.dt_committed)
    if case_detail.time_committed is not None:
        data["time_committed"] = serialize_datetime(case_detail.time_committed)

    # Create a new CaseDetails SQLAlchemy model instance with the data
    db_case_details = CaseDetails(**data)

    # Proceed with database operations
    case_detail_data = db_case_details.__dict__
    case_detail_data.pop("_sa_instance_state", None)  # Remove the non-serializable attribute

    # Convert case_detail_data to a JSON serializable form, excluding None values
    serializable_case_detail_data = {
        key: serialize_datetime(value) if isinstance(value, (date, time)) else value
        for key, value in case_detail_data.items() if value is not None
    }

    response = requests.post(f"{api_url}/case-details/", json=serializable_case_detail_data)

    if response.status_code == 200:
        print("Case Detail Data successfully input to the database.")
    else:
        print("Failed to input data to the database.")





def dataEntry_victimDetails(entry_number, victim_data, api_url):
    # Ensure victim_data is a dictionary
    if isinstance(victim_data, str):
        # Handle the case where victim_data is a string, perhaps from JSON
        try:
            victim_data = json.loads(victim_data)
        except json.JSONDecodeError:
            print("Invalid victim_data format. Expected a JSON string.")
            return
    elif not isinstance(victim_data, dict):
        print("Invalid victim_data format. Expected a dictionary.")
        return

    # Add entry_number to victim_data
    victim_data['entry_number'] = entry_number

    # Filter out None values
    victim_data = {k: v for k, v in victim_data.items() if v is not None}

    # Print the data to be sent
    # print("Data to be sent:", victim_data)

    # Send the data as a JSON payload to the API
    response = requests.post(f"{api_url}/victim-new-entry/", json=victim_data)

    # Print the response status and text for debugging
    # print("Response status code:", response.status_code)
    # print("Response text:", response.text)

    if response.status_code == 200:
        print("Victim Data successfully input to the database.")
    else:
        print("Failed to input data to the database. Status code:", response.status_code)




def dataEntry_suspectDetails(entry_number, suspect_data, api_url):
    # Ensure suspect_data is a dictionary
    if isinstance(suspect_data, str):
        # Handle the case where suspect_data is a string, perhaps from JSON
        import json
        try:
            suspect_data = json.loads(suspect_data)
        except json.JSONDecodeError:
            print("Invalid suspect_data format. Expected a JSON string.")
            return
    elif not isinstance(suspect_data, dict):
        print("Invalid suspect_data format. Expected a dictionary.")
        return

    # Add entry_number to suspect_data
    suspect_data['entry_number'] = entry_number

    # Filter out None values
    suspect_data = {k: v for k, v in suspect_data.items() if v is not None}

    # Send the data as a JSON payload to the API
    response = requests.post(f"{api_url}/suspect-new-entry/", json=suspect_data)

    if response.status_code == 200:
        print("Suspect Data successfully input to the database.")
    else:
        print("Failed to input data to the database.")

