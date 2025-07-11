# 🚀 Guía de Integración LMS - Asistente Chatbot Auxiliar de Farmacia

## 📋 Resumen

Esta guía te ayudará a integrar el asistente chatbot educativo en cualquier LMS (Learning Management System) de forma simple y efectiva.

## 🎯 ¿Qué necesitas?

1. **Archivos del widget**: `lms_widget_simple.html` y `lms_integration_simple.js`
2. **API funcionando**: `https://asistente-auxiliar-farmacia.onrender.com`
3. **Acceso a tu LMS** (Moodle, Canvas, Blackboard, etc.)

## 🔧 Pasos de Integración

### **Paso 1: Preparar los archivos**

1. Descarga los archivos:
   - `lms_widget_simple.html`
   - `lms_integration_simple.js`

2. Sube ambos archivos a tu servidor web o plataforma de hosting

### **Paso 2: Integrar en tu LMS**

#### **Opción A: Integración Directa (Recomendada)**

1. **Copia el contenido** de `lms_widget_simple.html`
2. **Pega en tu LMS** usando el editor HTML
3. **Sube el archivo JS** a tu servidor y actualiza la ruta en el HTML

#### **Opción B: Iframe (Alternativa)**

```html
<iframe 
    src="URL_DE_TU_SERVIDOR/lms_widget_simple.html" 
    width="100%" 
    height="600px" 
    frameborder="0"
    style="border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
</iframe>
```

### **Paso 3: Configurar en diferentes LMS**

#### **🌐 Moodle**

1. Ve a tu curso
2. Activa la edición
3. Agrega un recurso → Página
4. En el editor HTML, pega el contenido del widget
5. Guarda y muestra

#### **🎨 Canvas**

1. Ve a tu curso
2. Agrega una página
3. En el editor HTML, pega el contenido
4. Publica la página

#### **📚 Blackboard**

1. Ve a tu curso
2. Agrega contenido → Crear contenido → Página
3. En el editor HTML, pega el contenido
4. Envía

#### **📖 Open edX**

1. Ve al Studio
2. Agrega un componente HTML
3. Pega el contenido del widget
4. Publica

## 🔍 Verificación de Funcionamiento

### **Indicadores de Estado**

El widget muestra automáticamente el estado de conexión:

- 🟢 **API Online**: Conexión exitosa con el servidor
- 🟡 **Modo Offline**: Usando datos locales (funciona sin internet)

### **Pruebas Recomendadas**

1. **Probar conectividad**:
   - Abre la consola del navegador (F12)
   - Busca mensajes de "✅ API conectada" o "⚠️ Modo offline"

2. **Probar funcionalidad**:
   - Haz una pregunta simple
   - Verifica que recibas respuesta
   - Prueba las preguntas sugeridas

3. **Probar modo offline**:
   - Desconecta internet temporalmente
   - Verifica que el widget siga funcionando

## 🛠️ Solución de Problemas

### **Problema: No se conecta a la API**

**Síntomas:**
- Indicador muestra "🟡 Modo Offline"
- Mensajes de error en consola

**Soluciones:**
1. Verifica que la URL de la API sea correcta
2. Revisa la configuración CORS en tu LMS
3. Prueba desde un navegador diferente
4. Verifica que no haya bloqueadores de red

### **Problema: No carga el script JS**

**Síntomas:**
- El widget no responde
- Errores 404 en consola

**Soluciones:**
1. Verifica que el archivo JS esté en la ruta correcta
2. Asegúrate de que el servidor permita archivos .js
3. Usa rutas absolutas si es necesario

### **Problema: No funciona en LMS específico**

**Soluciones por LMS:**

**Moodle:**
- Usa el editor HTML completo (no el simple)
- Verifica que JavaScript esté habilitado
- Considera usar un bloque HTML personalizado

**Canvas:**
- Asegúrate de usar el editor HTML rico
- Verifica la configuración de seguridad del curso

**Blackboard:**
- Usa el editor HTML completo
- Verifica la configuración de herramientas

## 📊 Características del Widget

### **✅ Funcionalidades Incluidas**

- **Chat interactivo** con IA
- **Preguntas sugeridas** para facilitar el uso
- **Modo offline** con datos locales
- **Indicador de estado** de conexión
- **Historial de conversación** guardado localmente
- **Diseño responsive** para móviles
- **Integración automática** con la API

### **🎨 Personalización**

Puedes personalizar el widget editando:

1. **Colores**: Modifica las variables CSS en `:root`
2. **Logo**: Reemplaza el texto del header
3. **Preguntas sugeridas**: Edita el array en el JavaScript
4. **Estilo**: Modifica las clases CSS

### **📱 Responsive Design**

El widget se adapta automáticamente a:
- **Desktop**: Diseño completo con sidebar
- **Tablet**: Layout optimizado
- **Móvil**: Diseño vertical simplificado

## 🔒 Seguridad y Privacidad

### **Datos del Usuario**
- Las conversaciones se guardan **localmente** en el navegador
- **No se envían** datos personales a la API
- El historial se puede **borrar** fácilmente

### **Conexión API**
- Usa **HTTPS** para conexiones seguras
- **Timeouts** configurados para evitar bloqueos
- **Fallback** automático a modo offline

## 📈 Analytics y Reportes

### **Datos Recopilados**
- Preguntas realizadas
- Categorías consultadas
- Tiempo de uso
- Rendimiento en quizzes

### **Acceso a Reportes**
Los profesores pueden acceder a:
- Dashboard general: `/analytics/dashboard`
- Reportes individuales por estudiante
- Estadísticas de uso del sistema

## 🆘 Soporte

### **Contacto**
Si tienes problemas con la integración:
1. Revisa esta guía
2. Verifica la consola del navegador
3. Prueba en modo incógnito
4. Contacta al administrador del sistema

### **Recursos Adicionales**
- Documentación de la API
- Ejemplos de integración
- Guías específicas por LMS

---

## 🎉 ¡Listo!

Una vez completados estos pasos, tendrás un asistente chatbot educativo completamente funcional en tu LMS, con:

- ✅ Integración automática
- ✅ Modo offline
- ✅ Diseño responsive
- ✅ Analytics para profesores
- ✅ Fácil mantenimiento

¡Tu curso de Auxiliar de Farmacia ahora tiene un asistente inteligente disponible 24/7! 