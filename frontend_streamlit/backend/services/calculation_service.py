from frontend_streamlit.backend.models.scenario import Scenario

class CalculationService:

    def __init__(self):
        pass

    def calculate(self, scenario: Scenario) -> dict:
        """
            Algorithm to calculate the positions of the arrows on the map

            [{
                "from": {lat: float, lon: float},
                "to": {lat: float, lon: float}
            }, {...}, ...]

        :param scenario:
        :return: list({"from": {lat: float, lon: float},"to": {lat: float, lon: float}}, ... , ... )
        """
        default_radius = 42000

        test_scenario = {
            "regions": [{"name": "Region 1", "patients": 1000, "beds": 500}],
            "calculation": {"id": "test", "radius": default_radius},
            "hospitals": [{
                "id": "test",
                "allgemein_beds": {
                    "available": 0,
                    "used": 0
                }
            }]
        }

        for hospitals in test_scenario.hospitals:
            pass
