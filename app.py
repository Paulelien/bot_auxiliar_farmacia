import streamlit as st
import json
import os
import sqlite3
from datetime import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Panel de Administración - Bot Farmacia",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏥 Panel de Administración - Bot Asistente Virtual de Farmacia")
st.markdown("---")

# Configuración de la base de datos
DB_PATH = "chatbot_analytics.db"

def init_db():
    """Inicializar la base de datos si no existe"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Crear tabla de sesiones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                user_agent TEXT,
                ip_address TEXT
            )
        ''')
        
        # Crear tabla de preguntas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                question TEXT,
                response TEXT,
                timestamp TIMESTAMP,
                response_time REAL,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            )
        ''')
        
        # Crear tabla de resultados de quiz
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                quiz_id INTEGER,
                score INTEGER,
                total_questions INTEGER,
                completion_time REAL,
                timestamp TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        st.success("✅ Base de datos inicializada correctamente")

def get_db_stats():
    """Obtener estadísticas de la base de datos"""
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Estadísticas de sesiones
        sessions_count = pd.read_sql_query("SELECT COUNT(*) as total FROM sessions", conn).iloc[0]['total']
        
        # Estadísticas de preguntas
        questions_count = pd.read_sql_query("SELECT COUNT(*) as total FROM questions", conn).iloc[0]['total']
        
        # Estadísticas de quiz
        quiz_count = pd.read_sql_query("SELECT COUNT(*) as total FROM quiz_results", conn).iloc[0]['total']
        
        # Última actividad
        last_activity = pd.read_sql_query("""
            SELECT MAX(timestamp) as last_activity FROM (
                SELECT timestamp FROM questions
                UNION ALL
                SELECT timestamp FROM quiz_results
            )
        """, conn).iloc[0]['last_activity']
        
        conn.close()
        
        return {
            'sessions': sessions_count,
            'questions': questions_count,
            'quiz_results': quiz_count,
            'last_activity': last_activity
        }
    except Exception as e:
        st.error(f"❌ Error obteniendo estadísticas: {e}")
        return None

def load_casos_clinicos():
    """Cargar casos clínicos desde archivo JSON"""
    try:
        if os.path.exists('casos_clinicos.json'):
            with open('casos_clinicos.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Casos clínicos por defecto
            return {
                "casos_clinicos": [
                    {
                        "id": 1,
                        "titulo": "Caso Clínico: Paciente con Hipertensión",
                        "descripcion": "María, 65 años, acude a la farmacia con una receta médica para tratar su hipertensión arterial. Presenta presión arterial de 160/95 mmHg y tiene antecedentes de diabetes tipo 2.",
                        "preguntas": [
                            {
                                "id": 1,
                                "pregunta": "¿Cuál de los siguientes medicamentos NO es un antihipertensivo?",
                                "opciones": [
                                    "A) Losartán",
                                    "B) Amlodipino", 
                                    "C) Paracetamol",
                                    "D) Enalapril"
                                ],
                                "respuesta_correcta": 2,
                                "explicacion": "El paracetamol es un analgésico y antipirético, no un antihipertensivo. Losartán, Amlodipino y Enalapril son medicamentos antihipertensivos."
                            },
                            {
                                "id": 2,
                                "pregunta": "¿Qué precaución especial debe tener María al tomar antihipertensivos?",
                                "opciones": [
                                    "A) Tomar con el estómago lleno",
                                    "B) Evitar cambios bruscos de posición",
                                    "C) Exponerse al sol sin protección",
                                    "D) Hacer ejercicio intenso inmediatamente"
                                ],
                                "respuesta_correcta": 1,
                                "explicacion": "Los antihipertensivos pueden causar hipotensión ortostática, por lo que se debe evitar levantarse bruscamente."
                            }
                        ]
                    }
                ]
            }
    except Exception as e:
        st.error(f"❌ Error cargando casos clínicos: {e}")
        return None

def save_casos_clinicos(casos):
    """Guardar casos clínicos en archivo JSON"""
    try:
        with open('casos_clinicos.json', 'w', encoding='utf-8') as f:
            json.dump(casos, f, ensure_ascii=False, indent=4)
        st.success("✅ Casos clínicos guardados correctamente")
        return True
    except Exception as e:
        st.error(f"❌ Error guardando casos clínicos: {e}")
        return False

def export_analytics():
    """Exportar analytics a CSV"""
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Exportar sesiones
        sessions_df = pd.read_sql_query("SELECT * FROM sessions", conn)
        sessions_df.to_csv("sessions_export.csv", index=False)
        
        # Exportar preguntas
        questions_df = pd.read_sql_query("SELECT * FROM questions", conn)
        questions_df.to_csv("questions_export.csv", index=False)
        
        # Exportar resultados de quiz
        quiz_df = pd.read_sql_query("SELECT * FROM quiz_results", conn)
        quiz_df.to_csv("quiz_results_export.csv", index=False)
        
        conn.close()
        
        st.success("✅ Analytics exportados a CSV correctamente")
        
        # Proporcionar enlaces de descarga
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with open("sessions_export.csv", "r") as f:
                st.download_button(
                    label="📥 Descargar Sesiones",
                    data=f.read(),
                    file_name="sessions_export.csv",
                    mime="text/csv"
                )
        
        with col2:
            with open("questions_export.csv", "r") as f:
                st.download_button(
                    label="📥 Descargar Preguntas",
                    data=f.read(),
                    file_name="questions_export.csv",
                    mime="text/csv"
                )
        
        with col3:
            with open("quiz_results_export.csv", "r") as f:
                st.download_button(
                    label="📥 Descargar Quiz",
                    data=f.read(),
                    file_name="quiz_results_export.csv",
                    mime="text/csv"
                )
                
    except Exception as e:
        st.error(f"❌ Error exportando analytics: {e}")

# Inicializar base de datos
init_db()

# Sidebar para navegación
st.sidebar.title("🧭 Navegación")
page = st.sidebar.selectbox(
    "Selecciona una sección:",
    ["📊 Dashboard", "📝 Casos Clínicos", "📁 Gestión de Materiales", "📈 Analytics", "⚙️ Configuración"]
)

# Página principal - Dashboard
if page == "📊 Dashboard":
    st.header("📊 Dashboard del Sistema")
    
    # Estadísticas principales
    stats = get_db_stats()
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Sesiones", stats['sessions'])
        
        with col2:
            st.metric("❓ Preguntas", stats['questions'])
        
        with col3:
            st.metric("📝 Quiz Completados", stats['quiz_results'])
        
        with col4:
            if stats['last_activity']:
                st.metric("🕒 Última Actividad", stats['last_activity'][:19])
            else:
                st.metric("🕒 Última Actividad", "N/A")
    
    # Estado del sistema
    st.subheader("🔍 Estado del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Verificar archivos esenciales
        st.write("**📁 Archivos del Sistema:**")
        
        essential_files = [
            ("api.py", "Backend FastAPI"),
            ("index.html", "Frontend Principal"),
            ("index_actualizado.html", "Frontend Alternativo"),
            ("prompt.txt", "Instrucciones del Bot"),
            ("requirements.txt", "Dependencias")
        ]
        
        for filename, description in essential_files:
            if os.path.exists(filename):
                st.success(f"✅ {filename} - {description}")
            else:
                st.error(f"❌ {filename} - {description}")
    
    with col2:
        # Verificar directorios
        st.write("**📂 Directorios del Sistema:**")
        
        directories = [
            ("material", "Materiales del Curso"),
            ("analytics_exportados", "Analytics Exportados")
        ]
        
        for dirname, description in directories:
            if os.path.exists(dirname):
                st.success(f"✅ {dirname}/ - {description}")
            else:
                st.error(f"❌ {dirname}/ - {description}")

# Página de Casos Clínicos
elif page == "📝 Casos Clínicos":
    st.header("📝 Gestión de Casos Clínicos")
    
    # Cargar casos existentes
    casos = load_casos_clinicos()
    
    if casos:
        st.subheader("📋 Casos Clínicos Existentes")
        
        for i, caso in enumerate(casos['casos_clinicos']):
            with st.expander(f"📚 {caso['titulo']} (ID: {caso['id']})"):
                st.write(f"**Descripción:** {caso['descripcion']}")
                st.write(f"**Preguntas:** {len(caso['preguntas'])}")
                
                # Mostrar preguntas
                for j, pregunta in enumerate(caso['preguntas']):
                    st.write(f"**Pregunta {j+1}:** {pregunta['pregunta']}")
                    st.write(f"**Respuesta correcta:** Opción {chr(65 + pregunta['respuesta_correcta'])}")
                    st.write(f"**Explicación:** {pregunta['explicacion']}")
                    st.write("---")
    
    # Agregar nuevo caso
    st.subheader("➕ Agregar Nuevo Caso Clínico")
    
    with st.form("nuevo_caso"):
        titulo = st.text_input("Título del caso:")
        descripcion = st.text_area("Descripción del caso:")
        
        if st.form_submit_button("Agregar Caso"):
            if titulo and descripcion:
                nuevo_caso = {
                    "id": len(casos['casos_clinicos']) + 1,
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "preguntas": []
                }
                
                casos['casos_clinicos'].append(nuevo_caso)
                
                if save_casos_clinicos(casos):
                    st.success("✅ Nuevo caso agregado correctamente")
                    st.rerun()

# Página de Gestión de Materiales
elif page == "📁 Gestión de Materiales":
    st.header("📁 Gestión de Materiales del Curso")
    
    # Verificar directorio de materiales
    if os.path.exists("material"):
        st.success("✅ Directorio de materiales encontrado")
        
        # Listar archivos en el directorio
        archivos = os.listdir("material")
        if archivos:
            st.subheader("📄 Archivos Disponibles:")
            for archivo in archivos:
                st.write(f"📎 {archivo}")
        else:
            st.warning("⚠️ El directorio de materiales está vacío")
    else:
        st.warning("⚠️ No se encontró el directorio de materiales")
        if st.button("Crear Directorio"):
            os.makedirs("material")
            st.success("✅ Directorio de materiales creado")
            st.rerun()
    
    # Subir archivos
    st.subheader("📤 Subir Nuevos Materiales")
    
    uploaded_files = st.file_uploader(
        "Selecciona archivos para subir:",
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write(f"📎 {uploaded_file.name}")
            
            # Guardar archivo
            if not os.path.exists("material"):
                os.makedirs("material")
            
            with open(os.path.join("material", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ {uploaded_file.name} subido correctamente")

# Página de Analytics
elif page == "📈 Analytics":
    st.header("📈 Analytics Detallados")
    
    # Exportar analytics
    st.subheader("📊 Exportar Datos")
    
    if st.button("📥 Exportar Analytics a CSV"):
        export_analytics()
    
    # Mostrar datos recientes
    st.subheader("📋 Datos Recientes")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Últimas preguntas
        st.write("**❓ Últimas Preguntas:**")
        recent_questions = pd.read_sql_query("""
            SELECT question, response, timestamp 
            FROM questions 
            ORDER BY timestamp DESC 
            LIMIT 10
        """, conn)
        
        if not recent_questions.empty:
            st.dataframe(recent_questions)
        else:
            st.info("ℹ️ No hay preguntas registradas")
        
        # Resultados de quiz recientes
        st.write("**📝 Últimos Resultados de Quiz:**")
        recent_quiz = pd.read_sql_query("""
            SELECT score, total_questions, completion_time, timestamp 
            FROM quiz_results 
            ORDER BY timestamp DESC 
            LIMIT 10
        """, conn)
        
        if not recent_quiz.empty:
            st.dataframe(recent_quiz)
        else:
            st.info("ℹ️ No hay resultados de quiz registrados")
        
        conn.close()
        
    except Exception as e:
        st.error(f"❌ Error cargando datos: {e}")

# Página de Configuración
elif page == "⚙️ Configuración":
    st.header("⚙️ Configuración del Sistema")
    
    st.subheader("🔧 Configuración del Bot")
    
    # Verificar archivo de prompt
    if os.path.exists("prompt.txt"):
        st.success("✅ Archivo de prompt encontrado")
        
        with open("prompt.txt", "r", encoding="utf-8") as f:
            prompt_content = f.read()
        
        st.subheader("📝 Editar Prompt del Bot")
        
        edited_prompt = st.text_area(
            "Prompt del bot:",
            value=prompt_content,
            height=400
        )
        
        if st.button("💾 Guardar Cambios"):
            try:
                with open("prompt.txt", "w", encoding="utf-8") as f:
                    f.write(edited_prompt)
                st.success("✅ Prompt actualizado correctamente")
            except Exception as e:
                st.error(f"❌ Error guardando prompt: {e}")
    else:
        st.error("❌ No se encontró el archivo prompt.txt")
    
    st.subheader("🗄️ Base de Datos")
    
    if st.button("🔄 Reinicializar Base de Datos"):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            st.success("✅ Base de datos eliminada")
            init_db()
            st.rerun()
        else:
            st.info("ℹ️ No hay base de datos para reinicializar")

# Footer
st.markdown("---")
st.markdown("**🏥 Panel de Administración - Bot Asistente Virtual de Farmacia**")
st.markdown("*Desarrollado para el curso de Auxiliar de Farmacia*")

