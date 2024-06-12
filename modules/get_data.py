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


def get_suspect_data(entry_number):
    response = requests.get(f"{api_endpoint}/get_suspect_details", params={"entry_number": entry_number})
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list):
            suspect = data[0]
            
            suspect_data = {
                "id": suspect.get("id"),
                "pro": suspect.get("pro"),
                "mps_cps": suspect.get("mps_cps"),
                "sus_midname": suspect.get("sus_midname"),
                "sus_qlfr": suspect.get("sus_qlfr"),
                "sus_gndr": suspect.get("sus_gndr"),
                "sus_distprov": suspect.get("sus_distprov"),
                "sus_brgy": suspect.get("sus_brgy"),
                "date_encoded": suspect.get("date_encoded"),
                "entry_number": suspect.get("entry_number"),
                "ppo_cpo": suspect.get("ppo_cpo"),
                "sus_fname": suspect.get("sus_fname"),
                "sus_lname": suspect.get("sus_lname"),
                "sus_alias": suspect.get("sus_alias"),
                "sus_age": suspect.get("sus_age"),
                "sus_cityMun": suspect.get("sus_cityMun"),
                "sus_strName": suspect.get("sus_strName")
            }
            
            return suspect_data
        else:
            print("Unexpected JSON structure")
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")


def get_case_data(entry_number):
    response = requests.get(f"{api_endpoint}/get_case_details", params={"entry_number": entry_number})
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list):
            case = data[0]
            
            case_data = {
                "id": case.get("id"),
                "pro": case.get("pro"),
                "mps_cps": case.get("mps_cps"),
                "offense": case.get("offense"),
                "case_status": case.get("case_status"),
                "narrative": case.get("narrative"),
                "time_reported": case.get("time_reported"),
                "time_committed": case.get("time_committed"),
                "date_encoded": case.get("date_encoded"),
                "entry_number": case.get("entry_number"),
                "ppo_cpo": case.get("ppo_cpo"),
                "offense_class": case.get("offense_class"),
                "check": case.get("check"),
                "date_reported": case.get("date_reported"),
                "date_committed": case.get("date_committed")
            }
            
            return case_data
        else:
            print("Unexpected JSON structure")
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
