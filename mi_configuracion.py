# ========================================
# CONFIGURACIÓN PERSONALIZADA
# Sistema Keep-Alive para Bot de Farmacia
# ========================================

# 🌐 CONFIGURACIÓN DE LA API
API_URL = "https://asistente-auxiliar-farmacia.onrender.com"

# ⏰ CONFIGURACIÓN DE TIEMPOS
INTERVALO_SEGUNDOS = 60          # Consultar cada 60 segundos
TIMEOUT_CONSULTA = 30            # Timeout para consultas (30 segundos)
TIMEOUT_SALUD = 10               # Timeout para verificar salud (10 segundos)

# 🔄 CONFIGURACIÓN DE REINTENTOS
MAX_REINTENTOS = 3               # Máximo número de reintentos
TIEMPO_ENTRE_REINTENTOS = 5      # Segundos entre reintentos

# 📝 PREGUNTA PARA MANTENER API ACTIVA
PREGUNTA_SIMPLE = "¿Cuáles son las funciones del auxiliar de farmacia?"

# 📊 CONFIGURACIÓN DE LOGGING
LOG_LEVEL = "INFO"               # Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_FILE = "keep_alive.log"      # Nombre del archivo de log

# 📁 CONFIGURACIÓN DE ARCHIVOS
DIRECTORIO_LOGS = "logs"         # Directorio donde se guardan los logs
ARCHIVO_ESTADISTICAS = "keep_alive_stats.json"  # Archivo de estadísticas

# 🎯 CONFIGURACIÓN ADICIONAL
MOSTRAR_PROGRESO = True          # Mostrar barra de progreso
GUARDAR_ESTADISTICAS_CADA = 10   # Guardar estadísticas cada N ejecuciones
MAX_TIEMPOS_GUARDADOS = 100      # Máximo número de tiempos de respuesta a guardar

# ========================================
# INFORMACIÓN DEL PROYECTO
# ========================================
PROYECTO_NOMBRE = "Bot Auxiliar de Farmacia"
PROYECTO_VERSION = "1.0.0"
PROYECTO_DESCRIPCION = "Sistema Keep-Alive para mantener la API activa"

# ========================================
# CONFIGURACIÓN DE NOTIFICACIONES (FUTURO)
# ========================================
ENVIAR_NOTIFICACIONES = False    # Habilitar notificaciones por email/telegram
NOTIFICAR_FALLOS = True          # Notificar solo en caso de fallos
NOTIFICAR_CADA = 60              # Notificar cada N minutos (0 = solo en fallos)

# ========================================
# CONFIGURACIÓN DE MONITOREO
# ========================================
MONITOREO_ACTIVO = True          # Habilitar monitoreo en tiempo real
VERIFICAR_SALUD = True           # Verificar salud de la API antes de consultar
REGISTRAR_METRICAS = True        # Registrar métricas de rendimiento

# ========================================
# CONFIGURACIÓN DE SEGURIDAD
# ========================================
VERIFICAR_SSL = True             # Verificar certificados SSL
USER_AGENT = "Keep-Alive-Bot-Farmacia/1.0"  # User-Agent personalizado
TIMEOUT_CONEXION = 5             # Timeout para establecer conexión

# ========================================
# CONFIGURACIÓN DE DESARROLLO
# ========================================
MODO_DEBUG = False               # Habilitar modo debug
LOG_DETALLADO = False            # Logging más detallado
SIMULAR_FALLOS = False           # Simular fallos para testing

# ========================================
# FUNCIÓN PARA VALIDAR CONFIGURACIÓN
# ========================================
def validar_configuracion():
    """Valida que la configuración sea correcta"""
    errores = []
    
    if not API_URL or not API_URL.startswith(('http://', 'https://')):
        errores.append("API_URL debe ser una URL válida")
    
    if INTERVALO_SEGUNDOS < 10:
        errores.append("INTERVALO_SEGUNDOS debe ser al menos 10 segundos")
    
    if TIMEOUT_CONSULTA < 5:
        errores.append("TIMEOUT_CONSULTA debe ser al menos 5 segundos")
    
    if MAX_REINTENTOS < 1:
        errores.append("MAX_REINTENTOS debe ser al menos 1")
    
    if not PREGUNTA_SIMPLE:
        errores.append("PREGUNTA_SIMPLE no puede estar vacía")
    
    return errores

# ========================================
# INFORMACIÓN DE CONTACTO
# ========================================
CONTACTO = {
    "proyecto": "Bot Auxiliar de Farmacia",
    "version": "1.0.0",
    "fecha_creacion": "2024-12-19",
    "descripcion": "Sistema Keep-Alive para mantener la API activa y reducir tiempos de respuesta"
}

# ========================================
# MENSAJE DE INICIO
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("    CONFIGURACIÓN DEL SISTEMA KEEP-ALIVE")
    print("=" * 60)
    print(f"🌐 API URL: {API_URL}")
    print(f"⏰ Intervalo: {INTERVALO_SEGUNDOS} segundos")
    print(f"🔄 Reintentos: {MAX_REINTENTOS}")
    print(f"📁 Logs: {DIRECTORIO_LOGS}/")
    print("=" * 60)
    
    # Validar configuración
    errores = validar_configuracion()
    if errores:
        print("❌ Errores en la configuración:")
        for error in errores:
            print(f"   • {error}")
        print("=" * 60)
    else:
        print("✅ Configuración válida")
        print("=" * 60)
