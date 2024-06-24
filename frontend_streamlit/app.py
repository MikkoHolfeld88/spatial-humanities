import streamlit as st
from streamlit_keplergl import keplergl_static
from backend.services.map_service import MapService
from backend.services.converter_service import ConverterService
from backend.services.calculation_service import CaclulationService
from store import store as Store
from scenario_editor import edit_scenario
import json

map_service = MapService()
converter_service = ConverterService()

st.set_page_config(layout="wide")
st.sidebar.image('logo.png', use_column_width=True)


def add_scenario():
    Store.add_scenario({'name': 'Neues Szenario'})

def delete_scenario(index):
    Store.delete_scenario(index)

def open_modal(index):
    edit_scenario(index)

def activate_scenario(index):
    result = CaclulationService.calculate(Store.get_scenario(index))
    map_service.add_data_to_map(result, name=f"patient_flow_{index}")

st.sidebar.button("Szenario hinzufügen", on_click=add_scenario)


for idx, scenario in enumerate(Store.get_scenarios()):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.sidebar.button(scenario['name'], key=f"btn{idx}", on_click=open_modal, args=(idx,))
    with col2:
        st.sidebar.button("🗑️", key=f"del{idx}", on_click=delete_scenario, args=(idx,))

regions_le = converter_service.get_regions()
hospitals_le = converter_service.get_hospitals()

on_stadtteile_leipzig = st.sidebar.toggle("Stadtteile Leipzig", False)
on_krankenhauser_leipzig = st.sidebar.toggle("Krankenhäuser Leipzig", False)

if on_stadtteile_leipzig:
    map_service.add_data_to_map(json.loads(regions_le), name="regions_le")

if on_krankenhauser_leipzig:
    map_service.add_data_to_map(json.loads(hospitals_le), name="hospitals_le")

map_1 = map_service.get_map()
keplergl_static(map_1)
