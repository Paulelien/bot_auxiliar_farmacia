#!/usr/bin/env python3
"""
Script para consultar analytics diarios desde la base de datos (versión simple)
"""
import sqlite3
from datetime import datetime, timedelta
import csv

def consultar_analytics_diarios():
    """Consultar analytics diarios desde la base de datos"""
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('chatbot_analytics.db')
        
        print("📊 CONSULTA DE ANALYTICS DIARIOS")
        print("=" * 50)
        
        # 1. Métricas generales
        print("\n📈 MÉTRICAS GENERALES:")
        print("-" * 30)
        
        # Total estudiantes
        total_estudiantes = conn.execute("SELECT COUNT(*) FROM estudiantes").fetchone()[0]
        print(f"👥 Total estudiantes: {total_estudiantes}")
        
        # Total preguntas
        total_preguntas = conn.execute("SELECT COUNT(*) FROM preguntas").fetchone()[0]
        print(f"❓ Total preguntas: {total_preguntas}")
        
        # Total sesiones
        total_sesiones = conn.execute("SELECT COUNT(*) FROM sesiones").fetchone()[0]
        print(f"🕐 Total sesiones: {total_sesiones}")
        
        # 2. Analytics diarios
        print("\n📅 ANALYTICS DIARIOS:")
        print("-" * 30)
        
        analytics = conn.execute("""
            SELECT fecha, total_estudiantes_activos, total_preguntas, 
                   promedio_puntaje_quiz, categoria_mas_consultada
            FROM analytics_diarios 
            ORDER BY fecha DESC
        """).fetchall()
        
        if analytics:
            for fecha, estudiantes, preguntas, promedio, categoria in analytics:
                print(f"📅 {fecha}: {estudiantes} estudiantes, {preguntas} preguntas, "
                      f"promedio {promedio}%, categoría: {categoria}")
        else:
            print("⚠️ No hay analytics diarios registrados")
        
        # 3. Categorías más consultadas
        print("\n🏷️ CATEGORÍAS MÁS CONSULTADAS:")
        print("-" * 30)
        
        categorias = conn.execute("""
            SELECT categoria, COUNT(*) as total
            FROM preguntas 
            WHERE categoria IS NOT NULL
            GROUP BY categoria 
            ORDER BY total DESC
        """).fetchall()
        
        for categoria, total in categorias:
            print(f"📋 {categoria}: {total} consultas")
        
        # 4. Estudiantes más activos
        print("\n👑 ESTUDIANTES MÁS ACTIVOS:")
        print("-" * 30)
        
        estudiantes_activos = conn.execute("""
            SELECT e.nombre, COUNT(p.id) as preguntas
            FROM estudiantes e
            LEFT JOIN preguntas p ON e.id = p.estudiante_id
            GROUP BY e.id, e.nombre
            ORDER BY preguntas DESC
            LIMIT 5
        """).fetchall()
        
        for nombre, preguntas in estudiantes_activos:
            print(f"👤 {nombre}: {preguntas} preguntas")
        
        # 5. Preguntas más frecuentes
        print("\n🔍 PREGUNTAS MÁS FRECUENTES:")
        print("-" * 30)
        
        preguntas_frecuentes = conn.execute("""
            SELECT pregunta, COUNT(*) as total
            FROM preguntas 
            GROUP BY pregunta 
            ORDER BY total DESC
            LIMIT 5
        """).fetchall()
        
        for pregunta, total in preguntas_frecuentes:
            print(f"❓ '{pregunta[:50]}...': {total} veces")
        
        # 6. Rendimiento en quizzes
        print("\n📊 RENDIMIENTO EN QUIZZES:")
        print("-" * 30)
        
        quiz_stats = conn.execute("""
            SELECT AVG(puntaje) as promedio, COUNT(*) as total_quizzes
            FROM resultados_quiz
        """).fetchone()
        
        if quiz_stats[0]:
            print(f"📈 Promedio general: {quiz_stats[0]:.1f}%")
            print(f"📝 Total quizzes: {quiz_stats[1]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error consultando analytics: {e}")

def generar_reporte_csv():
    """Generar reporte CSV de analytics"""
    try:
        conn = sqlite3.connect('chatbot_analytics.db')
        
        # Exportar preguntas a CSV
        print("\n📄 Generando reporte de preguntas...")
        preguntas = conn.execute("""
            SELECT p.fecha, e.nombre, p.pregunta, p.categoria, p.tiempo_respuesta_ms
            FROM preguntas p
            JOIN estudiantes e ON p.estudiante_id = e.id
            ORDER BY p.fecha DESC
        """).fetchall()
        
        with open('reporte_preguntas.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Fecha', 'Estudiante', 'Pregunta', 'Categoría', 'Tiempo Respuesta (ms)'])
            writer.writerows(preguntas)
        
        print("✅ Reporte de preguntas guardado como 'reporte_preguntas.csv'")
        
        # Exportar sesiones a CSV
        print("📄 Generando reporte de sesiones...")
        sesiones = conn.execute("""
            SELECT s.fecha_inicio, s.fecha_fin, s.duracion_minutos, 
                   s.preguntas_realizadas, e.nombre
            FROM sesiones s
            JOIN estudiantes e ON s.estudiante_id = e.id
            ORDER BY s.fecha_inicio DESC
        """).fetchall()
        
        with open('reporte_sesiones.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Fecha Inicio', 'Fecha Fin', 'Duración (min)', 'Preguntas Realizadas', 'Estudiante'])
            writer.writerows(sesiones)
        
        print("✅ Reporte de sesiones guardado como 'reporte_sesiones.csv'")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error generando reportes: {e}")

if __name__ == "__main__":
    consultar_analytics_diarios()
    
    print("\n" + "=" * 50)
    respuesta = input("¿Deseas generar reportes CSV? (s/n): ").lower()
    if respuesta == 's':
        generar_reporte_csv() 