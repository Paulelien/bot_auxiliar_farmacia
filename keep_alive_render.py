#!/usr/bin/env python3
"""
Sistema de Keep-Alive para Render
Mantiene el servidor activo mediante pings regulares
"""

import requests
import time
import os
import logging
from datetime import datetime

# Configuración
BASE_URL = os.environ.get('PING_URL', 'https://asistente-auxiliar-farmacia.onrender.com')
ENDPOINTS = ['/health', '/ping', '/keep-alive']  # Múltiples endpoints
INTERVALO_SEGUNDOS = 30  # Ping cada 30 segundos
TIMEOUT_CONSULTA = 15
MAX_REINTENTOS = 3

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep_alive.log'),
        logging.StreamHandler()
    ]
)

def hacer_ping():
    """Hacer ping a múltiples endpoints"""
    for endpoint in ENDPOINTS:
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, timeout=TIMEOUT_CONSULTA)
            if response.status_code == 200:
                logging.info(f"✅ Ping exitoso a {endpoint} - Status: {response.status_code}")
                return True
            else:
                logging.warning(f"⚠️ Ping a {endpoint} con status inesperado: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Error en ping a {endpoint}: {e}")
    
    return False

def main():
    """Función principal del keep-alive"""
    logging.info("🚀 Iniciando sistema de Keep-Alive para Render")
    logging.info(f"📍 URL objetivo: {BASE_URL}")
    logging.info(f"🔗 Endpoints: {', '.join(ENDPOINTS)}")
    logging.info(f"⏰ Intervalo: {INTERVALO_SEGUNDOS} segundos")
    
    contador_pings = 0
    contador_exitos = 0
    contador_fallos = 0
    
    while True:
        try:
            contador_pings += 1
            logging.info(f"🔄 Ping #{contador_pings} - {datetime.now().strftime('%H:%M:%S')}")
            
            if hacer_ping():
                contador_exitos += 1
            else:
                contador_fallos += 1
                
            # Estadísticas cada 10 pings
            if contador_pings % 10 == 0:
                logging.info(f"📊 Estadísticas - Total: {contador_pings}, Exitos: {contador_exitos}, Fallos: {contador_fallos}")
            
            # Esperar antes del siguiente ping
            time.sleep(INTERVALO_SEGUNDOS)
            
        except KeyboardInterrupt:
            logging.info("🛑 Sistema de Keep-Alive detenido por el usuario")
            break
        except Exception as e:
            logging.error(f"💥 Error inesperado: {e}")
            time.sleep(5)  # Esperar antes de reintentar

if __name__ == "__main__":
    main()
