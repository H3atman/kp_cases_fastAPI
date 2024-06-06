from config.database import api_endpoint
import requests
import pandas as pd
import streamlit as st
import json

def encoded_data(mps_cps: str):
    try:
        # Make a GET request to the API endpoint with the mps_cps parameter
        response = requests.get(f"{api_endpoint}/cases", params={"mps_cps": mps_cps})

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the JSON response using the json.loads method
            try:
                data = json.loads(response.text)
            except json.JSONDecodeError:
                st.error("Error decoding JSON from response")
                return

            # Print the data variable to see what it contains
            # print(data)

            # Convert the JSON data to a DataFrame
            df = pd.DataFrame(data)

            # Set the index to the entry_number column if needed
            # df = df.set_index("Entry Number")

            # Display the DataFrame in a Streamlit table
            st.dataframe(df)
        else:
            st.error(f"Error: Received status code {response.status_code}")
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        print(f"Request failed: {e}")

# # Call the function to execute the code
# encoded_data()
