#!/usr/bin/env python3
"""
Script avanzado para mantener la API activa y reducir el tiempo de respuesta
de la primera pregunta. Incluye reintentos, mejor logging y monitoreo.

Uso:
    python keep_alive_avanzado.py

O en segundo plano:
    nohup python keep_alive_avanzado.py > keep_alive.log 2>&1 &

Para ejecutar como servicio del sistema:
    sudo cp keep_alive.service /etc/systemd/system/
    sudo systemctl enable keep_alive
    sudo systemctl start keep_alive
"""

import requests
import time
import logging
from datetime import datetime, timedelta
import os
import sys
import signal
from typing import Dict, Any
import json

# Importar configuración
try:
    from config_keep_alive import *
except ImportError:
    # Configuración por defecto si no existe el archivo
    API_URL = "https://asistente-auxiliar-farmacia.onrender.com"
    INTERVALO_SEGUNDOS = 60
    PREGUNTA_SIMPLE = "¿Cuáles son las funciones del auxiliar de farmacia?"
    TIMEOUT_CONSULTA = 30
    TIMEOUT_SALUD = 10
    LOG_LEVEL = "INFO"
    LOG_FILE = "keep_alive.log"
    MAX_REINTENTOS = 3
    TIEMPO_ENTRE_REINTENTOS = 5

