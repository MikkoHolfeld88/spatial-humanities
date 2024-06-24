import os
import pandas as pd

class ConverterService:
    def __init__(self):
        self.regions = self.load_regions()
        self.hospitals = self.load_hospitals()

    def load_regions(self):
        path = os.path.join(os.path.dirname(__file__), 'cities_saxony.geojson')
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def load_hospitals(self):
        path = os.path.join(os.path.dirname(__file__), 'hospitals_saxony.geojson')
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_regions(self):
        return self.regions

    def get_hospitals(self):
        return self.hospitals

    def get_population_by_region(self, region: str) -> int:
        df_regions = pd.read_json(self.regions)

        region = df_regions[df_regions['Gemeindename'] == region]

        print(region)

        population = region['Bevoelkerung_insgesamt'].values[0]

        print(population)

        return population


