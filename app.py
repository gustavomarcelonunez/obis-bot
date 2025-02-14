import streamlit as st
from datetime import datetime
import json
from utils_open_ai import get_openai_response
from utils_obis import search_data, get_occurrences
from disclaimer_popup import show_disclaimer_popup

# Configuración de la página
st.set_page_config(page_title="OBIS Bot", page_icon="🧉", layout="wide")

st.title("OBIS Bot: A tool to query OBIS data in natural language. 🧉")
st.header("Ask to OBIS Bot")
st.write("To ask about datasets, perform a search first and then consult. To ask about a specific dataset, select one from the results and chat! 😎")

# Inicializa el estado
if "json" not in st.session_state:
    st.session_state.json = None

if "specie_text_field" not in st.session_state:
    st.session_state.specie_text_field = ""

# Entradas para los parámetros de búsqueda en la barra lateral
st.sidebar.header("Search parameters")

st.session_state.specie_text_field = st.sidebar.text_input(
    "Enter the full scientific name of the species (wildcards are not supported).",
    value=st.session_state.specie_text_field
)

# Botón para ejecutar la búsqueda
if st.sidebar.button("Search"):
    results = search_data(st.session_state.specie_text_field)
    if results:
        st.session_state.selected_dataset_title = None
        st.session_state.prompt_msg = "Ask about recovered Datasets Metadata"
    else:
        st.session_state.json = None

if st.sidebar.button('Disclaimer'):
    show_disclaimer_popup()

if st.session_state.json:
    st.header("Recovered Datasets")

    with open('datasets.json', 'r') as f:
        datasets = json.load(f)

    for idx, row in enumerate(datasets['results']):
        if idx % 3 == 0:  # Crear una nueva fila cada 3 elementos
            if idx != 0:
                st.markdown("<hr>", unsafe_allow_html=True)  # Agrega una línea horizontal entre filas

            cols = st.columns(3)

        with cols[idx % 3]:

            st.write(f"**Title:** *{row['title']}*")
            if "created" in row and row["created"]:
                created_date = datetime.strptime(row["created"][:-1], "%Y-%m-%dT%H:%M:%S.%f")
                formatted_date = created_date.strftime("%B %d, %Y at %I:%M %p")
                st.write(f"**Created at:** {formatted_date}")
            else:
                st.write("**Created at:** Not available")

            if "updated" in row and row["updated"]:
                updated_date = datetime.strptime(row["updated"][:-1], "%Y-%m-%dT%H:%M:%S.%f")
                formatted_date = updated_date.strftime("%B %d, %Y at %I:%M %p")
                st.write(f"**Updated at:** {formatted_date}")
            else:
                st.write("**Updated at:** Not available")

            st.markdown(f"URL: {row['url']}")

            if st.button("🤖 Ask about this data", key=row['id']):
                st.session_state.selected_dataset_title = row['title']
                st.session_state.prompt_msg = f"Ask about selected Dataset: *{row['title']}*"
                # También puedes cargar los datos del dataset seleccionado
                get_occurrences(row['id'])
                st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(st.session_state.prompt_msg)

# Muestra el prompt con el mensaje adecuado
question = st.chat_input("Ask here:")

if question:
    # Obtener la respuesta del modelo OpenAI
    answer = get_openai_response(question, st.session_state.json)
    # Mostrar la respuesta del LLM
    st.write(f"Your question: {question}")
    st.write(f"Answer: {answer}")