#!/usr/bin/env python3
"""
Script para limpiar y regenerar el índice FAISS
"""

import os
import shutil

def limpiar_indice():
    """
    Elimina el índice existente para forzar su regeneración
    """
    print("🧹 Limpiando índice FAISS...")
    
    # Archivos a eliminar
    archivos_indice = [
        "material/faiss_index.bin",
        "material/textos.pkl"
    ]
    
    for archivo in archivos_indice:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"✅ Eliminado: {archivo}")
            except Exception as e:
                print(f"❌ Error eliminando {archivo}: {e}")
        else:
            print(f"ℹ️  No encontrado: {archivo}")
    
    print("\n🎉 Índice limpiado exitosamente!")
    print("🔄 El sistema regenerará automáticamente el índice al siguiente uso")
    print("✅ Solo se incluirán los archivos PDF que están actualmente en la carpeta material/")

if __name__ == "__main__":
    print("🤖 Limpiador de Índice FAISS")
    print("=" * 40)
    limpiar_indice() 