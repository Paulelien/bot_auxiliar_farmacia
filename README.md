# 🤖 Chatbot Educativo: Auxiliar de Farmacia

Chatbot inteligente para el curso de Auxiliar de Farmacia, desarrollado con Python, Streamlit y OpenAI.

## 🚀 Características

- **Búsqueda semántica** en material del curso
- **Preguntas frecuentes** automáticas
- **Historial de conversaciones**
- **Preguntas sugeridas** dinámicas
- **Exportación de chats**
- **Interfaz intuitiva** y responsive

## 📋 Requisitos

- Python 3.8+
- OpenAI API Key
- Dependencias listadas en `requirements.txt`

## 🛠️ Instalación Local

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd bot_auxiliar_farmacia
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar API Key:**
```bash
# Crear archivo .env
echo OPENAI_API_KEY=tu_clave_aqui > .env
```

4. **Agregar material del curso:**
- Colocar PDFs en la carpeta `material/`
- El bot procesará automáticamente todos los archivos

5. **Ejecutar:**
```bash
streamlit run app.py
```

## 🌐 Despliegue en Streamlit Cloud

1. **Subir a GitHub:**
```bash
git add .
git commit -m "Preparado para producción"
git push origin main
```

2. **Conectar con Streamlit Cloud:**
- Ir a [share.streamlit.io](https://share.streamlit.io)
- Conectar cuenta de GitHub
- Seleccionar repositorio
- Configurar variables de entorno (OPENAI_API_KEY)

## 📁 Estructura del Proyecto

```
bot_auxiliar_farmacia/
├── app.py                 # Aplicación principal
├── faq.py                 # Preguntas frecuentes
├── pdf_utils.py           # Procesamiento de PDFs
├── embedding_utils.py     # Búsqueda semántica
├── requirements.txt       # Dependencias
├── .env                   # Variables de entorno
├── .streamlit/            # Configuración Streamlit
└── material/              # Documentos del curso
    ├── *.pdf             # PDFs del curso
    └── *.txt             # Archivos de texto
```

## 🔧 Configuración

### Variables de Entorno
- `OPENAI_API_KEY`: Clave de API de OpenAI

### Configuración Streamlit
- Archivo `.streamlit/config.toml` para personalización

## 📊 Uso

1. **Preguntas directas:** Escribe tu pregunta en el campo de texto
2. **Preguntas sugeridas:** Usa los botones de preguntas rápidas
3. **Historial:** Revisa conversaciones anteriores
4. **Exportar:** Descarga tu conversación completa

## 🎯 Funcionalidades

- ✅ Búsqueda en FAQ
- ✅ Búsqueda semántica en PDFs
- ✅ Respuestas con IA (GPT-3.5-turbo)
- ✅ Historial de conversaciones
- ✅ Preguntas sugeridas dinámicas
- ✅ Exportación de chats
- ✅ Estadísticas de uso
- ✅ Interfaz responsive

## 🔒 Seguridad

- API Key protegida en variables de entorno
- No se almacenan datos sensibles
- Conversaciones locales (no persistentes)

## 📈 Monitoreo

- Estadísticas de uso en tiempo real
- Contador de preguntas realizadas
- Módulos consultados

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crear rama para nueva funcionalidad
3. Commit cambios
4. Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 📞 Soporte

Para soporte técnico o preguntas sobre el curso, contactar al administrador del sistema. 