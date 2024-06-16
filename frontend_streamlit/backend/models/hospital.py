from dataclasses import dataclass

@dataclass
class Hospital:
    id: str = ""
    used_beds: int = 0