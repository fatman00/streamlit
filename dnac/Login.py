import streamlit as st
import json
from dnacentersdk import api
import pandas as pd

st.set_page_config(
    page_title="My DNAC tools page",
    page_icon="⭐",
)
st.title("Login page")
st.sidebar.success("Select a page above")

if "dnac" not in st.session_state:

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')


if st.button("Login"):
    try:
        dnac = api.DNACenterAPI(username=username,
                            password=password,
                            base_url="https://dnac.dccat.dk:443",
                            version='2.3.5.3',
                            verify=False)
        st.success("Token: "+dnac.access_token)
        st.session_state["dnac"] = dnac
    except:
        st.error("Authentication Error")
        st.stop()