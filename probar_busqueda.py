#!/usr/bin/env python3
"""
Script para probar la búsqueda semántica con datos de ejemplo
"""

import os
import pickle
import numpy as np
from pdf_utils import cargar_multiples_pdfs

def crear_datos_ejemplo():
    """Crea datos de ejemplo para probar la búsqueda"""
    
    # Datos de ejemplo basados en el contenido que sabemos que existe
    datos_ejemplo = [
        {
            "archivo": "Modulo1_Legislación_farmacéutica.pdf.pdf",
            "pagina": 1,
            "texto": "LEGISLACIÓN FARMACÉUTICA CHILENA. El marco normativo que regula la actividad farmacéutica en Chile incluye diversos decretos y leyes que establecen las condiciones para el funcionamiento de farmacias, la dispensación de medicamentos y las responsabilidades del personal farmacéutico."
        },
        {
            "archivo": "Modulo1_Legislación_farmacéutica.pdf.pdf", 
            "pagina": 2,
            "texto": "DECRETO 405: Control de psicotrópicos y estupefacientes. Este decreto establece las normas para el control y dispensación de medicamentos psicotrópicos y estupefacientes, incluyendo los requisitos de receta médica, almacenamiento y registro de ventas."
        },
        {
            "archivo": "Modulo1_Legislación_farmacéutica.pdf.pdf",
            "pagina": 3, 
            "texto": "DECRETO 79: Norma los recetarios farmacéuticos. Este decreto establece las características y requisitos que deben cumplir los recetarios utilizados por los profesionales habilitados para prescribir medicamentos."
        },
        {
            "archivo": "Manual_del_participante 4.pdf",
            "pagina": 1,
            "texto": "FUNCIONES DEL AUXILIAR DE FARMACIA. El auxiliar de farmacia es un profesional que asiste al farmacéutico en las tareas de dispensación, venta y control de medicamentos, siempre bajo la supervisión del profesional responsable."
        },
        {
            "archivo": "Módulo_2_Tecnología_Farmacéutica.pdf",
            "pagina": 1,
            "texto": "TECNOLOGÍA FARMACÉUTICA. Las formas farmacéuticas son las presentaciones en las que se administran los medicamentos, incluyendo comprimidos, cápsulas, jarabes, inyectables y otras formas de administración."
        }
    ]
    
    return datos_ejemplo

def simular_busqueda_semantica(pregunta, datos_ejemplo):
    """Simula una búsqueda semántica simple"""
    
    pregunta_lower = pregunta.lower()
    resultados = []
    
    for dato in datos_ejemplo:
        texto_lower = dato["texto"].lower()
        
        # Búsqueda simple por palabras clave
        palabras_clave = pregunta_lower.split()
        coincidencias = 0
        
        for palabra in palabras_clave:
            if palabra in texto_lower:
                coincidencias += 1
        
        # Calcular similitud simple
        if coincidencias > 0:
            similitud = coincidencias / len(palabras_clave)
            if similitud >= 0.3:  # Umbral bajo para simulación
                resultado = dato.copy()
                resultado["similitud"] = similitud
                resultados.append(resultado)
    
    # Ordenar por similitud
    resultados.sort(key=lambda x: x["similitud"], reverse=True)
    return resultados[:3]

def probar_busqueda():
    """Prueba la búsqueda con diferentes preguntas"""
    
    print("🧪 Probando Búsqueda Semántica")
    print("=" * 50)
    
    # Crear datos de ejemplo
    datos_ejemplo = crear_datos_ejemplo()
    print(f"✅ Datos de ejemplo creados: {len(datos_ejemplo)} fragmentos")
    
    # Preguntas de prueba
    preguntas_prueba = [
        "¿Qué me puedes decir sobre la legislación farmacéutica?",
        "¿Qué es el Decreto 405?",
        "¿Cuáles son las funciones del auxiliar de farmacia?",
        "¿Qué son las formas farmacéuticas?",
        "¿Qué establece el Decreto 79?"
    ]
    
    for pregunta in preguntas_prueba:
        print(f"\n🔍 Pregunta: {pregunta}")
        print("-" * 40)
        
        resultados = simular_busqueda_semantica(pregunta, datos_ejemplo)
        
        if resultados:
            print(f"✅ Encontrados {len(resultados)} resultados:")
            for i, r in enumerate(resultados):
                archivo = r["archivo"]
                pagina = r["pagina"]
                similitud = r["similitud"]
                texto_corto = r["texto"][:100] + "..."
                print(f"  {i+1}. {archivo} (p.{pagina}) - Similitud: {similitud:.3f}")
                print(f"     Texto: {texto_corto}")
        else:
            print("❌ No se encontraron resultados")
        
        print()

if __name__ == "__main__":
    probar_busqueda() 