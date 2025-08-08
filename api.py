from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from embedding_utils import buscar_similares, cargar_o_crear_indice
import random
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from database_config import get_db
from models import Estudiante, Sesion, Pregunta, ResultadoQuiz

# Configuración
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Validar que la API key esté configurada
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY no está configurada. "
        "Por favor, configura la variable de entorno OPENAI_API_KEY en Render."
    )

client = OpenAI(api_key=api_key)

CARPETA_MATERIAL = "material"

# Importar configuración de umbrales
from config import UMBRAL_SIMILITUD_PRINCIPAL, UMBRAL_SIMILITUD_SECUNDARIO

# Estadísticas de uso
estadisticas_uso = {
    "preguntas_totales": 0,
    "preguntas_por_categoria": {},
    "preguntas_frecuentes": {},
    "ultima_actualizacion": None
}

# Cargar el índice y textos del material
indice, textos = cargar_o_crear_indice([])

# Inicialización para Render
print("🚀 Inicializando sistema...")
try:
    from inicializar_render import inicializar_render
    if inicializar_render():
        print("✅ Sistema inicializado correctamente")
        # Recargar el índice después de la inicialización
        indice, textos = cargar_o_crear_indice([])
    else:
        print("⚠️ Problema en la inicialización, continuando con configuración actual")
except Exception as e:
    print(f"⚠️ Error en inicialización: {e}, continuando con configuración actual")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS ---
class PreguntaRequest(BaseModel):
    pregunta: str

class EstudianteRequest(BaseModel):
    nombre: str
    email: str
    grupo: str = "General"

class QuizResultRequest(BaseModel):
    estudiante_id: int
    puntaje: int
    preguntas_correctas: int
    total_preguntas: int
    tiempo_completado_minutos: int

# --- PREGUNTAS SUGERIDAS ---
PREGUNTAS_SUGERIDAS = [
    "¿Cuáles son las funciones del auxiliar de farmacia?",
    "¿Qué es el Decreto 405?",
    "¿Cómo se almacenan los medicamentos termolábiles?",
    "¿Qué son los psicotrópicos?",
    "¿Cuáles son las formas farmacéuticas más comunes?",
    "¿Qué es la cadena de frío?",
    "¿Cómo se debe atender al cliente en una farmacia?",
    "¿Qué es el Decreto 79?",
    "¿Qué son los medicamentos de venta libre?"
]

