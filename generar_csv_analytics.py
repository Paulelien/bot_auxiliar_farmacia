#!/usr/bin/env python3
"""
Script para generar reportes CSV de analytics
"""
import sqlite3
import csv
from datetime import datetime

def generar_reportes_csv():
    """Generar todos los reportes CSV de analytics"""
    try:
        print("📊 GENERANDO REPORTES CSV DE ANALYTICS")
        print("=" * 50)
        
        # Conectar a la base de datos
        conn = sqlite3.connect('chatbot_analytics.db')
        
        # 1. Reporte de preguntas
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
        
        print(f"✅ Reporte de preguntas guardado: {len(preguntas)} registros")
        
        # 2. Reporte de sesiones
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
        
        print(f"✅ Reporte de sesiones guardado: {len(sesiones)} registros")
        
        # 3. Reporte de estudiantes
        print("📄 Generando reporte de estudiantes...")
        estudiantes = conn.execute("""
            SELECT e.nombre, e.email, e.grupo, e.fecha_registro,
                   COUNT(p.id) as total_preguntas,
                   COUNT(s.id) as total_sesiones
            FROM estudiantes e
            LEFT JOIN preguntas p ON e.id = p.estudiante_id
            LEFT JOIN sesiones s ON e.id = s.estudiante_id
            GROUP BY e.id, e.nombre, e.email, e.grupo, e.fecha_registro
            ORDER BY total_preguntas DESC
        """).fetchall()
        
        with open('reporte_estudiantes.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nombre', 'Email', 'Grupo', 'Fecha Registro', 'Total Preguntas', 'Total Sesiones'])
            writer.writerows(estudiantes)
        
        print(f"✅ Reporte de estudiantes guardado: {len(estudiantes)} registros")
        
        # 4. Reporte de resultados de quiz
        print("📄 Generando reporte de resultados de quiz...")
        resultados = conn.execute("""
            SELECT e.nombre, r.puntaje, r.preguntas_correctas, r.total_preguntas,
                   r.tiempo_completado_minutos, r.fecha
            FROM resultados_quiz r
            JOIN estudiantes e ON r.estudiante_id = e.id
            ORDER BY r.fecha DESC
        """).fetchall()
        
        with open('reporte_quizzes.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Estudiante', 'Puntaje (%)', 'Preguntas Correctas', 'Total Preguntas', 'Tiempo (min)', 'Fecha'])
            writer.writerows(resultados)
        
        print(f"✅ Reporte de quizzes guardado: {len(resultados)} registros")
        
        # 5. Reporte de categorías
        print("📄 Generando reporte de categorías...")
        categorias = conn.execute("""
            SELECT categoria, COUNT(*) as total_consultas,
                   AVG(tiempo_respuesta_ms) as tiempo_promedio_ms
            FROM preguntas 
            WHERE categoria IS NOT NULL
            GROUP BY categoria 
            ORDER BY total_consultas DESC
        """).fetchall()
        
        with open('reporte_categorias.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Categoría', 'Total Consultas', 'Tiempo Promedio (ms)'])
            writer.writerows(categorias)
        
        print(f"✅ Reporte de categorías guardado: {len(categorias)} registros")
        
        # 6. Reporte de analytics diarios
        print("📄 Generando reporte de analytics diarios...")
        analytics = conn.execute("""
            SELECT fecha, total_estudiantes_activos, total_preguntas, 
                   promedio_puntaje_quiz, categoria_mas_consultada
            FROM analytics_diarios 
            ORDER BY fecha DESC
        """).fetchall()
        
        with open('reporte_analytics_diarios.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Fecha', 'Estudiantes Activos', 'Total Preguntas', 'Promedio Quiz (%)', 'Categoría Más Consultada'])
            writer.writerows(analytics)
        
        print(f"✅ Reporte de analytics diarios guardado: {len(analytics)} registros")
        
        conn.close()
        
        print("\n🎉 TODOS LOS REPORTES CSV GENERADOS EXITOSAMENTE")
        print("=" * 50)
        print("📁 Archivos generados:")
        print("  - reporte_preguntas.csv")
        print("  - reporte_sesiones.csv") 
        print("  - reporte_estudiantes.csv")
        print("  - reporte_quizzes.csv")
        print("  - reporte_categorias.csv")
        print("  - reporte_analytics_diarios.csv")
        
    except Exception as e:
        print(f"❌ Error generando reportes: {e}")

if __name__ == "__main__":
    generar_reportes_csv() 