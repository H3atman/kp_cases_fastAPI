import streamlit as st
from modules.ui_models import input_time_committed, input_time_reported
import datetime
from modules.dataValidation import Case_Detail_Validation
from pydantic import ValidationError

def process_date(date_str):
    """
    Convert a date string in the format YYYY-MM-DD to a datetime.date object.
    If the input is None or the format is incorrect, return the current date.
    """
    if date_str:
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            st.error("The date format in casedata is incorrect. Expected format: YYYY-MM-DD")
            return None
    else:
        return None

def process_time(time_str):
    """
    Convert a time string in the format HH:MM:SS to HH:MM AM/PM format.
    If the input is None or the format is incorrect, return an empty string.
    """
    if time_str:
        try:
            time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S")
            return time_obj.strftime("%I:%M %p")
        except ValueError:
            st.error("The time format in casedata is incorrect. Expected format: HH:MM:SS")
            return ""
    else:
        return ""

def edit_case_Details(casedata):
    det_narrative = st.text_area("Narrative",value=casedata.get("narrative"))


    pro = casedata.get("pro")
    ppo_cpo = casedata.get("ppo_cpo")
    mps_cps = casedata.get("mps_cps")

    st.write("---")

    DTreported, DTcommitted = st.columns(2)

    # Initialize session state for times if not already done
    if "input_time_reported" not in st.session_state:
        st.session_state.input_time_reported = None
    if "input_time_committed" not in st.session_state:
        st.session_state.input_time_committed = None

    # Handling Date and Time Reported
    with DTreported:
        st.subheader("Date & Time Reported")

        processed_date_str = casedata.get("date_reported")
        # Use the function to process the date
        processed_date = process_date(processed_date_str)
        dt_reported = st.date_input(
            "Date Reported :red[#]",
            help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month",
            format="YYYY/MM/DD",value=processed_date
        )
        # if dt_reported == datetime.date.today():
        #     st.warning("Please change the Date Reported")
        
        col1, col2 = st.columns(2)
        time_reported_str = casedata.get("time_reported")
        time_reported_str = process_time(time_reported_str)
        
        if st.session_state.input_time_reported:
            time_reported_str = st.session_state.input_time_reported.strftime("%I:%M %p")
        col1.text_input("Time Reported", value=time_reported_str, disabled=True)
        col2.write("\n")
        col2.write("\n")
        if col2.button("Enter Time", use_container_width=True, key="timereported"):
            input_time_reported()

    # Handling Date and Time Committed
    with DTcommitted:
        st.subheader("Date & Time Committed")

        processed_date_str = casedata.get("date_committed")
        # Use the function to process the date
        processed_date = process_date(processed_date_str)
        dt_committed = st.date_input(
            "Date Committed",
            help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month",
            format="YYYY/MM/DD",value=processed_date
        )
        
        col1, col2 = st.columns(2)
        time_committed_str = casedata.get("time_committed")
        time_committed_str = process_time(time_committed_str)
        if st.session_state.input_time_committed:
            time_committed_str = st.session_state.input_time_committed.strftime("%I:%M %p")
        col1.text_input("Time Committed", value=time_committed_str, disabled=True)
        col2.write("\n")
        col2.write("\n")
        if col2.button("Enter Time", use_container_width=True, key="timecommitted"):
            input_time_committed()

    st.write("---")

    # Create a directory of data
    data = {
        "pro": pro,
        "ppo_cpo": ppo_cpo,
        "mps_cps": mps_cps,
        "det_narrative": det_narrative,
        "dt_reported": dt_reported,
        "time_reported": st.session_state.input_time_reported,
        "dt_committed": dt_committed,
        "time_committed": st.session_state.input_time_committed
    }

    # Mapping of field names to user-friendly names
    field_name_mapping = {
        "det_narrative": "Case Narrative",
        "dt_reported": "Date Reported",
        "time_reported": "Time Reported",
        "dt_committed": "Date Committed",
        "time_committed": "Time Committed"
    }

    case_detail = ""

    # Validate the data using Pydantic
    try:
        case_detail = Case_Detail_Validation(**data)
        # Data is valid, proceed with database operations
        return case_detail
    except ValidationError as e:
        st.error(e)
    # finally:
    #     st.write(case_detail)

    return case_detail