import streamlit as st
import requests
from modules.dataValidation import Offense_Validation
from pydantic import ValidationError


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
            if not otherOffense:
                st.warning("Please Type the Other Offense")
        else:
            otherOffense = otherOffense_placeholder.text_input("Others, Please Specify :red[#]", help="Press Enter to confirm the Other KP Incident",disabled=True,key="test4")


    st.subheader("Case Status")
    case_status = st.selectbox(
        "Status of the Case :red[#]",
        ("For Conciliation", "Settled", "For Record Purposes", "With Certificate to File Action"),
        index=None
    )
    if case_status is None:
        st.error("Please select Case Status.")


    # st.code(f"OffenseType: {offense}, Offense Classification: {offense_class}, Other Offense: {otherOffense}, Case Status: {case_status}, {check}")
    st.write("---")

        # Create a directory of data
    data = {
        "offense": offense,
        "offense_class": offense_class,
        "otherOffense": otherOffense,
        "case_status": case_status,
        "check": check
    }

    # Mapping of field names to user-friendly names
    field_name_mapping = {
        "offense": "Type of Offense based on the Dropdown",
        "offense_class": "Offense Classification",
        "otherOffense": "If Offense is not it the Dropdown, Type Offense Here",
        "case_status": "Status of the Offense",
        "check": "Check if the check function is enabled"
    }

    offense_detail = ""

    # Validate the data using Pydantic
    try:
        offense_detail = Offense_Validation(**data)
        # Data is valid, proceed with database operations
        return offense_detail
    except ValidationError as e:
        for error in e.errors():
            field = error['loc'][0]
            message = error['msg']
            user_friendly_field = field_name_mapping.get(field, field)
            st.error(f"Error in {user_friendly_field}: {message}")
    finally:
        st.write(offense_detail)

    return offense_detail
