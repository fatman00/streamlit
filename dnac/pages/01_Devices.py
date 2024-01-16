import streamlit as st
import pandas as pd
from dnacentersdk import api

st.title("Device list")
if "dnac" not in st.session_state:
    st.error("Not logged in")
    st.stop()

dnac = st.session_state["dnac"]
if st.button("Get device list(Switches and Hubs)"):
    # Find all devices that have 'Switches and Hubs' in their family
    devices = dnac.devices.get_device_list(family='Switches and Hubs')

    # Print all of demo devices
    df = pd.json_normalize(devices.response)
    st.dataframe(df)