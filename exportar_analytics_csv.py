#!/usr/bin/env python3
"""
Script para exportar toda la información de analytics del LMS a archivos CSV
Exporta las tablas: estudiantes, sesiones, preguntas, resultados_quiz, analytics_diarios
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime
import sys

def conectar_db():
    """Conectar a la base de datos SQLite"""
    try:
        db_path = "chatbot_analytics.db"
        if not os.path.exists(db_path):
            print(f"❌ No se encontró la base de datos: {db_path}")
            return None
        
        conn = sqlite3.connect(db_path)
        print(f"✅ Conectado a la base de datos: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return None

def obtener_tablas(conn):
    """Obtener lista de tablas disponibles"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [row[0] for row in cursor.fetchall()]
        return tablas
    except Exception as e:
        print(f"❌ Error obteniendo tablas: {e}")
        return []

def exportar_tabla_a_csv(conn, nombre_tabla, carpeta_export):
    """Exportar una tabla específica a CSV"""
    try:
        # Leer tabla con pandas
        df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conn)
        
        if df.empty:
            print(f"📝 Tabla '{nombre_tabla}' está vacía")
            return False
        
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{nombre_tabla}_{timestamp}.csv"
        ruta_completa = os.path.join(carpeta_export, nombre_archivo)
        
        # Exportar a CSV
        df.to_csv(ruta_completa, index=False, encoding='utf-8-sig')
        
        print(f"✅ Tabla '{nombre_tabla}' exportada: {nombre_archivo}")
        print(f"   📊 Filas: {len(df)} | Columnas: {len(df.columns)}")
        
        # Mostrar primeras filas como preview
        print(f"   👀 Preview (primeras 3 filas):")
        print(df.head(3).to_string(index=False))
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error exportando tabla '{nombre_tabla}': {e}")
        return False

