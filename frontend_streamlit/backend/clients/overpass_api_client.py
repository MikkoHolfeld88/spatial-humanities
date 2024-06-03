import requests
import json

class OverpassAPIClient:
    def __init__(self):
        self.url = "http://overpass-api.de/api/interpreter"

    def request(self, query: str, pretty_print=False):
        try:
            response = requests.post(self.url, data={'data': query})
            response.raise_for_status()
            data = response.json()
            if pretty_print:
                return json.dumps(data, indent=4)
            return data
        except requests.RequestException as e:
            print("Ein Fehler ist bei der Anfrage aufgetreten:", e)
            return None

overpass_api_client = OverpassAPIClient()