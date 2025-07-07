# Preguntas frecuentes del curso Auxiliar de Farmacia
FAQ = {
    "¿dónde puedo descargar mi certificado?": "El certificado se puede descargar directamente desde la plataforma. Para hacerlo, dirígete al menú superior y haz clic en la pestaña \"Progreso\". Allí encontrarás la opción para descargar tu certificado, una vez cumplas con los requisitos del curso.",
    
    "la plataforma dice que tengo habilitada la descarga del certificado, pero aún me faltan actividades por corregir. ¿estas actividades, cuando se corrijan, se actualizará el porcentaje?": "Sí. Cuando se corrigen las actividades pendientes, el porcentaje de avance se actualiza automáticamente. Esto ocurre porque, por defecto, la plataforma habilita la descarga del certificado al alcanzar un 60% de progreso.\n\nSi descargaste el certificado antes de que se corrigieran todas tus actividades, deberás regenerarlo. Para hacerlo, ve al menú superior, haz clic en \"Progreso\", y selecciona la opción \"Regenerar certificado\". Luego podrás descargar la versión actualizada.",
    
    "necesito saber cuánto dura el curso, cuál es el estado actual del curso, y si tengo prórroga.": "Para consultar la duración del curso, el estado actual de tu progreso, si tienes prórroga activa o el estado de la misma, por favor comunícate directamente con tu tutor a través del correo de soporte. Él podrá entregarte información actualizada y específica según tu caso."
}

def buscar_en_faq(pregunta_usuario):
    pregunta_usuario = pregunta_usuario.strip().lower()
    
    # Limpiar signos de puntuación para búsqueda más flexible
    pregunta_limpia = pregunta_usuario.replace('¿', '').replace('?', '').replace('¡', '').replace('!', '')
    
    # Definir palabras clave para cada pregunta del FAQ
    palabras_clave_faq = {
        "¿dónde puedo descargar mi certificado?": ["dónde", "descargar", "certificado", "plataforma", "progreso"],
        "la plataforma dice que tengo habilitada la descarga del certificado, pero aún me faltan actividades por corregir. ¿estas actividades, cuando se corrijan, se actualizará el porcentaje?": ["plataforma", "certificado", "actividades", "corregir", "porcentaje", "actualizar", "regenerar"],
        "necesito saber cuánto dura el curso, cuál es el estado actual del curso, y si tengo prórroga.": ["duración", "curso", "estado", "prórroga", "tutor", "soporte"],
    }
    
    # Buscar coincidencias por palabras clave
    for pregunta_faq, palabras_clave in palabras_clave_faq.items():
        # Contar cuántas palabras clave coinciden
        coincidencias = sum(1 for palabra in palabras_clave if palabra in pregunta_limpia)
        
        # Si al menos 2 palabras clave coinciden, considerar una match
        if coincidencias >= 2:
            return FAQ[pregunta_faq]
    
    # Búsqueda original como respaldo
    for pregunta, respuesta in FAQ.items():
        pregunta_sin_signos = pregunta.replace('¿', '').replace('?', '')
        if pregunta_sin_signos in pregunta_limpia or pregunta_limpia in pregunta_sin_signos:
            return respuesta
    
    return None 