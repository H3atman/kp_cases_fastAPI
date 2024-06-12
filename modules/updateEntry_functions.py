import requests
from config.models import CaseDetails
from datetime import date, time
import json



def update_case_details(entry_number, case_detail, offense_detail, api_url):

    def serialize_datetime(obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        return obj
    
    if not hasattr(offense_detail, 'offense'):
        raise ValueError("offense_detail does not have an 'offense' attribute")

    data = {
        "entry_number": entry_number,
        "pro": case_detail.pro,
        "ppo_cpo": case_detail.ppo_cpo,
        "mps_cps": case_detail.mps_cps,
        "offense": offense_detail.offense,
        "offense_class": offense_detail.offense_class,
        "case_status": offense_detail.case_status,
        "check": offense_detail.check,
        "narrative": case_detail.det_narrative,
        "date_reported": serialize_datetime(case_detail.dt_reported)
    }

    if case_detail.time_reported is not None:
        data["time_reported"] = serialize_datetime(case_detail.time_reported)
    if case_detail.dt_committed is not None:
        data["date_committed"] = serialize_datetime(case_detail.dt_committed)
    if case_detail.time_committed is not None:
        data["time_committed"] = serialize_datetime(case_detail.time_committed)

    print("Request data:", data) # Addedd Code for debugging
    response = requests.put(f"{api_url}/update-case-details/{entry_number}", json=data)
    print("Response status code:", response.status_code)  # Addedd Code for debugging
    print("Response text:", response.text)  # Addedd Code for debugging

    if response.status_code == 200:
        print("Case Detail Data successfully updated in the database.")
    else:
        print("Failed to update data in the database.")



def update_victim_details(entry_number, victim_data, api_url):
    if isinstance(victim_data, str):
        try:
            victim_data = json.loads(victim_data)
        except json.JSONDecodeError:
            print("Invalid victim_data format. Expected a JSON string.")
            return
    elif not isinstance(victim_data, dict):
        print("Invalid victim_data format. Expected a dictionary.")
        return

    victim_data['entry_number'] = entry_number

    victim_data = {k: v for k, v in victim_data.items() if v is not None}

    print("Request data:", victim_data) # Addedd Code for debugging
    response = requests.put(f"{api_url}/update-victim-details/{entry_number}", json=victim_data)
    print("Response status code:", response.status_code)  # Addedd Code for debugging
    print("Response text:", response.text)  # Addedd Code for debugging

    if response.status_code == 200:
        print("Victim Data successfully updated in the database.")
    else:
        print("Failed to update data in the database. Status code:", response.status_code)




def update_suspect_details(entry_number, suspect_data, api_url):
    if isinstance(suspect_data, str):
        try:
            suspect_data = json.loads(suspect_data)
        except json.JSONDecodeError:
            print("Invalid suspect_data format. Expected a JSON string.")
            return
    elif not isinstance(suspect_data, dict):
        print("Invalid suspect_data format. Expected a dictionary.")
        return

    suspect_data['entry_number'] = entry_number

    suspect_data = {k: v for k, v in suspect_data.items() if v is not None}

    print("Request data:", suspect_data) # Addedd Code for debugging
    response = requests.put(f"{api_url}/update-suspect-details/{entry_number}", json=suspect_data)
    print("Response status code:", response.status_code)  # Addedd Code for debugging
    print("Response text:", response.text)  # Addedd Code for debugging


    if response.status_code == 200:
        print("Suspect Data successfully updated in the database.")
    else:
        print("Failed to update data in the database.")
