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
    """
      Represents a hospital with available and used beds.

      Attributes:
      - id (str): Identifier for the hospital.
      - latitude (float): Latitude of the hospital.
      - longitude (float): Longitude of the hospital.
      - allgemein_beds (dict): Contains information about available and used beds. Example: {"available": 400, "used": 0}.
      """
    def __init__(self, id, latitude, longitude, allgemein_beds):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.allgemein_beds = allgemein_beds