# --- PREGUNTAS DE QUIZ ---
PREGUNTAS_QUIZ = [
    {
        "pregunta": "¿Cuál es la función principal del auxiliar de farmacia?",
        "opciones": [
            "Vender medicamentos sin receta",
            "Asistir al farmacéutico en la dispensación y venta de medicamentos",
            "Recetar medicamentos",
            "Realizar diagnósticos médicos"
        ],
        "correcta": "Asistir al farmacéutico en la dispensación y venta de medicamentos"
    },
    {
        "pregunta": "¿Qué establece el Decreto 405?",
        "opciones": [
            "Reglamento de farmacias",
            "Control de psicotrópicos y estupefacientes",
            "Venta de medicamentos",
            "Almacenamiento de productos"
        ],
        "correcta": "Control de psicotrópicos y estupefacientes"
    },
    {
        "pregunta": "¿A qué temperatura se deben almacenar los medicamentos termolábiles?",
        "opciones": [
            "Entre 2°C y 8°C",
            "A temperatura ambiente",
            "En congelador",
            "Al sol"
        ],
        "correcta": "Entre 2°C y 8°C"
    },
    {
        "pregunta": "¿Qué son los medicamentos de venta libre?",
        "opciones": [
            "Medicamentos que requieren receta médica",
            "Medicamentos que se pueden vender sin receta",
            "Medicamentos controlados",
            "Medicamentos psicotrópicos"
        ],
        "correcta": "Medicamentos que se pueden vender sin receta"
    },
    {
        "pregunta": "¿Qué documento regula la dispensación de psicotrópicos en Chile?",
        "opciones": [
            "Decreto 405",
            "Decreto 79",
            "Decreto 466",
            "Ley 20.000"
        ],
        "correcta": "Decreto 405"
    },
    {
        "pregunta": "¿Cuál es la temperatura recomendada para la cadena de frío?",
        "opciones": [
            "Entre 2°C y 8°C",
            "Entre 15°C y 25°C",
            "Menos de 0°C",
            "Más de 30°C"
        ],
        "correcta": "Entre 2°C y 8°C"
    },
    {
        "pregunta": "¿Qué debe hacer el auxiliar si un cliente presenta una receta ilegible?",
        "opciones": [
            "Interpretarla como pueda",
            "Consultar al farmacéutico o al médico que la emitió",
            "Entregar cualquier medicamento",
            "No entregar nada y guardar la receta"
        ],
        "correcta": "Consultar al farmacéutico o al médico que la emitió"
    },
    {
        "pregunta": "¿Cuál de las siguientes es una forma farmacéutica sólida?",
        "opciones": [
            "Jarabe",
            "Comprimido",
            "Solución",
            "Suspensión"
        ],
        "correcta": "Comprimido"
    },
    {
        "pregunta": "¿Qué es la farmacovigilancia?",
        "opciones": [
            "El estudio de la cadena de frío",
            "La vigilancia de los efectos adversos de los medicamentos",
            "El control de inventario en farmacia",
            "La venta de medicamentos sin receta"
        ],
        "correcta": "La vigilancia de los efectos adversos de los medicamentos"
    },
    {
        "pregunta": "¿Qué valor es fundamental en la ética profesional del auxiliar de farmacia?",
        "opciones": [
            "La confidencialidad",
            "La rapidez",
            "La simpatía",
            "La creatividad"
        ],
        "correcta": "La confidencialidad"
    },
    {
        "pregunta": "¿Qué debe hacer el auxiliar si detecta un medicamento vencido en el stock?",
        "opciones": [
            "Venderlo rápidamente",
            "Retirarlo del stock y notificar al responsable",
            "Mezclarlo con otros medicamentos",
            "Ignorarlo"
        ],
        "correcta": "Retirarlo del stock y notificar al responsable"
    },
    {
        "pregunta": "¿Cuál es el objetivo principal de la cadena de frío en farmacia?",
        "opciones": [
            "Evitar robos",
            "Mantener la potencia y seguridad de los medicamentos termolábiles",
            "Reducir costos",
            "Aumentar la venta"
        ],
        "correcta": "Mantener la potencia y seguridad de los medicamentos termolábiles"
    },
    {
        "pregunta": "¿Qué significa ATC en el contexto farmacéutico?",
        "opciones": [
            "Análisis Técnico de Cadena",
            "Clasificación Anatómica, Terapéutica y Química",
            "Atención Total al Cliente",
            "Almacenamiento Técnico de Cadena"
        ],
        "correcta": "Clasificación Anatómica, Terapéutica y Química"
    },
    {
        "pregunta": "¿Qué debe hacer el auxiliar si un cliente solicita información sobre un medicamento que no conoce?",
        "opciones": [
            "Inventar una respuesta",
            "Consultar fuentes oficiales o al farmacéutico",
            "Decir que no sabe y no ayudar",
            "Vender el medicamento igual"
        ],
        "correcta": "Consultar fuentes oficiales o al farmacéutico"
    },
    {
        "pregunta": "¿Cuál es la principal función del Decreto 79?",
        "opciones": [
            "Regular la venta de psicotrópicos",
            "Normar los recetarios farmacéuticos",
            "Controlar la temperatura de almacenamiento",
            "Definir la ética profesional"
        ],
        "correcta": "Normar los recetarios farmacéuticos"
    }
]

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "API del Chatbot Auxiliar de Farmacia"}

@app.get("/preguntas_sugeridas")
def obtener_preguntas_sugeridas():
    return {"preguntas": random.sample(PREGUNTAS_SUGERIDAS, k=4)}

@app.get("/quiz_pregunta")
def obtener_pregunta_quiz():
    pregunta = random.choice(PREGUNTAS_QUIZ)
    return pregunta

@app.get("/quiz_preguntas/{cantidad}")
def obtener_preguntas_quiz(cantidad: int = 7):
    if cantidad > len(PREGUNTAS_QUIZ):
        cantidad = len(PREGUNTAS_QUIZ)
    preguntas = random.sample(PREGUNTAS_QUIZ, k=cantidad)
    return {"preguntas": preguntas}

