# Funciones básicas de búsqueda para reemplazar embedding_utils
# Versión simplificada para mantener la aplicación funcionando

def buscar_similares(pregunta, indice, textos, k=5, umbral=0.5):
    """
    Función simplificada de búsqueda que devuelve resultados básicos
    """
    print(f"🔍 Búsqueda simplificada para: {pregunta}")
    
    # Si no hay textos disponibles, devolver mensaje genérico
    if not textos:
        return [{"texto": "Información del curso de Auxiliar de Farmacia", "archivo": "Manual del curso", "pagina": "N/A", "similitud": 0.8}]
    
    # Búsqueda básica por palabras clave
    pregunta_lower = pregunta.lower()
    resultados = []
    
    # Buscar en los textos disponibles
    for i, texto in enumerate(textos[:k]):
        if isinstance(texto, str):
            # Calcular similitud básica por palabras coincidentes
            palabras_pregunta = set(pregunta_lower.split())
            palabras_texto = set(texto.lower().split())
            coincidencias = len(palabras_pregunta.intersection(palabras_texto))
            
            if coincidencias > 0:
                similitud = min(0.9, coincidencias / len(palabras_pregunta))
                if similitud >= umbral:
                    resultados.append({
                        "texto": texto[:500] + "..." if len(texto) > 500 else texto,
                        "archivo": f"Documento_{i+1}",
                        "pagina": "N/A",
                        "similitud": similitud
                    })
    
    # Si no hay resultados, devolver información genérica
    if not resultados:
        resultados = [{
            "texto": "Información general del curso de Auxiliar de Farmacia. Para consultas específicas, contacta a tu tutor.",
            "archivo": "Manual del curso",
            "pagina": "N/A",
            "similitud": 0.5
        }]
    
    return resultados[:k]

def cargar_o_crear_indice(textos_existentes):
    """
    Función simplificada para cargar o crear un índice básico
    """
    print("📚 Cargando índice simplificado...")
    
    # Crear un índice básico con los textos disponibles
    indice = {
        "textos": textos_existentes if textos_existentes else [],
        "configurado": True
    }
    
    print(f"✅ Índice cargado con {len(indice['textos'])} documentos")
    return indice, textos_existentes if textos_existentes else []
