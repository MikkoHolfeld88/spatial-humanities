import streamlit as st

from store import store as Store


@st.experimental_dialog(title="Scenario Editor", width="large")
def edit_scenario(index):
    scenario = Store.get_scenario(index)

    if not scenario:
        st.error("Scenario not found")
        return

    with st.form("scenario_form"):

        with st.container():
            st.header("General"),
            st.text_input("Name", value=scenario['name']),

        regions, calculation, hospitals = st.columns(3)

        with regions:
            st.header("Regions"),
            st.selectbox("Region", options=["Region 1", "Region 2", "Region 3"], index=0),

            with st.container():
                st.subheader("Patients")



        with calculation:
            st.header("Calculation"),

        with hospitals:
            st.header("Hospitals"),

        submitted = st.form_submit_button("Save Scenario")

        if submitted:
            st.success("Scenario saved successfully!")
