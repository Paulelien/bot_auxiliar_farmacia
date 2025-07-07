import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Cargar API KEY desde .env
load_dotenv()
openai.api_key = os.getenv("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")

# Título de la app
st.set_page_config(page_title="Bot Auxiliar de Farmacia", page_icon="💊")
st.title("💊 Asistente Auxiliar de Farmacia")

# Cargar conocimiento base (puede ser texto plano, resumen de curso, etc.)
with open("contenido.txt", "r", encoding="utf-8") as file:
    base_conocimiento = file.read()

# Instrucciones del sistema
system_prompt = f"""
Eres un asistente experto en farmacia comunitaria en Chile, orientado a estudiantes del curso Auxiliar de Farmacia.
Responde de forma clara, técnica pero accesible. Usa normativa chilena (ISP, D.S. 466) cuando sea necesario.

Base del conocimiento:
{base_conocimiento}
"""

# Entrada del usuario
user_question = st.text_input("Haz tu pregunta sobre farmacia:")

if user_question:
    with st.spinner("Pensando..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.2,
            max_tokens=600
        )
        answer = response['choices'][0]['message']['content']
        st.markdown(f"**Respuesta:**\n\n{answer}")
print("API KEY:", os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv
import os

load_dotenv()
print("🔐 API Key cargada:", os.getenv("OPENAI_API_KEY"))
