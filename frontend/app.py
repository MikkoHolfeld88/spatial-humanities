import streamlit as st
from keplergl import KeplerGl
import pandas as pd
from data.load_data import load_data
from components.sidebar import create_sidebar
from components.map_config import configure_map

st.title("Dynamische Kepler.gl-Karte mit Streamlit")

# Daten laden
data = load_data()

# Sidebar erstellen und Benutzerinteraktionen handhaben
selected_column, filter_value = create_sidebar(data)

# Daten filtern, nur wenn die ausgewählte Spalte numerisch ist
if pd.api.types.is_numeric_dtype(data[selected_column]):
    filtered_data = data[data[selected_column] >= filter_value]
else:
    st.sidebar.warning("Die ausgewählte Spalte ist nicht numerisch. Bitte wählen Sie eine numerische Spalte.")
    filtered_data = data

# Karte konfigurieren
map_1 = configure_map(filtered_data)

# Karte anzeigen
st.markdown(map_1._repr_html_(), unsafe_allow_html=True)