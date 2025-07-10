# 🤖 Chatbot Educativo: Auxiliar de Farmacia

Chatbot inteligente para el curso de Auxiliar de Farmacia, desarrollado con **FastAPI**, **HTML/CSS/JavaScript** y **OpenAI**.

## 🚀 Características

- **API REST** con FastAPI para procesamiento de preguntas
- **Frontend moderno** con HTML5, CSS3 y JavaScript vanilla
- **Búsqueda semántica** en material del curso usando embeddings
- **Quiz interactivo** con preguntas de práctica
- **Preguntas frecuentes** automáticas
- **Historial de conversaciones** persistente
- **Preguntas sugeridas** dinámicas
- **Exportación de chats** en formato texto
- **Interfaz responsive** y moderna

## 🏗️ Arquitectura

### Backend (FastAPI)
- **Framework**: FastAPI + Uvicorn
- **IA**: OpenAI GPT + Embeddings
- **Búsqueda**: FAISS para similitud vectorial
- **Procesamiento**: PyMuPDF para documentos

### Frontend (HTML/CSS/JS)
- **Tecnologías**: HTML5, CSS3, JavaScript Vanilla
- **Diseño**: Responsive con paleta de colores Avanxa
- **Funcionalidades**: Chat, Quiz, Estadísticas, Exportación

## 📋 Requisitos

- Python 3.8+
- OpenAI API Key
- Dependencias listadas en `requirements.txt`

## 🛠️ Instalación Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Paulelien/bot_auxiliar_farmacia.git
cd bot_auxiliar_farmacia
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
pip install fastapi uvicorn
```

3. **Configurar API Key:**
```bash
# Crear archivo .env
echo OPENAI_API_KEY=tu_clave_aqui > .env
```

4. **Agregar material del curso:**
- Colocar PDFs en la carpeta `material/`
- El bot procesará automáticamente todos los archivos

5. **Ejecutar la API:**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

6. **Abrir el frontend:**
- Abrir `frontend.html` en tu navegador
- O usar un servidor local: `python -m http.server 8080`

## 🌐 Despliegue

### Opción 1: Render.com (Recomendado)
1. **Conectar repositorio** a Render
2. **Configurar servicio web** con FastAPI
3. **Variables de entorno**: `OPENAI_API_KEY`
4. **Comando de inicio**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

### Opción 2: Railway
1. **Conectar repositorio** a Railway
2. **Configurar variables** de entorno
3. **Deploy automático**

### Opción 3: Heroku
1. **Crear app** en Heroku
2. **Conectar repositorio**
3. **Configurar buildpack**: Python
4. **Variables de entorno**: `OPENAI_API_KEY`

## 📁 Estructura del Proyecto

```
bot_auxiliar_farmacia/
├── api.py                 # API FastAPI principal
├── app.py                 # Aplicación Streamlit (alternativa)
├── frontend.html          # Frontend principal
├── faq.py                 # Preguntas frecuentes
├── pdf_utils.py           # Procesamiento de PDFs
├── embedding_utils.py     # Búsqueda semántica
├── requirements.txt       # Dependencias Python
├── .env                   # Variables de entorno
├── .gitignore            # Archivos ignorados
├── logo_avanxa.png       # Logo institucional
└── material/              # Documentos del curso
    ├── *.pdf             # PDFs del curso
    └── *.txt             # Archivos de texto
```

## 🔧 Configuración

### Variables de Entorno
- `OPENAI_API_KEY`: Clave de API de OpenAI

### Endpoints de la API
- `GET /` - Información de la API
- `POST /preguntar` - Procesar pregunta
- `GET /preguntas_sugeridas` - Obtener sugerencias
- `GET /quiz_preguntas/{cantidad}` - Preguntas para quiz
- `GET /preguntas_frecuentes` - Estadísticas de uso

## 📊 Uso

### Chat Principal
1. **Escribir pregunta** en el campo de texto
2. **Presionar "Preguntar"** o Enter
3. **Recibir respuesta** basada en el material del curso

### Quiz de Práctica
1. **Hacer clic** en "Iniciar quiz"
2. **Responder** 7 preguntas de opción múltiple
3. **Ver puntaje** final y retroalimentación

### Funciones Adicionales
- **Preguntas sugeridas**: Botones para preguntas rápidas
- **Historial**: Conversaciones guardadas localmente
- **Exportar**: Descargar conversación en formato .txt
- **Estadísticas**: Ver preguntas más frecuentes

## 🎯 Funcionalidades

### Backend
- ✅ API REST con FastAPI
- ✅ Búsqueda semántica con embeddings
- ✅ Procesamiento de PDFs
- ✅ Generación de respuestas con GPT
- ✅ Sistema de quiz dinámico
- ✅ Estadísticas de uso

### Frontend
- ✅ Interfaz moderna y responsive
- ✅ Chat en tiempo real
- ✅ Quiz interactivo
- ✅ Historial persistente
- ✅ Exportación de datos
- ✅ Preguntas sugeridas

## 🔒 Seguridad

- API Key protegida en variables de entorno
- CORS configurado para comunicación segura
- No se almacenan datos sensibles
- Conversaciones locales (localStorage)

## 📈 Monitoreo

- Estadísticas de uso en tiempo real
- Contador de preguntas realizadas
- Categorización automática de consultas
- Reportes de preguntas frecuentes

## 🎨 Diseño

### Paleta de Colores (Avanxa)
- **Primario**: #4B2067 (Morado oscuro institucional)
- **Secundario**: #7C3FAF (Morado claro)
- **Acento**: #FF6B35 (Naranja para alertas)
- **Texto**: #2C3E50 (Azul oscuro)
- **Fondo**: #F8F9FA (Gris muy claro)

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crear rama para nueva funcionalidad: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m "Agregar nueva funcionalidad"`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 📞 Soporte

Para soporte técnico o preguntas sobre el curso:
- **Issues**: Crear issue en GitHub
- **Email**: Contactar al administrador del sistema
- **Documentación**: Revisar este README

## 🚀 Roadmap

- [ ] Integración con base de datos
- [ ] Sistema de usuarios
- [ ] Más tipos de preguntas
- [ ] Análisis de progreso
- [ ] Notificaciones push
- [ ] Modo offline 