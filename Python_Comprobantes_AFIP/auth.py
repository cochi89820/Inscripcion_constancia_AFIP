from afip import Afip

def inicializar_afip(cuit, cert, key, access_token, production=True):
    """Inicializa la instancia de AFIP."""
    return Afip({
        "CUIT": cuit,
        "cert": cert,
        "key": key,
        "access_token": access_token,
        "production": production
    })