@app.get("/preguntas_frecuentes")
def obtener_preguntas_frecuentes():
    """Endpoint para obtener reporte de preguntas más frecuentes"""
    # Si no hay datos reales, mostrar datos de ejemplo
    if estadisticas_uso["preguntas_totales"] == 0:
        return {
            "preguntas_frecuentes": [
                {
                    "pregunta": "¿Cuáles son las funciones del auxiliar de farmacia?",
                    "frecuencia": 85,
                    "categoria": "Funciones"
                },
                {
                    "pregunta": "¿Qué es el Decreto 405?",
                    "frecuencia": 72,
                    "categoria": "Normativas"
                },
                {
                    "pregunta": "¿Cómo se almacenan los medicamentos termolábiles?",
                    "frecuencia": 68,
                    "categoria": "Almacenamiento"
                },
                {
                    "pregunta": "¿Qué son los psicotrópicos?",
                    "frecuencia": 65,
                    "categoria": "Medicamentos"
                },
                {
                    "pregunta": "¿Cuáles son las formas farmacéuticas más comunes?",
                    "frecuencia": 58,
                    "categoria": "Farmacología"
                },
                {
                    "pregunta": "¿Qué es la cadena de frío?",
                    "frecuencia": 55,
                    "categoria": "Almacenamiento"
                },
                {
                    "pregunta": "¿Cómo se debe atender al cliente en una farmacia?",
                    "frecuencia": 52,
                    "categoria": "Atención al cliente"
                },
                {
                    "pregunta": "¿Qué es el Decreto 79?",
                    "frecuencia": 48,
                    "categoria": "Normativas"
                }
            ],
            "categorias_populares": [
                {"categoria": "Funciones", "total": 85},
                {"categoria": "Normativas", "total": 120},
                {"categoria": "Almacenamiento", "total": 123},
                {"categoria": "Medicamentos", "total": 65},
                {"categoria": "Farmacología", "total": 58},
                {"categoria": "Atención al cliente", "total": 52}
            ],
            "es_ejemplo": True
        }
    
    # Si hay datos reales, procesarlos
    preguntas_frecuentes = []
    for pregunta, datos in estadisticas_uso["preguntas_frecuentes"].items():
        preguntas_frecuentes.append({
            "pregunta": pregunta,
            "frecuencia": datos["contador"],
            "categoria": datos["categoria"]
        })
    
    # Ordenar por frecuencia
    preguntas_frecuentes.sort(key=lambda x: x["frecuencia"], reverse=True)
    
    # Procesar categorías
    categorias_populares = []
    for categoria, total in estadisticas_uso["preguntas_por_categoria"].items():
        categorias_populares.append({
            "categoria": categoria,
            "total": total
        })
    
    categorias_populares.sort(key=lambda x: x["total"], reverse=True)
    
    return {
        "preguntas_frecuentes": preguntas_frecuentes[:8],  # Top 8
        "categorias_populares": categorias_populares,
        "preguntas_totales": estadisticas_uso["preguntas_totales"],
        "es_ejemplo": False
    }

def detectar_categoria(pregunta):
    """Detecta la categoría de una pregunta basada en palabras clave"""
    pregunta_lower = pregunta.lower()
    
    categorias = {
        "Funciones": ["función", "funciones", "auxiliar", "trabajo", "responsabilidad"],
        "Normativas": ["decreto", "ley", "reglamento", "norma", "405", "79", "466"],
        "Almacenamiento": ["almacenar", "cadena de frío", "temperatura", "refrigeración", "conservación"],
        "Medicamentos": ["medicamento", "psicotrópico", "estupefaciente", "controlado", "receta"],
        "Farmacología": ["forma farmacéutica", "comprimido", "jarabe", "cápsula", "farmacología"],
        "Atención al cliente": ["cliente", "paciente", "atención", "servicio", "atender"]
    }
    
    for categoria, palabras_clave in categorias.items():
        for palabra in palabras_clave:
            if palabra in pregunta_lower:
                return categoria
    
    return "General"

@app.post("/preguntar")
def preguntar(req: PreguntaRequest):
    pregunta = req.pregunta.strip()
    if not pregunta:
        return {"respuesta": "Por favor, escribe una pregunta válida."}
    
    # Actualizar estadísticas
    estadisticas_uso["preguntas_totales"] += 1
    categoria = detectar_categoria(pregunta)
    
    # Actualizar contador por categoría
    if categoria in estadisticas_uso["preguntas_por_categoria"]:
        estadisticas_uso["preguntas_por_categoria"][categoria] += 1
    else:
        estadisticas_uso["preguntas_por_categoria"][categoria] = 1
    
    # Actualizar preguntas frecuentes
    if pregunta in estadisticas_uso["preguntas_frecuentes"]:
        estadisticas_uso["preguntas_frecuentes"][pregunta]["contador"] += 1
    else:
        estadisticas_uso["preguntas_frecuentes"][pregunta] = {
            "contador": 1,
            "categoria": categoria
        }
    
    estadisticas_uso["ultima_actualizacion"] = str(datetime.now())
    # Buscar contexto relevante con umbral alto de similitud
    
    resultados = buscar_similares(pregunta, indice, textos, k=3, umbral=UMBRAL_SIMILITUD_PRINCIPAL)
    contexto_partes = []
    
    if not resultados:
        # Si no hay resultados con umbral alto, buscar con umbral más bajo
        print("No se encontraron resultados con umbral alto, buscando con umbral más bajo...")
        resultados = buscar_similares(pregunta, indice, textos, k=3, umbral=UMBRAL_SIMILITUD_SECUNDARIO)
    
    for r in resultados:
        if isinstance(r, dict) and 'texto' in r:
            archivo = r.get('archivo', 'Desconocido')
            pagina = r.get('pagina', 'N/A')
            texto = r['texto']
            similitud = r.get('similitud', 'N/A')
            contexto_partes.append(f"[{archivo} - Página {pagina} - Similitud: {similitud:.3f}]\n{texto}")
        elif isinstance(r, str):
            contexto_partes.append(r)
    
    contexto = "\n".join(contexto_partes)
    
    # Si no hay contexto relevante, continuar con respuesta genérica
    if not contexto_partes:
        contexto = "No se encontró información específica en los documentos del curso."
    # Cargar el prompt desde el archivo de texto
    try:
        with open('prompt.txt', 'r', encoding='utf-8') as f:
            prompt_base = f.read()
    except FileNotFoundError:
        # Fallback si no se encuentra el archivo
        prompt_base = "Eres un asistente educativo experto en farmacia y normativa sanitaria chilena."
    
    prompt = f"{prompt_base}\n\nPregunta: {pregunta}\nContexto:\n{contexto}"
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
        return {"respuesta": respuesta_final}
    except Exception as e:
        return {"respuesta": f"Error al consultar OpenAI: {e}"}

