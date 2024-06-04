from config.database import api_endpoint
import requests
import pandas as pd
import streamlit as st
import json

def encoded_data():
    # Make a GET request to the API endpoint
    response = requests.get(f"{api_endpoint}/cases")

    # Parse the JSON response using the json.loads method
    data = json.loads(response.text)

    # Print the data variable to see what it contains
    print(data)

    # Convert the JSON data to a DataFrame
    df = pd.DataFrame(data)

    # Set the index to the entry_number column
    df = df.set_index("entry_number")

    # Display the DataFrame in a Streamlit table
    st.table(df)