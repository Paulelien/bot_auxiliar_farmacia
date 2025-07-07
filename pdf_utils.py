import fitz  # PyMuPDF
import os
import glob

def extraer_texto_pdf(ruta_pdf):
    """
    Extrae el texto de cada página del PDF y devuelve una lista de strings (uno por página).
    """
    texto_paginas = []
    try:
        with fitz.open(ruta_pdf) as doc:
            for pagina in doc:
                texto = pagina.get_text()
                texto_paginas.append(texto)
    except Exception as e:
        print(f"Error al procesar {ruta_pdf}: {e}")
        # Intentar con diferentes métodos si falla
        try:
            with fitz.open(ruta_pdf, filetype="pdf") as doc:
                for pagina in doc:
                    texto = pagina.get_text()
                    texto_paginas.append(texto)
        except Exception as e2:
            print(f"Error secundario al procesar {ruta_pdf}: {e2}")
            return []
    return texto_paginas

def extraer_texto_archivo(ruta_archivo):
    """
    Extrae el texto de un archivo de texto y lo divide en secciones.
    """
    if not os.path.exists(ruta_archivo):
        return []
    
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Dividir por módulos o secciones
    secciones = contenido.split('\n\n')
    return [seccion.strip() for seccion in secciones if seccion.strip()]

def cargar_multiples_pdfs(carpeta_material):
    """
    Carga todos los PDFs de una carpeta y devuelve una lista de textos con metadatos.
    """
    todos_textos = []
    
    # Buscar todos los PDFs en la carpeta
    pdfs = glob.glob(os.path.join(carpeta_material, "*.pdf"))
    
    if not pdfs:
        print("No se encontraron PDFs en la carpeta material/")
        return todos_textos
    
    for pdf_path in pdfs:
        nombre_archivo = os.path.basename(pdf_path)
        print(f"Procesando: {nombre_archivo}")
        
        texto_paginas = extraer_texto_pdf(pdf_path)
        
        # Agregar metadatos a cada página
        for i, texto in enumerate(texto_paginas):
            if texto.strip():  # Solo agregar páginas con contenido
                todos_textos.append({
                    "archivo": nombre_archivo,
                    "pagina": i + 1,
                    "texto": texto.strip()
                })
    
    return todos_textos 