# --- ENDPOINTS DE ANALYTICS ---

@app.post("/init_db")
def initialize_database():
    """Inicializar base de datos desde la API"""
    try:
        from init_db import init_database, create_sample_data
        
        # Inicializar base de datos
        init_database()
        
        # Crear datos de ejemplo
        create_sample_data()
        
        return {"mensaje": "Base de datos inicializada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inicializando base de datos: {str(e)}")

@app.post("/estudiantes/registrar")
def registrar_estudiante(estudiante: EstudianteRequest, db: Session = Depends(get_db)):
    """Registrar un nuevo estudiante"""
    try:
        nuevo_estudiante = Estudiante(
            nombre=estudiante.nombre,
            email=estudiante.email,
            grupo=estudiante.grupo
        )
        db.add(nuevo_estudiante)
        db.commit()
        db.refresh(nuevo_estudiante)
        return {"id": nuevo_estudiante.id, "mensaje": "Estudiante registrado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sesiones/iniciar")
def iniciar_sesion(estudiante_id: int, db: Session = Depends(get_db)):
    """Iniciar una nueva sesión para un estudiante"""
    try:
        sesion = Sesion(estudiante_id=estudiante_id)
        db.add(sesion)
        db.commit()
        db.refresh(sesion)
        return {"sesion_id": sesion.id, "mensaje": "Sesión iniciada"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sesiones/finalizar")
def finalizar_sesion(sesion_id: int, db: Session = Depends(get_db)):
    """Finalizar una sesión"""
    try:
        sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
        if not sesion:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        sesion.fecha_fin = datetime.now()
        if sesion.fecha_inicio is not None and sesion.fecha_fin is not None:
            duracion = (sesion.fecha_fin - sesion.fecha_inicio).total_seconds() / 60
            sesion.duracion_minutos = int(duracion)
        
        db.commit()
        return {"mensaje": "Sesión finalizada"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/quiz/resultado")
def guardar_resultado_quiz(resultado: QuizResultRequest, db: Session = Depends(get_db)):
    """Guardar resultado de un quiz"""
    try:
        nuevo_resultado = ResultadoQuiz(
            estudiante_id=resultado.estudiante_id,
            puntaje=resultado.puntaje,
            preguntas_correctas=resultado.preguntas_correctas,
            total_preguntas=resultado.total_preguntas,
            tiempo_completado_minutos=resultado.tiempo_completado_minutos
        )
        db.add(nuevo_resultado)
        db.commit()
        return {"mensaje": "Resultado guardado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/analytics/estudiante/{estudiante_id}")
def obtener_analytics_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    """Obtener analytics de un estudiante específico"""
    try:
        estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        # Estadísticas de sesiones
        sesiones = db.query(Sesion).filter(Sesion.estudiante_id == estudiante_id).all()
        total_sesiones = len(sesiones)
        tiempo_total = sum(s.duracion_minutos or 0 for s in sesiones)
        
        # Estadísticas de preguntas
        preguntas = db.query(Pregunta).filter(Pregunta.estudiante_id == estudiante_id).all()
        total_preguntas = len(preguntas)
        
        # Categorías más consultadas
        categorias = {}
        for p in preguntas:
            if p.categoria is not None:
                categorias[p.categoria] = categorias.get(p.categoria, 0) + 1
        
        # Resultados de quiz
        resultados = db.query(ResultadoQuiz).filter(ResultadoQuiz.estudiante_id == estudiante_id).all()
        promedio_quiz = sum(r.puntaje for r in resultados) / len(resultados) if resultados else 0
        
        return {
            "estudiante": {
                "id": estudiante.id,
                "nombre": estudiante.nombre,
                "email": estudiante.email,
                "grupo": estudiante.grupo
            },
            "estadisticas": {
                "total_sesiones": total_sesiones,
                "tiempo_total_minutos": tiempo_total,
                "total_preguntas": total_preguntas,
                "promedio_quiz": round(float(promedio_quiz), 2),
                "categorias_consultadas": len(categorias)
            },
            "categorias_mas_consultadas": [
                {"categoria": cat, "consultas": count}
                for cat, count in sorted(categorias.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/dashboard")
def obtener_dashboard(db: Session = Depends(get_db)):
    """Obtener dashboard general"""
    try:
        # Métricas generales
        total_estudiantes = db.query(Estudiante).count()
        total_preguntas = db.query(Pregunta).count()
        
        # Sesiones de hoy
        hoy = datetime.now().date()
        sesiones_hoy = db.query(Sesion).filter(
            Sesion.fecha_inicio >= hoy
        ).count()
        
        # Promedio de quiz
        resultados = db.query(ResultadoQuiz).all()
        promedio_quiz = sum(r.puntaje for r in resultados) / len(resultados) if resultados else 0
        
        # Categorías más consultadas
        categorias = db.query(Pregunta.categoria, func.count(Pregunta.id)).group_by(Pregunta.categoria).all()
        categorias_populares = [{"categoria": cat, "total": count} for cat, count in categorias if cat]
        
        return {
            "metricas_generales": {
                "total_estudiantes": total_estudiantes,
                "sesiones_hoy": sesiones_hoy,
                "total_preguntas": total_preguntas,
                "promedio_quiz_general": round(float(promedio_quiz), 2)
            },
            "categorias_populares": categorias_populares[:5]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test_analytics")
def test_analytics():
    """Endpoint de prueba para verificar que analytics funciona"""
    return {
        "status": "ok",
        "message": "Analytics endpoint funcionando",
        "timestamp": str(datetime.now()),
        "data": {
            "metricas_generales": {
                "total_estudiantes": 0,
                "sesiones_hoy": 0,
                "total_preguntas": 0,
                "promedio_quiz_general": 0
            },
            "categorias_populares": []
        }
    }

@app.get("/test_archivos")
def test_archivos():
    """Endpoint de prueba para verificar qué archivos están disponibles en Render"""
    import os
    
    # Verificar carpeta material
    carpeta_material = "material"
    archivos_disponibles = []
    
    if os.path.exists(carpeta_material):
        for archivo in os.listdir(carpeta_material):
            ruta_completa = os.path.join(carpeta_material, archivo)
            if os.path.isfile(ruta_completa):
                tamaño = os.path.getsize(ruta_completa)
                archivos_disponibles.append({
                    "nombre": archivo,
                    "tamaño_bytes": tamaño,
                    "tamaño_mb": round(tamaño / (1024 * 1024), 2)
                })
    
    # Verificar archivos de índice específicos
    faiss_existe = os.path.exists(os.path.join(carpeta_material, "faiss_index.bin"))
    textos_existe = os.path.exists(os.path.join(carpeta_material, "textos.pkl"))
    
    return {
        "carpeta_material_existe": os.path.exists(carpeta_material),
        "archivos_encontrados": len(archivos_disponibles),
        "faiss_index_existe": faiss_existe,
        "textos_pkl_existe": textos_existe,
        "archivos": archivos_disponibles,
        "directorio_actual": os.getcwd(),
        "contenido_directorio": os.listdir(".")
    }

@app.get("/test_prompt")
def test_prompt():
    """Endpoint de prueba para diagnosticar problemas con el prompt"""
    try:
        # Test 1: Prompt simple
        prompt_simple = "Responde brevemente: ¿Qué es la farmacia?"
        
        respuesta_simple = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_simple}],
            max_tokens=100,
            temperature=0.2
        )
        
        # Test 2: Prompt con contexto (versión simplificada)
        contexto_test = "La farmacia es un establecimiento donde se dispensan medicamentos."
        prompt_con_contexto = f"""
Eres un asistente de farmacia. Responde basándote en este contexto:

Contexto: {contexto_test}

Pregunta: ¿Qué es la farmacia?

Responde de forma clara y concisa.
"""
        
        respuesta_con_contexto = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_con_contexto}],
            max_tokens=150,
            temperature=0.2
        )
        
        # Test 3: Verificar longitud del prompt real
        prompt_real = f"""
Eres un asistente educativo experto en farmacia y normativa sanitaria chilena.

Pregunta: ¿Qué es la legislación farmacéutica?

Responde de forma clara y concisa.
"""
        
        return {
            "status": "ok",
            "api_key_configurada": bool(api_key),
            "longitud_api_key": len(api_key) if api_key else 0,
            "test_simple": {
                "prompt": prompt_simple,
                "longitud_prompt": len(prompt_simple),
                "respuesta": respuesta_simple.choices[0].message.content,
                "tokens_usados": respuesta_simple.usage.total_tokens
            },
            "test_con_contexto": {
                "prompt": prompt_con_contexto,
                "longitud_prompt": len(prompt_con_contexto),
                "respuesta": respuesta_con_contexto.choices[0].message.content,
                "tokens_usados": respuesta_con_contexto.usage.total_tokens
            },
            "prompt_real_ejemplo": {
                "longitud": len(prompt_real),
                "primeros_100_caracteres": prompt_real[:100]
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "tipo_error": type(e).__name__,
            "api_key_configurada": bool(api_key),
            "longitud_api_key": len(api_key) if api_key else 0
        }

@app.get("/test_busqueda")
def test_busqueda():
    """Endpoint de prueba para diagnosticar la función de búsqueda semántica"""
    try:
        
        # Verificar que tenemos datos
        if not textos or len(textos) == 0:
            return {
                "status": "error",
                "error": "No hay textos cargados",
                "textos_cargados": len(textos) if textos else 0
            }
        
        if not indice:
            return {
                "status": "error", 
                "error": "Índice FAISS no cargado"
            }
        
        # Test 1: Búsqueda con umbral principal
        pregunta_test = "legislación farmacéutica"
        print(f"Probando búsqueda con umbral principal: {UMBRAL_SIMILITUD_PRINCIPAL}")
        
        try:
            resultados_principal = buscar_similares(
                pregunta_test, 
                indice, 
                textos, 
                k=3, 
                umbral=UMBRAL_SIMILITUD_PRINCIPAL
            )
            print(f"Resultados con umbral principal: {len(resultados_principal)}")
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error en búsqueda con umbral principal: {str(e)}",
                "tipo_error": type(e).__name__
            }
        
        # Test 2: Búsqueda con umbral secundario
        print(f"Probando búsqueda con umbral secundario: {UMBRAL_SIMILITUD_SECUNDARIO}")
        try:
            resultados_secundario = buscar_similares(
                pregunta_test, 
                indice, 
                textos, 
                k=3, 
                umbral=UMBRAL_SIMILITUD_SECUNDARIO
            )
            print(f"Resultados con umbral secundario: {len(resultados_secundario)}")
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error en búsqueda con umbral secundario: {str(e)}",
                "tipo_error": type(e).__name__
            }
        
        # Test 3: Búsqueda sin umbral (para ver qué hay)
        print("Probando búsqueda sin umbral")
        try:
            resultados_sin_umbral = buscar_similares(
                pregunta_test, 
                indice, 
                textos, 
                k=5, 
                umbral=0.0
            )
            print(f"Resultados sin umbral: {len(resultados_sin_umbral)}")
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error en búsqueda sin umbral: {str(e)}",
                "tipo_error": type(e).__name__
            }
        
        return {
            "status": "ok",
            "umbral_principal": UMBRAL_SIMILITUD_PRINCIPAL,
            "umbral_secundario": UMBRAL_SIMILITUD_SECUNDARIO,
            "pregunta_test": pregunta_test,
            "resultados_principal": len(resultados_principal),
            "resultados_secundario": len(resultados_secundario),
            "resultados_sin_umbral": len(resultados_sin_umbral),
            "muestra_sin_umbral": [
                {
                    "archivo": r.get('archivo', 'N/A'),
                    "similitud": r.get('similitud', 'N/A'),
                    "texto_preview": r.get('texto', '')[:100] + "..." if r.get('texto') else 'N/A'
                }
                for r in resultados_sin_umbral[:3]
            ] if resultados_sin_umbral else [],
            "indice_cargado": indice is not None,
            "textos_cargados": len(textos) if textos else 0
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "tipo_error": type(e).__name__,
            "traceback": str(e.__traceback__) if hasattr(e, '__traceback__') else "No disponible"
        }

