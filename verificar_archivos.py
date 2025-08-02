#!/usr/bin/env python3
"""
Script para verificar que los archivos PDF estén disponibles
"""

import os
import glob

def verificar_archivos():
    """
    Verifica que los archivos PDF estén disponibles
    """
    print("🔍 Verificando archivos PDF...")
    
    # Carpeta donde están los archivos
    carpeta_material = "material"
    
    if not os.path.exists(carpeta_material):
        print(f"❌ Error: La carpeta {carpeta_material} no existe")
        return False
    
    # Buscar archivos PDF
    pdfs = glob.glob(os.path.join(carpeta_material, "*.pdf"))
    
    print(f"📄 Archivos PDF encontrados: {len(pdfs)}")
    
    for pdf in pdfs:
        nombre = os.path.basename(pdf)
        tamaño = os.path.getsize(pdf) / (1024 * 1024)  # MB
        print(f"  - {nombre} ({tamaño:.2f} MB)")
    
    # Buscar archivos de texto
    txts = glob.glob(os.path.join(carpeta_material, "*.txt"))
    
    print(f"📝 Archivos de texto encontrados: {len(txts)}")
    
    for txt in txts:
        nombre = os.path.basename(txt)
        tamaño = os.path.getsize(txt) / 1024  # KB
        print(f"  - {nombre} ({tamaño:.2f} KB)")
    
    total_archivos = len(pdfs) + len(txts)
    
    if total_archivos == 0:
        print("❌ No se encontraron archivos para procesar")
        return False
    else:
        print(f"✅ Total de archivos encontrados: {total_archivos}")
        return True

if __name__ == "__main__":
    print("🤖 Verificador de Archivos")
    print("=" * 30)
    
    if verificar_archivos():
        print("\n✅ Archivos disponibles correctamente")
    else:
        print("\n❌ Problema con los archivos") 