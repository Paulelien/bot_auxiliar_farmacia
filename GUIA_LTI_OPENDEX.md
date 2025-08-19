# 🚀 Guía de Integración LTI con Open edX

## 📋 ¿Qué es LTI?

**LTI (Learning Tools Interoperability)** es un estándar que permite integrar herramientas externas directamente dentro de Open edX, proporcionando una experiencia unificada para los estudiantes.

## 🎯 Ventajas de la Integración LTI

- ✅ **Integración nativa** en Open edX
- ✅ **Autenticación automática** de usuarios
- ✅ **Compartir datos** entre el bot y el LMS
- ✅ **Experiencia unificada** para los estudiantes
- ✅ **Estándar reconocido** por la industria
- ✅ **Sin necesidad de login** separado

## 🔧 Configuración en Open edX

### 1. **Acceder como Administrador**
- Inicia sesión en Open edX como administrador
- Ve a **Studio** (panel de administración)

### 2. **Crear Nueva Herramienta LTI**
- En tu curso, ve a **Content** → **Advanced**
- Selecciona **LTI Consumer**
- Haz clic en **Add LTI Consumer**

### 3. **Configurar la Herramienta**
```
Título: Bot Asistente Virtual de Farmacia
Descripción: Asistente virtual especializado en farmacología
LTI ID: bot_farmacia
```

### 4. **Configuración de URLs**
```
LTI URL: https://tu-bot.onrender.com/lti/launch
LTI Key: [Tu Consumer Key]
LTI Secret: [Tu Consumer Secret]
```

### 5. **Configuración Avanzada**
```
Launch Target: New Window
Privacy Level: Public
Send User Data: Yes
```

## 🔑 Obtener Credenciales LTI

### **Opción 1: Generar Credenciales Propias**
```bash
# Generar Consumer Key
openssl rand -hex 16
# Ejemplo: a1b2c3d4e5f6g7h8

# Generar Consumer Secret
openssl rand -base64 32
# Ejemplo: xYz123AbC456DeF789GhI012JkL345MnO678PqR
```

### **Opción 2: Usar Credenciales de Prueba**
```bash
Consumer Key: test_consumer_key
Consumer Secret: test_consumer_secret
```

## 🌐 Configuración en Variables de Entorno

### **En Render (Producción)**
```bash
LTI_CONSUMER_KEY=tu_consumer_key_aqui
LTI_CONSUMER_SECRET=tu_consumer_secret_aqui
```

### **En Local (Desarrollo)**
```bash
# Crear archivo .env
LTI_CONSUMER_KEY=test_consumer_key
LTI_CONSUMER_SECRET=test_consumer_secret
```

## 📱 Endpoints LTI Disponibles

### **1. Configuración LTI**
```
GET /lti/config
```
Retorna la configuración JSON para Open edX

### **2. Configuración XML**
```
GET /lti/xml
```
Retorna el archivo XML para importar en Open edX

### **3. Lanzamiento LTI**
```
POST /lti/launch
```
Endpoint principal que recibe las solicitudes desde Open edX

### **4. Prueba de Integración**
```
GET /lti/test
```
Verifica que la integración LTI esté funcionando

## 🧪 Probar la Integración

### **1. Verificar Endpoints**
```bash
# Probar configuración
curl https://tu-bot.onrender.com/lti/config

# Probar XML
curl https://tu-bot.onrender.com/lti/xml

# Probar integración
curl https://tu-bot.onrender.com/lti/test
```

### **2. Probar desde Open edX**
- Ve a tu curso en Open edX
- Busca la herramienta LTI agregada
- Haz clic en ella
- Debería abrirse el bot integrado

## 🔍 Flujo de Integración LTI

```
1. Estudiante hace clic en la herramienta LTI en Open edX
2. Open edX envía solicitud POST a /lti/launch
3. El bot valida la autenticación OAuth
4. Se extrae información del usuario (nombre, email, rol)
5. Se crea sesión personalizada
6. Se muestra interfaz del bot integrada
7. El estudiante interactúa con el bot
8. Los datos se sincronizan con Open edX
```

## 📊 Datos Compartidos

### **Información del Usuario**
- ✅ ID único del usuario
- ✅ Nombre completo
- ✅ Email
- ✅ Rol en el curso
- ✅ ID del contexto (curso)

### **Información del Curso**
- ✅ Título del curso
- ✅ ID del curso
- ✅ Instancia de Open edX
- ✅ URL de la herramienta

## 🛠️ Solución de Problemas

### **Error 401: Solicitud LTI Inválida**
- Verificar Consumer Key y Secret
- Comprobar timestamp (no más de 5 minutos)
- Verificar firma OAuth

### **Error 500: Error Interno**
- Revisar logs del servidor
- Verificar configuración de variables de entorno
- Comprobar importaciones de módulos

### **Bot no se abre en Open edX**
- Verificar URL de lanzamiento
- Comprobar configuración de privacidad
- Revisar permisos del usuario

## 📈 Monitoreo y Analytics

### **Logs de Integración LTI**
```python
# Los logs incluyen:
- Usuarios que acceden vía LTI
- Tiempo de sesión
- Preguntas realizadas
- Errores de autenticación
```

### **Métricas LTI**
- Usuarios únicos por curso
- Frecuencia de uso
- Tiempo promedio de sesión
- Preguntas más populares

## 🔒 Seguridad

### **Autenticación OAuth 1.0**
- Firma HMAC-SHA1
- Timestamp de expiración
- Nonce único por solicitud
- Validación de parámetros

### **Validaciones de Seguridad**
- Verificación de firma
- Validación de timestamp
- Comprobación de parámetros requeridos
- Sanitización de datos de entrada

## 🚀 Próximos Pasos

### **1. Implementar Sincronización de Datos**
- Enviar resultados de quiz a Open edX
- Sincronizar progreso del estudiante
- Compartir analytics con el instructor

### **2. Personalización por Curso**
- Configuraciones específicas por curso
- Materiales personalizados
- Casos clínicos adaptados

### **3. Integración con Calificaciones**
- Enviar puntajes a Open edX
- Sincronizar evaluaciones
- Reportes de progreso

## 📞 Soporte

### **Documentación Adicional**
- [Especificación LTI 1.0](https://www.imsglobal.org/specs/ltiv1p0)
- [Open edX LTI Documentation](https://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/exercises_tools/lti.html)

### **Comunidad**
- [Open edX Community](https://open.edx.org/community/)
- [LTI Developers Group](https://www.imsglobal.org/community/developers)

---

**🏥 Bot Asistente Virtual de Farmacia - Integración LTI**
*Desarrollado para el curso de Auxiliar de Farmacia*


