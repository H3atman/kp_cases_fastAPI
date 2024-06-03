import requests
from config.models import CaseDetails  # Import your Pydantic model
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

    data = {
        "entry_number": combined_value,
        "offense": offense_detail.offense,
        "offense_class": offense_detail.offense_class,
        "case_status": offense_detail.case_status,
        "check": offense_detail.check,
        "narrative": case_detail.det_narrative,
        "date_reported": serialize_datetime(case_detail.dt_reported),
        "time_reported": serialize_datetime(case_detail.time_reported),
        "date_committed": serialize_datetime(case_detail.dt_committed),
        "time_committed": serialize_datetime(case_detail.time_committed)
    }

    # Create a new CaseDetails SQLAlchemy model instance with the data
    db_case_details = CaseDetails(**data)

    # Proceed with database operations
    if st.button("Submit Data", use_container_width=True, type="primary"):
        case_detail_data = db_case_details.__dict__
        case_detail_data.pop("_sa_instance_state", None)  # Remove the non-serializable attribute
        
        # Convert case_detail_data to a JSON serializable form
        for key, value in case_detail_data.items():
            case_detail_data[key] = serialize_datetime(value)

        response = requests.post(f"{api_url}/case-details/", json=case_detail_data)

        if response.status_code == 200:
            print("Data successfully input to the database.")
        else:
            print("Failed to input data to the database.")

