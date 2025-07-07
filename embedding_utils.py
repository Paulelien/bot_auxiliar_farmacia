import faiss
import numpy as np
import openai
import os
import pickle

EMBEDDING_MODEL = "text-embedding-3-small"
INDICE_PATH = "material/faiss_index.bin"
TEXTOS_PATH = "material/textos.pkl"

# Función para obtener embedding de un texto
def obtener_embedding(texto):
    from openai import OpenAI
    client = OpenAI()
    resp = client.embeddings.create(
        input=texto,
        model=EMBEDDING_MODEL
    )
    return np.array(resp.data[0].embedding, dtype=np.float32)

# Crear o cargar índice FAISS
def cargar_o_crear_indice(textos_con_metadatos):
    if os.path.exists(INDICE_PATH) and os.path.exists(TEXTOS_PATH):
        with open(TEXTOS_PATH, "rb") as f:
            textos_con_metadatos = pickle.load(f)
        index = faiss.read_index(INDICE_PATH)
        return index, textos_con_metadatos
    
    # Extraer solo los textos para crear embeddings
    textos_solo = [item["texto"] for item in textos_con_metadatos]
    
    # Crear embeddings y FAISS
    embeddings = np.vstack([obtener_embedding(t) for t in textos_solo])
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.astype('float32'))
    faiss.write_index(index, INDICE_PATH)
    with open(TEXTOS_PATH, "wb") as f:
        pickle.dump(textos_con_metadatos, f)
    return index, textos_con_metadatos

# Buscar textos más similares
def buscar_similares(pregunta, index, textos_con_metadatos, k=3):
    emb = obtener_embedding(pregunta).reshape(1, -1)
    D, I = index.search(emb, k)
    resultados = []
    for idx in I[0]:
        resultados.append(textos_con_metadatos[idx])
    return resultados 