# DNAC Tools

### Versions
* Python: 3.9.2
* DNAC: 2.3.5.5-70026
### Description
This script will run a streamlit website where you can login to DNAC, and insert a list of IP ranges in a textbox.
This list will be created as individual discovery jobs as DNAC only support ranges of max 4096 IPs in one job.

* Start the webpage using streamlit
* Access the page using a browser on port 8501
* Login to the DNAC
* Go to discovery and fill the text area
### 
```
streamlit run Login.py
```