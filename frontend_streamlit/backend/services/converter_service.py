import os

import geopy.geocoders as geocoders
import json

class ConverterService:
    def __init__(self, user_agent: str, scheme: str = "http", domain: str = "nominatim.openstreetmap.org"):
        self.geolocator = geocoders.Nominatim(user_agent=user_agent, scheme=scheme, domain=domain)

    def geocode_address(self, address: str):
        location = self.geolocator.geocode(address)
        if location:
            return {"address": address, "lat": location.latitude, "lon": location.longitude}
        else:
            return {"address": address, "lat": None, "lon": None}

    def geocode_addresses(self, addresses: list):
        geocoded_data = []
        for address in addresses:
            geocoded_data.append(self.geocode_address(address))
        return geocoded_data

    def to_geojson(self, geocoded_data: list):
        features = []
        for item in geocoded_data:
            if item["lat"] is not None and item["lon"] is not None:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [item["lon"], item["lat"]]
                    },
                    "properties": {
                        "address": item["address"]
                    }
                })
        return {
            "type": "FeatureCollection",
            "features": features
        }

    def save_geojson(self, geojson_data: dict, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(geojson_data, f)

    def get_regions(self):
        path = os.path.join(os.path.dirname(__file__), 'cities_saxony.geojson')
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_hospitals(self):
        path = os.path.join(os.path.dirname(__file__), 'hospitals.geojson')
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()