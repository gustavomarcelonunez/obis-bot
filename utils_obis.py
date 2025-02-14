import streamlit as st
import pandas as pd
import requests
import json

def search_data(specie_text_field):
    url = "https://api.obis.org/v3/dataset"
    params = {
        "scientificname": specie_text_field,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            data['results'] = data['results'][:15]  # Limita a los primeros 10 elementos
            with open('datasets.json', 'w') as f:
                json.dump(data, f, indent=4)  # Guardar con indentación para mejor legibilidad
            st.session_state.json = data
            return data['results'][0]
        else:
            st.error("No data was found for the selected parameters.")
            return None
    elif response.status_code == 500:
        st.error(f"Request error: {response.status_code} - OBIS Internal Server Error")
        return None
    else:
        st.error(f"Request error: {response.status_code} - {response.text}")
        return None
    
def get_occurrences(dataset_id):

    url = "https://api.obis.org/v3/occurrence"
    params = {"datasetid": dataset_id,
              "size": 100}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            keys_to_keep = ["occurrenceID", "occurrenceStatus", "basisOfRecord", "scientificName", "scientificNameID", "eventDate", "decimalLatitude", "decimalLongitude"]

            filtered_results = [
                {key: dataset[key] for key in keys_to_keep if key in dataset}
                for dataset in data["results"]
            ]


            with open('ocurrencias.json', 'w') as f:
                json.dump(data, f, indent=4)  # Guardar con indentación para mejor legibilidad
            st.session_state.json = {"results": filtered_results}
        else:
            st.warning("No results found.")
    else:
        st.error(f"Request error: {response.status_code} - {response.text}")