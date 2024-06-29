from dataclasses import dataclass


@dataclass
class HospitalBeds:
    name: str
    available: int
    used: int