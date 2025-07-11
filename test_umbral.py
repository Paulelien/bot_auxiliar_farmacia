#!/usr/bin/env python3
"""
Script para probar el umbral de similitud semántica
"""

from embedding_utils import cargar_o_crear_indice, buscar_similares

def test_umbral():
    """
    Prueba diferentes umbrales de similitud
    """
    print("🧪 Probando Umbral de Similitud Semántica")
    print("=" * 50)
    
    # Cargar índice
    print("📚 Cargando índice...")
    indice, textos = cargar_o_crear_indice([])
    
    if not textos:
        print("❌ No hay textos disponibles para probar")
        return
    
    print(f"✅ Índice cargado con {len(textos)} fragmentos")
    
    # Preguntas de prueba
    preguntas_prueba = [
        "¿Qué es el Decreto 405?",
        "¿Cómo se almacenan los medicamentos termolábiles?",
        "¿Cuáles son las funciones del auxiliar de farmacia?",
        "¿Qué son los psicotrópicos?",
        "¿Cuál es la temperatura de la cadena de frío?",
        "¿Qué es el principio FEFO?",
        "¿Cómo se debe atender al cliente en una farmacia?",
        "¿Qué son los medicamentos de venta libre?",
        "¿Cuál es la función del ISP?",
        "¿Qué establece el Decreto 79?"
    ]
    
    # Umbrales a probar
    umbrales = [0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60]
    
    for pregunta in preguntas_prueba[:3]:  # Probar solo las primeras 3
        print(f"\n🔍 Pregunta: {pregunta}")
        print("-" * 40)
        
        for umbral in umbrales:
            print(f"\n📊 Umbral: {umbral}")
            resultados = buscar_similares(pregunta, indice, textos, k=3, umbral=umbral)
            
            if resultados:
                print(f"✅ Encontrados {len(resultados)} resultados")
                for i, r in enumerate(resultados[:2]):  # Mostrar solo los primeros 2
                    archivo = r.get('archivo', 'Desconocido')
                    pagina = r.get('pagina', 'N/A')
                    similitud = r.get('similitud', 0)
                    print(f"  {i+1}. {archivo} (p.{pagina}) - Similitud: {similitud:.3f}")
            else:
                print("❌ No se encontraron resultados")
        
        print("\n" + "="*50)

def configurar_umbral():
    """
    Permite configurar el umbral de similitud
    """
    print("⚙️  Configurador de Umbral de Similitud")
    print("=" * 40)
    
    print("\n📊 Umbrales recomendados:")
    print("• 0.95 - Muy estricto (solo respuestas casi idénticas)")
    print("• 0.90 - Estricto (respuestas muy similares)")
    print("• 0.85 - Moderado-alto (respuestas similares)")
    print("• 0.80 - Moderado (respuestas relacionadas)")
    print("• 0.75 - Moderado-bajo (respuestas algo relacionadas)")
    print("• 0.70 - Bajo (respuestas vagamente relacionadas)")
    print("• 0.65 - Muy bajo (casi cualquier cosa)")
    print("• 0.60 - Mínimo (todo)")
    
    try:
        umbral = float(input("\n🎯 Ingresa el umbral deseado (0.60 - 0.95): "))
        if 0.60 <= umbral <= 0.95:
            print(f"✅ Umbral configurado en: {umbral}")
            
            # Actualizar el archivo de configuración
            with open('embedding_utils.py', 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar el umbral
            contenido = contenido.replace(
                'UMBRAL_SIMILITUD = 0.85',
                f'UMBRAL_SIMILITUD = {umbral}'
            )
            
            with open('embedding_utils.py', 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            print("✅ Archivo actualizado. Reinicia la API para aplicar los cambios.")
            
        else:
            print("❌ Umbral fuera del rango válido")
    except ValueError:
        print("❌ Valor inválido")

def main():
    """
    Función principal
    """
    print("🤖 Probador de Umbral - Chatbot Auxiliar de Farmacia")
    print("=" * 60)
    
    while True:
        print("\n📋 Opciones:")
        print("1. Probar umbral actual")
        print("2. Configurar nuevo umbral")
        print("3. Salir")
        
        opcion = input("\n🎯 Selecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            test_umbral()
        elif opcion == "2":
            configurar_umbral()
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main() 