from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from embedding_utils import buscar_similares, cargar_o_crear_indice
import random
from datetime import datetime

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
    "¿Cuáles son los requisitos para trabajar en una farmacia?",
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
