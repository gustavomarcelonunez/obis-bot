from openai import OpenAI
import streamlit as st


# Cargar la API key desde el entorno
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)

def get_openai_response(question, json):
    try:

        if not json:
            return "Hi 👋! You must perform a search first using the sidebar before interacting with the chat."

        # Aclarar tema del archivo vacio de entrada
        chat_history = [
            {"role": "system", "content": "You are an assistant bot specialized in interpreting and providing information from a JSON file related to marine species and marine biodiversity data from the OBIS portal. Your primary focus is on providing accurate and relevant information based on this data. Always respond in English."},
            {"role": "system", "content": "You have access to a JSON file with the following content: "},
            {"role": "system", "content": f"{json}"},
            {"role": "system", "content": "Assume that any question the user asks is related to the data available in the json file, unless the user explicitly states otherwise. Respond based on the information from the JSON."},
            {"role": "system", "content": "The user can ask about the metadata of all retrieved datasets or choose a specific dataset from the list for more details. If no dataset is selected, provide general metadata information about all retrieved datasets."},
            {"role": "system", "content": "If the user asks questions unrelated to species, biodiversity, or the OBIS data, politely inform them that your function is limited to assisting with marine biodiversity-related queries and tasks."},
            {"role": "system", "content": "You can also assist with related tasks, such as drafting emails to contacts found within the dataset, but you should not engage in tasks unrelated to the application."}
        ]

        if "selected_dataset_title" in st.session_state:
            chat_history.append({"role": "system", "content": f"The selected dataset title is: {st.session_state.selected_dataset_title}"})

        chat_history.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            temperature=0,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return "Error."