from afip import Afip

# CUIT vinculado al certificado
CUIT = 20400953385
 
# Certificado y clave
cert = open("C:/Users/Administrador/Desktop/Python_Comprobantes_AFIP/certificados_prod/certificadoproduccion.pem").read()  # Actualiza el archivo de certificado
key = open("C:/Users/Administrador/Desktop/Python_Comprobantes_AFIP/certificados_prod/claveproduccion").read()  # Actualiza el archivo de clave

# Token de acceso obtenido desde el portal de la libreria AFIP
access_token = "RHn8MPJDN1NyiqZzThj2I7FDMYSgYLcaarekGLv3XJOhzyPHwzE5OK980tWXxW56" 

# Inicializamos la clase Afip con los parámetros para producción
afip = Afip({
    "CUIT": CUIT,
    "cert": cert,
    "key": key,
    "access_token": access_token,
    "production": True  
})

# Configuración del web service en producción
URL_TEST = "https://servicios.afip.gov.ar/sr-padron/webservices/personaServiceA5"  # URL de producción
soapV1_2 = True
servicio = "ws_sr_constancia_inscripcion"

options = {
    "URL_TEST": URL_TEST,
    "soapV1_2": soapV1_2
}

# Creación del web service
genericWebService = afip.webService(servicio, options)

# Obtención del Token Authorization
ta = genericWebService.getTokenAuthorization()

# Datos para la consulta
data = {
    "token": ta["token"],
    "sign": ta["sign"],
    "cuitRepresentada": afip.CUIT,
    "idPersona": 20940691169
}

try:
    # Realizamos la request al servicio web
    response = genericWebService.executeRequest("getPersona_v2", data)
    print("Respuesta completa del servidor:", response)

    # Validamos la estructura de la respuesta
    if "personaReturn" in response:
        persona = response["personaReturn"]
        print("Datos de la persona:", persona)

        # Validamos si existe un error en la constancia
        if "errorConstancia" in persona:
            error = persona["errorConstancia"]
            print("Error en la constancia:", error)

            # Imprimimos detalles del error si están presentes
            if "error" in error:
                print("Errores:", error["error"])
        else:
            print("No se encontraron errores en la constancia.")

    else:
        raise Exception("El campo 'personaReturn' no está presente en la respuesta.")
except Exception as e:
    print("Error en la ejecución:", e)

