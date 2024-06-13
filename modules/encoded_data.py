import requests
import json
import pandas as pd
import streamlit as st
from config.database import api_endpoint

def encoded_data_mps(mps_cps: str):
    if not mps_cps or not api_endpoint:
        st.error("Both MPS/CPS value and API endpoint must be provided")
        return
    
    try:
        with st.spinner("Fetching case count..."):
            response = requests.get(f"{api_endpoint}/count_cases_encoded", params={"mps_cps": mps_cps})

            if response.status_code == 200:
                try:
                    offense_count = response.json()["count"]
                except KeyError:
                    st.error("Invalid response format")
                    return
            else:
                st.error(f"Failed to fetch case count: Received status code {response.status_code}")
                return

        st.subheader(f"Total Number of Cases Encoded: :red[{offense_count}]")

        with st.spinner("Fetching case data..."):
            response = requests.get(f"{api_endpoint}/cases", params={"mps_cps": mps_cps})

            if response.status_code == 200:
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    st.error("Error decoding JSON from response")
                    return

                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.error(f"Failed to fetch case data: Received status code {response.status_code}")
                print(f"Error: Received status code {response.status_code}")
                print(response.text)
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        print(f"Request failed: {e}")

def encoded_data_ppo(ppo_cpo: str):
    if not ppo_cpo or not api_endpoint:
        st.error("Both MPS/CPS value and API endpoint must be provided")
        return
    
    try:
        with st.spinner("Fetching case count..."):
            response = requests.get(f"{api_endpoint}/count_cases_encoded-ppo", params={"ppo_cpo": ppo_cpo})

            if response.status_code == 200:
                try:
                    offense_count = response.json()["count"]
                except KeyError:
                    st.error("Invalid response format")
                    return
            else:
                st.error(f"Failed to fetch case count: Received status code {response.status_code}")
                return

        st.subheader(f"Total Number of Cases Encoded: :red[{offense_count}]")

        with st.spinner("Fetching case data..."):
            response = requests.get(f"{api_endpoint}/cases-ppo", params={"ppo_cpo": ppo_cpo})

            if response.status_code == 200:
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    st.error("Error decoding JSON from response")
                    return

                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.error(f"Failed to fetch case data: Received status code {response.status_code}")
                print(f"Error: Received status code {response.status_code}")
                print(response.text)
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        print(f"Request failed: {e}")


def encoded_data_pro(mps_cps: str):
    if not mps_cps or not api_endpoint:
        st.error("Both MPS/CPS value and API endpoint must be provided")
        return
    
    try:
        with st.spinner("Fetching case count..."):
            response = requests.get(f"{api_endpoint}/count_cases_encoded", params={"mps_cps": mps_cps})

            if response.status_code == 200:
                try:
                    offense_count = response.json()["count"]
                except KeyError:
                    st.error("Invalid response format")
                    return
            else:
                st.error(f"Failed to fetch case count: Received status code {response.status_code}")
                return

        st.subheader(f"Total Number of Cases Encoded: :red[{offense_count}]")

        with st.spinner("Fetching case data..."):
            response = requests.get(f"{api_endpoint}/cases", params={"mps_cps": mps_cps})

            if response.status_code == 200:
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    st.error("Error decoding JSON from response")
                    return

                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.error(f"Failed to fetch case data: Received status code {response.status_code}")
                print(f"Error: Received status code {response.status_code}")
                print(response.text)
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        print(f"Request failed: {e}")
# # Call the function to execute the code
# encoded_data()
