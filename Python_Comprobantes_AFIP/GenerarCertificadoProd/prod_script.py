
from afip import Afip

tax_id = 20400953385

# Usuario para ingresar a AFIP.
# Para la mayoria es el mismo CUIT, pero al administrar
# una sociedad el CUIT con el que se ingresa es el del administrador
# de la sociedad.
username = "20400953385"

# Contraseña para ingresar a AFIP.
password = "03idargmoO"

# Alias para el certificado (Nombre para reconocerlo en AFIP)
# un alias puede tener muchos certificados, si estas renovando
# un certificado pordes utilizar le mismo alias
cert_alias = "certificadoproduccion"


# Creamos una instancia de la libreria
afip = Afip({
    "CUIT": tax_id,
    "access_token": "RHn8MPJDN1NyiqZzThj2I7FDMYSgYLcaarekGLv3XJOhzyPHwzE5OK980tWXxW56",
    "production": True
})

# Creamos el certificado (¡Paciencia! Esto toma unos cuantos segundos)
res = afip.createCert(username, password, cert_alias)

# Mostramos el certificado por pantalla
print(res["cert"])

# Mostramos la key por pantalla
print(res["key"])