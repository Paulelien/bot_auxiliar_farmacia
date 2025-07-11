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

# Estadísticas de uso
estadisticas_uso = {
    "preguntas_totales": 0,
    "preguntas_por_categoria": {},
    "preguntas_frecuentes": {},
    "ultima_actualizacion": None
}

# Cargar el índice y textos del material
indice, textos = cargar_o_crear_indice([])

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
    # Buscar contexto relevante
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

REGLAS DE RESPUESTA FUNDAMENTALES:

1. **RESPONDE EXACTAMENTE LO QUE SE PREGUNTA**: Si preguntan sobre "receta médica retenida", responde específicamente sobre recetas retenidas, NO sobre recetas en general. Si preguntan sobre "receta médica tipo cheque", responde específicamente sobre ese tipo de receta.

2. **PRECISIÓN ESPECÍFICA**: 
   - Si preguntan sobre un concepto específico, define ESE concepto específico
   - Si preguntan sobre un procedimiento específico, explica ESE procedimiento específico
   - Si preguntan sobre un tipo de documento específico, describe ESE tipo de documento específico

3. **NO GENERALICES**: Evita dar respuestas generales cuando se pregunta algo específico. Por ejemplo:
   - ❌ Si preguntan "¿Qué es una receta médica retenida?" NO respondas "Una receta médica es..."
   - ✅ Si preguntan "¿Qué es una receta médica retenida?" responde "Una receta médica retenida es..."

4. **CONTEXTO ESPECÍFICO**: Usa el contexto proporcionado para encontrar información específica sobre lo que se pregunta, no información general relacionada.

5. **NO INVENTES**: Si no encuentras información específica sobre lo que se pregunta en el contexto, indícalo claramente.

📌 **Uso del Vademécum (https://www.vademecum.es/chile/cl/alfa)**  
Solo redirige al Vademécum si el usuario consulta específicamente sobre:
- Principio activo de un medicamento específico
- Dosis exacta de un medicamento
- Grupo terapéutico
- Clasificación ATC

No lo uses para responder sobre normativas, funciones del auxiliar o conceptos generales.

📘 **Responde normalmente usando el contexto del curso en preguntas sobre:**
- Conceptos específicos de farmacología
- Formas farmacéuticas específicas
- Funciones específicas del auxiliar de farmacia
- Normativas específicas (como el Decreto 405)
- Procedimientos específicos de almacenamiento y cadena de frío
- Protocolos específicos de atención al cliente
- Aspectos específicos de ética profesional
- Tecnología farmacéutica específica

📑 **Normativas legales específicas:**
Si el usuario menciona leyes o decretos como el Decreto 79:
- Intenta recuperar la información exacta desde los documentos cargados.
- Si no encuentras el artículo solicitado, responde:  
  "Actualmente no tengo acceso directo al artículo solicitado del Decreto 79. Te recomiendo consultarlo directamente en: https://www.leychile.cl o escribir a tu tutor académico desde el apartado de Consultas Académicas en el menú superior de la plataforma."

⚠️ No confundas el Decreto 79 con otros (como el Decreto 466) a menos que esté expresamente mencionado.

EJEMPLOS DE RESPUESTAS CORRECTAS:
- Pregunta: "¿Qué es una receta médica retenida?" → Responde específicamente sobre recetas retenidas
- Pregunta: "¿Qué es una receta tipo cheque?" → Responde específicamente sobre recetas tipo cheque
- Pregunta: "¿Qué es el Decreto 405?" → Responde específicamente sobre el Decreto 405, no sobre decretos en general

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
