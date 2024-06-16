import streamlit as st
from enum import Enum

class SessionStateKey(Enum):
    MAP_DATA = 'map_data'
    STADTTEILE_LEIPZIG = 'stadtteile_leipzig'
    KRANKENHAUSER_LEIPZIG = 'krankenhauser_leipzig'
    SCENARIOS = 'scenarios'

class Store():
    def __init__(self):
        if 'initialized' not in st.session_state:
            self.initialize()
            st.session_state['initialized'] = True

    def initialize(self):
        st.session_state = {
            SessionStateKey.MAP_DATA.value: {
                 SessionStateKey.STADTTEILE_LEIPZIG.value: None,
                 SessionStateKey.KRANKENHAUSER_LEIPZIG.value: None
            },
            SessionStateKey.SCENARIOS.value: []
        }

    def set_stadtteile_leipzig(self, data):
        st.session_state[SessionStateKey.MAP_DATA.value][SessionStateKey.STADTTEILE_LEIPZIG.value] = data

    def get_stadtteile_leipzig(self):
        return st.session_state[SessionStateKey.MAP_DATA.value][SessionStateKey.STADTTEILE_LEIPZIG.value]

    def set_krankenhauser_leipzig(self, data):
        st.session_state[SessionStateKey.MAP_DATA.value][SessionStateKey.KRANKENHAUSER_LEIPZIG.value] = data

    def get_krankenhauser_leipzig(self):
        return st.session_state[SessionStateKey.MAP_DATA.value][SessionStateKey.KRANKENHAUSER_LEIPZIG.value]

    def get_scenarios(self):
        return st.session_state.get(SessionStateKey.SCENARIOS.value, [])

    def get_scenario(self, index):
        scenarios = self.get_scenarios()
        if 0 <= index < len(scenarios):
            return scenarios[index]
        return None

    def add_scenario(self, scenario):
        scenarios = self.get_scenarios()
        scenarios.append(scenario)
        st.session_state[SessionStateKey.SCENARIOS.value] = scenarios

    def delete_scenario(self, index):
        scenarios = self.get_scenarios()
        if 0 <= index < len(scenarios):
            del scenarios[index]
            st.session_state[SessionStateKey.SCENARIOS.value] = scenarios

    def update_scenario(self, index, scenario):
        scenarios = self.get_scenarios()
        if 0 <= index < len(scenarios):
            scenarios[index] = scenario
            st.session_state[SessionStateKey.SCENARIOS.value] = scenarios

store = Store()