@app.get("/test_busqueda_simple")
def test_busqueda_simple():
    """Endpoint de prueba simple para diagnosticar errores en búsqueda"""
    try:
        # Test 1: Verificar si el índice y textos están cargados
        info_basica = {
            "indice_cargado": indice is not None,
            "textos_cargados": len(textos) if textos else 0,
            "tipo_indice": str(type(indice)) if indice else "None",
            "tipo_textos": str(type(textos)) if textos else "None"
        }
        
        # Test 2: Verificar si hay textos
        if textos and len(textos) > 0:
            info_basica["primer_texto"] = {
                "archivo": textos[0].get('archivo', 'N/A'),
                "texto_preview": textos[0].get('texto', '')[:50] + "..." if textos[0].get('texto') else 'N/A'
            }
        
        # Test 3: Intentar obtener embedding (sin búsqueda)
        try:
            from embedding_utils import obtener_embedding
            embedding_test = obtener_embedding("test")
            info_basica["embedding_funciona"] = True
            info_basica["dimension_embedding"] = len(embedding_test)
        except Exception as e:
            info_basica["embedding_funciona"] = False
            info_basica["error_embedding"] = str(e)
        
        return {
            "status": "ok",
            "info": info_basica
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "tipo_error": type(e).__name__,
            "traceback": str(e.__traceback__) if hasattr(e, '__traceback__') else "No disponible"
        }

