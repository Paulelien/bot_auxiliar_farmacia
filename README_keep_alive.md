# 🚀 Sistema Keep-Alive para API

## 📋 **Descripción**

Este sistema mantiene tu API activa consultándola cada 60 segundos, lo que reduce significativamente el tiempo de respuesta de la primera pregunta al evitar el "cold start" en servicios como Render, Heroku, o cualquier hosting que inactiva las aplicaciones por inactividad.

## 🎯 **Beneficios**

- ✅ **Reduce el tiempo de respuesta** de la primera pregunta
- ✅ **Evita el cold start** en servicios de hosting
- ✅ **Monitorea la salud** de tu API constantemente
- ✅ **Registra estadísticas** de rendimiento
- ✅ **Reintentos automáticos** en caso de fallos
- ✅ **Logging detallado** para monitoreo
- ✅ **Ejecución como servicio** del sistema

## 📁 **Archivos del Sistema**

```
📁 Sistema Keep-Alive/
├── 📄 keep_alive.py              # Versión básica
├── 📄 keep_alive_avanzado.py     # Versión avanzada (recomendada)
├── 📄 config_keep_alive.py       # Configuración
├── 📄 keep_alive.service         # Servicio Linux
├── 📄 keep_alive_windows.bat     # Script Windows
├── 📁 logs/                      # Directorio de logs
└── 📄 README_keep_alive.md       # Este archivo
```

## 🚀 **Instalación y Configuración**

### **1. Instalar Dependencias**

```bash
pip install requests python-dotenv
```

### **2. Configurar Variables**

Edita `config_keep_alive.py` con tu URL de API:

```python
# Cambia esto por tu URL real
API_URL = "https://tu-api.onrender.com"

# Ajusta el intervalo según necesites
INTERVALO_SEGUNDOS = 60  # 1 minuto
```

### **3. Verificar Endpoints**

Asegúrate de que tu API tenga estos endpoints:
- `GET /health` - Para verificar salud
- `POST /preguntar` - Para mantener activa

## 💻 **Uso**

### **Opción A: Ejecución Manual**

```bash
# Versión básica
python keep_alive.py

# Versión avanzada (recomendada)
python keep_alive_avanzado.py
```

### **Opción B: Ejecución en Segundo Plano**

```bash
# Linux/Mac
nohup python keep_alive_avanzado.py > keep_alive.log 2>&1 &

# Windows
start /B python keep_alive_avanzado.py
```

### **Opción C: Como Servicio del Sistema**

#### **Linux (systemd)**

```bash
# 1. Editar el archivo de servicio
sudo nano /etc/systemd/system/keep_alive.service

# 2. Cambiar las rutas en el archivo
WorkingDirectory=/ruta/real/a/tu/proyecto
ExecStart=/usr/bin/python3 /ruta/real/a/tu/proyecto/keep_alive_avanzado.py

# 3. Habilitar y ejecutar
sudo systemctl daemon-reload
sudo systemctl enable keep_alive
sudo systemctl start keep_alive

# 4. Verificar estado
sudo systemctl status keep_alive
sudo journalctl -u keep_alive -f
```

#### **Windows (Servicio)**

```cmd
# Ejecutar como administrador
keep_alive_windows.bat

# O crear un servicio con NSSM
nssm install KeepAliveAPI "C:\Python39\python.exe" "C:\ruta\keep_alive_avanzado.py"
nssm start KeepAliveAPI
```

## 📊 **Monitoreo y Logs**

### **Logs en Tiempo Real**

```bash
# Linux
tail -f logs/keep_alive.log

# Windows
Get-Content logs/keep_alive.log -Wait
```

### **Estadísticas**

El sistema guarda estadísticas en `logs/keep_alive_stats.json`:

```json
{
  "fecha_actualizacion": "2024-12-19T18:30:00",
  "contador_exitos": 150,
  "contador_fallos": 2,
  "contador_reintentos": 5,
  "mejor_tiempo_respuesta": 0.85,
  "peor_tiempo_respuesta": 15.2,
  "tiempo_promedio": 2.1,
  "ultima_respuesta_exitosa": "2024-12-19T18:29:00"
}
```

