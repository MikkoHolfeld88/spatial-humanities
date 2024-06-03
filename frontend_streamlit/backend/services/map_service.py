from keplergl import KeplerGl


class MapService():
    def __init__(self):
        self.map = KeplerGl(height=800)
        self.map.config = {
            'version': 'v1',
            'config': {
                'mapState': {
                    'latitude': 51.340199,
                    'longitude': 12.360103,
                    'zoom': 11,
                    'bearing': 0,
                    'pitch': 0,
                    'style': 'light'
                }
            }
        }

    def add_data_to_map(self, data, name="data"):
        self.map.add_data(data=data, name=name)

    def get_map(self):
        return self.map

map_service = MapService()