import os
import re

import numpy as np
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

    # def get_patient_flow_example(self):
    #     df = pd.read_csv('Patientenfluss.csv')
    #     return df

    def convert_flows_to_geojson(self, flows):
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }

        for flow in flows:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [flow['from']['lon'], flow['from']['lat']],
                        [flow['to']['lon'], flow['to']['lat']]
                    ]
                },
                "properties": {
                    "patients": flow['patients']
                }
            }
            geojson['features'].append(feature)

        return geojson

    # def convert_flows_to_geojson(self, flows):
    #     geojson = {
    #         "type": "FeatureCollection",
    #         "features": []
    #     }
    #
    #     for flow in flows:
    #         # Start- und Endpunkte extrahieren
    #         start = [flow['from']['lon'], flow['from']['lat']]
    #         end = [flow['to']['lon'], flow['to']['lat']]
    #
    #         # Mittelpunkt und Radius für den Bogen berechnen
    #         mid = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 0.01]  # Leichter Nordversatz für den Bogen
    #         radius = np.sqrt((mid[0] - start[0]) ** 2 + (mid[1] - start[1]) ** 2)
    #
    #         # Punkte des Bogens generieren
    #         angle_start = np.arctan2(start[1] - mid[1], start[0] - mid[0])
    #         angle_end = np.arctan2(end[1] - mid[1], end[0] - mid[0])
    #         if angle_start < angle_end:
    #             angle_start, angle_end = angle_end, angle_start
    #
    #         arc_angle = np.linspace(angle_end, angle_start, num=30)  # Anzahl der Punkte kann angepasst werden
    #         arc = [[mid[0] + radius * np.cos(angle), mid[1] + radius * np.sin(angle)] for angle in arc_angle]
    #
    #         # Pfeilspitze am Ende des Bogens hinzufügen
    #         arrow_size = 0.0005  # Größe der Pfeilspitze anpassen
    #         arrow_head = [
    #             [end[0], end[1]],
    #             [end[0] + arrow_size * np.cos(angle_start - np.pi / 6),
    #              end[1] + arrow_size * np.sin(angle_start - np.pi / 6)],
    #             [end[0] + arrow_size * np.cos(angle_start + np.pi / 6),
    #              end[1] + arrow_size * np.sin(angle_start + np.pi / 6)],
    #             [end[0], end[1]]
    #         ]
    #
    #         # Feature für den GeoJSON
    #         feature = {
    #             "type": "Feature",
    #             "geometry": {
    #                 "type": "LineString",
    #                 "coordinates": arc + arrow_head
    #             },
    #             "properties": {
    #                 "patients": flow['patients']
    #             }
    #         }
    #         geojson['features'].append(feature)
    #
    #     return geojson

converter_service = ConverterService()

coords = converter_service.get_total_population_by_region_name("Nord Leipzig, Saxony, Germany")
print(coords)

#
# region_names = converter_service.get_region_names()
# print(region_names)

