import streamlit as st
from modules.ui_models import input_time_committed, input_time_reported
import datetime




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