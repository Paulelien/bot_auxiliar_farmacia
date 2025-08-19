"""
Integración LTI (Learning Tools Interoperability) para el Bot Asistente Virtual de Farmacia
Permite integrar el bot directamente en Open edX como una herramienta externa
"""

import hashlib
import hmac
import base64
import urllib.parse
import time
import json
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request, Form
from fastapi.responses import HTMLResponse
import requests

class LTIIntegration:
    """Clase para manejar la integración LTI con Open edX"""
    
    def __init__(self, consumer_key: str, consumer_secret: str):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.lti_version = "LTI-1p0"
        self.oauth_version = "1.0"
        self.oauth_signature_method = "HMAC-SHA1"
    
    def generate_oauth_signature(self, params: Dict[str, str], method: str, url: str) -> str:
        """Genera la firma OAuth para la autenticación LTI"""
        # Ordenar parámetros
        sorted_params = sorted(params.items())
        
        # Crear string de parámetros
        param_string = "&".join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted_params])
        
        # Crear string base para firma
        base_string = "&".join([
            method,
            urllib.parse.quote(url, safe=''),
            urllib.parse.quote(param_string, safe='')
        ])
        
        # Generar firma HMAC-SHA1
        signature = hmac.new(
            self.consumer_secret.encode('utf-8'),
            base_string.encode('utf-8'),
            hashlib.sha1
        ).digest()
        
        return base64.b64encode(signature).decode('utf-8')
    
    def validate_lti_request(self, request_data: Dict[str, Any]) -> bool:
        """Valida una solicitud LTI entrante"""
        try:
            # Verificar parámetros requeridos
            required_params = [
                'oauth_consumer_key',
                'oauth_signature',
                'oauth_timestamp',
                'oauth_nonce',
                'lti_message_type',
                'lti_version'
            ]
            
            for param in required_params:
                if param not in request_data:
                    raise ValueError(f"Parámetro requerido faltante: {param}")
            
            # Verificar timestamp (no más de 5 minutos de diferencia)
            timestamp = int(request_data['oauth_timestamp'])
            current_time = int(time.time())
            if abs(current_time - timestamp) > 300:  # 5 minutos
                raise ValueError("Timestamp expirado")
            
            # Verificar firma
            received_signature = request_data['oauth_signature']
            calculated_signature = self.generate_oauth_signature(
                {k: v for k, v in request_data.items() if k != 'oauth_signature'},
                'POST',
                request_data.get('tool_consumer_instance_url', '')
            )
            
            if not hmac.compare_digest(received_signature, calculated_signature):
                raise ValueError("Firma OAuth inválida")
            
            return True
            
        except Exception as e:
            print(f"Error validando solicitud LTI: {e}")
            return False
    
    def extract_user_info(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae información del usuario desde los datos LTI"""
        return {
            'user_id': request_data.get('user_id'),
            'lis_person_name_full': request_data.get('lis_person_name_full'),
            'lis_person_contact_email_primary': request_data.get('lis_person_contact_email_primary'),
            'roles': request_data.get('roles', '').split(','),
            'context_id': request_data.get('context_id'),
            'context_title': request_data.get('context_title'),
            'resource_link_id': request_data.get('resource_link_id'),
            'resource_link_title': request_data.get('resource_link_title'),
            'tool_consumer_instance_url': request_data.get('tool_consumer_instance_url'),
            'tool_consumer_instance_name': request_data.get('tool_consumer_instance_name')
        }
    
    def create_lti_response(self, user_info: Dict[str, Any]) -> str:
        """Crea la respuesta HTML para la integración LTI"""
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Asistente Virtual - {user_info.get('context_title', 'Curso')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .lti-header {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            text-align: center;
        }}
        .lti-header h1 {{
            color: #333;
            margin: 0;
            font-size: 24px;
        }}
        .lti-header p {{
            color: #666;
            margin: 10px 0 0 0;
        }}
        .bot-container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .chat-header {{
            background: #7c3faf;
            color: white;
            padding: 15px 20px;
            text-align: center;
        }}
        .chat-header h2 {{
            margin: 0;
            font-size: 18px;
        }}
        .chat-messages {{
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }}
        .chat-input {{
            display: flex;
            padding: 20px;
            background: white;
            border-top: 1px solid #e9ecef;
        }}
        .chat-input input {{
            flex: 1;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
        }}
        .chat-input input:focus {{
            border-color: #7c3faf;
        }}
        .chat-input button {{
            margin-left: 10px;
            padding: 12px 24px;
            background: #7c3faf;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }}
        .chat-input button:hover {{
            background: #6b35a0;
        }}
        .message {{
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 80%;
            word-wrap: break-word;
        }}
        .message.user {{
            background: #7c3faf;
            color: white;
            margin-left: auto;
        }}
        .message.bot {{
            background: white;
            color: #333;
            border: 1px solid #e9ecef;
        }}
        .user-info {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #2196f3;
        }}
        .user-info h3 {{
            margin: 0 0 10px 0;
            color: #1976d2;
        }}
        .user-info p {{
            margin: 5px 0;
            color: #424242;
        }}
    </style>
</head>
<body>
    <div class="lti-header">
        <h1>🏥 Bot Asistente Virtual de Farmacia</h1>
        <p>Integrado en: {user_info.get('context_title', 'Curso')}</p>
    </div>
    
    <div class="user-info">
        <h3>👤 Información del Usuario</h3>
        <p><strong>Nombre:</strong> {user_info.get('lis_person_name_full', 'No disponible')}</p>
        <p><strong>Email:</strong> {user_info.get('lis_person_contact_email_primary', 'No disponible')}</p>
        <p><strong>Rol:</strong> {', '.join(user_info.get('roles', ['Estudiante']))}</p>
        <p><strong>Instancia:</strong> {user_info.get('tool_consumer_instance_name', 'Open edX')}</p>
    </div>
    
    <div class="bot-container">
        <div class="chat-header">
            <h2>💬 Chat con el Asistente Virtual</h2>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                ¡Hola! Soy tu asistente virtual de farmacia. ¿En qué puedo ayudarte hoy?
            </div>
        </div>
        
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Escribe tu pregunta aquí..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>
    
    <script>
        let sessionId = '{user_info.get('user_id', '')}_{user_info.get('context_id', '')}';
        
        function handleKeyPress(event) {{
            if (event.key === 'Enter') {{
                sendMessage();
            }}
        }}
        
        function sendMessage() {{
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (message) {{
                addMessage('user', message);
                input.value = '';
                
                // Mostrar mensaje de carga
                const loadingId = addMessage('bot', 'El asistente está escribiendo...');
                
                // Enviar pregunta al bot
                fetch('/preguntar', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        pregunta: message,
                        session_id: sessionId,
                        user_info: {{
                            user_id: '{user_info.get('user_id', '')}',
                            context_id: '{user_info.get('context_id', '')}',
                            roles: {user_info.get('roles', [])},
                            lti_integration: true
                        }}
                    })
                }})
                .then(response => response.json())
                .then(data => {{
                    // Remover mensaje de carga
                    const loadingElement = document.getElementById(loadingId);
                    if (loadingElement) {{
                        loadingElement.remove();
                    }}
                    
                    // Mostrar respuesta del bot
                    addMessage('bot', data.respuesta);
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    const loadingElement = document.getElementById(loadingId);
                    if (loadingElement) {{
                        loadingElement.remove();
                    }}
                    addMessage('bot', 'Lo siento, hubo un error al procesar tu pregunta. Por favor, inténtalo de nuevo.');
                }});
            }}
        }}
        
        function addMessage(sender, text) {{
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            const messageId = 'msg_' + Date.now();
            
            messageDiv.id = messageId;
            messageDiv.className = `message ${{sender}}`;
            messageDiv.textContent = text;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            return messageId;
        }}
        
        // Mensaje de bienvenida personalizado
        setTimeout(() => {{
            const welcomeMessage = `¡Bienvenido al curso de Auxiliar de Farmacia! 
            
Estoy aquí para ayudarte con:
• Consultas sobre medicamentos
• Casos clínicos
• Información farmacológica
• Dudas sobre el curso

¿Con qué te puedo ayudar hoy?`;
            
            const loadingElement = document.querySelector('.message.bot');
            if (loadingElement) {{
                loadingElement.textContent = welcomeMessage;
            }}
        }}, 1000);
    </script>
</body>
</html>
"""

# Configuración LTI para Open edX
LTI_CONFIG = {
    "title": "Bot Asistente Virtual de Farmacia",
    "description": "Asistente virtual especializado en farmacología y casos clínicos",
    "launch_url": "/lti/launch",
    "icon": "https://cdn-icons-png.flaticon.com/512/1995/1995574.png",
    "secure_launch_url": "/lti/launch",
    "privacy_level": "public",
    "lti_version": "LTI-1p0",
    "tool_consumer_info_product_family_code": "canvas",
    "extensions": {
        "canvas": {
            "privacy_level": "public",
            "domain": "your-domain.com"
        }
    }
}

# Configuración XML para Open edX
LTI_XML_CONFIG = f"""<?xml version="1.0" encoding="UTF-8"?>
<cartridge_basiclti_link xmlns="http://www.imsglobal.org/xsd/imslticc_v1p0"
    xmlns:blti = "http://www.imsglobal.org/xsd/imsbasiclti_v1p0"
    xmlns:lticm ="http://www.imsglobal.org/xsd/imslticm_v1p0"
    xmlns:lticp ="http://www.imsglobal.org/xsd/imslticp_v1p0"
    xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation = "http://www.imsglobal.org/xsd/imslticc_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticc_v1p0.xsd
    http://www.imsglobal.org/xsd/imsbasiclti_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imsbasiclti_v1p0.xsd
    http://www.imsglobal.org/xsd/imslticm_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticm_v1p0.xsd
    http://www.imsglobal.org/xsd/imslticp_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticp_v1p0.xsd">
    <blti:title>{LTI_CONFIG['title']}</blti:title>
    <blti:description>{LTI_CONFIG['description']}</blti:description>
    <blti:launch_url>{LTI_CONFIG['launch_url']}</blti:launch_url>
    <blti:extensions platform="canvas">
        <lticm:property name="privacy_level">public</lticm:property>
        <lticm:property name="domain">your-domain.com</lticm:property>
    </blti:extensions>
    <cartridge_bundle identifierref="BLTI001_Bundle"/>
    <cartridge_icon identifierref="BLTI001_Icon"/>
</cartridge_basiclti_link>"""

def get_lti_config():
    """Retorna la configuración LTI"""
    return LTI_CONFIG

def get_lti_xml():
    """Retorna la configuración XML para Open edX"""
    return LTI_XML_CONFIG

def create_lti_launch_url(base_url: str, consumer_key: str, context_id: str, user_id: str) -> str:
    """Crea una URL de lanzamiento LTI para pruebas"""
    params = {
        'lti_message_type': 'basic-lti-launch-request',
        'lti_version': 'LTI-1p0',
        'resource_link_id': 'bot_farmacia',
        'resource_link_title': 'Bot Asistente Virtual',
        'user_id': user_id,
        'context_id': context_id,
        'roles': 'Learner',
        'oauth_consumer_key': consumer_key,
        'oauth_timestamp': str(int(time.time())),
        'oauth_nonce': str(int(time.time() * 1000)),
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_version': '1.0'
    }
    
    # Generar firma
    lti = LTIIntegration(consumer_key, 'your_secret_here')
    signature = lti.generate_oauth_signature(params, 'POST', base_url)
    params['oauth_signature'] = signature
    
    # Crear URL
    query_string = '&'.join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    return f"{base_url}?{query_string}"

