#!/usr/bin/env python3
"""
Script para forzar la regeneración completa del índice FAISS
"""

import os
import sys
import shutil
from pdf_utils import cargar_multiples_pdfs
from embedding_utils import cargar_o_crear_indice

def forzar_regeneracion():
    """
    Fuerza la regeneración completa del índice
    """
    print("🔄 Forzando regeneración completa del índice FAISS...")
    
    # Carpeta donde están los archivos
    carpeta_material = "material"
    
    # Eliminar archivos del índice existente
    archivos_a_eliminar = [
        "material/faiss_index.bin",
        "material/textos.pkl"
    ]
    
    print("🧹 Eliminando archivos del índice anterior...")
    for archivo in archivos_a_eliminar:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"✅ Eliminado: {archivo}")
            except Exception as e:
                print(f"❌ Error eliminando {archivo}: {e}")
    
    if not os.path.exists(carpeta_material):
        print(f"❌ Error: La carpeta {carpeta_material} no existe")
        return False
    
    try:
        # Cargar todos los textos de los PDFs
        print("📄 Procesando PDFs disponibles...")
        textos_con_metadatos = cargar_multiples_pdfs(carpeta_material)
        
        if not textos_con_metadatos:
            print("❌ No se encontraron PDFs para procesar")
            return False
        
        print(f"✅ Se procesaron {len(textos_con_metadatos)} fragmentos de texto")
        
        # Mostrar archivos procesados
        archivos_procesados = set()
        for texto in textos_con_metadatos:
            archivos_procesados.add(texto['archivo'])
        
        print("\n📋 Archivos procesados:")
        for archivo in sorted(archivos_procesados):
            print(f"  - {archivo}")
        
        # Verificar que NO esté el archivo eliminado
        if "Tarea practica 2 unidad 3.pdf" in archivos_procesados:
            print("❌ ERROR: El archivo eliminado sigue apareciendo en el procesamiento")
            return False
        else:
            print("✅ Confirmado: El archivo eliminado NO está incluido")
        
        # Crear nuevo índice
        print("\n🔍 Creando nuevo índice FAISS...")
        indice, textos_actualizados = cargar_o_crear_indice(textos_con_metadatos)
        
        print(f"✅ Índice regenerado exitosamente")
        print(f"📊 Total de fragmentos en el nuevo índice: {len(textos_actualizados)}")
        return True
        
    except Exception as e:
        print(f"❌ Error al regenerar el índice: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Forzador de Regeneración de Índice FAISS")
    print("=" * 50)
    
    if forzar_regeneracion():
        print("\n🎉 ¡Regeneración completada exitosamente!")
        print("✅ El chatbot ahora usa SOLO los archivos disponibles")
        print("✅ El archivo eliminado ya no está incluido")
        print("🔄 Reinicia la API para aplicar los cambios")
    else:
        print("\n❌ Error en la regeneración")
        sys.exit(1) 