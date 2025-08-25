import csv
from bd_estudioFrutos import obtener_cuit
from auth import inicializar_afip
from servicio.constancia_inscripcion import (
    configurar_web_service,
    obtener_token_authorization,
    realizar_consulta_persona,
    procesar_respuesta
)

def cargar_archivo(ruta):
    """Carga un archivo y devuelve su contenido como texto."""
    with open(ruta, "r") as archivo:
        return archivo.read()

def guardar_datos_csv(datos, ruta_archivo):
    """Guarda los datos en un archivo CSV delimitado por punto y coma."""
    try:
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Escribir encabezados
            escritor.writerow(["CUIT", "Estado", "Fecha", "Error"])

        
            for fila in datos:
                cliente_id = fila.get("CUIT", "N/A")
                estado = fila.get("EstadoClave", "N/A")
                fecha_id = fila.get("FechaHora", "N/A").split('T')[0] if "FechaHora" in fila else "N/A"
                error = " | ".join(fila.get("Errores", []))  
                escritor.writerow([cliente_id, estado, fecha_id, error])

        print(f"Datos guardados correctamente en {ruta_archivo}")
    except Exception as e:
        print(f"Error al guardar los datos en CSV: {e}")

def main():
    # Configuración
    CUIT = 20400953385
    CERT_PATH = "C:/Users/Administrador/Desktop/Python_Comprobantes_AFIP/certificados_prod/certificadoproduccion.pem"
    KEY_PATH = "C:/Users/Administrador/Desktop/Python_Comprobantes_AFIP/certificados_prod/claveproduccion"
    ACCESS_TOKEN = "6oQpsX0zeeBOaO7xKX3UU4ZPVxOKcFbYqj3pYwqp5TfZMzV2sTAvkl9BLrVuKg6i"
    URL_TEST = "https://servicios.afip.gov.ar/sr-padron/webservices/personaServiceA5"
    SERVICIO = "ws_sr_constancia_inscripcion"

    # Parámetros de la base de datos
    SERVER = 'T-SERVER4'
    DATABASE = 'DWESTUDIO'
    USERNAME = 'sa'
    PASSWORD = 'Remote98'

    # Ruta para guardar el archivo CSV
    RUTA_ARCHIVO_CSV = r"P:\PROGRAMACION\ESTUDIO\CSV_WS_AFIP\datos_clientes.csv"

    try:
        # Cargar certificado y clave
        cert = cargar_archivo(CERT_PATH)
        key = cargar_archivo(KEY_PATH)

        # Inicialización
        afip = inicializar_afip(CUIT, cert, key, ACCESS_TOKEN)
        web_service = configurar_web_service(afip, SERVICIO, URL_TEST)

        # Obtención de token y autorización
        ta = obtener_token_authorization(web_service)

        # Consulta de CUITs desde la base de datos
        cuits = obtener_cuit(SERVER, DATABASE, USERNAME, PASSWORD)
        print(f"CUITs obtenidos: {cuits}")

        # Lista para almacenar los datos a guardar
        datos_a_guardar = []

        # Consulta al servicio de AFIP para cada CUIT
        for cuit_persona in cuits:
            try:
                response = realizar_consulta_persona(
                    web_service,
                    token=ta["token"],
                    sign=ta["sign"],
                    cuit_representada=CUIT,
                    id_persona=cuit_persona
                )
                # Procesa y guarda la respuesta
                datos = procesar_respuesta(response)
                datos_a_guardar.append(datos)

            except Exception as e:
                print(f"Error al consultar CUIT {cuit_persona}: {e}")

        # Guarda los datos en un archivo CSV
        if datos_a_guardar:
            print(f"Datos a guardar: {datos_a_guardar}")
            guardar_datos_csv(datos_a_guardar, RUTA_ARCHIVO_CSV)
        else:
            print("No hay datos válidos para guardar en el archivo CSV.")

    except Exception as e:
        print("Error en la ejecución principal:", e)

if __name__ == "__main__":
    main()