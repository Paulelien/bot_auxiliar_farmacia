@echo off
REM Script de Windows para ejecutar el Keep-Alive de la API
REM Ejecutar como administrador para mejor rendimiento

echo ========================================
echo    KEEP-ALIVE API - WINDOWS
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si existe el archivo principal
if not exist "keep_alive_avanzado.py" (
    echo ERROR: No se encontró keep_alive_avanzado.py
    echo Asegúrate de estar en el directorio correcto
    pause
    exit /b 1
)

REM Crear directorio de logs si no existe
if not exist "logs" mkdir logs

echo Iniciando Keep-Alive para la API...
echo.
echo Presiona Ctrl+C para detener
echo.

REM Ejecutar el keep-alive
python keep_alive_avanzado.py

echo.
echo Keep-Alive detenido
pause