@app.get("/test_busqueda_paso_a_paso")
def test_busqueda_paso_a_paso():
    """Endpoint de prueba paso a paso para identificar el error exacto"""
    resultados = {}
    
    try:
        # Paso 1: Verificar datos básicos
        resultados["paso_1"] = {
            "indice_existe": indice is not None,
            "textos_existen": textos is not None,
            "cantidad_textos": len(textos) if textos else 0
        }
        
        # Paso 2: Verificar configuración
        from config import UMBRAL_SIMILITUD_PRINCIPAL, UMBRAL_SIMILITUD_SECUNDARIO
        resultados["paso_2"] = {
            "umbral_principal": UMBRAL_SIMILITUD_PRINCIPAL,
            "umbral_secundario": UMBRAL_SIMILITUD_SECUNDARIO
        }
        
        # Paso 3: Verificar función de embedding
        try:
            from embedding_utils import obtener_embedding
            embedding_test = obtener_embedding("test simple")
            resultados["paso_3"] = {
                "embedding_funciona": True,
                "dimension": len(embedding_test)
            }
        except Exception as e:
            resultados["paso_3"] = {
                "embedding_funciona": False,
                "error": str(e)
            }
            return {"status": "error_en_paso_3", "resultados": resultados}
        
        # Paso 4: Verificar función buscar_similares (sin llamarla)
        try:
            from embedding_utils import buscar_similares
            resultados["paso_4"] = {
                "funcion_importada": True
            }
        except Exception as e:
            resultados["paso_4"] = {
                "funcion_importada": False,
                "error": str(e)
            }
            return {"status": "error_en_paso_4", "resultados": resultados}
        
        # Paso 5: Llamar buscar_similares con umbral 0.0 (más permisivo)
        try:
            pregunta_test = "legislación"
            resultados_busqueda = buscar_similares(
                pregunta_test, 
                indice, 
                textos, 
                k=1, 
                umbral=0.0
            )
            resultados["paso_5"] = {
                "busqueda_funciona": True,
                "resultados_encontrados": len(resultados_busqueda),
                "primer_resultado": {
                    "archivo": resultados_busqueda[0].get('archivo', 'N/A'),
                    "similitud": resultados_busqueda[0].get('similitud', 'N/A'),
                    "texto_preview": resultados_busqueda[0].get('texto', '')[:50] + "..." if resultados_busqueda[0].get('texto') else 'N/A'
                } if resultados_busqueda else None
            }
        except Exception as e:
            resultados["paso_5"] = {
                "busqueda_funciona": False,
                "error": str(e),
                "tipo_error": type(e).__name__
            }
            return {"status": "error_en_paso_5", "resultados": resultados}
        
        return {"status": "ok", "resultados": resultados}
        
    except Exception as e:
        return {
            "status": "error_general",
            "error": str(e),
            "tipo_error": type(e).__name__,
            "resultados": resultados
        }

