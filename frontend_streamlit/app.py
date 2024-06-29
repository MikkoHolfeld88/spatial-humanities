import streamlit as st
from streamlit_keplergl import keplergl_static

from backend.models.scenario import Scenario
from backend.services.map_service import MapService
from backend.services.converter_service import ConverterService
from backend.services.calculation_service import CalculationService
from store import store as Store, SessionStateKey

############# SERVICES #############
map_service = MapService()
converter_service = ConverterService()
calculation_service = CalculationService()

############# DATA #############
available_region_names = converter_service.get_region_names()


state = Store.get_state()

############## LAYOUT ##############
st.set_page_config(layout="wide")


############## DIALOGS ##############
def edit_scenario(index):
    scenario = Store.get_scenario(index)

    if not scenario:
        st.error("Scenario not found")
        return

    st.title("General")
    new_name = st.text_input("Name", value=scenario.name, key=f"scenario_name_{index}")
    new_desc = st.text_area("Description", value=scenario.desc, key=f"scenario_desc_{index}")

    st.title("Regions")
    col1, col2 = st.columns(2)
    with col1:
        selected_regions = st.multiselect("Select Regions", available_region_names, [region for region in scenario.regions], key=f"scenario_regions_{index}")
    with col2:
        population = converter_service.get_population_by_regions(selected_regions)
        st.write("Population")
        st.data_editor(population)

        total_population = population.loc[population['type'] == '🟰 Total', 'value'].iloc[0]

    st.write("Patient Demand")
    fraction = st.number_input("Insert patient (fraction of population)", key=f"patient_demand_{index}", min_value=0.0, max_value=1.0, step=0.01, value=scenario.fraction)
    patient_demand = fraction * total_population
    st.markdown(f"<b style='color:blue;'>Patient Demand: {patient_demand:.0f}</b>", unsafe_allow_html=True)

    if st.button("Save", key=f"save_{index}"):
        new_scenario = Scenario(
            name=new_name,
            desc=new_desc,
            fraction=fraction,
            patient_demand=patient_demand,
            regions=selected_regions,
            calculation=None,
            hospitals=[])

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
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎬 Start", key=f"activate_scenario_{i + 1}"):
                    # visualize regions
                    map_service.add_data_to_map(converter_service.get_region_coordinates_by_name(scenario.regions))
                    pass
            with col2:
                if st.button("📝 Edit", key=f"edit_scenario_{i + 1}"):
                    open_edit_dialog(i)
            with col3:
                st.button("🗑 Delete", on_click=Store.delete_scenario, args=(i,), key=f"delete_scenario_{i + 1}")

map_1 = map_service.get_map()
keplergl_static(map_1)
