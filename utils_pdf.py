import streamlit as st
import requests
import json
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter # dividir en chunks
from langchain.embeddings import SentenceTransformerEmbeddings # Embeddings


@st.cache_resource
def get_pdfs():

    DATA_PATH = "./pdf/CV Nuñez.pdf"
    loader = PyPDFDirectoryLoader(DATA_PATH)
    data_on_pdf = loader.load()
    
    for doc in data_on_pdf:
        doc.page_content = re.sub(r'\s+', ' ', doc.page_content).strip()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, # Delimitar tamaño de los chunks
        chunk_overlap=100 # overlapping para preservar el contexto
        # separators=["\n\n", "\n", ". ", " ", ""], -> usar otros separadores
    )
    splits = text_splitter.split_documents(data_on_pdf)

    model_name = "paraphrase-MiniLM-L6-v2" # "all-MiniLM-L6-v2"  "paraphrase-MiniLM-L6-v2"
    embeddings_model = SentenceTransformerEmbeddings(model_name=model_name)
    
    path_db = "/content/db_vectorial"
    db_name=path_db.split("/")[-1]

    # Almacenamos los chunks en la base de datos
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings_model,
        persist_directory=path_db,
        collection_name=db_name,
        )
    
    
    return doc

