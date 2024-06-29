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