class KeepAliveAPI:
    """Clase para mantener la API activa"""
    
    def __init__(self):
        self.contador_exitos = 0
        self.contador_fallos = 0
        self.contador_reintentos = 0
        self.ultima_respuesta_exitosa = None
        self.mejor_tiempo_respuesta = float('inf')
        self.peor_tiempo_respuesta = 0
        self.tiempos_respuesta = []
        
        # Configurar logging
        self._configurar_logging()
        
        # Configurar señales para detención graceful
        signal.signal(signal.SIGINT, self._manejar_senal)
        signal.signal(signal.SIGTERM, self._manejar_senal)
        
        self.ejecutando = True
        
    def _configurar_logging(self):
        """Configura el sistema de logging"""
        # Crear directorio de logs si no existe
        os.makedirs('logs', exist_ok=True)
        
        # Configurar logging
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/{LOG_FILE}'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def _manejar_senal(self, signum, frame):
        """Maneja señales de interrupción"""
        self.logger.info(f"\n🛑 Señal {signum} recibida. Deteniendo Keep-Alive...")
        self.ejecutando = False
        
    def verificar_salud_api(self) -> bool:
        """Verifica el estado de salud de la API con reintentos"""
        for intento in range(MAX_REINTENTOS):
            try:
                response = requests.get(
                    f"{API_URL}/health", 
                    timeout=TIMEOUT_SALUD
                )
                
                if response.status_code == 200:
                    self.logger.info("✅ API saludable - Status: 200")
                    return True
                else:
                    self.logger.warning(f"⚠️ API respondió con status: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"⚠️ Intento {intento + 1}/{MAX_REINTENTOS} falló: {e}")
                
                if intento < MAX_REINTENTOS - 1:
                    time.sleep(TIEMPO_ENTRE_REINTENTOS)
                    continue
                else:
                    self.logger.error(f"❌ Todos los intentos fallaron para verificar salud")
                    return False
                    
        return False
        
    def mantener_api_activa(self) -> bool:
        """Envía una pregunta simple para mantener la API activa"""
        for intento in range(MAX_REINTENTOS):
            try:
                inicio = time.time()
                
                response = requests.post(
                    f"{API_URL}/preguntar",
                    json={"pregunta": PREGUNTA_SIMPLE},
                    headers={"Content-Type": "application/json"},
                    timeout=TIMEOUT_CONSULTA
                )
                
                tiempo_respuesta = time.time() - inicio
                
                if response.status_code == 200:
                    # Actualizar estadísticas
                    self._actualizar_estadisticas(tiempo_respuesta)
                    self.ultima_respuesta_exitosa = datetime.now()
                    
                    self.logger.info(f"✅ API activa - Respuesta en {tiempo_respuesta:.2f}s")
                    return True
                else:
                    self.logger.warning(f"⚠️ API respondió con status: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"⚠️ Intento {intento + 1}/{MAX_REINTENTOS} falló: {e}")
                
                if intento < MAX_REINTENTOS - 1:
                    time.sleep(TIEMPO_ENTRE_REINTENTOS)
                    continue
                else:
                    self.logger.error(f"❌ Todos los intentos fallaron para mantener API activa")
                    return False
                    
        return False
        
    def _actualizar_estadisticas(self, tiempo_respuesta: float):
        """Actualiza las estadísticas de tiempo de respuesta"""
        self.tiempos_respuesta.append(tiempo_respuesta)
        
        # Mantener solo los últimos 100 tiempos
        if len(self.tiempos_respuesta) > 100:
            self.tiempos_respuesta.pop(0)
            
        # Actualizar mejores/peores tiempos
        if tiempo_respuesta < self.mejor_tiempo_respuesta:
            self.mejor_tiempo_respuesta = tiempo_respuesta
            
        if tiempo_respuesta > self.peor_tiempo_respuesta:
            self.peor_tiempo_respuesta = tiempo_respuesta
            
    def mostrar_estadisticas(self):
        """Muestra estadísticas detalladas"""
        if self.tiempos_respuesta:
            tiempo_promedio = sum(self.tiempos_respuesta) / len(self.tiempos_respuesta)
        else:
            tiempo_promedio = 0
            
        self.logger.info("📊 Estadísticas Detalladas:")
        self.logger.info(f"   • Éxitos totales: {self.contador_exitos}")
        self.logger.info(f"   • Fallos totales: {self.contador_fallos}")
        self.logger.info(f"   • Reintentos: {self.contador_reintentos}")
        self.logger.info(f"   • Mejor tiempo: {self.mejor_tiempo_respuesta:.2f}s")
        self.logger.info(f"   • Peor tiempo: {self.peor_tiempo_respuesta:.2f}s")
        self.logger.info(f"   • Tiempo promedio: {tiempo_promedio:.2f}s")
        
        if self.ultima_respuesta_exitosa:
            self.logger.info(f"   • Última respuesta exitosa: {self.ultima_respuesta_exitosa.strftime('%Y-%m-%d %H:%M:%S')}")
            
    def guardar_estadisticas(self):
        """Guarda las estadísticas en un archivo JSON"""
        stats = {
            "fecha_actualizacion": datetime.now().isoformat(),
            "contador_exitos": self.contador_exitos,
            "contador_fallos": self.contador_fallos,
            "contador_reintentos": self.contador_reintentos,
            "mejor_tiempo_respuesta": self.mejor_tiempo_respuesta,
            "peor_tiempo_respuesta": self.peor_tiempo_respuesta,
            "tiempo_promedio": sum(self.tiempos_respuesta) / len(self.tiempos_respuesta) if self.tiempos_respuesta else 0,
            "ultima_respuesta_exitosa": self.ultima_respuesta_exitosa.isoformat() if self.ultima_respuesta_exitosa else None
        }
        
        try:
            with open('logs/keep_alive_stats.json', 'w') as f:
                json.dump(stats, f, indent=2)
            self.logger.info("💾 Estadísticas guardadas en logs/keep_alive_stats.json")
        except Exception as e:
            self.logger.error(f"❌ Error guardando estadísticas: {e}")
            
    def ejecutar(self):
        """Ejecuta el keep-alive principal"""
        self.logger.info("🚀 Iniciando Keep-Alive Avanzado para la API")
        self.logger.info(f"🌐 URL de la API: {API_URL}")
        self.logger.info(f"⏰ Intervalo de consulta: {INTERVALO_SEGUNDOS} segundos")
        self.logger.info(f"🔄 Máximo reintentos: {MAX_REINTENTOS}")
        self.logger.info("=" * 60)
        
        try:
            while self.ejecutando:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.logger.info(f"\n🕐 {timestamp} - Ejecutando verificación...")
                
                # Verificar salud de la API
                salud_ok = self.verificar_salud_api()
                
                if salud_ok:
                    # Mantener API activa
                    api_activa = self.mantener_api_activa()
                    
                    if api_activa:
                        self.contador_exitos += 1
                    else:
                        self.contador_fallos += 1
                        self.contador_reintentos += 1
                else:
                    self.contador_fallos += 1
                    self.contador_reintentos += 1
                
                # Mostrar estadísticas
                self.mostrar_estadisticas()
                
                # Guardar estadísticas cada 10 ejecuciones
                if (self.contador_exitos + self.contador_fallos) % 10 == 0:
                    self.guardar_estadisticas()
                
                # Esperar antes de la siguiente consulta
                if self.ejecutando:
                    self.logger.info(f"⏳ Esperando {INTERVALO_SEGUNDOS} segundos hasta la próxima consulta...")
                    time.sleep(INTERVALO_SEGUNDOS)
                    
        except Exception as e:
            self.logger.error(f"💥 Error inesperado: {e}")
        finally:
            self.logger.info("\n🛑 Keep-Alive detenido")
            self.logger.info("📊 Resumen final:")
            self.mostrar_estadisticas()
            self.guardar_estadisticas()

def main():
    """Función principal"""
    keep_alive = KeepAliveAPI()
    keep_alive.ejecutar()

if __name__ == "__main__":
    main()
