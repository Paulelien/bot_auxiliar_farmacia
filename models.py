from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database_config import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    grupo = Column(String(50))
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    sesiones = relationship("Sesion", back_populates="estudiante")
    preguntas = relationship("Pregunta", back_populates="estudiante")
    resultados_quiz = relationship("ResultadoQuiz", back_populates="estudiante")

class Sesion(Base):
    __tablename__ = "sesiones"
    
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime)
    duracion_minutos = Column(Integer, default=0)
    preguntas_realizadas = Column(Integer, default=0)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="sesiones")
    preguntas = relationship("Pregunta", back_populates="sesion")

class Pregunta(Base):
    __tablename__ = "preguntas"
    
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    sesion_id = Column(Integer, ForeignKey("sesiones.id"))
    pregunta = Column(Text, nullable=False)
    respuesta = Column(Text)
    categoria = Column(String(50))
    fecha = Column(DateTime, default=datetime.utcnow)
    tiempo_respuesta_ms = Column(Integer)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="preguntas")
    sesion = relationship("Sesion", back_populates="preguntas")

class ResultadoQuiz(Base):
    __tablename__ = "resultados_quiz"
    
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    puntaje = Column(Integer)
    preguntas_correctas = Column(Integer)
    total_preguntas = Column(Integer)
    fecha = Column(DateTime, default=datetime.utcnow)
    tiempo_completado_minutos = Column(Integer)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="resultados_quiz")

class AnalyticsDiario(Base):
    __tablename__ = "analytics_diarios"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, unique=True)
    total_estudiantes_activos = Column(Integer, default=0)
    total_preguntas = Column(Integer, default=0)
    promedio_puntaje_quiz = Column(Float, default=0.0)
    categoria_mas_consultada = Column(String(50))
    pregunta_mas_frecuente = Column(Text) 