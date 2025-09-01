# 🚀 Guía Completa para Replicar el Bot para Otro Curso

## 📋 **Resumen del Proyecto Original**

Este bot de **Auxiliar de Farmacia** incluye:
- ✅ Chat inteligente con OpenAI
- ✅ Sistema de casos clínicos interactivos
- ✅ Base de datos para analytics
- ✅ Panel de administración con Streamlit
- ✅ Búsqueda semántica en material del curso
- ✅ Interfaz web responsive

## 🎯 **Pasos para Replicar**

### **1. Preparación del Entorno**

```bash
# Crear nueva carpeta para el proyecto
mkdir mi_nuevo_curso_bot
cd mi_nuevo_curso_bot

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### **2. Estructura de Carpetas**

```
mi_nuevo_curso_bot/
├── 📁 material/                 # Documentos del nuevo curso
├── 📁 material_problematico/    # Material que causa problemas
├── 📄 api.py                    # API principal (FastAPI)
├── 📄 app.py                    # Panel admin (Streamlit)
├── 📄 models.py                 # Modelos de BD
├── 📄 database_config.py        # Configuración BD
├── 📄 embedding_utils.py        # Búsqueda semántica
├── 📄 requirements.txt           # Dependencias
├── 📄 index.html                # Interfaz principal
├── 📄 casos_clinicos.json       # Casos del nuevo curso
├── 📄 prompt.txt                 # Prompt personalizado
├── 📄 Procfile                  # Para Heroku
├── 📄 render.yaml               # Para Render
└── 📄 runtime.txt               # Versión Python
```

### **3. Archivos Clave a Modificar**

#### **A. index.html - Interfaz Principal**
Cambiar:
- Título del curso
- Colores del tema CSS
- Descripción del asistente
- Casos clínicos específicos

#### **B. api.py - API Principal**
Modificar:
- Prompt del sistema
- Material de referencia
- Preguntas sugeridas
- Categorías del curso

#### **C. casos_clinicos.json - Casos Clínicos**
Crear casos relevantes para el nuevo curso

#### **D. prompt.txt - Prompt del Sistema**
Personalizar para el nuevo curso

### **4. Configuración de Variables de Entorno**

Crear archivo `.env`:
```env
OPENAI_API_KEY=tu_api_key_aqui
DATABASE_URL=sqlite:///chatbot_analytics.db
```

### **5. Personalización del Tema**

En `index.html`, cambiar las variables CSS:
```css
:root {
    --color-primario: #4B2067;      /* Color principal */
    --color-secundario: #7C3FAF;    /* Color secundario */
    --color-acento: #FF6B35;        /* Color de acento */
    --color-texto: #2C3E50;         /* Color de texto */
    --color-fondo: #F8F9FA;         /* Color de fondo */
}
```

### **6. Adaptación de Casos Clínicos**

Crear `casos_clinicos.json` con estructura:
```json
{
    "casos_clinicos": [
        {
            "id": 1,
            "titulo": "Caso del Nuevo Curso",
            "descripcion": "Descripción del caso...",
            "preguntas": [
                {
                    "id": 1,
                    "pregunta": "Pregunta del caso...",
                    "opciones": ["A) Opción 1", "B) Opción 2", "C) Opción 3", "D) Opción 4"],
                    "respuesta_correcta": 0,
                    "explicacion": "Explicación de la respuesta..."
                }
            ]
        }
    ]
}
```

### **7. Configuración de la Base de Datos**

El sistema creará automáticamente:
- Tabla de estudiantes
- Tabla de sesiones
- Tabla de preguntas
- Tabla de resultados de quiz
- Tabla de analytics diarios

### **8. Despliegue**

#### **Opción A: Render (Recomendado)**
1. Subir código a GitHub
2. Conectar con Render
3. Configurar variables de entorno
4. Desplegar automáticamente

#### **Opción B: Heroku**
1. Crear app en Heroku
2. Conectar repositorio
3. Configurar variables de entorno
4. Desplegar

#### **Opción C: Local**
```bash
# Ejecutar API
uvicorn api:app --reload

# Ejecutar panel admin
streamlit run app.py
```

## 🔧 **Personalizaciones Específicas por Curso**

### **Para Curso de Medicina:**
- Casos clínicos médicos
- Terminología médica
- Protocolos de emergencia

### **Para Curso de Enfermería:**
- Procedimientos de enfermería
- Cuidados del paciente
- Protocolos de medicación

### **Para Curso de Psicología:**
- Casos psicológicos
- Técnicas terapéuticas
- Evaluaciones psicológicas

### **Para Curso de Derecho:**
- Casos legales
- Procedimientos judiciales
- Legislación específica

## 📊 **Analytics y Monitoreo**

El sistema incluye:
- 📈 Estadísticas de uso
- 👥 Seguimiento de estudiantes
- ❓ Preguntas más frecuentes
- 🎯 Rendimiento en casos clínicos
- ⏱️ Tiempo de sesión
- 📱 Dispositivos utilizados

## 🚨 **Consideraciones Importantes**

1. **API Key de OpenAI**: Configurar en variables de entorno
2. **Material del Curso**: Asegurar que esté en formato compatible
3. **Casos Clínicos**: Crear casos relevantes y actualizados
4. **Prompt del Sistema**: Personalizar para el nuevo curso
5. **Base de Datos**: Verificar permisos y conexión
6. **CORS**: Configurar dominios permitidos

## 📞 **Soporte y Mantenimiento**

- Monitorear logs de la API
- Revisar analytics regularmente
- Actualizar casos clínicos
- Mantener material del curso actualizado
- Verificar funcionamiento de OpenAI

## 🎉 **¡Listo para Usar!**

Con esta guía podrás replicar exitosamente el bot para cualquier curso. El sistema es modular y fácil de adaptar a diferentes disciplinas académicas.

---

**¿Necesitas ayuda con algún paso específico?** ¡Estoy aquí para ayudarte!

