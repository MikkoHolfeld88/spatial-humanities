import streamlit as st

def create_sidebar(data):
    st.sidebar.header("Kartenoptionen")

    # Auswahlbox zur Auswahl einer Spalte
    column_options = data.select_dtypes(include=[float, int]).columns.tolist()
    selected_column = st.sidebar.selectbox("Wählen Sie eine Spalte für die Visualisierung:", column_options)

    # Filterwert für die ausgewählte Spalte
    if selected_column:
        filter_value = st.sidebar.slider("Wählen Sie einen Filterwert für die Spalte:",
                                         min_value=float(data[selected_column].min()),
                                         max_value=float(data[selected_column].max()),
                                         value=float(data[selected_column].mean()))
    else:
        filter_value = None

    return selected_column, filter_value
