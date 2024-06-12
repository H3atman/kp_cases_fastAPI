import streamlit as st
import random

st.header("Test.py")

# Initialize session state if it doesn't exist
if "quantity" not in st.session_state:
    st.session_state.quantity = random.randint(1, 10)
    st.session_state.numbers = [random.randint(1, 100) for _ in range(st.session_state.quantity)]

for i in range(st.session_state.quantity):
    number = st.session_state.numbers[i]
    st.write(number)
    if st.button("Test", key=str(number)):
        st.write(f"Hello World! {number}")
        print(f"Hello its me number {number}")
        st.switch_page("pages/edit_form.py")
