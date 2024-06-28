import math
from typing import List, Dict, Any
from dataclasses import dataclass
from backend.models.calculation import Calculation
from backend.models.hospital import Hospital
from backend.models.region import Region
from backend.models.scenario import Scenario


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
        default_radius = scenario.calculation['radius']
        flows = []

        for region in scenario.regions:
            region_patients = region.patient_demand['count']
            region_lat = region.latitude
            region_lon = region.longitude
            hospitals_sorted_by_distance = sorted(
                scenario.hospitals,
                key=lambda h: self.haversine(region_lat, region_lon, h.latitude, h.longitude)
            )

            for hospital in hospitals_sorted_by_distance:
                distance = self.haversine(region_lat, region_lon, hospital.latitude, hospital.longitude)
                if distance <= default_radius and region_patients > 0:
                    available_beds = hospital.allgemein_beds['available']
                    if available_beds > 0:
                        patients_to_transfer = min(region_patients, available_beds)
                        flows.append({
                            "from": {"lat": region_lat, "lon": region_lon},
                            "to": {"lat": hospital.latitude, "lon": hospital.longitude},
                            "patients": patients_to_transfer
                        })
                        region_patients -= patients_to_transfer
                        hospital.allgemein_beds['available'] -= patients_to_transfer

        return flows


# Example Usage

# Initialize the scenario
scenario = Scenario()
scenario.calculation = {"id": "test", "radius": 50000}  # Radius in meters (50 km)

# Define regions
regions = [
    Region(
        name="Region 1",
        population=500000,
        patient_demand={"count": 1000, "specification": None},
        latitude=0,
        longitude=0
    ),
    Region(
        name="Region 2",
        population=300000,
        patient_demand={"count": 500, "specification": None},
        latitude=0.5,
        longitude=0.5
    ),
    Region(
        name="Region 3",
        population=200000,
        patient_demand={"count": 200, "specification": None},
        latitude=1,
        longitude=1
    )
]

# Define hospitals
hospitals = [
    Hospital(
        id="Hospital 1",
        latitude=0.3,
        longitude=0.3,
        allgemein_beds={"available": 400, "used": 0}
    ),
    Hospital(
        id="Hospital 2",
        latitude=0.6,
        longitude=0.6,
        allgemein_beds={"available": 300, "used": 0}
    ),
    Hospital(
        id="Hospital 3",
        latitude=1.2,
        longitude=1.2,
        allgemein_beds={"available": 200, "used": 0}
    )
]

# Add regions and hospitals to the scenario
scenario.regions.extend(regions)
scenario.hospitals.extend(hospitals)

# Calculate patient flows
calculator = PatientFlowCalculator()
flows = calculator.calculate(scenario)

# Output the results
print(flows)
