import faiss
import numpy as np
import openai
import os
import pickle
from config import (
    UMBRAL_SIMILITUD_PRINCIPAL, 
    UMBRAL_SIMILITUD_SECUNDARIO,
    K_MAX_RESULTADOS,
    MODELO_EMBEDDING,
    INDICE_FAISS_PATH,
    TEXTOS_PATH,
    MOSTRAR_DEBUG,
    MOSTRAR_SIMILITUD
)

# Función para obtener embedding de un texto
def obtener_embedding(texto):
    from openai import OpenAI
    client = OpenAI()
    resp = client.embeddings.create(
        input=texto,
        model=MODELO_EMBEDDING
    )
    return np.array(resp.data[0].embedding, dtype=np.float32)

# Crear o cargar índice FAISS
def cargar_o_crear_indice(textos_con_metadatos):
    if os.path.exists(INDICE_FAISS_PATH) and os.path.exists(TEXTOS_PATH):
        try:
            with open(TEXTOS_PATH, "rb") as f:
                textos_con_metadatos = pickle.load(f)
            index = faiss.read_index(INDICE_FAISS_PATH)
            return index, textos_con_metadatos
        except Exception as e:
            print(f"Error cargando archivos existentes: {e}")
            # Si falla la carga, continuar con la creación
    
    # Verificar que hay textos para procesar
    if not textos_con_metadatos:
        print("No hay textos para procesar. Creando índice vacío.")
        # Crear un índice vacío con dimensión estándar
        dimension = 1536  # Dimensión de text-embedding-3-small
        index = faiss.IndexFlatL2(dimension)
        return index, []
    
    # Extraer solo los textos para crear embeddings
    textos_solo = [item["texto"] for item in textos_con_metadatos]
    
    if not textos_solo:
        print("No hay textos válidos para crear embeddings.")
        dimension = 1536
        index = faiss.IndexFlatL2(dimension)
        return index, []
    
    # Crear embeddings y FAISS
    embeddings = np.vstack([obtener_embedding(t) for t in textos_solo])
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.astype('float32'))
    faiss.write_index(index, INDICE_FAISS_PATH)
    with open(TEXTOS_PATH, "wb") as f:
        pickle.dump(textos_con_metadatos, f)
    return index, textos_con_metadatos

# Buscar textos más similares con umbral
def buscar_similares(pregunta, index, textos_con_metadatos, k=3, umbral=None):
    # Verificar si el índice está vacío
    if not textos_con_metadatos:
        print("Sin textos disponibles. Retornando lista vacía.")
        return []
    
    # Usar umbral por defecto si no se especifica
    if umbral is None:
        umbral = UMBRAL_SIMILITUD_PRINCIPAL
    
    try:
        emb = obtener_embedding(pregunta).reshape(1, -1)
        # Buscar más resultados para poder filtrar por umbral
        D, I = index.search(emb, min(K_MAX_RESULTADOS, len(textos_con_metadatos)))
        
        resultados = []
        for i, (distancia, idx) in enumerate(zip(D[0], I[0])):
            if idx < len(textos_con_metadatos):
                # Convertir distancia a similitud (FAISS usa distancia L2, menor = más similar)
                # Normalizar la similitud entre 0 y 1
                similitud = 1.0 / (1.0 + distancia)
                
                # Solo incluir resultados que superen el umbral
                if similitud >= umbral:
                    texto_con_metadatos = textos_con_metadatos[idx]
                    texto_con_metadatos['similitud'] = similitud
                    texto_con_metadatos['distancia'] = distancia
                    resultados.append(texto_con_metadatos)
                    if MOSTRAR_DEBUG:
                        print(f"Resultado {i+1}: Similitud = {similitud:.3f}, Distancia = {distancia:.3f}")
                else:
                    if MOSTRAR_DEBUG:
                        print(f"Resultado {i+1} descartado: Similitud = {similitud:.3f} < umbral {umbral}")
        
        # Ordenar por similitud (mayor primero)
        resultados.sort(key=lambda x: x['similitud'], reverse=True)
        
        # Limitar a k resultados
        resultados = resultados[:k]
        
        if MOSTRAR_DEBUG:
            print(f"Retornando {len(resultados)} resultados con similitud >= {umbral}")
        return resultados
        
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return [] 