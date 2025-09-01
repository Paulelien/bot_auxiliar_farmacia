@echo off
title Sistema Keep-Alive API - Bot Farmacia
color 0A

echo ========================================
echo    SISTEMA KEEP-ALIVE API
echo    Bot Auxiliar de Farmacia
echo ========================================
echo.

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado
    echo Por favor, instala Python desde https://python.org
    pause
    exit /b 1
)
echo ✅ Python encontrado
echo.

REM Verificar dependencias
echo [2/5] Verificando dependencias...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Instalando dependencias...
    pip install requests python-dotenv
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
)
echo ✅ Dependencias verificadas
echo.

REM Crear directorio de logs
echo [3/5] Preparando directorio de logs...
if not exist "logs" mkdir logs
echo ✅ Directorio de logs listo
echo.

REM Verificar archivos
echo [4/5] Verificando archivos del sistema...
if not exist "keep_alive_avanzado.py" (
    echo ❌ ERROR: No se encontró keep_alive_avanzado.py
    pause
    exit /b 1
)
if not exist "config_keep_alive.py" (
    echo ❌ ERROR: No se encontró config_keep_alive.py
    pause
    exit /b 1
)
echo ✅ Archivos del sistema verificados
echo.

REM Mostrar configuración
echo [5/5] Configuración del sistema:
echo.
echo 🌐 URL de la API: https://asistente-auxiliar-farmacia.onrender.com
echo ⏰ Intervalo de consulta: 60 segundos
echo 📁 Logs se guardarán en: logs/
echo.
echo ========================================
echo    INICIANDO SISTEMA KEEP-ALIVE
echo ========================================
echo.
echo El sistema se ejecutará cada 60 segundos
echo Presiona Ctrl+C para detener
echo.
echo Iniciando en 3 segundos...
timeout /t 3 /nobreak >nul

REM Ejecutar el keep-alive
python keep_alive_avanzado.py

echo.
echo ========================================
echo    SISTEMA DETENIDO
echo ========================================
echo.
echo Para ver logs: tail -f logs/keep_alive.log
echo Para ver estadísticas: cat logs/keep_alive_stats.json
echo.
pause
