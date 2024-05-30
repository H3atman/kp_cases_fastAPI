import streamlit as st
from datetime import datetime

# Functions to input time reported and committed
@st.experimental_dialog("Input the time", width="medium")
def input_time_reported():
    hr, min, ampm = st.columns(3)
    hour = hr.number_input("Hour", step=1, min_value=1, max_value=12)
    minutes = min.number_input("Minutes", step=1, min_value=0, max_value=59, format="%02d")
    time_class = ampm.selectbox("AM/PM", options=("AM", "PM"))
    timevalue = "{}:{} {}".format(hour, minutes, time_class)
    if st.button("Submit", type="primary"):
        dt = datetime.strptime(timevalue, "%I:%M %p")
        st.session_state.input_time_reported = dt.time()
        st.rerun()




@st.experimental_dialog("Input the time", width="medium")
def input_time_committed():
    hr, min, ampm = st.columns(3)
    hour = hr.number_input("Hour", step=1, min_value=1, max_value=12)
    minutes = min.number_input("Minutes", step=1, min_value=0, max_value=59, format="%02d")
    time_class = ampm.selectbox("AM/PM", options=("AM", "PM"))
    timevalue = "{}:{} {}".format(hour, minutes, time_class)
    if st.button("Submit", type="primary"):
        dt = datetime.strptime(timevalue, "%I:%M %p")
        st.session_state.input_time_committed = dt.time()
        st.rerun()

