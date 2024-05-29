import streamlit as st
from modules.ui_models import input_time_committed, input_time_reported
import datetime
from modules.dataValidation import Case_Detail_Validation
from pydantic import ValidationError




def case_Details():
    det_narrative = st.text_area("Narrative")

    st.write("---")

    time_reported_str = None
    time_committed_str = None
    DTreported, DTcommitted = st.columns(2)
    if "input_time_reported" not in st.session_state:
        with DTreported:
            st.subheader("Date & Time Reported")
            dt_reported = st.date_input("Date Reported :red[#]",help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month", format="YYYY/MM/DD")
            if dt_reported == datetime.date.today():
                st.warning("Please change the Date Reported")
            col1 , col2 = st.columns(2)
            col1.text_input("Time Reported", disabled=True)
            col2.write("\n")
            col2.write("\n")
            if col2.button("Enter Time",use_container_width=True, key="timereported"):
                input_time_reported()
    else:
        with DTreported:
            st.subheader("Date & Time Reported")
            dt_reported = st.date_input("Date Reported :red[#]",help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month", format="YYYY/MM/DD")
            if dt_reported == datetime.date.today():
                st.warning("Please change the Date Reported")
            col1 , col2 = st.columns(2)
            # Format the datetime object to a string representing time in the "%I:%M %p" format
            time_reported_str = st.session_state.input_time_reported["timevalue"].strftime("%I:%M %p")
            col1.text_input("Time Reported",value=time_reported_str,disabled=True)
            col2.write("\n")
            col2.write("\n")
            if col2.button("Enter Time",use_container_width=True, key="timereported1"):
                input_time_reported()


    if "input_time_committed" not in st.session_state:

        with DTcommitted:
            st.subheader("Date & Time Committed")
            dt_committed = st.date_input("Date Committed",help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month",value=None, format="YYYY/MM/DD")
            col1 , col2 = st.columns(2)
            col1.text_input("Time Committed", disabled=True)
            col2.write("\n")
            col2.write("\n")
            if col2.button("Enter Time",use_container_width=True,key="timecommitted"):
                input_time_committed()
    else:
        with DTcommitted:
            st.subheader("Date & Time Committed")
            dt_committed = st.date_input("Date Committed",help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month",value=None, format="YYYY/MM/DD")
            col1 , col2 = st.columns(2)
            # Format the datetime object to a string representing time in the "%I:%M %p" format
            time_committed_str = st.session_state.input_time_committed["timevalue"].strftime("%I:%M %p")
            col1.text_input("Time Committed",value=time_committed_str,disabled=True)
            col2.write("\n")
            col2.write("\n")
            if col2.button("Enter Time",use_container_width=True,key="timecommitted1"):
                input_time_committed()


    st.write("---")

    # Create a directory of data
    data = {
        "det_narrative": det_narrative,
        "dt_reported": dt_reported,
        "time_reported_str": time_reported_str,
        "dt_committed": dt_committed,
        "time_committed_str": time_committed_str
    }

    # Mapping of field names to user-friendly names
    field_name_mapping = {
        "det_narrative": "Case Narrative",
        "dt_reported": "Date Reported",
        "time_reported_str": "Time Reported",
        "dt_committed": "Date Committed",
        "time_committed_str": "Time Committed"
    }

    case_detail = ""

    # Validate the data using Pydantic
    try:
        case_detail = Case_Detail_Validation(**data)
        # Data is valid, proceed with database operations
        return case_detail
    except ValidationError as e:
        for error in e.errors():
            field = error['loc'][0]
            message = error['msg']
            user_friendly_field = field_name_mapping.get(field, field)
            st.error(f"Error in {user_friendly_field}: {message}")
    finally:
        st.write(case_detail)