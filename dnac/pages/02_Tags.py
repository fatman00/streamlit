import streamlit as st
import pandas as pd
from dnacentersdk import api

st.title("Tags list")
if "dnac" not in st.session_state:
    st.error("Not logged in")
    st.stop()

dnac = st.session_state["dnac"]
if st.button("Get Tags"):
    # Find all devices that have 'Switches and Hubs' in their family
    tags = dnac.tag.get_tag(sort_by='name', order='des')

    # Print all of demo devices
    df = pd.json_normalize(tags.response)
    st.dataframe(df)