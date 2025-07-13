#!/usr/bin/env python3
"""
Script para verificar la integridad de los PDFs
"""

import os
import fitz  # PyMuPDF
from pdf_utils import extraer_texto_pdf

def verificar_pdf(ruta_pdf):
    """Verifica si un PDF se puede abrir y extraer texto"""
    try:
        with fitz.open(ruta_pdf) as doc:
            texto_total = ""
            for pagina in doc:
                texto = pagina.get_text()
                texto_total += texto
            return len(texto_total) > 0, len(texto_total)
    except Exception as e:
        return False, str(e)

def verificar_todos_pdfs():
    """Verifica todos los PDFs en la carpeta material"""
    carpeta_material = "material"
    
    if not os.path.exists(carpeta_material):
        print(f"❌ La carpeta {carpeta_material} no existe")
        return
    
    pdfs = [f for f in os.listdir(carpeta_material) if f.lower().endswith('.pdf')]
    
    if not pdfs:
        print("❌ No se encontraron PDFs en la carpeta material/")
        return
    
    print("🔍 Verificando PDFs...")
    print("=" * 50)
    
    pdfs_validos = []
    pdfs_problematicos = []
    
    for pdf in pdfs:
        ruta_completa = os.path.join(carpeta_material, pdf)
        print(f"📄 Verificando: {pdf}")
        
        es_valido, resultado = verificar_pdf(ruta_completa)
        
        if es_valido:
            print(f"✅ OK - {resultado} caracteres extraídos")
            pdfs_validos.append(pdf)
        else:
            print(f"❌ ERROR - {resultado}")
            pdfs_problematicos.append(pdf)
        
        print("-" * 30)
    
    print("\n📊 RESUMEN:")
    print(f"✅ PDFs válidos: {len(pdfs_validos)}")
    print(f"❌ PDFs problemáticos: {len(pdfs_problematicos)}")
    
    if pdfs_validos:
        print("\n✅ PDFs que funcionan:")
        for pdf in pdfs_validos:
            print(f"  - {pdf}")
    
    if pdfs_problematicos:
        print("\n❌ PDFs con problemas:")
        for pdf in pdfs_problematicos:
            print(f"  - {pdf}")
        print("\n💡 SUGERENCIAS:")
        print("1. Intenta abrir los PDFs problemáticos en un lector de PDF")
        print("2. Si están corruptos, descárgalos nuevamente")
        print("3. Convierte a PDF usando herramientas online si es necesario")

if __name__ == "__main__":
    verificar_todos_pdfs() 