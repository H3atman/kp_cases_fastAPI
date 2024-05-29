import streamlit as st
from datetime import date
import requests

# Fomat the dates
def dateseq():
    # Get the current date
    current_date = date.today()

    # Format the date to 'YYYYMM'
    formatted_date = current_date.strftime('%Y%m')

    return formatted_date

# Function to fetch seq by mps_cps
st.cache_data(ttl="60m")
def fetch_seq_by_mps_cps(mps_cps):
    try:
        response = requests.get(f"http://127.0.0.1:8000/stations/{mps_cps}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Function to get the next entry number (placeholder)
def get_next_entry_number():
    # Placeholder implementation for demonstration purposes
    return 1



def newEntry(mps_cps):

    st.warning("""
        
           You can hover to question mark icons "❔" to learn more.
           
           """)
    
    # Get the Blotter Sequence

    # Fetch the station sequence from the backend
    station_sequences = fetch_seq_by_mps_cps(mps_cps)


    if not station_sequences:
        st.error(f"No data found for mps_cps: {mps_cps}")
        return

    # Assuming we take the first result
    seq = station_sequences[0]['seq'] if station_sequences else ''

    # Get the Blotter Sequence
    entrySeq, dateMon, monthRep, entryNum = st.columns(4)

    entrySeq_value = entrySeq.text_input("Station Code", seq, disabled=True,key="entrySeq")
    dateMon_value = dateMon.text_input("Year|Month Encoded", dateseq(), disabled=True,key="dateMon")
    monthRep_value = monthRep.number_input("Year|Month 'YYYYMM'",
                                           help="Enter the YEAR and MONTH the KP Incident is Reported (e.g 202105, 202212)",
                                           step=1, min_value=202101, max_value=202412)

    # Auto-suggest for the next entry number
    next_value = get_next_entry_number()
    entryNum_value = entryNum.number_input("Entry Number", step=1, min_value=1, value=next_value)

    combined_value = f"{entrySeq_value}-{dateMon_value}-{monthRep_value}-{entryNum_value}"

    # Store the combined_value in the session state
    st.session_state.combined_value = combined_value

    if st.button("New Entry", type="primary", use_container_width=True):
        response = requests.post(f"http://127.0.0.1:8000/temp-entries/", json={"combined_value": st.session_state.combined_value})
        if response.status_code == 200:
            st.session_state.temp_entry_id = response.json()["id"]
            print(st.session_state.combined_value)
            st.switch_page("pages/entry_form.py")
        else:
            st.error("Failed to store the entry")

    return combined_value
    