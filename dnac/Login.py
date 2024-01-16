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
    url = st.text_input("Server IP/name")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')


btn_login = st.button("Login")

if btn_login:
    try:
        dnac = api.DNACenterAPI(username=username,
                            password=password,
                            base_url=f"https://{url}:443",
                            version='2.3.5.3',
                            verify=False)
        st.success("Token: "+dnac.access_token)
        st.session_state["dnac"] = dnac
    except:
        st.error("Authentication Error")
        st.stop()

if st.button("Logout"):
    del st.session_state["dnac"]