@app.get("/test_basico")
def test_basico():
    """Endpoint de diagnóstico básico sin importaciones adicionales"""
    try:
        # Verificar variables globales básicas
        info_basica = {
            "api_key_existe": bool(api_key),
            "client_openai_existe": client is not None,
            "carpeta_material": CARPETA_MATERIAL,
            "indice_tipo": str(type(indice)) if indice else "None",
            "textos_tipo": str(type(textos)) if textos else "None",
            "textos_cantidad": len(textos) if textos else 0
        }
        
        # Verificar si podemos acceder a config sin importar
        try:
            import config
            info_basica["config_importable"] = True
            info_basica["umbral_principal"] = getattr(config, 'UMBRAL_SIMILITUD_PRINCIPAL', 'No encontrado')
            info_basica["umbral_secundario"] = getattr(config, 'UMBRAL_SIMILITUD_SECUNDARIO', 'No encontrado')
        except Exception as e:
            info_basica["config_importable"] = False
            info_basica["error_config"] = str(e)
        
        # Verificar si podemos acceder a embedding_utils sin importar
        try:
            import embedding_utils
            info_basica["embedding_utils_importable"] = True
        except Exception as e:
            info_basica["embedding_utils_importable"] = False
            info_basica["error_embedding_utils"] = str(e)
        
        # Verificar si hay archivos en la carpeta material
        try:
            import os
            if os.path.exists(CARPETA_MATERIAL):
                archivos = os.listdir(CARPETA_MATERIAL)
                info_basica["archivos_material"] = archivos
                info_basica["cantidad_archivos"] = len(archivos)
            else:
                info_basica["carpeta_material_existe"] = False
        except Exception as e:
            info_basica["error_verificar_archivos"] = str(e)
        
        return {
            "status": "ok",
            "info": info_basica
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "tipo_error": type(e).__name__,
            "linea_error": getattr(e, '__traceback__', None)
        }

@app.get("/test_openai")
def test_openai():
    """
    Endpoint para probar la conexión con OpenAI
    """
    try:
        # Verificar si la API key está configurada
        if not api_key:
            return {
                "status": "error",
                "message": "OPENAI_API_KEY no está configurada",
                "api_key_configured": False
            }
        
        # Verificar si la API key es válida (sin exponer la clave)
        api_key_length = len(api_key)
        api_key_prefix = api_key[:7] if api_key else ""
        
        # Intentar una llamada simple a OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hola"}],
                max_tokens=10,
                temperature=0
            )
            
            return {
                "status": "success",
                "message": "Conexión con OpenAI exitosa",
                "api_key_configured": True,
                "api_key_length": api_key_length,
                "api_key_prefix": api_key_prefix,
                "openai_response": "OK"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al conectar con OpenAI: {str(e)}",
                "api_key_configured": True,
                "api_key_length": api_key_length,
                "api_key_prefix": api_key_prefix,
                "openai_error": str(e)
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error general: {str(e)}",
            "api_key_configured": False
        }

