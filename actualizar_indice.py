#!/usr/bin/env python3
"""
Script para actualizar el índice FAISS con nuevos PDFs
"""

import os
import sys
from pdf_utils import cargar_multiples_pdfs
from embedding_utils import cargar_o_crear_indice

def actualizar_indice():
    """
    Actualiza el índice FAISS con todos los PDFs en la carpeta material/
    """
    print("🔄 Iniciando actualización del índice...")
    
    # Carpeta donde están los PDFs
    carpeta_material = "material"
    
    if not os.path.exists(carpeta_material):
        print(f"❌ Error: La carpeta {carpeta_material} no existe")
        return False
    
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
    try:
        indice, textos_actualizados = cargar_o_crear_indice(textos_con_metadatos)
        print(f"✅ Índice actualizado exitosamente")
        print(f"📊 Total de fragmentos en el índice: {len(textos_actualizados)}")
        return True
    except Exception as e:
        print(f"❌ Error al crear el índice: {e}")
        return False

def verificar_indice():
    """
    Verifica el estado actual del índice
    """
    print("🔍 Verificando estado del índice...")
    
    indice_path = "material/faiss_index.bin"
    textos_path = "material/textos.pkl"
    
    if os.path.exists(indice_path) and os.path.exists(textos_path):
        print("✅ Índice FAISS encontrado")
        print(f"📁 Tamaño del índice: {os.path.getsize(indice_path) / 1024 / 1024:.2f} MB")
        print(f"📁 Tamaño de textos: {os.path.getsize(textos_path) / 1024 / 1024:.2f} MB")
        return True
    else:
        print("❌ Índice FAISS no encontrado")
        return False

def main():
    """
    Función principal
    """
    print("🤖 Actualizador de Índice - Chatbot Auxiliar de Farmacia")
    print("=" * 60)
    
    # Verificar estado actual
    if verificar_indice():
        print("\n⚠️  Se encontró un índice existente.")
        respuesta = input("¿Deseas actualizarlo con los nuevos PDFs? (s/n): ").lower()
        if respuesta != 's':
            print("❌ Actualización cancelada")
            return
    
    # Actualizar índice
    print("\n🚀 Iniciando actualización...")
    if actualizar_indice():
        print("\n🎉 ¡Actualización completada exitosamente!")
        print("✅ El chatbot ahora puede usar el nuevo contenido")
        print("🔄 Reinicia la API para aplicar los cambios")
    else:
        print("\n❌ Error en la actualización")
        sys.exit(1)

if __name__ == "__main__":
    main() 