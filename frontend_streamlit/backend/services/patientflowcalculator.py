import math
from typing import List, Dict, Any
from backend.models.scenario import Scenario
from backend.services.converter_service import ConverterService

converter_service = ConverterService()


class PatientFlowCalculator:
    """
      Provides functionality to calculate the patient flow from regions to hospitals based on proximity and bed availability.
      """

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """
               Calculates the distance between two points on the Earth specified by latitude/longitude.

               Parameters:
               - lat1 (float): Latitude of the first point.
               - lon1 (float): Longitude of the first point.
               - lat2 (float): Latitude of the second point.
               - lon2 (float): Longitude of the second point.

               Returns:
               - float: Distance between the two points in meters.
               """
        R = 6371  # Radius of the Earth in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(
            dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c * 1000  # Return distance in meters

    def calculate(self, scenario: Scenario) -> List[Dict[str, Any]]:
        """
        Calculates the patient flow from regions to hospitals.

        Parameters:
        - scenario (Scenario): The scenario containing regions and hospitals.

        Returns:
        - list[dict]: A list of dictionaries representing the patient flow. Each dictionary has the following structure:
            {
                "from": {"lat": float, "lon": float},
                "to": {"lat": float, "lon": float},
                "patients": int
            }
        """
        flows = []
        hospitals_calc = converter_service.map_hospitals()
        available_beds_dict = {hospital["name"]: hospital["available"] for hospital in hospitals_calc}
        default_radius = scenario.calculation.radius * 1000 # Convert radius from kilometers to meters

        for region in scenario.regions: #FIXME: Distance is calculated for every region, but only the last one is used
            region_patients = converter_service.get_total_population_by_region_name(region) * scenario.fraction
            region_coords = converter_service.get_coordinate_centre_by_region_name(region)

            region_lat = region_coords['lat']
            region_lon = region_coords['long']

            hospitals_sorted_by_distance = sorted(hospitals_calc, key=lambda h: self.haversine(region_lat, region_lon, h["lat"], h["long"]))

            for hospital in hospitals_sorted_by_distance:
                distance = self.haversine(region_lat, region_lon, hospital["lat"], hospital["long"])

                if distance <= default_radius and region_patients > 0:
                    hospital_name = hospital["name"]
                    available_beds = available_beds_dict.get(hospital_name, 0)

                    if available_beds > 0:
                        patients_to_transfer = min(region_patients, available_beds)
                        flows.append({
                            "from": {"lat": region_lat, "lon": region_lon},
                            "to": {"lat": hospital["lat"], "lon": hospital["long"]},
                            "patients": patients_to_transfer
                        })
                        region_patients -= patients_to_transfer
                        available_beds_dict[hospital_name] -= patients_to_transfer

        return flows

# # Example Usage
#
# # Initialize the scenario
# scenario = Scenario()
# scenario.calculation = {"id": "test", "radius": 50000}  # Radius in meters (50 km)
#
# # Define regions
# regions = [
#     Region(
#         name="Region 1",
#         population=500000,
#         patient_demand={"count": 1000, "specification": None},
#         latitude=0,
#         longitude=0
#     ),
#     Region(
#         name="Region 2",
#         population=300000,
#         patient_demand={"count": 500, "specification": None},
#         latitude=0.5,
#         longitude=0.5
#     ),
#     Region(
#         name="Region 3",
#         population=200000,
#         patient_demand={"count": 200, "specification": None},
#         latitude=1,
#         longitude=1
#     )
# ]
#
# # Define hospitals
# hospitals = [
#     Hospital(
#         id="Hospital 1",
#         latitude=0.3,
#         longitude=0.3,
#         allgemein_beds={"available": 400, "used": 0}
#     ),
#     Hospital(
#         id="Hospital 2",
#         latitude=0.6,
#         longitude=0.6,
#         allgemein_beds={"available": 300, "used": 0}
#     ),
#     Hospital(
#         id="Hospital 3",
#         latitude=1.2,
#         longitude=1.2,
#         allgemein_beds={"available": 200, "used": 0}
#     )
# ]
#
# # Add regions and hospitals to the scenario
# scenario.regions.extend(regions)
# scenario.hospitals.extend(hospitals)
#
# # Calculate patient flows
# calculator = PatientFlowCalculator()
# flows = calculator.calculate(scenario)
#
# # Output the results
# print(flows)
