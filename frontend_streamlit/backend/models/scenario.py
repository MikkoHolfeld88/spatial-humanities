from dataclasses import dataclass

from traittypes.traittypes import DataFrame

from backend.models.calculation import Calculation
from backend.models.hospital_beds import HospitalBeds


@dataclass
class Scenario:
    name: str
    desc: str
    fraction: float
    patient_demand: int
    regions: list[str]
    calculation: Calculation | None
    hospitals: list[str]
    hospital_beds: list[HospitalBeds] | None
