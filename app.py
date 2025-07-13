import streamlit as st
import os
from faq import buscar_en_faq
from embedding_utils import cargar_o_crear_indice, buscar_similares
from openai import OpenAI
from dotenv import load_dotenv
import random
import re
import difflib

# Configuración de la página
st.set_page_config(
    page_title="ChatBot Auxiliar de Farmacia",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta de colores Avanxa (morado institucional)
COLORES = {
    'primario': '#4B2067',      # Morado oscuro institucional Avanxa
    'secundario': '#7C3FAF',    # Morado claro
    'acento': '#FF6B35',        # Naranja para alertas
    'texto': '#2C3E50',         # Azul oscuro
    'fondo': '#F8F9FA'          # Gris muy claro
}

# Aplicar estilos CSS personalizados con la nueva paleta
st.markdown(f"""
<style>
:root {{
    --color-primario: {COLORES['primario']};
    --color-secundario: {COLORES['secundario']};
    --color-acento: {COLORES['acento']};
    --color-texto: {COLORES['texto']};
    --color-fondo: {COLORES['fondo']};
}}

.stApp {{
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

.main-header {{
    background: linear-gradient(90deg, {COLORES['primario']} 0%, {COLORES['secundario']} 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(76, 31, 103, 0.3);
    text-align: center;
}}

.info-card {{
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-left: 4px solid {COLORES['secundario']};
    transition: transform 0.2s ease;
}}

.info-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}}

.stButton > button {{
    background: linear-gradient(90deg, {COLORES['primario']} 0%, {COLORES['secundario']} 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(76, 31, 103, 0.3);
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(76, 31, 103, 0.4);
    background: linear-gradient(90deg, #2C1040 0%, {COLORES['primario']} 100%);
}}

.stTextInput > div > div > input {{
    border-radius: 25px;
    border: 2px solid #E9ECEF;
    padding: 1rem 1.5rem;
    font-size: 16px;
    transition: all 0.3s ease;
}}

.stTextInput > div > div > input:focus {{
    border-color: {COLORES['secundario']};
    box-shadow: 0 0 0 3px rgba(124, 63, 175, 0.1);
}}

.sidebar .sidebar-content {{
    background: linear-gradient(180deg, {COLORES['primario']} 0%, {COLORES['secundario']} 100%);
    color: white;
}}

.streamlit-expanderHeader {{
    background: linear-gradient(90deg, {COLORES['secundario']} 0%, #A084CA 100%);
    color: white;
    border-radius: 8px;
    font-weight: 600;
}}

.stSuccess {{
    background: linear-gradient(90deg, {COLORES['secundario']} 0%, #A084CA 100%);
    color: white;
    border-radius: 12px;
    padding: 1rem;
    border-left: 4px solid {COLORES['primario']};
}}

.stError {{
    background: linear-gradient(90deg, #F44336 0%, #EF5350 100%);
    color: white;
    border-radius: 12px;
    padding: 1rem;
    border-left: 4px solid #D32F2F;
}}

.chat-container {{
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    margin: 2rem 0;
    border: 3px solid #4B2067; /* Morado institucional Avanxa */
}}

.chat-history {{
    background: #F8F9FA;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid #E9ECEF;
}}

.emoji-icon {{
    font-size: 1.5rem;
    margin-right: 0.5rem;
}}

@media (max-width: 768px) {{
    .main-header {{
        padding: 1rem;
        margin-bottom: 1rem;
    }}
    .info-card {{
        padding: 1rem;
        margin: 0.5rem 0;
    }}
    .chat-container {{
        padding: 1rem;
        margin: 1rem 0;
    }}
}}
</style>
""", unsafe_allow_html=True)

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Header con la nueva paleta
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo_avanxa.png", use_container_width=True)
    st.markdown("---")

st.markdown(f"""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">Chatbot Auxiliar de Farmacia</h1>
    <p style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Asistente educativo inteligente para el curso de Auxiliar de Farmacia</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con información y guía
with st.sidebar:
    st.header("Información y Ayuda")
    with st.expander("Como usar el bot"):
        st.markdown("""
        1. Escribe tu pregunta en el campo de texto.
        2. Presiona 'Preguntar' o Enter.
        3. Recibirás una respuesta basada en el material del curso.
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

# Botón destacado para Información y Ayuda
st.markdown('<div style="display: flex; justify-content: center; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
if st.button('ℹ️ Ver Información y Ayuda', key='info_ayuda_btn', use_container_width=False):
    st.info('La sección **Información y Ayuda** se encuentra en el menú lateral izquierdo. Haz clic en el ícono de menú (☰) si no la ves.')
st.markdown('</div>', unsafe_allow_html=True)

# --- PREGUNTAS SUGERIDAS DINÁMICAS ---

# Función para extraer preguntas del material
@st.cache_resource(show_spinner="Extrayendo preguntas sugeridas del material...")
def extraer_preguntas_sugeridas():
    preguntas = []
    ruta = os.path.join(CARPETA_MATERIAL, "preguntas_tipo.txt")
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if linea.startswith('¿') and linea.endswith('?'):
                    preguntas.append(linea)
    return preguntas

PREGUNTAS_MATERIALES = extraer_preguntas_sugeridas()

# Inicializar preguntas sugeridas en el estado de sesión
if 'preguntas_sugeridas' not in st.session_state or st.session_state.get('forzar_nuevas_preguntas', False):
    st.session_state.preguntas_sugeridas = random.sample(PREGUNTAS_MATERIALES, k=min(4, len(PREGUNTAS_MATERIALES)))
    st.session_state.forzar_nuevas_preguntas = False

# --- INTERACCIÓN NATURAL ---

# Script para autofoco y scroll al input cuando cambia el valor
st.markdown('''
<script>
window.addEventListener('DOMContentLoaded', function() {
    const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
    if (input) { input.focus(); }
});
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'focusInput') {
        const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
        if (input) { input.focus(); input.scrollIntoView({behavior: 'smooth', block: 'center'}); }
    }
});
</script>
''', unsafe_allow_html=True)

# Mostrar sección de preguntas sugeridas con botones Streamlit estilizados y confirmación visual
st.markdown("""
<div class="chat-container">
    <h3 style="color: #4B2067; margin-bottom: 1.5rem; text-align:center;">🤔 Preguntas sugeridas</h3>
</div>
""", unsafe_allow_html=True)

if 'pregunta_sugerida_idx' not in st.session_state:
    st.session_state.pregunta_sugerida_idx = None

for i, pregunta_sug in enumerate(st.session_state.preguntas_sugeridas):
    btn_color = '#7C3FAF' if st.session_state.pregunta_sugerida_idx != i else '#4B2067'
    if st.button(pregunta_sug, key=f"preg_sug_{i}", help="Haz clic para rellenar la pregunta abajo"):
        st.session_state["chat_input"] = pregunta_sug
        st.session_state.pregunta_sugerida_idx = i
        # Enviar mensaje JS para enfocar y hacer scroll al input
        st.components.v1.html("""
        <script>
        window.parent.postMessage({type: 'focusInput'}, '*');
        </script>
        """, height=0)
    st.markdown(f'''<style>button[data-testid="baseButton-preg_sug_{i}"] {{background: {btn_color} !important;}}</style>''', unsafe_allow_html=True)

# Botón para cambiar preguntas sugeridas, centrado y estilizado
st.markdown('<div style="display: flex; justify-content: center; margin-top: 1.5rem;">', unsafe_allow_html=True)
def cambiar_preguntas():
    st.session_state.forzar_nuevas_preguntas = True
st.button("Cambiar preguntas", on_click=cambiar_preguntas, use_container_width=False, key="cambiar_preguntas_btn", help="Muestra nuevas preguntas sugeridas")
st.markdown('</div>', unsafe_allow_html=True)

# --- Lógica para enviar pregunta con botón o Enter ---
def enviar_pregunta():
    pregunta = st.session_state.get('chat_input', '').strip()
    if not pregunta:
        st.warning("⚠️ Por favor, escribe una pregunta antes de presionar 'Preguntar'", icon="⚠️")
        return
    st.session_state.pregunta_anterior = pregunta
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
Eres un asistente educativo experto en farmacia y normativa sanitaria chilena. Estás diseñado para apoyar a estudiantes que están preparando el examen oficial de la SEREMI de Salud de Chile, requerido para obtener la autorización como Auxiliar de Farmacia.

⚠️ IMPORTANTE: Este curso no otorga por sí solo la habilitación legal para ejercer como auxiliar de farmacia.  
El estudiante debe cumplir con los requisitos legales establecidos por la autoridad sanitaria y aprobar el examen correspondiente. No afirmes ni sugieras lo contrario.

🎯 Tu objetivo es guiar al estudiante en el aprendizaje de los contenidos del curso y facilitar la comprensión de la normativa aplicable, sin reemplazar la consulta formal de los decretos ni la asesoría del tutor académico.

---

📘 CONTENIDOS DEL CURSO

El curso está dividido en tres grandes áreas temáticas:

1. **Tecnología Farmacéutica**  
   - Formas farmacéuticas  
   - Vías de administración  
   - Técnicas de acondicionamiento y dispensación  
   - Buenas prácticas de almacenamiento  

2. **Legislación Farmacéutica**  
   - Decretos relevantes: Decreto 466, Decreto 405, Decreto 38, Decreto 3, entre otros  
   - Funciones y limitaciones del auxiliar de farmacia  
   - Trazabilidad, control y normas de seguridad sanitaria  

3. **Arsenal Farmacoterapéutico**  
   - Clasificación general de medicamentos  
   - Grupos terapéuticos según el Vademécum chileno  
   - Principios activos y sus usos más comunes  
   - Condiciones de conservación y dispensación  

---

📑 FUENTES AUTORIZADAS

Responde únicamente en base a:

- Documentos oficiales cargados al sistema (decretos, guías, normativa)  
- Contenidos del curso  
- Vademécum Chile (https://www.vademecum.es/chile/cl/alfa), **solo si la consulta es específica sobre**:
  - Principio activo  
  - Dosis  
  - Grupo terapéutico  
  - Clasificación ATC  

No uses conocimiento general del modelo. Si la información no está en los documentos, responde lo siguiente:

> "La información solicitada no se encuentra en los documentos disponibles. Te recomiendo comunicarte con tu tutor académico a través del apartado *Consultas Académicas* en el menú superior de la plataforma."

---

🔐 REGLAS DE RESPUESTA

- No inventes información.

- No completes con inferencias, intuiciones ni suposiciones.
- No confundas artículos con decretos.
- No atribuyas atribuciones legales al auxiliar de farmacia si no están explícitamente descritas en la normativa cargada.
- Si la pregunta es legal o administrativa y no tienes la información documentada, redirige al estudiante al tutor académico o a www.leychile.cl.
- Si no tienes información suficiente, responde de forma general o sugiere consultar fuentes oficiales o al tutor académico.

---

🎓 ENFOQUE PEDAGÓGICO

- Usa un lenguaje claro, técnico pero comprensible.  
- Responde con precisión, brevedad y foco en el aprendizaje del examen.  
- Si hay pasos o procedimientos relevantes en la normativa (por ejemplo, condiciones de almacenamiento, criterios de dispensación o restricción), descríbelos tal como se indican en la fuente.


📌 Preguntas sobre atribuciones legales:

Nunca respondas que el curso habilita al estudiante a ejercer como auxiliar. Si se pregunta sobre acreditación, certificación o legalidad para trabajar, responde:

“La información que solicitas no se encuentra en los documentos disponibles. Por favor, consulta con tu tutor académico.”





"""







Pregunta: {pregunta}
Contexto:
{contexto}
"""
    with st.spinner("Pensando..."):
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
            # Animación de fade-in para la respuesta
            st.markdown(
                f'<div style="animation: fadein 1s;">{respuesta_final}</div>'
                '<style>@keyframes fadein {{from {{opacity: 0;}} to {{opacity: 1;}}}}</style>',
                unsafe_allow_html=True
            )
            st.session_state.chat_history.append((pregunta, respuesta_final))
        except Exception as e:
            st.error(f"Error al consultar OpenAI: {e}")

# Chat al final del panel con diseño mejorado
st.markdown("""
<div class="chat-container">
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #4B2067; margin-bottom: 0.5rem;">Haz tus preguntas en el espacio abajo 👇</h2>
        <p style="color: #666; font-size: 1.1rem; margin: 0;">Escribe tu pregunta sobre el curso de Auxiliar de Farmacia</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.text_input(
    "Escribe tu pregunta",
    placeholder="Ej: ¿Qué es el principio FEFO?",
    value=st.session_state.get('chat_input', ''),
    label_visibility="collapsed",
    key="chat_input",
    on_change=enviar_pregunta
)

if st.button("Preguntar", help="Haz clic o presiona Enter para enviar tu pregunta"):
    enviar_pregunta()

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

# --- QUIZ DE OPCIONES MÚLTIPLES ---

# Función mejorada para extraer preguntas, respuestas y módulo/tema
@st.cache_resource(show_spinner="Cargando preguntas de quiz...")
def extraer_preguntas_respuestas_modulo():
    preguntas = []
    ruta = os.path.join(CARPETA_MATERIAL, "preguntas_tipo.txt")
    modulo_actual = "General"
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        pregunta = None
        respuesta = None
        for i, linea in enumerate(lines):
            linea = linea.strip()
            if linea.upper().startswith('MÓDULO'):
                modulo_actual = linea
            if linea.startswith('¿') and linea.endswith('?'):
                pregunta = linea
            if linea.lower().startswith('respuesta:') and pregunta:
                respuesta = linea.split(':', 1)[1].strip()
                preguntas.append({'pregunta': pregunta, 'respuesta': respuesta, 'modulo': modulo_actual})
                pregunta = None
                respuesta = None
    return preguntas

PREGUNTAS_QUIZ = extraer_preguntas_respuestas_modulo()

# Función mejorada para generar distractores relacionados
def generar_opciones(pregunta_idx, preguntas, n_opciones=4):
    correcta = preguntas[pregunta_idx]['respuesta']
    modulo = preguntas[pregunta_idx]['modulo']
    # Buscar distractores del mismo módulo
    distractores_modulo = [p['respuesta'] for i, p in enumerate(preguntas)
                           if i != pregunta_idx and p['modulo'] == modulo and p['respuesta']]
    # Si hay menos de 3, buscar por similitud de palabras clave
    if len(distractores_modulo) < n_opciones-1:
        # Buscar distractores con palabras clave similares
        pregunta_base = preguntas[pregunta_idx]['pregunta']
        palabras_base = set(pregunta_base.lower().replace('¿','').replace('?','').split())
        distractores_similares = [p['respuesta'] for i, p in enumerate(preguntas)
                                 if i != pregunta_idx and p['respuesta'] and len(palabras_base.intersection(set(p['pregunta'].lower().split()))) > 0]
        distractores = list(set(distractores_modulo + distractores_similares))
    else:
        distractores = distractores_modulo
    # Si aún faltan, completar con aleatorios
    if len(distractores) < n_opciones-1:
        otros = [p['respuesta'] for i, p in enumerate(preguntas) if i != pregunta_idx and p['respuesta'] and p['respuesta'] not in distractores]
        distractores += random.sample(otros, k=min(n_opciones-1-len(distractores), len(otros)))
    distractores = distractores[:n_opciones-1]
    opciones = distractores + [correcta]
    random.shuffle(opciones)
    return opciones, correcta

# Sección de Quiz
st.markdown("""
<div class="chat-container">
    <h3 style="color: #4B2067; margin-bottom: 1.5rem; text-align:center;">📝 Quiz de Auxiliar de Farmacia</h3>
</div>
""", unsafe_allow_html=True)

if 'quiz_activo' not in st.session_state:
    st.session_state.quiz_activo = False
if 'quiz_puntaje' not in st.session_state:
    st.session_state.quiz_puntaje = 0
if 'quiz_pregunta_actual' not in st.session_state:
    st.session_state.quiz_pregunta_actual = 0
if 'quiz_preguntas_orden' not in st.session_state:
    st.session_state.quiz_preguntas_orden = []
if 'quiz_opcion_seleccionada' not in st.session_state:
    st.session_state.quiz_opcion_seleccionada = None
if 'quiz_feedback' not in st.session_state:
    st.session_state.quiz_feedback = ''
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 5

# Botón para iniciar quiz y seleccionar cantidad de preguntas
if not st.session_state.quiz_activo:
    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
    st.session_state.quiz_total = st.slider("¿Cuántas preguntas quieres responder?", min_value=3, max_value=min(15, len(PREGUNTAS_QUIZ)), value=5)
    if st.button("Iniciar Quiz", key="iniciar_quiz_btn"):
        st.session_state.quiz_activo = True
        st.session_state.quiz_puntaje = 0
        st.session_state.quiz_pregunta_actual = 0
        st.session_state.quiz_feedback = ''
        st.session_state.quiz_opcion_seleccionada = None
        st.session_state.quiz_preguntas_orden = random.sample(range(len(PREGUNTAS_QUIZ)), k=st.session_state.quiz_total)
    st.markdown('</div>', unsafe_allow_html=True)

# Mostrar preguntas del quiz
if st.session_state.quiz_activo and st.session_state.quiz_pregunta_actual < st.session_state.quiz_total:
    idx = st.session_state.quiz_preguntas_orden[st.session_state.quiz_pregunta_actual]
    pregunta = PREGUNTAS_QUIZ[idx]['pregunta']
    opciones, correcta = generar_opciones(idx, PREGUNTAS_QUIZ)
    st.markdown(f'<div style="margin-bottom:1rem; font-weight:600; color:#4B2067;">Pregunta {st.session_state.quiz_pregunta_actual+1} de {st.session_state.quiz_total}:</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="margin-bottom:1.2rem; font-size:1.1rem;">{pregunta}</div>', unsafe_allow_html=True)
    opcion = st.radio("Selecciona una opción:", opciones, key=f"quiz_radio_{st.session_state.quiz_pregunta_actual}")
    if 'quiz_respondida' not in st.session_state:
        st.session_state.quiz_respondida = False
    if st.button("Responder", key=f"quiz_responder_{st.session_state.quiz_pregunta_actual}") and not st.session_state.quiz_respondida:
        st.session_state.quiz_opcion_seleccionada = opcion
        st.session_state.quiz_respondida = True
        if opcion == correcta:
            st.session_state.quiz_puntaje += 1
            st.session_state.quiz_feedback = '✅ ¡Correcto!'
        else:
            st.session_state.quiz_feedback = f'❌ Incorrecto. La respuesta correcta era: {correcta}'
    if st.session_state.quiz_respondida:
        st.info(st.session_state.quiz_feedback)
        if st.button("Siguiente pregunta", key=f"quiz_siguiente_{st.session_state.quiz_pregunta_actual}"):
            st.session_state.quiz_pregunta_actual += 1
            st.session_state.quiz_opcion_seleccionada = None
            st.session_state.quiz_feedback = ''
            st.session_state.quiz_respondida = False

# Mostrar resultado final
if st.session_state.quiz_activo and st.session_state.quiz_pregunta_actual >= st.session_state.quiz_total:
    st.success(f'¡Quiz finalizado! Puntaje: {st.session_state.quiz_puntaje} de {st.session_state.quiz_total}')
    if st.button("Reiniciar Quiz", key="quiz_reiniciar"):
        st.session_state.quiz_activo = False
        st.session_state.quiz_puntaje = 0
        st.session_state.quiz_pregunta_actual = 0
        st.session_state.quiz_feedback = ''
        st.session_state.quiz_opcion_seleccionada = None
        st.session_state.quiz_preguntas_orden = [] 