#!/usr/bin/env python3
"""
Script para consultar toda la actividad del LMS
Usa los endpoints de analytics de api.py para mostrar:
- Dashboard general
- Estudiantes registrados
- Sesiones activas
- Preguntas realizadas
- Resultados de quiz
"""

import requests
import json
from datetime import datetime
import sys

# Configuración
API_BASE_URL = "https://asistente-auxiliar-farmacia.onrender.com"

def hacer_request(endpoint, metodo="GET", datos=None):
    """Hacer request a la API"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if metodo == "GET":
            response = requests.get(url, timeout=30)
        elif metodo == "POST":
            response = requests.post(url, json=datos, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error decodificando JSON: {e}")
        return None

def mostrar_dashboard_general():
    """Mostrar dashboard general del LMS"""
    print("\n" + "="*60)
    print("📊 DASHBOARD GENERAL DEL LMS")
    print("="*60)
    
    dashboard = hacer_request("/analytics/dashboard")
    if dashboard:
        metricas = dashboard.get("metricas_generales", {})
        categorias = dashboard.get("categorias_populares", [])
        
        print(f"👥 Total de estudiantes: {metricas.get('total_estudiantes', 0)}")
        print(f"📅 Sesiones hoy: {metricas.get('sesiones_hoy', 0)}")
        print(f"❓ Total de preguntas: {metricas.get('total_preguntas', 0)}")
        print(f"📈 Promedio quiz general: {metricas.get('promedio_quiz_general', 0)}")
        
        if categorias:
            print("\n🏆 Categorías más consultadas:")
            for i, cat in enumerate(categorias[:5], 1):
                print(f"   {i}. {cat['categoria']}: {cat['total']} consultas")
        else:
            print("\n📝 No hay categorías registradas aún")
    else:
        print("❌ No se pudo obtener el dashboard")

def mostrar_estudiantes():
    """Mostrar información de estudiantes"""
    print("\n" + "="*60)
    print("👥 ESTUDIANTES REGISTRADOS")
    print("="*60)
    
    # Primero probar si hay estudiantes
    test_estudiante = hacer_request("/analytics/estudiante/1")
    if test_estudiante:
        print("✅ Hay estudiantes registrados en el sistema")
        print("📊 Para ver detalles específicos, usa el endpoint /analytics/estudiante/{id}")
    else:
        print("📝 No hay estudiantes registrados aún")

def mostrar_estadisticas_uso():
    """Mostrar estadísticas de uso del sistema"""
    print("\n" + "="*60)
    print("📈 ESTADÍSTICAS DE USO")
    print("="*60)
    
    # Probar endpoint de preguntas frecuentes
    preguntas_freq = hacer_request("/preguntas_frecuentes")
    if preguntas_freq:
        print("✅ Sistema de preguntas frecuentes activo")
        print(f"📝 Preguntas disponibles: {len(preguntas_freq)}")
    else:
        print("📝 No hay preguntas frecuentes configuradas")

def mostrar_casos_clinicos():
    """Mostrar información de casos clínicos"""
    print("\n" + "="*60)
    print("🏥 CASOS CLÍNICOS")
    print("="*60)
    
    casos = hacer_request("/casos_clinicos")
    if casos:
        print(f"✅ Casos clínicos disponibles: {len(casos)}")
        for i, caso in enumerate(casos[:3], 1):  # Mostrar solo los primeros 3
            print(f"   {i}. Caso {caso.get('id', 'N/A')}: {caso.get('titulo', 'Sin título')}")
        if len(casos) > 3:
            print(f"   ... y {len(casos) - 3} casos más")
    else:
        print("📝 No hay casos clínicos configurados")

def mostrar_estado_sistema():
    """Mostrar estado general del sistema"""
    print("\n" + "="*60)
    print("🔧 ESTADO DEL SISTEMA")
    print("="*60)
    
    # Probar endpoints básicos
    root = hacer_request("/")
    if root:
        print("✅ API funcionando correctamente")
    
    # Probar archivos disponibles
    archivos = hacer_request("/test_archivos")
    if archivos:
        print("✅ Sistema de archivos funcionando")
        carpeta_material = archivos.get("carpeta_material_existe", False)
        faiss_index = archivos.get("faiss_index_existe", False)
        textos_pkl = archivos.get("textos_pkl_existe", False)
        
        print(f"📁 Carpeta material: {'✅' if carpeta_material else '❌'}")
        print(f"🔍 Índice FAISS: {'✅' if faiss_index else '❌'}")
        print(f"📄 Archivo textos: {'✅' if textos_pkl else '❌'}")
        
        if archivos.get("archivos"):
            print(f"📚 Archivos disponibles: {archivos['archivos_encontrados']}")
    else:
        print("❌ No se pudo verificar el estado del sistema")

def mostrar_menu():
    """Mostrar menú de opciones"""
    print("\n" + "="*60)
    print("🎯 CONSULTAR ACTIVIDAD DEL LMS")
    print("="*60)
    print("1. 📊 Dashboard general")
    print("2. 👥 Estudiantes registrados")
    print("3. 📈 Estadísticas de uso")
    print("4. 🏥 Casos clínicos")
    print("5. 🔧 Estado del sistema")
    print("6. 🚀 Ver TODO (todas las opciones)")
    print("0. ❌ Salir")
    print("="*60)

def main():
    """Función principal"""
    print("🚀 Iniciando consulta de actividad del LMS...")
    print(f"🌐 Conectando a: {API_BASE_URL}")
    
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción (0-6): ").strip()
        
        if opcion == "0":
            print("👋 ¡Hasta luego!")
            break
        elif opcion == "1":
            mostrar_dashboard_general()
        elif opcion == "2":
            mostrar_estudiantes()
        elif opcion == "3":
            mostrar_estadisticas_uso()
        elif opcion == "4":
            mostrar_casos_clinicos()
        elif opcion == "5":
            mostrar_estado_sistema()
        elif opcion == "6":
            print("\n🚀 Ejecutando TODAS las consultas...")
            mostrar_dashboard_general()
            mostrar_estudiantes()
            mostrar_estadisticas_uso()
            mostrar_casos_clinicos()
            mostrar_estado_sistema()
        else:
            print("❌ Opción no válida. Intenta de nuevo.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Consulta interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1) 