import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/website/bart-stations.json"
    data = pd.read_json(url)
    return data
