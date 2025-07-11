# 🤖 Asistente Chatbot Auxiliar de Farmacia

## 📋 Descripción

Sistema educativo completo para el curso de Auxiliar de Farmacia con chatbot inteligente, sistema de quizzes, analytics y integración LMS.

## 🏗️ Arquitectura

### **Backend (FastAPI)**
- **`api.py`** - API principal con endpoints para chat, quiz y analytics
- **`app.py`** - Aplicación Streamlit (alternativa)
- **`models.py`** - Modelos de base de datos SQLAlchemy
- **`database_config.py`** - Configuración de base de datos
- **`embedding_utils.py`** - Utilidades para búsqueda semántica
- **`init_db.py`** - Script de inicialización de base de datos
- **`faq.py`** - Preguntas frecuentes
- **`pdf_utils.py`** - Utilidades para procesamiento de PDFs

### **Frontend**
- **`index.html`** - Aplicación principal completa (chat + quiz + analytics)
- **`dashboard_profesor.html`** - Panel de control para profesores
- **`lms_widget_completo.html`** - Widget simplificado para integración en LMS

### **Configuración**
- **`requirements.txt`** - Dependencias de Python
- **`runtime.txt`** - Versión de Python para Render
- **`Procfile`** - Configuración para Render
- **`render.yaml`** - Configuración de despliegue
- **`.gitignore`** - Archivos ignorados por Git

### **Recursos**
- **`logo_avanxa.png`** - Logo de la institución
- **`material/`** - Carpeta con material educativo
- **`contenido.txt`** - Contenido del curso

## 🚀 Despliegue

### **API Backend**
- **URL**: https://asistente-auxiliar-farmacia.onrender.com
- **Plataforma**: Render.com
- **Base de datos**: SQLite

### **Frontend**
- **Aplicación principal**: `index.html` (GitHub Pages o servidor web)
- **Widget LMS**: `lms_widget_completo.html` (Integración directa)

## 📊 Funcionalidades

### **Chatbot Educativo**
- ✅ Respuestas basadas en IA (OpenAI GPT-3.5-turbo)
- ✅ Búsqueda semántica en material del curso
- ✅ Preguntas frecuentes y sugeridas
- ✅ Historial de conversaciones

### **Sistema de Quiz**
- ✅ Preguntas de opción múltiple
- ✅ Evaluación automática
- ✅ Estadísticas de rendimiento
- ✅ Diferentes categorías

### **Analytics y Reportes**
- ✅ Dashboard para profesores
- ✅ Estadísticas individuales por estudiante
- ✅ Métricas de uso del sistema
- ✅ Reportes de progreso

### **Integración LMS**
- ✅ Widget autónomo para cualquier LMS
- ✅ Modo offline con respuestas locales
- ✅ Diseño responsive
- ✅ Fácil integración (copia y pega)

## 🔧 Instalación y Uso

### **1. Configurar API**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
OPENAI_API_KEY=tu_clave_api

# Inicializar base de datos
python init_db.py

# Ejecutar API
python api.py
```

### **2. Usar Aplicación Principal**
- Abrir `index.html` en navegador
- Funciona con API online u offline

### **3. Integrar en LMS**
- Copiar contenido de `lms_widget_completo.html`
- Pegar en editor HTML del LMS
- ¡Listo!

## 📱 Características Técnicas

### **Tecnologías Utilizadas**
- **Backend**: FastAPI, SQLAlchemy, OpenAI API
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Base de datos**: SQLite
- **Búsqueda**: FAISS + OpenAI Embeddings
- **IA**: GPT-3.5-turbo

### **Compatibilidad**
- ✅ Navegadores modernos (Chrome, Firefox, Safari, Edge)
- ✅ Dispositivos móviles (responsive design)
- ✅ LMS principales (Moodle, Canvas, Blackboard, Open edX)
- ✅ Modo offline (funciona sin internet)

## 📈 Analytics Disponibles

### **Métricas Generales**
- Total de estudiantes activos
- Preguntas realizadas por día
- Promedio de rendimiento en quizzes
- Categorías más consultadas

### **Reportes Individuales**
- Progreso por estudiante
- Tiempo de sesión
- Preguntas realizadas
- Rendimiento en evaluaciones

## 🔒 Seguridad y Privacidad

- ✅ Conexiones HTTPS
- ✅ Datos locales en navegador
- ✅ Sin almacenamiento de información personal
- ✅ API key segura en variables de entorno

## 🆘 Soporte

### **Problemas Comunes**
1. **API no responde**: El sistema funciona en modo offline
2. **Error de conexión**: Verificar configuración de red
3. **Widget no carga**: Verificar que JavaScript esté habilitado

### **Contacto**
- Revisar `GUIA_INTEGRACION_LMS.md` para integración
- Verificar consola del navegador para errores
- Consultar logs de la API en Render

## 📄 Licencia

Proyecto educativo para Avanxa - Curso de Auxiliar de Farmacia

---

**🎉 ¡Sistema completo y funcional para educación farmacéutica!** 