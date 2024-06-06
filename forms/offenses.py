import streamlit as st
import requests
from modules.dataValidation import Offense_Validation
from pydantic import ValidationError
from config.database import api_endpoint



# Cache data for 30 minutes
@st.cache_data(ttl=1800)
def get_offense_classifications():
    # Make a GET request to the FastAPI endpoint
    response = requests.get(f"{api_endpoint}/offense_classifications")
    response.raise_for_status()  # Ensure we handle HTTP errors

    # Parse the JSON response
    data = response.json()

    return data

data = get_offense_classifications()

def addOffense():
    # Initialize Offense Values
    offense_classifications = get_offense_classifications()
    offense_values = []
    classifications = []
    for item in offense_classifications:
        if 'incidents' in item:
            offense_values.append(item['incidents'])
        if 'classification' in item:
            classifications.append(item['classification'])

    offenseType_placeholder = st.empty()
    offenseType = offenseType_placeholder.selectbox("Select Offense :red[#]", offense_values, index=None)
    warning = st.empty()
    if offenseType is None:
        warning.warning("Please select an Offense")

    # Initialize classification
    classification = None

    # Get the Incident Classification from cached data
    offense_classification_placeholder = st.empty()
    if offenseType is None:
        offense_classification = offense_classification_placeholder.text_input("Offense Classification",value=None, disabled=True)
    else:
        classification = classifications[offense_values.index(offenseType)]
        offense_classification = offense_classification_placeholder.text_input("Offense Classification", classification, disabled=True)

    # Check if the Offense is not in the option
    check = st.checkbox("Tick the checkbox for Other Cases not found in Select Offense Dropdown above")

    if not check:
        offense = offenseType
        offense_class = offense_classification
        otherOffense = None
    else:
        offenseType_placeholder.selectbox("Select Offense :red[#]", offense_values, index=None, disabled=True ,key="test")
        warning.empty()
        offense_classification = offense_classification_placeholder.text_input("Offense Classification", disabled=True ,value=None, key="test2")
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

    if offense is None:
        offense = otherOffense

    # Create a directory of data
    data = {
        "offense": offense,
        "offense_class": offense_class,
        "case_status": case_status,
        "check": check
    }


    # Mapping of field names to user-friendly names
    field_name_mapping = {
        "offense": "Type of Offense based on the Dropdown",
        "offense_class": "Offense Classification",
        "otherOffense": "If Offense is not in the Dropdown, Type Offense Here",
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