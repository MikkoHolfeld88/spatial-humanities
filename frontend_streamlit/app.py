import streamlit as st
from streamlit_keplergl import keplergl_static
import pandas as pd

from backend.models.calculation import Calculation
from backend.models.hospital_beds import HospitalBeds
from backend.models.scenario import Scenario
from backend.services.map_service import MapService
from backend.services.converter_service import ConverterService
from backend.services.calculation_service import CalculationService
from store import store as Store

############# SERVICES #############
map_service = MapService()
converter_service = ConverterService()
calculation_service = CalculationService()

############# DATA #############
available_region_names = converter_service.get_region_names()
hospital_names = converter_service.get_hospital_names()

state = Store.get_state()

############## LAYOUT ##############
st.set_page_config(layout="wide")


############## DIALOGS ##############
def edit_scenario(index):
    scenario = Store.get_scenario(index)

    if not scenario:
        st.error("Scenario not found")
        return

    st.title("🦾General")
    new_name = st.text_input("Name", value=scenario.name, key=f"scenario_name_{index}")
    new_desc = st.text_area("Description", value=scenario.desc, key=f"scenario_desc_{index}")

    st.title("🌍Regions")
    col1, col2 = st.columns(2)
    with col1:
        select_all = st.checkbox("Select All Regions", key=f"select_all_{index}",
                                 value=scenario.regions == available_region_names)

        if select_all:
            selected_regions = st.multiselect("Select Regions", available_region_names, available_region_names,
                                              key=f"scenario_regions_{index}")
        else:
            selected_regions = st.multiselect("Select Regions", available_region_names,
                                              [region for region in scenario.regions], key=f"scenario_regions_{index}")
    with col2:
        population = converter_service.get_population_by_regions(selected_regions)
        st.write("Population")
        st.data_editor(population)

        total_population = population.loc[population['type'] == '🟰 Total', 'value'].iloc[0]

    st.write("Patient Demand ❤️‍🩹")
    fraction = st.number_input("Insert patient (fraction of population)", key=f"patient_demand_{index}", min_value=0.0,
                               max_value=1.0, step=0.01, value=scenario.fraction)
    patient_demand = fraction * total_population
    st.markdown(f"<b style='color:blue;'>Patient Demand: {patient_demand:.0f}</b>", unsafe_allow_html=True)

    st.title("Calculation Configuration")
    value = st.slider("Algortihm radius", 1, 200, scenario.calculation.radius if scenario.calculation else 5, 1, key=f"radius_{index}")
    st.write("Radius:", value)

    calclulation = Calculation(radius=value)

    st.title("🏥 Hospitals")
    selected_hospitals = st.multiselect("Select Hospitals", hospital_names, [hospital for hospital in scenario.hospitals], key=f"scenario_hospitals_{index}")

    hospital_beds: list[HospitalBeds] | None = [
        HospitalBeds(
            name=hospital_name,
            available=converter_service.get_available_beds_by_hospital_name(hospital_name),
            used=0) for hospital_name in selected_hospitals
    ]


    new_hospital_beds = hospital_beds
    for idx, hospital in enumerate(hospital_beds):
        with st.container(border=True):
            col1_, col2_, col3_ = st.columns(3)
            st.write(f"🏥 {hospital.name}")
            st.write(f"Available Beds: {hospital.available}")
            new_hospital_beds[idx].used = st.number_input(
                "Used Beds",
                key=f"used_beds_{index}_{idx}",
                min_value=0,
                max_value=hospital.available if hospital else 0,
                value=scenario.hospital_beds[idx].used if scenario.hospital_beds else 0)

    if st.button("Save", key=f"save_{index}"):
        new_scenario = Scenario(
            name=new_name,
            desc=new_desc,
            fraction=fraction,
            patient_demand=patient_demand,
            regions=selected_regions,
            calculation=calclulation,
            hospitals=selected_hospitals,
            hospital_beds=new_hospital_beds)

        Store.update_scenario(index, new_scenario)
        st.rerun()


@st.experimental_dialog(title="Scenario Editor", width="large")
def open_edit_dialog(index):
    edit_scenario(index)


#################### SIDEBAR ####################
st.sidebar.image('logo.png', use_column_width=True)
st.sidebar.button("➕ Add Scenario", on_click=Store.add_scenario)

# Initialisierung und Seitenlayout wie zuvor definiert
with st.sidebar:
    for i, scenario in enumerate(Store.get_scenarios()):
        expander_label = f"🪧 {scenario.name}"

        with st.expander(label=expander_label, expanded=False):
            st.write(f"❤️‍🩹Patient Demand:", int(scenario.patient_demand) or 0)
            st.write(f"🌐Radius: ", scenario.calculation.radius if scenario.calculation else 0)
            st.write(f"🛌Used beds: ", sum([beds.used for beds in scenario.hospital_beds]) if scenario.hospital_beds else 0)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎬 Start", key=f"activate_scenario_{i + 1}"):
                    # visualize regions
                    map_service.add_data_to_map(converter_service.get_region_coordinates_by_name(scenario.regions),"Regions")
                    pass
            with col2:
                if st.button("📝 Edit", key=f"edit_scenario_{i + 1}"):
                    open_edit_dialog(i)
            with col3:
                st.button("🗑 Delete", on_click=Store.delete_scenario, args=(i,), key=f"delete_scenario_{i + 1}")

map_1 = map_service.get_map()
keplergl_static(map_1)
