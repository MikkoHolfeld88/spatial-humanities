import streamlit as st
from enum import Enum

class SessionStateKey(Enum):
    MAP_DATA = 'map_data'
    GEMEINDEN = 'gemeinden'
    KRANKENHAUSER = 'krankenhauser'
    SCENARIOS = 'scenarios'

class Store():
    def __init__(self):
        if 'initialized' not in st.session_state:
            self.initialize()
            st.session_state['initialized'] = True

    def initialize(self):
        st.session_state = {
            SessionStateKey.MAP_DATA.value: {
                 SessionStateKey.GEMEINDEN.value: None,
                 SessionStateKey.KRANKENHAUSER.value: None
            },
            SessionStateKey.SCENARIOS.value: []
        }

    def set_gemeinden(self, data):
        st.session_state[SessionStateKey.MAP_DATA.value][SessionStateKey.GEMEINDEN.value] = data

    def get_gemeinden(self):
        return st.session_state[SessionStateKey.MAP_DATA.value][SessionStateKey.GEMEINDEN.value]

    def set_krankenhauser(self, data):
        st.session_state[SessionStateKey.MAP_DATA.value][SessionStateKey.KRANKENHAUSER.value] = data

    def get_krankenhauser(self):
        return st.session_state[SessionStateKey.MAP_DATA.value][SessionStateKey.KRANKENHAUSER.value]

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