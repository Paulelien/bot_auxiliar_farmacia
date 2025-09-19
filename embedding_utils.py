"""
Utilidades de embeddings y búsqueda semántica con FAISS.
Lee PDFs desde el directorio 'material/', genera embeddings (OpenAI)
y construye un índice FAISS para recuperar pasajes relevantes.
"""

import os
import json
from typing import List, Tuple, Dict, Any

import numpy as np

try:
    import faiss  # faiss-cpu
except Exception:
    faiss = None

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
MATERIAL_DIR = os.getenv("MATERIAL_DIR", "material")
INDEX_DIR = os.getenv("INDEX_DIR", "index_store")
INDEX_PATH = os.path.join(INDEX_DIR, "indice.faiss")
METADATA_PATH = os.path.join(INDEX_DIR, "textos.json")

_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def _ensure_dirs() -> None:
    os.makedirs(INDEX_DIR, exist_ok=True)


def _read_pdf_text(pdf_path: str) -> List[Dict[str, Any]]:
    """Extrae texto por página de un PDF. Devuelve lista de dicts con texto, archivo y página."""
    if fitz is None:
        return []
    out: List[Dict[str, Any]] = []
    try:
        with fitz.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text").strip()
                if text:
                    out.append({
                        "texto": text,
                        "archivo": os.path.basename(pdf_path),
                        "pagina": page_num + 1
                    })
    except Exception:
        return []
    return out


def _read_txt_text(txt_path: str) -> List[Dict[str, Any]]:
    """Lee texto de un archivo .txt y devuelve un solo registro tipo página."""
    try:
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()
        if not text:
            return []
        return [{
            "texto": text,
            "archivo": os.path.basename(txt_path),
            "pagina": 1
        }]
    except Exception:
        return []


def _chunk_text(text: str, max_chars: int = 1200, overlap: int = 200) -> List[str]:
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks


def _embed_texts(texts: List[str]) -> np.ndarray:
    if _client is None:
        raise RuntimeError("OPENAI_API_KEY no configurada para embeddings")
    vectors: List[List[float]] = []
    for i in range(0, len(texts), 100):
        batch = texts[i:i+100]
        resp = _client.embeddings.create(model=EMBED_MODEL, input=batch)
        vectors.extend([d.embedding for d in resp.data])
    arr = np.array(vectors, dtype="float32")
    if faiss is not None:
        faiss.normalize_L2(arr)
    return arr


def _build_faiss_index(embeddings: np.ndarray):
    if faiss is None:
        return None
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


def cargar_o_crear_indice(textos_existentes: List[str]) -> Tuple[Any, List[Dict[str, Any]]]:
    """Crea o carga índice FAISS y metadatos desde 'material/'.
    Ignora el parámetro textos_existentes para compatibilidad con llamadas previas.
    """
    _ensure_dirs()
    print("📚 Cargando índice (FAISS)…")

    # Intentar cargar desde disco (si existe)
    if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH) and faiss is not None:
        try:
            index = faiss.read_index(INDEX_PATH)
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                metadatos = json.load(f)
            print(f"✅ Índice cargado con {len(metadatos)} chunks")
            return index, metadatos
        except Exception:
            print("⚠️ No se pudo cargar índice previo. Se regenerará.")

    # Recolectar documentos (PDF y TXT) de forma recursiva
    documentos: List[Dict[str, Any]] = []
    total_archivos = 0
    if os.path.isdir(MATERIAL_DIR):
        for root, _dirs, files in os.walk(MATERIAL_DIR):
            for fname in files:
                path = os.path.join(root, fname)
                lower = fname.lower()
                if lower.endswith('.pdf'):
                    total_archivos += 1
                    documentos.extend(_read_pdf_text(path))
                elif lower.endswith('.txt'):
                    total_archivos += 1
                    documentos.extend(_read_txt_text(path))

    if total_archivos:
        print(f"🔎 Detectados {total_archivos} archivos en '{MATERIAL_DIR}' (PDF/TXT)")

    if not documentos:
        print("✅ Índice cargado con 0 documentos (no se encontraron PDFs/TXTs)")
        return None, []

    # Chunking y metadatos
    textos: List[str] = []
    metadatos: List[Dict[str, Any]] = []
    for doc in documentos:
        for chunk in _chunk_text(doc["texto"]):
            textos.append(chunk)
            metadatos.append({
                "texto": chunk,
                "archivo": doc["archivo"],
                "pagina": doc["pagina"]
            })

    # Embeddings e índice
    embeddings = _embed_texts(textos)
    index = _build_faiss_index(embeddings)

    # Guardar (si FAISS disponible)
    if index is not None and faiss is not None:
        try:
            faiss.write_index(index, INDEX_PATH)
            with open(METADATA_PATH, "w", encoding="utf-8") as f:
                json.dump(metadatos, f, ensure_ascii=False)
        except Exception:
            pass

    print(f"✅ Índice generado con {len(metadatos)} chunks")
    return index, metadatos


def _embed_query(query: str) -> np.ndarray:
    vec = _client.embeddings.create(model=EMBED_MODEL, input=[query]).data[0].embedding
    arr = np.array([vec], dtype="float32")
    if faiss is not None:
        faiss.normalize_L2(arr)
    return arr


def buscar_similares(pregunta: str, indice: Any, textos: List[Dict[str, Any]], k: int = 5, umbral: float = 0.5) -> List[Dict[str, Any]]:
    """Retorna hasta k pasajes con similitud >= umbral usando FAISS. Si no hay índice, lista vacía."""
    if indice is None or not textos or faiss is None or _client is None:
        return []
    try:
        qv = _embed_query(pregunta)
        D, I = indice.search(qv, k)
        resultados: List[Dict[str, Any]] = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            if float(score) < umbral:
                continue
            md = textos[int(idx)]
            resultados.append({
                "texto": md["texto"],
                "archivo": md.get("archivo", ""),
                "pagina": md.get("pagina", ""),
                "similitud": float(score)
            })
        return resultados
    except Exception:
        return []
