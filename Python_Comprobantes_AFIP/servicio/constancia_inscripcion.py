from datetime import datetime

def configurar_web_service(afip, servicio, url_test, soap_v1_2=True):
    """Configura y devuelve un web service."""
    options = {
        "URL_TEST": url_test,
        "soapV1_2": soap_v1_2
    }
    return afip.webService(servicio, options)

def obtener_token_authorization(web_service):
    """Obtiene el token y la autorización para el servicio."""
    return web_service.getTokenAuthorization()

def realizar_consulta_persona(web_service, token, sign, cuit_representada, id_persona):
    """Realiza la consulta de datos de una persona."""
    data = {
        "token": token,
        "sign": sign,
        "cuitRepresentada": cuit_representada,
        "idPersona": id_persona
    }
    return web_service.executeRequest("getPersona_v2", data)

def procesar_respuesta(response):
    """Procesa la respuesta del servidor y devuelve los datos estructurados."""

    if "personaReturn" not in response:
        raise Exception("La respuesta no contiene el campo esperado: 'personaReturn'.")

    persona = response["personaReturn"]

    # datos comunes
    cuit_persona = persona.get("datosGenerales", {}).get("idPersona", "N/A")
    estado_clave = persona.get("datosGenerales", {}).get("estadoClave", "N/A")
    fecha_hora = datetime.now().strftime("%Y-%m-%d")
    errores = []

    # Manejo de errores en la constancia
    if "errorConstancia" in persona:
        error_info = persona["errorConstancia"]
        estado_clave = "BLOQUEADO"   
        errores = error_info.get("error", [])
        cuit_persona = error_info.get("idPersona", cuit_persona)
        fecha_hora = datetime.now().strftime("%Y-%m-%d")
    # Retorna los datos estructurados
    return {
        "CUIT": cuit_persona,
        "EstadoClave": estado_clave,
        "FechaHora": fecha_hora,
        "Errores": errores
    }