@app.get("/test_pregunta_simple")
def test_pregunta_simple():
    """
    Endpoint para probar una pregunta simple sin el prompt complejo
    """
    try:
        pregunta = "¿Qué es la cadena de frío?"
        
        # Buscar contexto
        resultados = buscar_similares(pregunta, indice, textos, k=3, umbral=0.5)
        
        if resultados:
            contexto = "Contexto encontrado: " + str(len(resultados)) + " resultados"
        else:
            contexto = "No se encontró contexto"
        
        # Prompt simple
        prompt_simple = f"Responde brevemente: {pregunta}"
        
        # Llamada a OpenAI
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_simple}],
            max_tokens=100,
            temperature=0.2
        )
        
        respuesta_final = respuesta.choices[0].message.content
        
        return {
            "status": "success",
            "pregunta": pregunta,
            "contexto_encontrado": contexto,
            "respuesta_openai": respuesta_final,
            "modelo_usado": "gpt-3.5-turbo"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "tipo_error": type(e).__name__
        }

# --- ENDPOINTS PARA CASOS CLÍNICOS ---
import json

def cargar_casos_clinicos():
    """Cargar los casos clínicos desde el archivo JSON"""
    try:
        with open('casos_clinicos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"casos_clinicos": []}
    except Exception as e:
        print(f"Error al cargar casos clínicos: {e}")
        return {"casos_clinicos": []}

@app.get("/casos_clinicos")
def obtener_casos_clinicos():
    """Obtener todos los casos clínicos disponibles"""
    try:
        casos = cargar_casos_clinicos()
        return {
            "status": "success",
            "casos": casos["casos_clinicos"],
            "total_casos": len(casos["casos_clinicos"])
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/casos_clinicos/{caso_id}")
def obtener_caso_clinico(caso_id: int):
    """Obtener un caso clínico específico por ID"""
    try:
        casos = cargar_casos_clinicos()
        caso = next((c for c in casos["casos_clinicos"] if c["id"] == caso_id), None)
        
        if caso:
            return {
                "status": "success",
                "caso": caso
            }
        else:
            return {
                "status": "error",
                "message": f"Caso clínico con ID {caso_id} no encontrado"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/casos_clinicos/{caso_id}/preguntas")
def obtener_preguntas_caso_clinico(caso_id: int):
    """Obtener las preguntas de un caso clínico específico"""
    try:
        casos = cargar_casos_clinicos()
        caso = next((c for c in casos["casos_clinicos"] if c["id"] == caso_id), None)
        
        if caso:
            return {
                "status": "success",
                "caso_id": caso_id,
                "titulo": caso["titulo"],
                "descripcion": caso["descripcion"],
                "preguntas": caso["preguntas"],
                "total_preguntas": len(caso["preguntas"])
            }
        else:
            return {
                "status": "error",
                "message": f"Caso clínico con ID {caso_id} no encontrado"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/quiz_casos_clinicos")
def obtener_quiz_casos_clinicos():
    """Obtener un quiz completo con todos los casos clínicos"""
    try:
        casos = cargar_casos_clinicos()
        
        if not casos["casos_clinicos"]:
            return {
                "status": "error",
                "message": "No hay casos clínicos disponibles"
            }
        
        # Crear el quiz con todos los casos
        quiz = {
            "titulo": "Quiz de Casos Clínicos - Auxiliar de Farmacia",
            "descripcion": "Evaluación basada en casos clínicos reales",
            "casos": casos["casos_clinicos"],
            "total_casos": len(casos["casos_clinicos"]),
            "total_preguntas": sum(len(caso["preguntas"]) for caso in casos["casos_clinicos"])
        }
        
        return {
            "status": "success",
            "quiz": quiz
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

class RespuestaCasoClinico(BaseModel):
    caso_id: int
    pregunta_id: int
    respuesta_seleccionada: int

@app.post("/casos_clinicos/verificar_respuesta")
def verificar_respuesta_caso_clinico(respuesta: RespuestaCasoClinico):
    """Verificar si una respuesta a un caso clínico es correcta"""
    try:
        casos = cargar_casos_clinicos()
        caso = next((c for c in casos["casos_clinicos"] if c["id"] == respuesta.caso_id), None)
        
        if not caso:
            return {
                "status": "error",
                "message": f"Caso clínico con ID {respuesta.caso_id} no encontrado"
            }
        
        pregunta = next((p for p in caso["preguntas"] if p["id"] == respuesta.pregunta_id), None)
        
        if not pregunta:
            return {
                "status": "error",
                "message": f"Pregunta con ID {respuesta.pregunta_id} no encontrada en el caso {respuesta.caso_id}"
            }
        
        es_correcta = respuesta.respuesta_seleccionada == pregunta["respuesta_correcta"]
        
        return {
            "status": "success",
            "es_correcta": es_correcta,
            "respuesta_correcta": pregunta["respuesta_correcta"],
            "explicacion": pregunta["explicacion"],
            "opcion_correcta": pregunta["opciones"][pregunta["respuesta_correcta"]]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
