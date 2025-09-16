#!/usr/bin/env python3
"""
Script avanzado para mantener la API activa y reducir el tiempo de respuesta
de la primera pregunta. Incluye reintentos, mejor logging y monitoreo.
VERSIÓN SIN EMOJIS para compatibilidad con Windows.

Uso:
    python keep_alive_sin_emojis.py

O en segundo plano:
    nohup python keep_alive_sin_emojis.py > keep_alive.log 2>&1 &
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
        self.tiempos_respuesta = []
        self.mejor_tiempo = float('inf')
        self.peor_tiempo = 0
        
        # Configurar logging
        self._configurar_logging()
        
        # Configurar manejo de señales
        signal.signal(signal.SIGINT, self._manejar_senal)
        signal.signal(signal.SIGTERM, self._manejar_senal)
        
        self.logger.info("=== SISTEMA KEEP-ALIVE INICIADO ===")
        self.logger.info(f"URL de la API: {API_URL}")
        self.logger.info(f"Intervalo: {INTERVALO_SEGUNDOS} segundos")
        self.logger.info(f"Pregunta de prueba: {PREGUNTA_SIMPLE}")
    
    def _configurar_logging(self):
        """Configurar el sistema de logging"""
        # Crear directorio de logs si no existe
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar formato de logging
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configurar handler para archivo
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # Configurar handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        # Configurar logger
        self.logger = logging.getLogger('KeepAliveAPI')
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _manejar_senal(self, signum, frame):
        """Manejar señales del sistema para cierre limpio"""
        self.logger.info(f"Recibida señal {signum}. Cerrando sistema...")
        self.mostrar_estadisticas()
        self.guardar_estadisticas()
        sys.exit(0)
    
    def verificar_salud_api(self) -> bool:
        """Verificar que la API esté funcionando correctamente"""
        try:
            url_salud = f"{API_URL}/health"
            self.logger.info(f"Verificando salud de la API: {url_salud}")
            
            response = requests.get(
                url_salud,
                timeout=TIMEOUT_SALUD,
                headers={'User-Agent': 'KeepAlive-System/1.0'}
            )
            
            if response.status_code == 200:
                self.logger.info("API saludable - Status: 200")
                return True
            else:
                self.logger.warning(f"API con problemas - Status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al verificar salud de la API: {e}")
            return False
    
    def mantener_api_activa(self) -> bool:
        """Hacer una consulta a la API para mantenerla activa"""
        try:
            url_consulta = f"{API_URL}/chat"
            self.logger.info(f"Manteniendo API activa con pregunta: {PREGUNTA_SIMPLE}")
            
            inicio = time.time()
            
            response = requests.post(
                url_consulta,
                json={"pregunta": PREGUNTA_SIMPLE},
                timeout=TIMEOUT_CONSULTA,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'KeepAlive-System/1.0'
                }
            )
            
            tiempo_respuesta = time.time() - inicio
            
            if response.status_code == 200:
                self.contador_exitos += 1
                self.ultima_respuesta_exitosa = datetime.now()
                self._actualizar_estadisticas(tiempo_respuesta)
                self.logger.info(f"API activa - Respuesta en {tiempo_respuesta:.2f}s")
                return True
            else:
                self.logger.warning(f"Respuesta inesperada - Status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al mantener API activa: {e}")
            return False
    
    def _actualizar_estadisticas(self, tiempo_respuesta: float):
        """Actualizar estadísticas de rendimiento"""
        self.tiempos_respuesta.append(tiempo_respuesta)
        
        # Mantener solo los últimos 100 tiempos
        if len(self.tiempos_respuesta) > 100:
            self.tiempos_respuesta = self.tiempos_respuesta[-100:]
        
        # Actualizar mejor y peor tiempo
        if tiempo_respuesta < self.mejor_tiempo:
            self.mejor_tiempo = tiempo_respuesta
        if tiempo_respuesta > self.peor_tiempo:
            self.peor_tiempo = tiempo_respuesta
    
    def mostrar_estadisticas(self):
        """Mostrar estadísticas detalladas"""
        if not self.tiempos_respuesta:
            return
        
        tiempo_promedio = sum(self.tiempos_respuesta) / len(self.tiempos_respuesta)
        
        self.logger.info("=== ESTADISTICAS DETALLADAS ===")
        self.logger.info(f"   • Exitos totales: {self.contador_exitos}")
        self.logger.info(f"   • Fallos totales: {self.contador_fallos}")
        self.logger.info(f"   • Reintentos: {self.contador_reintentos}")
        self.logger.info(f"   • Mejor tiempo: {self.mejor_tiempo:.2f}s")
        self.logger.info(f"   • Peor tiempo: {self.peor_tiempo:.2f}s")
        self.logger.info(f"   • Tiempo promedio: {tiempo_promedio:.2f}s")
        
        if self.ultima_respuesta_exitosa:
            self.logger.info(f"   • Ultima respuesta exitosa: {self.ultima_respuesta_exitosa.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def guardar_estadisticas(self):
        """Guardar estadísticas en archivo JSON"""
        try:
            stats = {
                "timestamp": datetime.now().isoformat(),
                "exitos_totales": self.contador_exitos,
                "fallos_totales": self.contador_fallos,
                "reintentos": self.contador_reintentos,
                "mejor_tiempo": self.mejor_tiempo,
                "peor_tiempo": self.peor_tiempo,
                "tiempo_promedio": sum(self.tiempos_respuesta) / len(self.tiempos_respuesta) if self.tiempos_respuesta else 0,
                "ultima_respuesta_exitosa": self.ultima_respuesta_exitosa.isoformat() if self.ultima_respuesta_exitosa else None,
                "total_consultas": len(self.tiempos_respuesta)
            }
            
            with open("estadisticas_keep_alive.json", "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error al guardar estadísticas: {e}")
    
    def ejecutar(self):
        """Ejecutar el sistema Keep-Alive"""
        self.logger.info("Iniciando sistema Keep-Alive...")
        
        while True:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.logger.info(f"\n{timestamp} - Ejecutando verificacion...")
                
                # Verificar salud de la API
                salud_ok = self.verificar_salud_api()
                
                if salud_ok:
                    # Mantener API activa
                    api_activa = self.mantener_api_activa()
                    
                    if not api_activa:
                        self.contador_fallos += 1
                        self.logger.warning("Fallo al mantener API activa")
                else:
                    self.contador_fallos += 1
                    self.logger.warning("API no saludable")
                
                # Mostrar estadísticas cada 5 consultas
                if self.contador_exitos % 5 == 0 and self.contador_exitos > 0:
                    self.mostrar_estadisticas()
                    self.guardar_estadisticas()
                
                # Esperar hasta la próxima consulta
                self.logger.info(f"Esperando {INTERVALO_SEGUNDOS} segundos hasta la proxima consulta...")
                time.sleep(INTERVALO_SEGUNDOS)
                
            except KeyboardInterrupt:
                self.logger.info("Interrupcion del usuario. Cerrando sistema...")
                break
            except Exception as e:
                self.logger.error(f"Error inesperado: {e}")
                time.sleep(10)  # Esperar antes de reintentar

def main():
    """Función principal"""
    try:
        keep_alive = KeepAliveAPI()
        keep_alive.ejecutar()
    except Exception as e:
        print(f"Error al iniciar el sistema Keep-Alive: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

