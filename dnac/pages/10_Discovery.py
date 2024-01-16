import streamlit as st
import pandas as pd
from dnacentersdk import api
from datetime import datetime
import ipaddress

st.title("Discovery")
if "dnac" not in st.session_state:
    st.error("Not logged in")
    st.stop()

dnac = st.session_state["dnac"]

st.subheader("Creadentials")
cli_list = dnac.discovery.get_global_credentials(credential_sub_type="CLI")
cli_option = [cred.username for cred in cli_list.response]
cli_selection = st.selectbox(label="CLI", options=cli_option)
cli_id = [cred.id for cred in cli_list.response if cred.username == cli_selection][0]

snmp_list = dnac.discovery.get_global_credentials(credential_sub_type="SNMPV2_READ_COMMUNITY")
snmp_option = [cred.description for cred in snmp_list.response]
snmp_selection = st.selectbox(label="SNMP", options=snmp_option)
snmp_id = [cred.id for cred in snmp_list.response if cred.description == snmp_selection][0]

netconf_list = dnac.discovery.get_global_credentials(credential_sub_type="NETCONF")
netconf_option = [cred.netconfPort for cred in netconf_list.response]
netconf_selection = st.selectbox(label="NETCONF", options=netconf_option)
netconf_id = [cred.id for cred in netconf_list.response if cred.netconfPort == netconf_selection][0]

global_creds_id = [cli_id, snmp_id, netconf_id]
st.write('CLI: ', cli_selection, "(", cli_id , ")")
st.write('SNMP: ', snmp_selection, "(", snmp_id , ")")
st.write('NETCONF: ', netconf_selection, "(", netconf_id , ")")

st.subheader("New discovery")
with st.form("Discovery form"):
    disc_area = st.text_area("One element on each line", "10.0.0.0-10.0.0.255\n10.1.1.1\n10.2.2.0/24")
    submitted = st.form_submit_button("submit")

    if submitted:
        st.table(disc_area.splitlines())
        st.write("Starting Job Creation...")
        
        now = datetime.now() # current date and time

        for job in disc_area.splitlines():
            try:
                date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
                if not "-" in job: # If the job is not an range already
                    net = ipaddress.ip_network(job, strict=False) # Use ipaddress library to find first and last IP and create range string.
                    first, last = net[0], net[-1]
                    range = f"{first}-{last}"
                else:
                    range = job
                dnac.discovery.start_discovery(name=f"job_{date_time}_{job}", discoveryType="Range", preferredMgmtIPMethod="UseLoopBack", ipAddressList=range, protocolOrder="ssh,telnet", globalCredentialIdList=global_creds_id)
                st.success(f"job_{date_time}_{job} created:{range}")
            except Exception as err:
                st.error(err)

st.subheader("Discovery jobs")
col1, col2, col3 = st.columns(3)
col1.write("All current discoveries:")
col2.button("Reload")

discs = dnac.discovery.get_discoveries_by_range(100, 1)
df = pd.json_normalize(discs.response)

column_config = {
    "name": "Name",
    "discoveryType": "Type",
    "ipAddressList": "Address",
    "deviceIds": None,
    "passwordList": None,
    "ipFilterList": None,
    "enablePasswordList": None,
    "snmpRoCommunity": None,
    "protocolOrder": None,
    "discoveryCondition": "discoveryCondition",
    "discoveryStatus": "discoveryStatus",
    "timeOut": None,
    "numDevices": "numDevices",
    "retryCount": None,
    "isAutoCdp": None,
    "globalCredentialIdList": None,
    "preferredMgmtIPMethod": None,
    "onlyNewDevice": None,
    "siteId": None,
    "id": None
}
st.dataframe(df, column_config = column_config)
with st.expander("See full data table"):
    st.dataframe(df)