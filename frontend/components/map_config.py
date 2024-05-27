from keplergl import KeplerGl

def configure_map(data):
    map_1 = KeplerGl(height=600)
    map_1.add_data(data, "data")
    return map_1