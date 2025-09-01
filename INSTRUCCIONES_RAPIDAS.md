# 🚀 INSTRUCCIONES RÁPIDAS - Sistema Keep-Alive

## ⚡ **INICIO SUPER RÁPIDO (Windows)**

### **Opción 1: Doble clic (Más fácil)**
1. **Hacer doble clic** en `iniciar_keep_alive.bat`
2. **Esperar** a que se inicie automáticamente
3. **¡Listo!** El sistema se ejecutará cada 60 segundos

### **Opción 2: Desde línea de comandos**
```cmd
# Abrir cmd como administrador
iniciar_keep_alive.bat
```

## 🐧 **INICIO SUPER RÁPIDO (Linux/Mac)**

```bash
# Hacer ejecutable y ejecutar
chmod +x iniciar_keep_alive.sh
./iniciar_keep_alive.sh
```

## 🔧 **CONFIGURACIÓN PERSONALIZADA**

### **Editar configuración:**
```bash
# Editar archivo de configuración
nano mi_configuracion.py

# O en Windows
notepad mi_configuracion.py
```

### **Cambios comunes:**
```python
# Cambiar intervalo de consulta
INTERVALO_SEGUNDOS = 30  # Cada 30 segundos

# Cambiar pregunta
PREGUNTA_SIMPLE = "¿Cuál es el objetivo del curso?"

# Cambiar URL de API
API_URL = "https://tu-nueva-api.com"
```

## 📊 **MONITOREO EN TIEMPO REAL**

### **Ver logs:**
```bash
# Windows
Get-Content logs/keep_alive.log -Wait

# Linux/Mac
tail -f logs/keep_alive.log
```

### **Ver estadísticas:**
```bash
# Ver estadísticas actuales
cat logs/keep_alive_stats.json

# Con formato bonito (si tienes jq)
cat logs/keep_alive_stats.json | jq .
```

## 🛑 **DETENER EL SISTEMA**

### **Si está en primer plano:**
- Presionar `Ctrl+C`

### **Si está en segundo plano:**
```bash
# Encontrar proceso
ps aux | grep keep_alive

# Matar proceso
pkill -f keep_alive_avanzado.py
```

## 🔍 **VERIFICAR FUNCIONAMIENTO**

### **Comandos de verificación:**
```bash
# Ver si está ejecutándose
ps aux | grep keep_alive

# Ver logs recientes
tail -n 20 logs/keep_alive.log

# Ver estadísticas
ls -la logs/
```

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Error: "ModuleNotFoundError"**
```bash
pip install requests python-dotenv
```

### **Error: "Connection refused"**
- Verificar que tu API esté funcionando
- Verificar la URL en `mi_configuracion.py`

### **Error: "Timeout"**
- Aumentar timeouts en `mi_configuracion.py`
- Verificar velocidad de conexión

## 📈 **MÉTRICAS ESPERADAS**

### **Antes del Keep-Alive:**
- Primera pregunta: 15-30 segundos
- Preguntas siguientes: 2-5 segundos

### **Después del Keep-Alive:**
- Primera pregunta: 2-5 segundos ⚡
- Preguntas siguientes: 2-5 segundos

### **Mejora:**
- **Reducción del 80-90%** en tiempo de primera respuesta

## 🎯 **ARCHIVOS IMPORTANTES**

```
📁 Tu Proyecto/
├── 🚀 iniciar_keep_alive.bat      # Script Windows
├── 🐧 iniciar_keep_alive.sh       # Script Linux/Mac
├── ⚙️ mi_configuracion.py         # Configuración personalizada
├── 🔧 keep_alive_avanzado.py      # Sistema principal
├── 📊 logs/                       # Logs y estadísticas
└── 📋 INSTRUCCIONES_RAPIDAS.md    # Este archivo
```

## 🎉 **¡LISTO PARA USAR!**

1. **Hacer doble clic** en `iniciar_keep_alive.bat` (Windows)
2. **O ejecutar** `./iniciar_keep_alive.sh` (Linux/Mac)
3. **El sistema se ejecutará automáticamente** cada 60 segundos
4. **Tu API estará siempre activa** y responderá rápidamente

---

**¿Problemas?** Revisa los logs en `logs/keep_alive.log`
**¿Dudas?** Lee el `README_keep_alive.md` completo
