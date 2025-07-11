# Configuración del Chatbot Auxiliar de Farmacia

# Umbral de similitud semántica (0.0 a 1.0)
# - 0.95: Muy estricto (solo respuestas casi idénticas)
# - 0.90: Estricto (respuestas muy similares)
# - 0.85: Moderado-alto (respuestas similares) - RECOMENDADO
# - 0.80: Moderado (respuestas relacionadas)
# - 0.75: Moderado-bajo (respuestas algo relacionadas)
# - 0.70: Bajo (respuestas vagamente relacionadas)
# - 0.65: Muy bajo (casi cualquier cosa)
# - 0.60: Mínimo (todo)

UMBRAL_SIMILITUD_PRINCIPAL = 0.85
UMBRAL_SIMILITUD_SECUNDARIO = 0.70

# Configuración de búsqueda
K_MAX_RESULTADOS = 5
K_RESULTADOS_FINALES = 3

# Configuración de OpenAI
MODELO_EMBEDDING = "text-embedding-3-small"
MODELO_CHAT = "gpt-3.5-turbo"
TEMPERATURA_CHAT = 0.2
MAX_TOKENS = 512

# Configuración de archivos
INDICE_FAISS_PATH = "material/faiss_index.bin"
TEXTOS_PATH = "material/textos.pkl"

# Configuración de logging
MOSTRAR_DEBUG = True
MOSTRAR_SIMILITUD = True 