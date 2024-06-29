from dataclasses import dataclass

@dataclass
class Bed:
    available: int
    used: int

@dataclass
class Hospital:
    id: str
    allgemein_beds: Bed
    innere_medizin_beds: Bed
    kardiologie_beds: Bed
    allgemeine_chirugie_beds: Bed
    herz_chirugie_beds: Bed
    urologie_beds: Bed
    hno_beds: Bed
    psychiatrie_beds: Bed