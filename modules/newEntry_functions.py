import requests
from config.models import CaseDetails
import streamlit as st
from datetime import date, time

def validate_and_input_data_to_database(combined_value, case_detail, offense_detail, api_url):
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
        "entry_number": combined_value,
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
    if st.button("Submit Data", use_container_width=True, type="primary"):
        case_detail_data = db_case_details.__dict__
        case_detail_data.pop("_sa_instance_state", None)  # Remove the non-serializable attribute

        # Convert case_detail_data to a JSON serializable form, excluding None values
        serializable_case_detail_data = {
            key: serialize_datetime(value) if isinstance(value, (date, time)) else value
            for key, value in case_detail_data.items() if value is not None
        }

        response = requests.post(f"{api_url}/case-details/", json=serializable_case_detail_data)

        if response.status_code == 200:
            print("Data successfully input to the database.")
        else:
            print("Failed to input data to the database.")
