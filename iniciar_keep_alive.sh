#!/bin/bash

# Sistema Keep-Alive API - Bot Farmacia
# Script para Linux/Mac

echo "========================================"
echo "    SISTEMA KEEP-ALIVE API"
echo "    Bot Auxiliar de Farmacia"
echo "========================================"
echo

# Verificar Python
echo "[1/5] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python3 no está instalado"
    echo "Por favor, instala Python desde https://python.org"
    exit 1
fi
echo "✅ Python encontrado: $(python3 --version)"
echo

# Verificar dependencias
echo "[2/5] Verificando dependencias..."
if ! python3 -c "import requests" &> /dev/null; then
    echo "⚠️ Instalando dependencias..."
    pip3 install requests python-dotenv
    if [ $? -ne 0 ]; then
        echo "❌ Error instalando dependencias"
        exit 1
    fi
fi
echo "✅ Dependencias verificadas"
echo

# Crear directorio de logs
echo "[3/5] Preparando directorio de logs..."
mkdir -p logs
echo "✅ Directorio de logs listo"
echo

# Verificar archivos
echo "[4/5] Verificando archivos del sistema..."
if [ ! -f "keep_alive_avanzado.py" ]; then
    echo "❌ ERROR: No se encontró keep_alive_avanzado.py"
    exit 1
fi
if [ ! -f "config_keep_alive.py" ]; then
    echo "❌ ERROR: No se encontró config_keep_alive.py"
    exit 1
fi
echo "✅ Archivos del sistema verificados"
echo

# Mostrar configuración
echo "[5/5] Configuración del sistema:"
echo
echo "🌐 URL de la API: https://asistente-auxiliar-farmacia.onrender.com"
echo "⏰ Intervalo de consulta: 60 segundos"
echo "📁 Logs se guardarán en: logs/"
echo
echo "========================================"
echo "    INICIANDO SISTEMA KEEP-ALIVE"
echo "========================================"
echo
echo "El sistema se ejecutará cada 60 segundos"
echo "Presiona Ctrl+C para detener"
echo
echo "Iniciando en 3 segundos..."
sleep 3

# Ejecutar el keep-alive
python3 keep_alive_avanzado.py

echo
echo "========================================"
echo "    SISTEMA DETENIDO"
echo "========================================"
echo
echo "Para ver logs: tail -f logs/keep_alive.log"
echo "Para ver estadísticas: cat logs/keep_alive_stats.json"
echo
