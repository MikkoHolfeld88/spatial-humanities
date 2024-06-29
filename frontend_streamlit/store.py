from enum import Enum
from functools import wraps
import json

from backend.models.scenario import Scenario

from json import JSONEncoder

class CustomEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, Scenario):
                return {
                    "name": obj.name,
                    "desc": obj.desc,
                    "regions": [self.default(region) for region in obj.regions],
                    "calculation": self.default(obj.calculation) if obj.calculation else None,
                    "hospitals": [self.default(hospital) for hospital in obj.hospitals]
                }
            elif hasattr(obj, '__dict__'):
                return {k: self.default(v) for k, v in obj.__dict__.items()}
            return super().default(obj)
        except TypeError as e:
            print(f"Failed to serialize {type(obj)} with value {obj}: {e}")
            raise

def log_state_change(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            state_before = json.dumps(self.state, indent=4, cls=CustomEncoder)
        except TypeError as e:
            print(f"Serialization error before method {method.__name__}: {e}")
            state_before = "Serialization error"
        result = method(self, *args, **kwargs)
        try:
            state_after = json.dumps(self.state, indent=4, cls=CustomEncoder)
        except TypeError as e:
            print(f"Serialization error after method {method.__name__}: {e}")
            state_after = "Serialization error"
        print(f"========= Before =========\n {method.__name__}: {state_before}")
        print(f"^^^^^^^^^^^ After ^^^^^^^^^^^^\n{method.__name__}: {state_after}")
        return result
    return wrapper

class SessionStateKey(Enum):
    MAP_DATA = 'map_data'
    REGIONS = 'regions'
    HOSPITALS = 'hospitals'
    SCENARIOS = 'scenarios'


class Store:
    def __init__(self):
        self.state = {}

        if self.state == {}:
            self.initialize_state()

    def initialize_state(self):
        self.state = {
            SessionStateKey.MAP_DATA.value: {
                SessionStateKey.REGIONS.value: None,
                SessionStateKey.HOSPITALS.value: None
            },
            SessionStateKey.SCENARIOS.value: []
        }

    @log_state_change
    def set_gemeinden(self, data):
        self.state[SessionStateKey.MAP_DATA.value][SessionStateKey.REGIONS.value] = data

    @log_state_change
    def set_krankenhauser(self, data):
        self.state[SessionStateKey.MAP_DATA.value][SessionStateKey.HOSPITALS.value] = data

    @log_state_change
    def add_scenario(self):
        scenarios = self.get_scenarios()
        scenario: Scenario = Scenario(
            name=f"Scenario {len(scenarios) + 1}",
            desc="",
            patient_demand=0,
            fraction=0.0,
            regions=[],
            calculation=None,
            hospitals=[])
        scenarios.append(scenario)
        self.state[SessionStateKey.SCENARIOS.value] = scenarios

    @log_state_change
    def delete_scenario(self, index):
        scenarios = self.get_scenarios()
        if 0 <= index < len(scenarios):
            del scenarios[index]
            self.state[SessionStateKey.SCENARIOS.value] = scenarios

    @log_state_change
    def update_scenario(self, index, scenario):
        scenarios = self.get_scenarios()
        if 0 <= index < len(scenarios):
            scenarios[index] = scenario
            self.state[SessionStateKey.SCENARIOS.value] = scenarios

    @log_state_change
    def update_scenario_name(self, index, name):
        scenarios = self.get_scenarios()
        if 0 <= index < len(scenarios):
            scenario = scenarios[index]
            scenario.name = name
            self.update_scenario(index, scenario)

    @log_state_change
    def update_scenario_desc(self, index, desc):
        scenarios = self.get_scenarios()
        if 0 <= index < len(scenarios):
            scenario = scenarios[index]
            scenario.desc = desc
            self.update_scenario(index, scenario)

    def get_state(self):
        return self.state

    def get_gemeinden(self):
        return self.state[SessionStateKey.MAP_DATA.value][SessionStateKey.REGIONS.value]

    def get_scenario(self, index):
        scenarios = self.get_scenarios()
        if 0 <= index < len(scenarios):
            return scenarios[index]
        return None

    def get_krankenhauser(self):
        return self.state[SessionStateKey.MAP_DATA.value][SessionStateKey.HOSPITALS.value]

    def get_scenarios(self):
        return self.state.get(SessionStateKey.SCENARIOS.value, [])

store = Store()
