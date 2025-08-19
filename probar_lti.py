#!/usr/bin/env python3
"""
Script para probar la integración LTI del Bot Asistente Virtual de Farmacia
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
BASE_URL = "http://localhost:8000"  # Cambiar por tu URL de producción
LTI_CONSUMER_KEY = os.getenv("LTI_CONSUMER_KEY", "test_consumer_key")
LTI_CONSUMER_SECRET = os.getenv("LTI_CONSUMER_SECRET", "test_consumer_secret")

def test_lti_endpoints():
    """Probar todos los endpoints LTI"""
    print("🧪 Probando integración LTI...")
    print("=" * 50)
    
    # 1. Probar endpoint de configuración
    print("\n1️⃣ Probando /lti/config...")
    try:
        response = requests.get(f"{BASE_URL}/lti/config")
        if response.status_code == 200:
            config = response.json()
            print("✅ Configuración LTI obtenida correctamente")
            print(f"   Título: {config.get('title')}")
            print(f"   Descripción: {config.get('description')}")
            print(f"   URL de lanzamiento: {config.get('launch_url')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Probar endpoint XML
    print("\n2️⃣ Probando /lti/xml...")
    try:
        response = requests.get(f"{BASE_URL}/lti/xml")
        if response.status_code == 200:
            print("✅ Configuración XML obtenida correctamente")
            print(f"   Tipo de contenido: {response.headers.get('content-type')}")
            print(f"   Tamaño: {len(response.content)} bytes")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Probar endpoint de prueba
    print("\n3️⃣ Probando /lti/test...")
    try:
        response = requests.get(f"{BASE_URL}/lti/test")
        if response.status_code == 200:
            test_data = response.json()
            print("✅ Endpoint de prueba funcionando")
            print(f"   Estado: {test_data.get('status')}")
            print(f"   Mensaje: {test_data.get('message')}")
            print(f"   Consumer Key: {test_data.get('config', {}).get('consumer_key')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Probar endpoint de lanzamiento (simulado)
    print("\n4️⃣ Probando /lti/launch (simulado)...")
    try:
        # Datos simulados de LTI
        lti_data = {
            'lti_message_type': 'basic-lti-launch-request',
            'lti_version': 'LTI-1p0',
            'resource_link_id': 'test_resource',
            'user_id': 'test_user_123',
            'context_id': 'test_course_456',
            'roles': 'Learner',
            'oauth_consumer_key': LTI_CONSUMER_KEY,
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': 'test_nonce_789',
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_version': '1.0',
            'oauth_signature': 'test_signature'  # Esto fallará, pero probamos el endpoint
        }
        
        response = requests.post(f"{BASE_URL}/lti/launch", data=lti_data)
        if response.status_code == 401:
            print("✅ Endpoint de lanzamiento responde correctamente (401 esperado por firma inválida)")
        else:
            print(f"⚠️ Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_basic_endpoints():
    """Probar endpoints básicos del bot"""
    print("\n🔍 Probando endpoints básicos...")
    print("=" * 50)
    
    # Probar endpoint principal
    print("\n1️⃣ Probando endpoint principal...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Endpoint principal funcionando")
        else:
            print(f"⚠️ Endpoint principal: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Probar endpoint de preguntas
    print("\n2️⃣ Probando endpoint de preguntas...")
    try:
        test_question = {
            "pregunta": "¿Qué es el paracetamol?",
            "session_id": "test_session_lti"
        }
        response = requests.post(f"{BASE_URL}/preguntar", json=test_question)
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint de preguntas funcionando")
            print(f"   Respuesta recibida: {len(data.get('respuesta', ''))} caracteres")
        else:
            print(f"⚠️ Endpoint de preguntas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def generate_lti_credentials():
    """Generar credenciales LTI de prueba"""
    print("\n🔑 Generando credenciales LTI de prueba...")
    print("=" * 50)
    
    import secrets
    
    consumer_key = secrets.token_hex(16)
    consumer_secret = secrets.token_urlsafe(32)
    
    print(f"Consumer Key: {consumer_key}")
    print(f"Consumer Secret: {consumer_secret}")
    
    print("\n📝 Agregar estas credenciales a tu archivo .env:")
    print(f"LTI_CONSUMER_KEY={consumer_key}")
    print(f"LTI_CONSUMER_SECRET={consumer_secret}")
    
    return consumer_key, consumer_secret

def main():
    """Función principal"""
    print("🏥 Bot Asistente Virtual de Farmacia - Pruebas LTI")
    print("=" * 60)
    
    # Verificar si el servidor está corriendo
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print("✅ Servidor detectado y funcionando")
    except requests.exceptions.RequestException:
        print("❌ No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo en:", BASE_URL)
        print("   O cambia BASE_URL en este script")
        return
    
    # Probar endpoints básicos
    test_basic_endpoints()
    
    # Probar endpoints LTI
    test_lti_endpoints()
    
    # Generar credenciales de prueba
    generate_lti_credentials()
    
    print("\n" + "=" * 60)
    print("🎯 Resumen de pruebas LTI:")
    print("✅ Si todos los endpoints responden, la integración LTI está funcionando")
    print("❌ Revisa los errores para identificar problemas")
    print("\n📚 Consulta GUIA_LTI_OPENDEX.md para más información")

if __name__ == "__main__":
    import time
    main()


