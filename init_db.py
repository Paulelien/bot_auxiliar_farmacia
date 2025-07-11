from database_config import engine
from models import Base
import sqlite3

def init_database():
    """Inicializar la base de datos y crear tablas"""
    print("Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada correctamente")

def create_sample_data():
    """Crear datos de ejemplo para testing"""
    from sqlalchemy.orm import Session
    from models import Estudiante, Sesion, Pregunta, ResultadoQuiz
    from datetime import datetime, timedelta
    
    db = Session(engine)
    
    try:
        # Verificar si ya existen estudiantes
        existing_students = db.query(Estudiante).count()
        if existing_students > 0:
            print("✅ Ya existen estudiantes en la base de datos. Saltando creación de datos de ejemplo.")
            return
        
        # Crear estudiantes de ejemplo
        estudiantes = [
            Estudiante(nombre="María González", email="maria@ejemplo.com", grupo="Auxiliar 2024"),
            Estudiante(nombre="Juan Pérez", email="juan@ejemplo.com", grupo="Auxiliar 2024"),
            Estudiante(nombre="Ana López", email="ana@ejemplo.com", grupo="Auxiliar 2024"),
        ]
        
        for estudiante in estudiantes:
            db.add(estudiante)
        db.commit()
        
        # Crear sesiones de ejemplo
        for estudiante in estudiantes:
            sesion = Sesion(
                estudiante_id=estudiante.id,
                fecha_inicio=datetime.now() - timedelta(hours=2),
                fecha_fin=datetime.now() - timedelta(hours=1),
                duracion_minutos=60,
                preguntas_realizadas=5
            )
            db.add(sesion)
        db.commit()
        
        # Crear preguntas de ejemplo
        preguntas_ejemplo = [
            "¿Qué es el Decreto 405?",
            "¿Cómo se almacenan los medicamentos termolábiles?",
            "¿Cuáles son las funciones del auxiliar de farmacia?",
            "¿Qué son los psicotrópicos?",
            "¿Qué es la cadena de frío?"
        ]
        
        for i, estudiante in enumerate(estudiantes):
            for j, pregunta_texto in enumerate(preguntas_ejemplo[:3]):
                pregunta = Pregunta(
                    estudiante_id=estudiante.id,
                    sesion_id=estudiante.sesiones[0].id,
                    pregunta=pregunta_texto,
                    respuesta=f"Respuesta de ejemplo para: {pregunta_texto}",
                    categoria="General",
                    tiempo_respuesta_ms=2000 + (i * 500) + (j * 300)
                )
                db.add(pregunta)
        db.commit()
        
        # Crear resultados de quiz de ejemplo
        for estudiante in estudiantes:
            resultado = ResultadoQuiz(
                estudiante_id=estudiante.id,
                puntaje=75 + (estudiante.id * 5),
                preguntas_correctas=5 + (estudiante.id % 3),
                total_preguntas=7,
                tiempo_completado_minutos=15 + (estudiante.id * 2)
            )
            db.add(resultado)
        db.commit()
        
        print("✅ Datos de ejemplo creados correctamente")
        
    except Exception as e:
        print(f"❌ Error creando datos de ejemplo: {e}")
        db.rollback()
    finally:
        db.close()

def clear_database():
    """Limpiar todos los datos de la base de datos"""
    from sqlalchemy.orm import Session
    from models import Estudiante, Sesion, Pregunta, ResultadoQuiz, AnalyticsDiario
    
    db = Session(engine)
    
    try:
        print("🗑️ Limpiando base de datos...")
        db.query(AnalyticsDiario).delete()
        db.query(ResultadoQuiz).delete()
        db.query(Pregunta).delete()
        db.query(Sesion).delete()
        db.query(Estudiante).delete()
        db.commit()
        print("✅ Base de datos limpiada correctamente")
    except Exception as e:
        print(f"❌ Error limpiando base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_database()
    
    init_database()
    create_sample_data() 