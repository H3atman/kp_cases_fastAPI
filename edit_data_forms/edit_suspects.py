import streamlit as st
import requests
from pydantic import ValidationError
from modules.dataValidation import SuspectData_Validation
from config.database import api_endpoint


# Process Unidentified and Unknown Entries
# -First Name, Middle Name, Last Name alias and Qualifier
def process_suspect_names(susfname, susmidname, suslastname, susalias):
    # List of terms to replace with None
    terms_to_replace = ["Unidentified", "Unknown", "alias Unknown"]
    
    # Function to check and replace terms
    def check_and_replace(name):
        if name in terms_to_replace:
            return None
        return name
    
    # Process each name
    susfname = check_and_replace(susfname)
    susmidname = check_and_replace(susmidname)
    suslastname = check_and_replace(suslastname)
    susalias = check_and_replace(susalias)
    
    return susfname, susmidname, suslastname, susalias


@st.cache_data(ttl=1800)  # Cache data for 30 minutes
def get_brgy_city_mun(mps_cps):
    # Make a GET request to the FastAPI endpoint
    response = requests.get(f"{api_endpoint}/brgy-city-mun/{mps_cps}")

    # Parse the JSON response
    data = response.json()

    # Extract the brgy_values and city_mun_value
    brgy_values = [item['brgy'] for item in data['brgy_values']]
    city_mun_value = data['city_mun_value']['city_mun']
    province_value = data['province_value']['province']


    return brgy_values, city_mun_value, province_value

def get_brgy_index(vicbrgydetails, brgy_values):
    if vicbrgydetails in brgy_values:
        return brgy_values.index(vicbrgydetails)
    return None


def get_gender_index(vicgenderdetails, gender_values):
    if vicgenderdetails in ["Unidentified", "Unknown"]:
        return None
    if vicgenderdetails in gender_values:
        return gender_values.index(vicgenderdetails)
    return None



def editSuspect(susdetails):
    # Initialize Barangay Values and City Mun Values
    brgy_values, city_mun_value, province_value = get_brgy_city_mun(susdetails.get("mps_cps"))

    pro = susdetails.get("pro")
    ppo_cpo = susdetails.get("ppo_cpo")
    mps_cps = susdetails.get("mps_cps")

    # First, Middle, and Last Name Portion
    susfname = susdetails.get("sus_fname")
    susmidname = susdetails.get("sus_midname")
    suslastname = susdetails.get("sus_lname")
    susalias = susdetails.get("sus_alias")

    #  Process Victim Names
    susfname, susmidname, suslastname, susalias = process_suspect_names(susfname, susmidname, suslastname, susalias)

    # First, Middle, and Last Name Portion
    fname, mname = st.columns(2)
    sus_fname = fname.text_input("First Name",key="sus_fname",value=susfname)
    sus_midname = mname.text_input("Middle Name",key="sus_mname",value=susmidname)
    sus_lname = st.text_input("Last Name",key="sus_lname",value=suslastname)



    # Qualifier, Alias and Gender
    qlfr, alias, gndr= st.columns(3)
    sus_qlfr = qlfr.text_input("Qualifier",key="sus_qlfr",value=susdetails.get("sus_qlfr"))
    sus_alias = alias.text_input("Alias",key="sus_alias",value=susalias)
    if sus_alias is None:
        sus_alias = None
    else:
        sus_alias = f"alias {sus_alias}"

    with gndr:
        gender_values = ["Male","Female"]
        sus_gender_details = susdetails.get("sus_gndr")
        gender_index = get_gender_index(sus_gender_details, gender_values)
        sus_gndr = st.radio("Gender",gender_values,index=gender_index,horizontal=True,key="sus_gndr")

    # Age Group
    ageGrp, age = st.columns(2)
    ageGrp.selectbox("Age Group",index=None,placeholder="Select Victims Age Group",options=("Infant (0-12 months)","Toddler (1-3 y/o)","Kid (4-9 y/o)","Preteen (10-12 y/o)","Teenager (13-18 y/o)","Young Adult (19-39 y/o)","Middle age Adult (40-64 y/o)","Old Age Adult (65 y/o-up)"),key="sus_ageGrp")
    sus_age = age.number_input("Estimated or Exact Age",step=1,min_value=0,key="sus_age")

    # Address - Region and Disttict/Province
    st.subheader("Suspect's Address")
    region, distprov = st.columns(2)
    region.text_input("Region",value="Region XII",disabled=True,key="sus_region")
    sus_distprov = distprov.selectbox("District/Province",([province_value]),disabled=True,key="sus_distprov")



    # Address - RCity/Municipality, Barangay and House No/Street Name
    citymun, brgy = st.columns(2)
    sus_cityMun = citymun.selectbox("City/Municipality",([city_mun_value]),disabled=True,key="sus_citymun")
    #  Process barangay Selectbox
    sus_brgy_details = susdetails.get("sus_brgy")
    brgy_index = get_brgy_index(sus_brgy_details, brgy_values)
    sus_brgy = brgy.selectbox("Barangay :red[#]",brgy_values,placeholder="Please select a Barangay",key="sus_abrgy",index=brgy_index)

    sus_strName = st.text_input("House No./Street Name",key="sus_strName",value=susdetails.get("vic_strName"))


    st.write("---")

    # Create a dictionary of the data
    data = {
        "pro": pro,
        "ppo_cpo": ppo_cpo,
        "mps_cps": mps_cps,
        "sus_fname": sus_fname,
        "sus_midname": sus_midname,
        "sus_lname": sus_lname,
        "sus_qlfr": sus_qlfr,
        "sus_alias": sus_alias,
        "sus_gndr": sus_gndr,
        "sus_age": sus_age,
        "sus_distprov": sus_distprov,
        "sus_cityMun": sus_cityMun,
        "sus_brgy": sus_brgy,
        "sus_strName": sus_strName
    }

    # Mapping of field names to user-friendly names
    field_name_mapping = {
        "pro": "PRO",
        "ppo_cpo": "PPO",
        "mps_cps": "Station",
        "sus_fname": "Suspect's First Name",
        "sus_midname": "Suspect's Middle Name",
        "sus_lname": "Suspect's Last Name",
        "sus_qlfr": "Qualifier",
        "sus_alias": "Alias",
        "sus_gndr": "Gender",
        "sus_age": "Age",
        "sus_distprov": "District/Province",
        "sus_cityMun": "City/Municipality",
        "sus_brgy": "Barangay",
        "sus_strName": "House No./Street Name"
    }


    # Validate the data using Pydantic
    suspect_data = ""
    # Validate the data using Pydantic
    try:
        suspect_data = SuspectData_Validation(**data)
        # Data is valid, proceed with database operations
        return suspect_data
    except ValidationError as e:
        for error in e.errors():
            field = error['loc'][0]
            message = error['msg']
            user_friendly_field = field_name_mapping.get(field, field)
            st.error(f"Error in {user_friendly_field}: {message}")
    finally:
        if suspect_data:
            return dict(suspect_data)