#!/usr/bin/env python3
"""
Script para probar la búsqueda de información sobre cadena de frío
"""

from embedding_utils import cargar_o_crear_indice, buscar_similares

def probar_cadena_frio():
    """
    Prueba la búsqueda de información sobre cadena de frío
    """
    print("🧪 Probando búsqueda: '¿Qué es la cadena de frío?'")
    print("=" * 60)
    
    # Cargar índice
    print("📚 Cargando índice...")
    indice, textos = cargar_o_crear_indice([])
    
    if not textos:
        print("❌ No hay textos disponibles para probar")
        return
    
    print(f"✅ Índice cargado con {len(textos)} fragmentos")
    
    # Pregunta de prueba
    pregunta = "¿Qué es la cadena de frío?"
    
    print(f"\n🔍 Buscando: '{pregunta}'")
    print("-" * 40)
    
    # Buscar con diferentes umbrales
    umbrales = [0.65, 0.55, 0.45, 0.35]
    
    for umbral in umbrales:
        print(f"\n📊 Probando umbral: {umbral}")
        resultados = buscar_similares(pregunta, indice, textos, k=3, umbral=umbral)
        
        if resultados:
            print(f"✅ Encontrados {len(resultados)} resultados:")
            for i, resultado in enumerate(resultados, 1):
                if isinstance(resultado, dict):
                    archivo = resultado.get('archivo', 'Desconocido')
                    pagina = resultado.get('pagina', 'N/A')
                    similitud = resultado.get('similitud', 'N/A')
                    texto = resultado.get('texto', '')[:200] + "..." if len(resultado.get('texto', '')) > 200 else resultado.get('texto', '')
                    
                    print(f"  {i}. [{archivo} - Página {pagina} - Similitud: {similitud:.3f}]")
                    print(f"     {texto}")
                else:
                    print(f"  {i}. {resultado}")
        else:
            print(f"❌ No se encontraron resultados con umbral {umbral}")
    
    print("\n" + "=" * 60)
    print("🎯 Prueba completada")

if __name__ == "__main__":
    probar_cadena_frio() 