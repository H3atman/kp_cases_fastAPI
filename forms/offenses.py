import streamlit as st
import requests


# Cache data for 30 minutes
@st.cache_data(ttl=1800)
def get_offense():
    # Make a GET request to the FastAPI endpoint
    response = requests.get("http://localhost:8000/offense_values")
    response.raise_for_status()  # Ensure we handle HTTP errors

    # Parse the JSON response
    data = response.json()

    # Extract the offense values
    offense_values = [item['incidents'] for item in data]

    return offense_values

# Cache each classification separately for 30 minutes
@st.cache_data(ttl=1800, show_spinner=False)
def get_offense_classification(offense):
    # Make a GET request to the FastAPI endpoint
    response = requests.get(f"http://localhost:8000/offense_classification/{offense}")
    response.raise_for_status()  # Ensure we handle HTTP errors

    # Parse the JSON response
    data = response.json()

    # Extract the classification
    classification = data['classification']

    return classification

def addOffense():
    # Initialize Offense Values
    generate_offense = get_offense()



    offenseType_placeholder = st.empty()
    offenseType = offenseType_placeholder.selectbox("Select Offense :red[#]", generate_offense, index=None)
    warning = st.empty()
    if offenseType is None:
        warning.warning("Please select an Offense")

    # Initialize classification
    # classification = None

    # Get the Incident Classification from cached data
    offense_classification_placeholder = st.empty()
    if offenseType is None:
        offense_classification = offense_classification_placeholder.text_input("Offense Classification",value=None, disabled=True)
    else:
        classification = get_offense_classification(offenseType)
        offense_classification = offense_classification_placeholder.text_input("Offense Classification", classification, disabled=True)


    # Check if the Offense is not in the option
    check = st.checkbox("Tick the checkbox for Other Cases not found in Select Offense Dropdown above")

    if not check:
        offense = offenseType
        offense_class = offense_classification
        otherOffense = None
    else:
        offenseType_placeholder.selectbox("Select Offense :red[#]", generate_offense, index=None,disabled=True, key="test")
        warning.empty()
        offense_classification_placeholder.text_input("Offense Classification",value=None, disabled=True, key="test2")
        offense = None
        offense_class = "Other Crimes"
    
    otherOffense_placeholder = st.empty()
    otherOffense = otherOffense_placeholder.text_input("Others, Please Specify :red[#]", value=None, help="Press Enter to confirm the Other KP Incident",disabled=True)
    if check:
        if otherOffense is None:
            otherOffense= otherOffense_placeholder.text_input("Others, Please Specify :red[#]", help="Press Enter to confirm the Other KP Incident",key="test3")
        else:
            otherOffense = otherOffense_placeholder.text_input("Others, Please Specify :red[#]", help="Press Enter to confirm the Other KP Incident",disabled=True,key="test4")
            st.warning("Please Type the Other Offense")


    st.subheader("Case Status")
    case_status = st.selectbox(
        "Status of the Case :red[#]",
        ("For Conciliation", "Settled", "For Record Purposes", "With Certificate to File Action"),
        index=None
    )
    if case_status is None:
        st.error("Please select Case Status.")

    st.write("---")
    st.code(f"OffenseType: {offense}, Offense Classification: {offense_class}, Other Offense: {otherOffense}, Case Status: {case_status}, {check}")
