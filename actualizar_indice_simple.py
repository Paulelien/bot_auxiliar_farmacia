#!/usr/bin/env python3
"""
Script simple para actualizar el índice FAISS
"""

import os
import sys
from pdf_utils import cargar_multiples_pdfs
from embedding_utils import cargar_o_crear_indice

def actualizar_indice_simple():
    """
    Actualiza el índice FAISS de forma simple
    """
    print("🔄 Actualizando índice FAISS...")
    
    # Carpeta donde están los archivos
    carpeta_material = "material"
    
    if not os.path.exists(carpeta_material):
        print(f"❌ Error: La carpeta {carpeta_material} no existe")
        return False
    
    try:
        # Cargar todos los textos de los PDFs
        print("📄 Procesando PDFs...")
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
        
        # Crear o actualizar el índice
        print("\n🔍 Creando/actualizando índice FAISS...")
        indice, textos_actualizados = cargar_o_crear_indice(textos_con_metadatos)
        
        print(f"✅ Índice actualizado exitosamente")
        print(f"📊 Total de fragmentos en el índice: {len(textos_actualizados)}")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar el índice: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Actualizador Simple de Índice")
    print("=" * 40)
    
    if actualizar_indice_simple():
        print("\n🎉 ¡Actualización completada!")
        print("✅ El chatbot ahora usa solo los archivos disponibles")
    else:
        print("\n❌ Error en la actualización")
        sys.exit(1) 