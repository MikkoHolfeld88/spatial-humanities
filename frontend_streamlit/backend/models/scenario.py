from dataclasses import dataclass

from backend.models.calculation import Calculation
from backend.models.hospital import Hospital
from backend.models.region import Region


@dataclass
class Scenario:
    regions: list[Region]
    calculation: Calculation
    hospitals: list[Hospital]