def exportar_estadisticas_generales(conn, carpeta_export):
    """Exportar estadísticas generales del sistema"""
    try:
        # Crear carpeta si no existe
        os.makedirs(carpeta_export, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Resumen de estudiantes
        df_estudiantes = pd.read_sql_query("SELECT * FROM estudiantes", conn)
        if not df_estudiantes.empty:
            resumen_estudiantes = {
                'total_estudiantes': len(df_estudiantes),
                'estudiantes_por_grupo': df_estudiantes['grupo'].value_counts().to_dict(),
                'fecha_primer_registro': df_estudiantes['fecha_registro'].min(),
                'fecha_ultimo_registro': df_estudiantes['fecha_registro'].max()
            }
            
            df_resumen_est = pd.DataFrame([resumen_estudiantes])
            archivo_resumen = os.path.join(carpeta_export, f"resumen_estudiantes_{timestamp}.csv")
            df_resumen_est.to_csv(archivo_resumen, index=False, encoding='utf-8-sig')
            print(f"✅ Resumen de estudiantes exportado: resumen_estudiantes_{timestamp}.csv")
        
        # 2. Resumen de sesiones
        df_sesiones = pd.read_sql_query("SELECT * FROM sesiones", conn)
        if not df_sesiones.empty:
            resumen_sesiones = {
                'total_sesiones': len(df_sesiones),
                'sesiones_hoy': len(df_sesiones[df_sesiones['fecha_inicio'].str.contains(datetime.now().strftime('%Y-%m-%d'))]),
                'promedio_duracion_minutos': df_sesiones['duracion_minutos'].mean(),
                'total_preguntas_realizadas': df_sesiones['preguntas_realizadas'].sum()
            }
            
            df_resumen_ses = pd.DataFrame([resumen_sesiones])
            archivo_resumen = os.path.join(carpeta_export, f"resumen_sesiones_{timestamp}.csv")
            df_resumen_ses.to_csv(archivo_resumen, index=False, encoding='utf-8-sig')
            print(f"✅ Resumen de sesiones exportado: resumen_sesiones_{timestamp}.csv")
        
        # 3. Resumen de preguntas
        df_preguntas = pd.read_sql_query("SELECT * FROM preguntas", conn)
        if not df_preguntas.empty:
            resumen_preguntas = {
                'total_preguntas': len(df_preguntas),
                'preguntas_hoy': len(df_preguntas[df_preguntas['fecha'].str.contains(datetime.now().strftime('%Y-%m-%d'))]),
                'promedio_tiempo_respuesta_ms': df_preguntas['tiempo_respuesta_ms'].mean(),
                'categorias_unicas': df_preguntas['categoria'].nunique()
            }
            
            df_resumen_pre = pd.DataFrame([resumen_preguntas])
            archivo_resumen = os.path.join(carpeta_export, f"resumen_preguntas_{timestamp}.csv")
            df_resumen_pre.to_csv(archivo_resumen, index=False, encoding='utf-8-sig')
            print(f"✅ Resumen de preguntas exportado: resumen_preguntas_{timestamp}.csv")
        
        # 4. Resumen de quiz
        df_quiz = pd.read_sql_query("SELECT * FROM resultados_quiz", conn)
        if not df_quiz.empty:
            resumen_quiz = {
                'total_quiz_completados': len(df_quiz),
                'quiz_hoy': len(df_quiz[df_quiz['fecha'].str.contains(datetime.now().strftime('%Y-%m-%d'))]),
                'promedio_puntaje': df_quiz['puntaje'].mean(),
                'promedio_preguntas_correctas': df_quiz['preguntas_correctas'].mean(),
                'promedio_tiempo_completado_minutos': df_quiz['tiempo_completado_minutos'].mean()
            }
            
            df_resumen_quiz = pd.DataFrame([resumen_quiz])
            archivo_resumen = os.path.join(carpeta_export, f"resumen_quiz_{timestamp}.csv")
            df_resumen_quiz.to_csv(archivo_resumen, index=False, encoding='utf-8-sig')
            print(f"✅ Resumen de quiz exportado: resumen_quiz_{timestamp}.csv")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exportando estadísticas generales: {e}")
        return False

def exportar_analytics_avanzados(conn, carpeta_export):
    """Exportar analytics avanzados y métricas"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Preguntas por categoría
        df_preguntas = pd.read_sql_query("SELECT * FROM preguntas", conn)
        if not df_preguntas.empty:
            preguntas_por_categoria = df_preguntas['categoria'].value_counts().reset_index()
            preguntas_por_categoria.columns = ['categoria', 'total_preguntas']
            
            archivo_cat = os.path.join(carpeta_export, f"preguntas_por_categoria_{timestamp}.csv")
            preguntas_por_categoria.to_csv(archivo_cat, index=False, encoding='utf-8-sig')
            print(f"✅ Preguntas por categoría exportado: preguntas_por_categoria_{timestamp}.csv")
        
        # 2. Actividad por día
        df_preguntas = pd.read_sql_query("SELECT * FROM preguntas", conn)
        if not df_preguntas.empty:
            df_preguntas['fecha'] = pd.to_datetime(df_preguntas['fecha'])
            df_preguntas['fecha_solo'] = df_preguntas['fecha'].dt.date
            
            actividad_diaria = df_preguntas.groupby('fecha_solo').agg({
                'id': 'count',
                'tiempo_respuesta_ms': 'mean'
            }).reset_index()
            actividad_diaria.columns = ['fecha', 'total_preguntas', 'promedio_tiempo_respuesta_ms']
            
            archivo_act = os.path.join(carpeta_export, f"actividad_diaria_{timestamp}.csv")
            actividad_diaria.to_csv(archivo_act, index=False, encoding='utf-8-sig')
            print(f"✅ Actividad diaria exportado: actividad_diaria_{timestamp}.csv")
        
        # 3. Rendimiento de estudiantes
        df_estudiantes = pd.read_sql_query("SELECT * FROM estudiantes", conn)
        df_quiz = pd.read_sql_query("SELECT * FROM resultados_quiz", conn)
        
        if not df_estudiantes.empty and not df_quiz.empty:
            rendimiento_estudiantes = df_quiz.groupby('estudiante_id').agg({
                'puntaje': 'mean',
                'preguntas_correctas': 'mean',
                'tiempo_completado_minutos': 'mean',
                'id': 'count'
            }).reset_index()
            rendimiento_estudiantes.columns = ['estudiante_id', 'promedio_puntaje', 'promedio_correctas', 'promedio_tiempo_min', 'total_quiz']
            
            # Agregar nombre del estudiante
            rendimiento_estudiantes = rendimiento_estudiantes.merge(
                df_estudiantes[['id', 'nombre', 'email', 'grupo']], 
                left_on='estudiante_id', 
                right_on='id', 
                how='left'
            )
            
            archivo_rend = os.path.join(carpeta_export, f"rendimiento_estudiantes_{timestamp}.csv")
            rendimiento_estudiantes.to_csv(archivo_rend, index=False, encoding='utf-8-sig')
            print(f"✅ Rendimiento de estudiantes exportado: rendimiento_estudiantes_{timestamp}.csv")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exportando analytics avanzados: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando exportación de analytics del LMS a CSV...")
    
    # Conectar a la base de datos
    conn = conectar_db()
    if not conn:
        return
    
    try:
        # Crear carpeta de exportación
        carpeta_export = "analytics_exportados"
        os.makedirs(carpeta_export, exist_ok=True)
        print(f"📁 Carpeta de exportación creada: {carpeta_export}")
        
        # Obtener tablas disponibles
        tablas = obtener_tablas(conn)
        print(f"📋 Tablas encontradas: {', '.join(tablas)}")
        
        # Exportar cada tabla
        print("\n📤 Exportando tablas principales...")
        tablas_exportadas = 0
        
        for tabla in tablas:
            if exportar_tabla_a_csv(conn, tabla, carpeta_export):
                tablas_exportadas += 1
        
        # Exportar estadísticas generales
        print("\n📊 Exportando estadísticas generales...")
        if exportar_estadisticas_generales(conn, carpeta_export):
            print("✅ Estadísticas generales exportadas")
        
        # Exportar analytics avanzados
        print("\n🔍 Exportando analytics avanzados...")
        if exportar_analytics_avanzados(conn, carpeta_export):
            print("✅ Analytics avanzados exportados")
        
        print(f"\n🎉 Exportación completada!")
        print(f"📁 Archivos guardados en: {carpeta_export}")
        print(f"📊 Tablas exportadas: {tablas_exportadas}")
        print(f"📈 Archivos de resumen creados")
        
        # Mostrar contenido de la carpeta
        print(f"\n📂 Contenido de la carpeta de exportación:")
        archivos = os.listdir(carpeta_export)
        for archivo in sorted(archivos):
            ruta_completa = os.path.join(carpeta_export, archivo)
            tamaño = os.path.getsize(ruta_completa)
            print(f"   📄 {archivo} ({tamaño} bytes)")
        
    except Exception as e:
        print(f"❌ Error durante la exportación: {e}")
    
    finally:
        conn.close()
        print("\n🔒 Conexión a la base de datos cerrada")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exportación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1) 