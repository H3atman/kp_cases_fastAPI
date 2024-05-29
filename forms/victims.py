import streamlit as st
import requests

@st.cache_data(ttl=1800)  # Cache data for 30 minutes
def get_brgy_city_mun(mps_cps):
    # Make a GET request to the FastAPI endpoint
    response = requests.get(f"http://localhost:8000/brgy-city-mun/{mps_cps}")

    # Parse the JSON response
    data = response.json()

    # Extract the brgy_values and city_mun_value
    brgy_values = [item['brgy'] for item in data['brgy_values']]
    city_mun_value = data['city_mun_value']['city_mun']
    province_value = data['province_value']['province']


    return brgy_values, city_mun_value, province_value


def addVictim(mps_cps):
    # Initialize Barangay Values and City Mun Values
    brgy_values, city_mun_value, province_value = get_brgy_city_mun(mps_cps)


    # First, Middle, and Last Name Portion
    fname, mname = st.columns(2)
    vic_fname = fname.text_input("First Name :red[#]",key="vic_fname")
    vic_midname = mname.text_input("Middle Name",key="vic_mname")
    vic_lname = st.text_input("Last Name :red[#]",key="vic_lname")

    if not vic_fname:
        fname.warning('Please enter a first name.')
    if not vic_lname:
        st.warning('Please enter a last name.')

    # Qualifier, Alias and Gender
    qlfr, alias, gndr= st.columns(3)
    vic_qlfr = qlfr.text_input("Qualifier",key="vic_qlfr")
    vic_alias = alias.text_input("Alias",key="vic_alias")
    with gndr:
        vic_gndr = st.radio("Gender :red[#]",("Male", "Female"),index=None,horizontal=True,key="vic_gndr")

    if not vic_gndr:
        gndr.warning('Please select a gender.')


    # Age Group
    ageGrp, age = st.columns(2)
    ageGrp.selectbox("Age Group",index=None,placeholder="Select Victims Age Group",options=("Infant (0-12 months)","Toddler (1-3 y/o)","Kid (4-9 y/o)","Preteen (10-12 y/o)","Teenager (13-18 y/o)","Young Adult (19-39 y/o)","Middle age Adult (40-64 y/o)","Old Age Adult (65 y/o-up)"),key="vic_ageGrp")
    vic_age = age.number_input("Estimated or Exact Age",step=1,min_value=0,key="vic_age")

    # Address - Region and Disttict/Province
    st.subheader("Victim's Address")
    region, distprov = st.columns(2)
    region.text_input("Region",value="Region XII",disabled=True,key="vic_region")
    vic_distprov = distprov.selectbox("District/Province",([province_value]),disabled=True,key="vic_distprov")

    # Address - RCity/Municipality, Barangay and House No/Street Name
    citymun, brgy = st.columns(2)
    vic_cityMun = citymun.selectbox("City/Municipality",([city_mun_value]),disabled=True,key="vic_citymun")
    vic_brgy = brgy.selectbox("Barangay :red[#]",brgy_values,placeholder="Please select a Barangay",key="vic_abrgy",index=None)


    # Check if a Barangay was selected
    if vic_brgy == None:
        st.warning("Please select a Barangay.")
    else:
        vic_add_street = st.text_input("House No./Street Name",key="vic_strName")

    st.write("---")