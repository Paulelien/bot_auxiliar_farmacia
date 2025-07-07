import streamlit as st
import os
from faq import buscar_en_faq
from embedding_utils import cargar_o_crear_indice, buscar_similares
from openai import OpenAI
from dotenv import load_dotenv

# Configuración de la página
st.set_page_config(
    page_title="ChatBot Auxiliar de Farmacia",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Aplicar estilos CSS personalizados
st.markdown("""
<style>
/* Paleta de colores farmacéutica */
:root {
    --color-primario: #2E7D32;
    --color-secundario: #4CAF50;
    --color-acento: #FF6B35;
    --color-texto: #2C3E50;
    --color-fondo: #F8F9FA;
    --color-blanco: #FFFFFF;
    --color-gris-claro: #E9ECEF;
}

/* Estilos generales */
.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header principal */
.main-header {
    background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
    text-align: center;
}

/* Tarjetas de información */
.info-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-left: 4px solid #4CAF50;
    transition: transform 0.2s ease;
}

.info-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

/* Botones personalizados */
.stButton > button {
    background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(46, 125, 50, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4);
    background: linear-gradient(90deg, #1B5E20 0%, #388E3C 100%);
}

/* Input de texto personalizado */
.stTextInput > div > div > input {
    border-radius: 25px;
    border: 2px solid #E9ECEF;
    padding: 1rem 1.5rem;
    font-size: 16px;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #4CAF50;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

/* Sidebar mejorado */
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #2E7D32 0%, #4CAF50 100%);
    color: white;
}

/* Expanders personalizados */
.streamlit-expanderHeader {
    background: linear-gradient(90deg, #4CAF50 0%, #66BB6A 100%);
    color: white;
    border-radius: 8px;
    font-weight: 600;
}

/* Mensajes de éxito */
.stSuccess {
    background: linear-gradient(90deg, #4CAF50 0%, #66BB6A 100%);
    color: white;
    border-radius: 12px;
    padding: 1rem;
    border-left: 4px solid #2E7D32;
}

/* Mensajes de error */
.stError {
    background: linear-gradient(90deg, #F44336 0%, #EF5350 100%);
    color: white;
    border-radius: 12px;
    padding: 1rem;
    border-left: 4px solid #D32F2F;
}

/* Chat container */
.chat-container {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    margin: 2rem 0;
}

/* Historial de chat */
.chat-history {
    background: #F8F9FA;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid #E9ECEF;
}

/* Iconos y emojis */
.emoji-icon {
    font-size: 1.5rem;
    margin-right: 0.5rem;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header {
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .info-card {
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .chat-container {
        padding: 1rem;
        margin: 1rem 0;
    }
}
</style>
""", unsafe_allow_html=True)

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Logo de Avanxa prominente
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo_avanxa.png", use_container_width=True)
    st.markdown("---")

# Título principal con diseño mejorado
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">Chatbot Auxiliar de Farmacia</h1>
    <p style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Asistente educativo inteligente para el curso de Auxiliar de Farmacia</p>
</div>
""", unsafe_allow_html=True)

# Paleta de colores farmacéutica
COLORES = {
    'primario': '#2E7D32',      # Verde farmacia
    'secundario': '#4CAF50',    # Verde claro
    'acento': '#FF6B35',        # Naranja para alertas
    'texto': '#2C3E50',         # Azul oscuro
    'fondo': '#F8F9FA'          # Gris muy claro
}



# Sidebar con información y guía
with st.sidebar:
    st.header("Información y Ayuda")
    with st.expander("Como usar el bot"):
        st.markdown("""
        1. Escribe tu pregunta en el campo de texto.
        2. Presiona 'Preguntar' o Enter.
        3. Recibirás una respuesta basada en el material del curso.
        """)
    with st.expander("Tipos de preguntas que puedes hacer"):
        st.markdown("""
        **Preguntas sobre el curso:**
        - ¿Dónde descargar mi certificado?
        - ¿Se actualiza el porcentaje de avance?
        - ¿Tengo prórroga disponible?
        **Preguntas sobre farmacia:**
        - ¿Qué hace un auxiliar de farmacia?
        - ¿Qué son las formas farmacéuticas?
        - ¿Cómo se mantiene la cadena de frío?
        - ¿Qué dice el Decreto 405?
        **Preguntas sobre normativas:**
        - ¿Cuáles son las normativas vigentes?
        - ¿Qué dice el Decreto 79?
        - ¿Cómo se regulan los psicotrópicos?
        """)
    with st.expander("Consejos para mejores respuestas"):
        st.markdown("""
        **Haz preguntas específicas:**
        - "¿Qué son las cápsulas?" (mejor que "medicamentos")
        **Puedes preguntar en lenguaje natural:**
        - "¿Qué necesito para trabajar en una farmacia?"
        - "¿Cómo se guardan las vacunas?"
        **Para preguntas sobre el curso:**
        - Usa palabras como "certificado", "prórroga", "porcentaje"
        **Para preguntas técnicas:**
        - El bot buscará en el material del curso
        """)
    with st.expander("Material disponible"):
        st.markdown("""
        **Módulos del curso:**
        - Legislación farmacéutica
        - Tecnología farmacéutica
        - Arsenal farmacoterapéutico
        - Atención al paciente crónico
        **Documentos legales:**
        - Decreto 405 (psicotrópicos)
        - Decreto 79
        - DTO-466
        **Preguntas frecuentes:**
        - Certificados y descargas
        - Porcentaje de avance
        - Prórrogas disponibles
        """)

st.markdown("""
Bienvenido/a al asistente del curso **Auxiliar de Farmacia**. 
Puedes hacer preguntas sobre el contenido técnico del curso. 
""")

# Cargar FAQ y material del curso
CARPETA_MATERIAL = "material"

# Cargar texto y embeddings del material
@st.cache_resource(show_spinner="Cargando y procesando el material del curso...")
def cargar_material():
    from pdf_utils import cargar_multiples_pdfs, extraer_texto_archivo
    textos_con_metadatos = cargar_multiples_pdfs(CARPETA_MATERIAL)
    if not textos_con_metadatos:
        txt_path = os.path.join(CARPETA_MATERIAL, "contenido_curso.txt")
        if os.path.exists(txt_path):
            secciones = extraer_texto_archivo(txt_path)
            textos_con_metadatos = [{"archivo": "contenido_curso.txt", "pagina": i+1, "texto": seccion} 
                                   for i, seccion in enumerate(secciones)]
    if not textos_con_metadatos:
        st.error("No se encontró material del curso. Asegúrate de tener PDFs o el archivo de texto en la carpeta material/")
        return None, []
    indice, textos = cargar_o_crear_indice(textos_con_metadatos)
    return indice, textos

indice, textos = cargar_material()

# Inicializar historial de chat
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Agregar contenido principal antes del chat
st.markdown("""
<div class="chat-container">
    <h2 style="color: #2E7D32; margin-bottom: 1.5rem;">📚 Información del Curso</h2>
    <p style="font-size: 1.1rem; line-height: 1.6; color: #2C3E50;">
        Este asistente te ayuda con preguntas sobre el curso de <strong>Auxiliar de Farmacia</strong>. 
        Puedes consultar sobre legislación, tecnología farmacéutica, arsenal farmacoterapéutico y más.
    </p>
</div>
""", unsafe_allow_html=True)

# Mostrar información sobre el material disponible con tarjetas visuales
st.markdown("""
<div style="margin: 2rem 0;">
    <h3 style="color: #2E7D32; margin-bottom: 1.5rem;">📖 Material Disponible</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
        <div class="info-card">
            <h4 style="color: #2E7D32; margin-bottom: 1rem;">🎓 Módulos del Curso</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: #F8F9FA; border-radius: 8px;">📋 Legislación farmacéutica</li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: #F8F9FA; border-radius: 8px;">🔬 Tecnología farmacéutica</li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: #F8F9FA; border-radius: 8px;">💊 Arsenal farmacoterapéutico</li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: #F8F9FA; border-radius: 8px;">👥 Atención al paciente crónico</li>
            </ul>
        </div>
        <div class="info-card">
            <h4 style="color: #2E7D32; margin-bottom: 1rem;">📜 Documentos Legales</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: #F8F9FA; border-radius: 8px;">📜 Decreto 405 (psicotrópicos)</li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: #F8F9FA; border-radius: 8px;">📜 Decreto 79</li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: #F8F9FA; border-radius: 8px;">📜 DTO-466</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat al final del panel con diseño mejorado
st.markdown("""
<div class="chat-container">
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #2E7D32; margin-bottom: 0.5rem;">💬 Chat Inteligente</h2>
        <p style="color: #666; font-size: 1.1rem; margin: 0;">Escribe tu pregunta sobre el curso de Auxiliar de Farmacia</p>
    </div>
</div>
""", unsafe_allow_html=True)

pregunta = st.text_input("Escribe tu pregunta", placeholder="Ej: ¿Qué es el principio FEFO?", value=st.session_state.get('pregunta_sugerida', ''), label_visibility="collapsed", key="chat_input")
pregunta_limpia = pregunta.strip() if pregunta else ""
boton_presionado = st.button("Preguntar")
pregunta_enviada = boton_presionado
if boton_presionado and not pregunta_limpia:
    st.warning("Por favor, escribe una pregunta antes de presionar 'Preguntar'")
if pregunta_enviada and pregunta_limpia:
    st.session_state.pregunta_anterior = pregunta_limpia
    if pregunta and pregunta != st.session_state.get('pregunta_sugerida', ''):
        st.session_state.contador_interacciones = st.session_state.get('contador_interacciones', 0) + 1
    if 'pregunta_sugerida' in st.session_state:
        del st.session_state.pregunta_sugerida
    respuesta_faq = None
    palabras_faq = ['certificado', 'descargar', 'plataforma', 'actividades', 'porcentaje', 'prórroga', 'tutor', 'soporte']
    palabras_tecnicas = ['farmacéuticas', 'fármacos', 'medicamentos', 'almacenamiento', 'cadena', 'frío', 
                        'decreto', 'legislación', 'tecnología', 'arsenal', 'atención', 'cliente', 
                        'ética', 'auxilios', 'inventario', 'recetas', 'psicotrópicos']
    if any(palabra in pregunta.lower() for palabra in palabras_faq) and not any(palabra in pregunta.lower() for palabra in palabras_tecnicas):
        respuesta_faq = buscar_en_faq(pregunta)
    if respuesta_faq:
        st.success(respuesta_faq)
    else:
        resultados = buscar_similares(pregunta, indice, textos, k=3)
        contexto_partes = []
        for r in resultados:
            if isinstance(r, dict) and 'texto' in r:
                archivo = r.get('archivo', 'Desconocido')
                pagina = r.get('pagina', 'N/A')
                texto = r['texto']
                contexto_partes.append(f"[{archivo} - Página {pagina}]\n{texto}")
            elif isinstance(r, str):
                contexto_partes.append(r)
        contexto = "\n".join(contexto_partes)
        prompt = f"""
Eres un asistente educativo experto en farmacia y normativa sanitaria chilena. Estás diseñado para apoyar a estudiantes del curso de Auxiliar de Farmacia en Chile, respondiendo con información clara, precisa y confiable, basada exclusivamente en los contenidos del curso, documentos cargados y fuentes oficiales.

REGLAS DE RESPUESTA:

- No inventes información. Si no sabes con certeza un dato o no está en los documentos cargados, indícalo y sugiere al estudiante consultar con su tutor académico.
- No completes con inferencias ni suposiciones. Sé riguroso en la fuente de cada respuesta.
- Si no encuentras la información que necesita el estudiante o se requiere una orientación académica más específica, responde:  
  "**Si no encuentras la información que necesitas o requieres una orientación académica más específica, te recomiendo comunicarte con tu tutor académico a través del apartado *Consultas Académicas* en el menú superior de la plataforma.**"

📌 **Uso del Vademécum (https://www.vademecum.es/chile/cl/alfa)**  
Solo redirige al Vademécum si el usuario consulta específicamente sobre:
- Principio activo de un medicamento específico
- Dosis exacta de un medicamento
- Grupo terapéutico
- Clasificación ATC

No lo uses para responder sobre normativas, funciones del auxiliar o conceptos generales.

📘 **Responde normalmente usando el contexto del curso en preguntas sobre:**
- Conceptos generales de farmacología
- Formas farmacéuticas (comprimidos, cápsulas, jarabes, etc.)
- Funciones del auxiliar de farmacia
- Normativas (como el Decreto 405)
- Almacenamiento y cadena de frío
- Atención al cliente
- Ética profesional
- Tecnología farmacéutica

📑 **Normativas legales específicas:**
Si el usuario menciona leyes o decretos como el Decreto 79:
- Intenta recuperar la información exacta desde los documentos cargados.
- Si no encuentras el artículo solicitado, responde:  
  "Actualmente no tengo acceso directo al artículo solicitado del Decreto 79. Te recomiendo consultarlo directamente en: https://www.leychile.cl o escribir a tu tutor académico desde el apartado de Consultas Académicas en el menú superior de la plataforma."

⚠️ No confundas el Decreto 79 con otros (como el Decreto 466) a menos que esté expresamente mencionado.

Pregunta: {pregunta}
Contexto:
{contexto}
"""
        try:
            respuesta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Eres un asistente educativo experto en farmacia."},
                          {"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.2
            )
            respuesta_final = respuesta.choices[0].message.content
            if respuesta_final:
                respuesta_final = respuesta_final.strip()
            else:
                respuesta_final = "Lo siento, no pude generar una respuesta. Por favor, intenta reformular tu pregunta."
            st.success(respuesta_final)
            st.session_state.chat_history.append((pregunta, respuesta_final))
        except Exception as e:
            st.error(f"Error al consultar OpenAI: {e}")

# Mostrar historial de conversación con diseño mejorado
if st.session_state.chat_history:
    st.markdown("""
    <div class="chat-history">
        <h3 style="color: #2E7D32; margin-bottom: 1.5rem;">💬 Conversaciones Anteriores</h3>
        <p style="color: #666; margin-bottom: 1rem;">Últimas 3 conversaciones</p>
    </div>
    """, unsafe_allow_html=True)
    
    conversaciones_recientes = st.session_state.chat_history[-3:]
    for i, (pregunta_hist, respuesta_hist) in enumerate(conversaciones_recientes, 1):
        with st.expander(f"🗨️ Conversación {len(st.session_state.chat_history) - 3 + i}", expanded=False):
            st.markdown(f"""
            <div style="background: #F8F9FA; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <h4 style="color: #2E7D32; margin-bottom: 0.5rem;">❓ Pregunta:</h4>
                <p style="margin: 0; font-weight: 500;">{pregunta_hist}</p>
            </div>
            <div style="background: #E8F5E8; padding: 1rem; border-radius: 8px;">
                <h4 style="color: #2E7D32; margin-bottom: 0.5rem;">💡 Respuesta:</h4>
                <p style="margin: 0;">{respuesta_hist}</p>
            </div>
            """, unsafe_allow_html=True)

# Botón para descargar conversación con diseño mejorado
if st.session_state.chat_history:
    st.markdown("""
    <div class="info-card" style="text-align: center; margin: 2rem 0;">
        <h3 style="color: #2E7D32; margin-bottom: 1rem;">📝 Descargar Conversación</h3>
        <p style="color: #666; margin-bottom: 1.5rem;">
            Guarda tus preguntas y respuestas para repasar conceptos, crear apuntes, 
            tener evidencia de estudio, compartir con compañeros, consultar offline 
            y preparar material para tu práctica profesional.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Descargar Conversación", use_container_width=True):
            chat_text = "\n\n".join([f"Pregunta: {p}\nRespuesta: {r}" for p, r in st.session_state.chat_history])
            st.download_button(
                label="📄 Descargar Chat",
                data=chat_text,
                file_name="chat_auxiliar_farmacia.txt",
                mime="text/plain",
                use_container_width=True
            ) 