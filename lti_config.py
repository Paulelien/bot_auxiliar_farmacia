"""
Configuración LTI para el Bot Asistente Virtual de Farmacia
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
LTI_XML_CONFIG = """<?xml version="1.0" encoding="UTF-8"?>
<cartridge_basiclti_link xmlns="http://www.imsglobal.org/xsd/imslticc_v1p0"
    xmlns:blti = "http://www.imsglobal.org/xsd/imsbasiclti_v1p0"
    xmlns:lticm ="http://www.imsglobal.org/xsd/imslticm_v1p0"
    xmlns:lticp ="http://www.imsglobal.org/xsd/imslticp_v1p0"
    xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation = "http://www.imsglobal.org/xsd/imslticc_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticc_v1p0.xsd
    http://www.imsglobal.org/xsd/imsbasiclti_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imsbasiclti_v1p0.xsd
    http://www.imsglobal.org/xsd/imslticm_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticm_v1p0.xsd
    http://www.imsglobal.org/xsd/imslticp_v1p0 http://www.imsglobal.org/xsd/lti/ltiv1p0/imslticp_v1p0.xsd">
    <blti:title>Bot Asistente Virtual de Farmacia</blti:title>
    <blti:description>Asistente virtual especializado en farmacología y casos clínicos</blti:description>
    <blti:launch_url>/lti/launch</blti:launch_url>
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


