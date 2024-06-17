import os


class ConverterService:

    def get_regions(self):
        path = os.path.join(os.path.dirname(__file__), 'cities_saxony.geojson')
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_hospitals(self):
        path = os.path.join(os.path.dirname(__file__), 'hospitals_saxony.geojson')
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()