from backend.models.hospital import Hospital
from backend.models.region import Region
from backend.models.scenario import Scenario


class CalculationService:
    def calculate(self, scenario: Scenario, regions: list[Region], hospitals: list[Hospital]) -> list:
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

        test_scenario: Scenario = Scenario()

        test_scenario.calculation = {
            "id": "test",
            "radius": default_radius
        }

        test_scenario.regions = [
            {
                    "name": "Region 1",
                    "population": 500000,
                    "patient_demand": {
                        "count": 1000,
                        "specification": None
                    },
                    "latitude": 0,
                    "longitude": 0
                }
        ],

        test_scenario.hospitals = [
            {
                "id": "",
                "allgemein_beds": {
                    "available": 0,
                    "used": 0
                }
            }
        ]

        for hospitals in test_scenario.hospitals:
            pass

    def find_next_hospital(self, radius, coordinates_region):
        pass

    def calc_distance(self, radius, coordinates_region):
        pass
