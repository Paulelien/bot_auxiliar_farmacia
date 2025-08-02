#!/usr/bin/env python3
"""
Script para actualizar el índice FAISS con nuevos PDFs y archivos de texto
"""

import os
import sys
from pdf_utils import cargar_multiples_pdfs
from embedding_utils import cargar_o_crear_indice

from dotenv import load_dotenv
load_dotenv()

def cargar_archivos_texto(carpeta_material):
    """
    Carga archivos de texto (.txt) de la carpeta material
    """
    textos_texto = []
    
    for archivo in os.listdir(carpeta_material):
        if archivo.endswith('.txt'):
            ruta_archivo = os.path.join(carpeta_material, archivo)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Dividir el contenido en fragmentos más pequeños
                fragmentos = contenido.split('\n\n')  # Dividir por párrafos dobles
                
                for i, fragmento in enumerate(fragmentos):
                    if fragmento.strip():  # Solo fragmentos no vacíos
                        textos_texto.append({
                            'texto': fragmento.strip(),
                            'archivo': archivo,
                            'pagina': i + 1
                        })
                
                print(f"  ✅ Procesado: {archivo} ({len(fragmentos)} fragmentos)")
                
            except Exception as e:
                print(f"  ❌ Error procesando {archivo}: {e}")
    
    return textos_texto

def actualizar_indice():
    """
    Actualiza el índice FAISS con todos los PDFs y archivos de texto en la carpeta material/
    """
    print("🔄 Iniciando actualización del índice...")
    
    # Carpeta donde están los archivos
    carpeta_material = "material"
    
    if not os.path.exists(carpeta_material):
        print(f"❌ Error: La carpeta {carpeta_material} no existe")
        return False
    
    # Cargar todos los textos de los PDFs
    print("📄 Procesando PDFs...")
    textos_con_metadatos = cargar_multiples_pdfs(carpeta_material)
    
    # Cargar archivos de texto
    print("📝 Procesando archivos de texto...")
    textos_texto = cargar_archivos_texto(carpeta_material)
    
    # Combinar todos los textos
    todos_los_textos = textos_con_metadatos + textos_texto
    
    if not todos_los_textos:
        print("❌ No se encontraron archivos para procesar")
        return False
    
    print(f"✅ Se procesaron {len(todos_los_textos)} fragmentos de texto total")
    
    # Mostrar archivos procesados
    archivos_procesados = set()
    for texto in todos_los_textos:
        archivos_procesados.add(texto['archivo'])
    
    print("\n📋 Archivos procesados:")
    for archivo in sorted(archivos_procesados):
        print(f"  - {archivo}")
    
    # Crear o actualizar el índice
    print("\n🔍 Creando/actualizando índice FAISS...")
    try:
        indice, textos_actualizados = cargar_o_crear_indice(todos_los_textos)
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
        print("🔄 Actualizando automáticamente con los archivos disponibles...")
    else:
        print("\n🆕 Creando nuevo índice...")
    
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