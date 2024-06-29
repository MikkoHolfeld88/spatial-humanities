from dataclasses import dataclass

from backend.models.calculation import Calculation
from backend.models.hospital import Hospital
from backend.models.region import Region


@dataclass
class Scenario:
    name: str
    desc: str
    fraction: float
    patient_demand: int
    regions: list[Region]
    calculation: Calculation | None
    hospitals: list[Hospital]
