from dataclasses import dataclass

@dataclass
class PatientDemand:
    count: int = 0
    specification: list[str] = None

@dataclass
class Region:
    id: str = ""
    name: str = ""
    population: int = 0
    patient_demand: float | PatientDemand = None
    latitude: float = 0
    longitude: float = 0
