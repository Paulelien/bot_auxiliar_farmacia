#!/usr/bin/env python3
"""
Script para mantener la API activa y reducir el tiempo de respuesta
de la primera pregunta. Se ejecuta en paralelo con la aplicación principal.

Uso:
    python keep_alive.py

O en segundo plano:
    nohup python keep_alive.py > keep_alive.log 2>&1 &
"""

import requests
import time
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
API_URL = os.getenv('API_URL', 'https://asistente-auxiliar-farmacia.onrender.com')
HEALTH_ENDPOINT = f"{API_URL}/health"
PREGUNTA_ENDPOINT = f"{API_URL}/preguntar"
INTERVALO_SEGUNDOS = 60  # Consultar cada 60 segundos

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep_alive.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def verificar_salud_api():
    """Verifica el estado de salud de la API"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        if response.status_code == 200:
            logger.info("✅ API saludable - Status: 200")
            return True
        else:
            logger.warning(f"⚠️ API respondió con status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error conectando a la API: {e}")
        return False

def mantener_api_activa():
    """Envía una pregunta simple para mantener la API activa"""
    try:
        pregunta_simple = "¿Cuáles son las funciones del auxiliar de farmacia?"
        
        response = requests.post(
            PREGUNTA_ENDPOINT,
            json={"pregunta": pregunta_simple},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            tiempo_respuesta = response.elapsed.total_seconds()
            logger.info(f"✅ API activa - Respuesta en {tiempo_respuesta:.2f}s")
            return True
        else:
            logger.warning(f"⚠️ API respondió con status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error manteniendo API activa: {e}")
        return False

def main():
    """Función principal que ejecuta el keep-alive"""
    logger.info("🚀 Iniciando Keep-Alive para la API")
    logger.info(f"🌐 URL de la API: {API_URL}")
    logger.info(f"⏰ Intervalo de consulta: {INTERVALO_SEGUNDOS} segundos")
    logger.info("=" * 50)
    
    contador_exitos = 0
    contador_fallos = 0
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"\n🕐 {timestamp} - Ejecutando verificación...")
            
            # Verificar salud de la API
            salud_ok = verificar_salud_api()
            
            if salud_ok:
                # Mantener API activa
                api_activa = mantener_api_activa()
                
                if api_activa:
                    contador_exitos += 1
                    logger.info(f"📊 Estadísticas - Éxitos: {contador_exitos}, Fallos: {contador_fallos}")
                else:
                    contador_fallos += 1
                    logger.warning(f"📊 Estadísticas - Éxitos: {contador_exitos}, Fallos: {contador_fallos}")
            else:
                contador_fallos += 1
                logger.warning(f"📊 Estadísticas - Éxitos: {contador_exitos}, Fallos: {contador_fallos}")
            
            # Esperar antes de la siguiente consulta
            logger.info(f"⏳ Esperando {INTERVALO_SEGUNDOS} segundos hasta la próxima consulta...")
            time.sleep(INTERVALO_SEGUNDOS)
            
    except KeyboardInterrupt:
        logger.info("\n🛑 Keep-Alive detenido por el usuario")
        logger.info(f"📊 Resumen final - Éxitos: {contador_exitos}, Fallos: {contador_fallos}")
    except Exception as e:
        logger.error(f"💥 Error inesperado: {e}")
        logger.info(f"📊 Resumen final - Éxitos: {contador_exitos}, Fallos: {contador_fallos}")

if __name__ == "__main__":
    main()
