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


def addSuspect(mps_cps):
    # Initialize Barangay Values and City Mun Values
    brgy_values, city_mun_value, province_value = get_brgy_city_mun(mps_cps)

    # First, Middle, and Last Name Portion
    fname, mname = st.columns(2)
    sus_fname = fname.text_input("First Name",key="sus_fname")
    sus_midname = mname.text_input("Middle Name",key="sus_mname")
    sus_lname = st.text_input("Last Name",key="sus_lname")

    # Qualifier, Alias and Gender
    qlfr, alias, gndr= st.columns(3)
    sus_qlfr = qlfr.text_input("Qualifier",key="sus_qlfr")
    sus_alias = alias.text_input("Alias",key="sus_alias")
    with gndr:
        sus_gndr = st.radio("Gender",("Male", "Female"),index=None,horizontal=True,key="sus_gndr")

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
    sus_brgy = brgy.selectbox("Barangay",brgy_values,placeholder="Please select a Barangay",key="sus_abrgy",index=None)
    sus_add_street = st.text_input("House No./Street Name",key="sus_strName")


    st.write("---")