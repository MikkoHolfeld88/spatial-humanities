import os
import pandas as pd
import geopandas as gpd
import json

from traittypes.traittypes import DataFrame


class ConverterService:
    def __init__(self):
        self.regions = self.load_regions()
        self.hospitals = self.load_hospitals()

    def load_regions(self):
        path = os.path.join(os.path.dirname(__file__), 'cities_saxony.geojson')
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
            return json.loads(data)

    def load_hospitals(self):
        path = os.path.join(os.path.dirname(__file__), 'hospitals_saxony.geojson')
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_regions(self):
        return self.regions

    def get_region_names(self):
        gdf = gpd.GeoDataFrame.from_features(self.regions['features'])
        return gdf['Gemeindename'].tolist()

    def get_hospitals(self):
        return self.hospitals

    def get_region_coordinates_by_name(self, names: list[str]):
        gdf = gpd.GeoDataFrame.from_features(self.regions['features'])
        filtered_gdf = gdf[gdf['Gemeindename'].isin(names)]
        return filtered_gdf

    def get_population_by_regions(self, regions: list[str]) -> DataFrame:
        filtered_gdf = self.get_region_coordinates_by_name(regions)

        total_population = filtered_gdf["Bevoelkerung_insgesamt"].sum()
        male_population = filtered_gdf["Bevoelkerung_maennlich"].sum()
        female_population = filtered_gdf["Bevoelkerung_weiblich"].sum()

        df = pd.DataFrame(
            [
                {"type": "♀ Female", "value": female_population},
                {"type": "♂ Male", "value": male_population},
                {"type": "🟰 Total", "value": total_population}
            ]
        )

        return df


# converter_service = ConverterService()
#
# region_names = converter_service.get_region_names()
# print(region_names)