### **Dashboard de Monitoreo**

```bash
# Ver estadísticas en tiempo real
watch -n 5 'cat logs/keep_alive_stats.json | jq .'
```

## ⚙️ **Configuración Avanzada**

### **Ajustar Intervalo de Consulta**

```python
# En config_keep_alive.py
INTERVALO_SEGUNDOS = 30  # Cada 30 segundos (más agresivo)
INTERVALO_SEGUNDOS = 120 # Cada 2 minutos (más conservador)
```

### **Configurar Reintentos**

```python
# En config_keep_alive.py
MAX_REINTENTOS = 5           # Más reintentos
TIEMPO_ENTRE_REINTENTOS = 10 # Más tiempo entre reintentos
```

### **Personalizar Pregunta**

```python
# En config_keep_alive.py
PREGUNTA_SIMPLE = "¿Cuál es el objetivo del curso?"  # Tu pregunta
```

## 🔧 **Solución de Problemas**

### **Error: "Connection refused"**

```bash
# Verificar que la API esté funcionando
curl https://tu-api.onrender.com/health

# Verificar firewall
sudo ufw status
```

### **Error: "Timeout"**

```bash
# Aumentar timeout en config_keep_alive.py
TIMEOUT_CONSULTA = 60  # 60 segundos
TIMEOUT_SALUD = 20     # 20 segundos
```

### **Logs muy grandes**

```bash
# Rotar logs automáticamente
sudo logrotate -f /etc/logrotate.d/keep_alive
```

### **Alto uso de CPU/Memoria**

```bash
# Verificar procesos
ps aux | grep keep_alive

# Matar proceso si es necesario
pkill -f keep_alive_avanzado.py
```

## 📈 **Métricas de Rendimiento**

### **Antes del Keep-Alive**
- Primera pregunta: 15-30 segundos
- Preguntas siguientes: 2-5 segundos

### **Después del Keep-Alive**
- Primera pregunta: 2-5 segundos
- Preguntas siguientes: 2-5 segundos

### **Mejora Esperada**
- ⚡ **Reducción del 80-90%** en tiempo de primera respuesta
- 📊 **Consistencia** en tiempos de respuesta
- 🎯 **Mejor experiencia** del usuario

## 🚨 **Consideraciones Importantes**

1. **Costo**: El keep-alive consume recursos de tu hosting
2. **Rate Limiting**: Verifica límites de tu proveedor
3. **Logs**: Monitorea el tamaño de los archivos de log
4. **Backup**: Mantén copias de la configuración
5. **Monitoreo**: Revisa logs regularmente

## 🔄 **Mantenimiento**

### **Reiniciar el Servicio**

```bash
# Linux
sudo systemctl restart keep_alive

# Windows
net stop KeepAliveAPI
net start KeepAliveAPI
```

### **Actualizar Configuración**

```bash
# Editar configuración
nano config_keep_alive.py

# Reiniciar servicio
sudo systemctl restart keep_alive
```

### **Limpiar Logs**

```bash
# Limpiar logs antiguos
find logs/ -name "*.log" -mtime +7 -delete
find logs/ -name "*.json" -mtime +30 -delete
```

## 📞 **Soporte**

### **Comandos Útiles**

```bash
# Ver estado del servicio
sudo systemctl status keep_alive

# Ver logs en tiempo real
sudo journalctl -u keep_alive -f

# Reiniciar servicio
sudo systemctl restart keep_alive

# Ver estadísticas
cat logs/keep_alive_stats.json | jq .
```

### **Verificar Funcionamiento**

```bash
# Verificar que esté ejecutándose
ps aux | grep keep_alive

# Verificar logs
tail -n 20 logs/keep_alive.log

# Verificar estadísticas
ls -la logs/
```

## 🎉 **¡Listo para Usar!**

Con este sistema keep-alive, tu API estará siempre activa y responderá rápidamente a las primeras consultas de los usuarios.

---

**¿Necesitas ayuda?** Revisa los logs en `logs/keep_alive.log` para diagnosticar problemas.
