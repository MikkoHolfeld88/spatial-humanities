from dataclasses import dataclass

from frontend_streamlit.backend.models.calculation import Calculation
from frontend_streamlit.backend.models.hospital import Hospital
from frontend_streamlit.backend.models.region import Region


@dataclass
class Scenario:
    regions: list[Region] = None
    calculation: Calculation = Calculation()
    hospitals: list[Hospital] = None


