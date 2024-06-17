from dataclasses import dataclass

@dataclass
class Bed:
    available: number = 0
    used: number = 0

@dataclass
class Hospital:
    id: str = ""
    allgemein_beds: Bed = Bed()
    innere_medizin_beds: Bed = Bed()
    kardiologie_beds: Bed = Bed()
    allgemeine_chirugie_beds: Bed = Bed()
    herz_chirugie_beds: Bed = Bed()
    urologie_beds: Bed = Bed()
    hno_beds: Bed = Bed()
    psychiatrie_beds: Bed = Bed()