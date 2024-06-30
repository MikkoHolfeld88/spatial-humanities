import os
import re

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
            data = file.read()
            return json.loads(data)

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

    def get_total_population_by_region_name(self, region_name: str) -> int:
        gdf = self.get_region_coordinates_by_name([region_name])

        if not gdf.empty:
            total_population = gdf["Bevoelkerung_insgesamt"].sum()
            return total_population
        else:
            return 0

    def get_hospital_names(self):
        gdf = gpd.GeoDataFrame.from_features(self.hospitals['features'])
        if 'Name_Einrichtung' in gdf.columns:
            return gdf['Name_Einrichtung'].tolist()
        else:
            return []


    def get_available_beds_by_hospital_name(self, hospital_name: str):
        gdf = gpd.GeoDataFrame.from_features(self.hospitals['features'])
        matched_facility = gdf[gdf['Name_Einrichtung'] == hospital_name]
        if not matched_facility.empty:
            return int(matched_facility['INSG'].iloc[0])
        else:
            return None

    def get_hospital_coordinates_by_name(self, hospital_name):
        gdf = gpd.GeoDataFrame.from_features(self.hospitals['features'])
        matched_hospital = gdf[gdf['Name_Einrichtung'] == hospital_name]

        if not matched_hospital.empty:
            point = matched_hospital.iloc[0].geometry
            return {"lat": point.y, "long": point.x}
        else:
            return None

    def get_coordinate_centre_by_region_name(self, region_name: str):
        gdf = gpd.GeoDataFrame.from_features(self.regions['features'])
        matched_region = gdf[gdf['Gemeindename'] == region_name]

        if not matched_region.empty:
            coordinate_str = matched_region['coordinate_centre'].iloc[0]
            # Assume the coordinates are stored as a string "POINT (lon lat)"
            # Using regular expressions to extract the numbers
            match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", coordinate_str)
            if match:
                longitude = float(match.group(1))
                latitude = float(match.group(2))
                return {"lat": latitude, "long": longitude}
            else:
                return None
        else:
            return None

    def map_hospitals(self):
        gdf = gpd.GeoDataFrame.from_features(self.hospitals['features'])

        hospital_data = [{
            "name": row['Name_Einrichtung'],
            "lat": row.geometry.y,
            "long": row.geometry.x,
            "available": int(row['INSG'])
        } for index, row in gdf.iterrows() if 'Name_Einrichtung' in gdf.columns and row.geometry]

        return hospital_data

converter_service = ConverterService()

coords = converter_service.get_total_population_by_region_name("Nord Leipzig, Saxony, Germany")
print(coords)

#
# region_names = converter_service.get_region_names()
# print(region_names)

