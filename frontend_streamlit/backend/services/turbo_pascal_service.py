from ..clients.overpass_api_client import OverpassAPIClient


class TurboPascalService:
    def __init__(self):
        self.overpass_client = OverpassAPIClient()

    def execute_query(self, query):
        """ executes query and returns the result """

        return self.overpass_client.request(query)

    def get_leipzig_suburbs(self):
        """Returns all suburbs of Leipzig in GeoJSON format."""

        query = """
            [out:json];
            area["name"="Leipzig"];
            relation["boundary"="administrative"]["admin_level"="8"](area);
            out geom;
        """
        return self.execute_query(query)