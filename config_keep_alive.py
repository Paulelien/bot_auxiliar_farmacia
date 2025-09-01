# Configuración para el Keep-Alive de la API
# Ajusta estos valores según tu configuración

# URL de tu API (cambia esto por tu URL real)
API_URL = "https://asistente-auxiliar-farmacia.onrender.com"

# Intervalo de consulta en segundos (60 = 1 minuto)
INTERVALO_SEGUNDOS = 60

# Pregunta simple para mantener la API activa
PREGUNTA_SIMPLE = "¿Cuáles son las funciones del auxiliar de farmacia?"

# Timeout para las consultas (en segundos)
TIMEOUT_CONSULTA = 30
TIMEOUT_SALUD = 10

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FILE = "keep_alive.log"

# Configuración adicional
MAX_REINTENTOS = 3
TIEMPO_ENTRE_REINTENTOS = 5  # segundos
