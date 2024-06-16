from keplergl import KeplerGl


class MapService:
    def __init__(self):
        self.config = {
            'version': 'v1',
            'config': {
                'mapState': {
                    'latitude': 51.340199,
                    'longitude': 12.360103,
                    'zoom': 11,
                    'bearing': 0,
                    'pitch': 45,  # Pitch für 3D-Ansicht
                },
                'mapStyle': {
                    'styleType': 'light'
                },
                'visState': {
                    'layers': [
                        {
                            'id': 'regions_layer',
                            'type': 'geojson',
                            'config': {
                                'dataId': 'regions_le',
                                'isVisible': False,
                                'isConfigActive': True,
                                'extruded': True,
                                'sizeRange': [0, 1],
                                'coverage': 1,
                                'enable3d': True
                            }
                        },

                    ]
                }
            }
        }
        self.map = KeplerGl(height=800, config=self.config)

    def add_data_to_map(self, data, name="data"):
        self.map.add_data(data=data, name=name)

    def set_layer_visibility(self, name, visible):
        for layer in self.map.config["config"]["visState"]["layers"]:
            if layer["config"]["dataId"] == name:
                layer["config"]["isVisible"] = visible

        print(self.map.config)

    def get_map(self):
        return self.map
