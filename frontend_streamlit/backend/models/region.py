from dataclasses import dataclass

@dataclass
class PatientDemand:
    count: int
    specification: list[str]

@dataclass
class Region:
    id: str
    name: str
    population: int
    patient_demand: float | PatientDemand
    latitude: float
    longitude: float
    """
    Represents a region with a population and patient demand.

    Attributes:
    - name (str): Name of the region.
    - population (int): Population of the region.
    - patient_demand (dict): Contains patient demand information. Example: {"count": 1000, "specification": None}.
    - latitude (float): Latitude of the region.
    - longitude (float): Longitude of the region.
    """
    def __init__(self, name, population, patient_demand, latitude, longitude):
        self.name = name
        self.population = population
        self.patient_demand = patient_demand
        self.latitude = latitude
        self.longitude = longitude