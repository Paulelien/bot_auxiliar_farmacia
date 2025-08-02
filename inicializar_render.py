#!/usr/bin/env python3
"""
Script para inicializar Render y verificar archivos PDF
"""

import os
import glob
import shutil
from pdf_utils import cargar_multiples_pdfs
from embedding_utils import cargar_o_crear_indice

def inicializar_render():
    """
    Inicializa el sistema en Render verificando archivos
    """
    print("🚀 Inicializando sistema en Render...")
    
    # Carpeta donde están los archivos
    carpeta_material = "material"
    
    if not os.path.exists(carpeta_material):
        print(f"❌ Error: La carpeta {carpeta_material} no existe")
        return False
    
    # Verificar archivos PDF
    pdfs = glob.glob(os.path.join(carpeta_material, "*.pdf"))
    print(f"📄 Archivos PDF encontrados en Render: {len(pdfs)}")
    
    for pdf in pdfs:
        nombre = os.path.basename(pdf)
        tamaño = os.path.getsize(pdf) / (1024 * 1024)  # MB
        print(f"  - {nombre} ({tamaño:.2f} MB)")
    
    # Verificar archivos de texto
    txts = glob.glob(os.path.join(carpeta_material, "*.txt"))
    print(f"📝 Archivos de texto encontrados: {len(txts)}")
    
    total_archivos = len(pdfs) + len(txts)
    
    if total_archivos == 0:
        print("❌ No se encontraron archivos en Render")
        print("🔍 Verificando estructura de directorios...")
        
        # Listar todo el directorio
        for root, dirs, files in os.walk("."):
            print(f"Directorio: {root}")
            for file in files:
                print(f"  - {file}")
        
        return False
    
    print(f"✅ Total de archivos encontrados: {total_archivos}")
    
    # Intentar cargar los PDFs
    try:
        print("📄 Intentando cargar PDFs...")
        textos_con_metadatos = cargar_multiples_pdfs(carpeta_material)
        
        if not textos_con_metadatos:
            print("❌ No se pudieron cargar los PDFs")
            return False
        
        print(f"✅ Se cargaron {len(textos_con_metadatos)} fragmentos de texto")
        
        # Crear índice
        print("🔍 Creando índice FAISS...")
        indice, textos_actualizados = cargar_o_crear_indice(textos_con_metadatos)
        
        print(f"✅ Índice creado exitosamente con {len(textos_actualizados)} fragmentos")
        return True
        
    except Exception as e:
        print(f"❌ Error al procesar archivos: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Inicializador de Render")
    print("=" * 40)
    
    if inicializar_render():
        print("\n🎉 Sistema inicializado correctamente en Render")
    else:
        print("\n❌ Error en la inicialización de Render") 