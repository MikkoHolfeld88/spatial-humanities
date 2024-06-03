import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl

st.set_page_config(layout="wide")

map_1 = KeplerGl(height=800)

config = {
    'version': 'v1',
    'config': {
        'mapState': {
            'latitude': 51.340199,
            'longitude': 12.360103,
            'zoom': 11
        }
    }
}

map_1.config = config

keplergl_static(map_1)