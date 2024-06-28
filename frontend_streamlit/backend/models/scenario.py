from dataclasses import dataclass

from backend.models.calculation import Calculation
from backend.models.hospital import Hospital
from backend.models.region import Region


@dataclass
class Scenario:
    """
       Represents the entire scenario containing regions and hospitals.

       Attributes:
       - calculation (dict): Contains calculation parameters like radius.
       - regions (list): List of Region objects.
       - hospitals (list): List of Hospital objects.
       """
    regions: list[Region]
    calculation: Calculation
    hospitals: list[Hospital]

    def __init__(self):
        self.calculation = None
        self.regions = []
        self.hospitals = []