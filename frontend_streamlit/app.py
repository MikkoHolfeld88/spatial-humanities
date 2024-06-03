import streamlit as st
from streamlit_keplergl import keplergl_static
from backend.services.map_service import map_service
from backend.services.converter_service import ConverterService
import json

converter_service = ConverterService(user_agent="converter_service")

st.set_page_config(layout="wide")

if 'stadtteile_leipzig' not in st.session_state:
    st.session_state.stadtteile_leipzig = None

if 'krankenhauser_leipzig' not in st.session_state:
    st.session_state.krankenhauser_leipzig = None

st.sidebar.image('logo.png', use_column_width=True)

if st.sidebar.button("+ Stadtteile Leipzig"):
    regions = converter_service.get_regions()
    if regions:
        st.session_state['stadtteile_leipzig'] = regions
        map_service.add_data_to_map(json.loads(regions), name="Stadtteile Leipzig")
    else:
        st.error("Fehler beim Laden der Daten.")

if st.sidebar.button("+ Krankenhäuser Leipzig"):
    hospitals = converter_service.get_hospitals()
    if hospitals:
        st.session_state['krankenhauser_leipzig'] = hospitals
        map_service.add_data_to_map(json.loads(hospitals), name="Krankehäuser Leipzig")
    else:
        st.error("Fehler beim Laden der Daten.")

map_1 = map_service.get_map()
keplergl_static(map_1)
