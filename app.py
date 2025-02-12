import streamlit as st
from datetime import datetime
from utils_open_ai import get_openai_response
from utils_pdf import get_pdfs

# Configuración de la página
st.set_page_config(page_title="Gustavo Marcelo Nuñez", page_icon="🧉", layout="wide")

st.title("Gustavo Marcelo Nuñez: About ChatBot 🧉")
st.header("Ask to ChatBot")
st.write("This tool was develop to ask about Gustavo's skills, academic history, work experience, etc. Just feel free to ask here! 😎")

# Inicializa el estado
if "json" not in st.session_state:
    st.session_state.json = None

doc = get_pdfs()
#if "country" not in st.session_state:
#    st.session_state.country = None

#if "dataset_type" not in st.session_state:
#    st.session_state.dataset_type = None

#if "text_field" not in st.session_state:
#    st.session_state.text_field = ""

# Muestra el prompt con el mensaje adecuado
question = st.chat_input("Ask here:")

if question:
    # Obtener la respuesta del modelo OpenAI
    answer = get_openai_response(question, st.session_state.json)
    # Mostrar la respuesta del LLM
    st.write(f"Your question: {question}")
    st.write(f"Answer: {answer}")
