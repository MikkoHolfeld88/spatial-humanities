from dataclasses import dataclass

@dataclass
class HospitalBedCategories:
    chirugie: int | None
    herzchirugie: int | None
    innere_medizin: int | None
    neurologie: int | None
    orthopaedie: int | None
    psychiatrie: int | None
    urologie: int | None
    kardiologie: int | None
    hno: int | None


@dataclass
class HospitalBeds:
    name: str
    available: int
    used: int
    categories: HospitalBedCategories | None