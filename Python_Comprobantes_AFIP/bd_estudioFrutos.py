import pyodbc
from datetime import datetime

def obtener_cuit(server, database, username, password):
    """
    Consulta a la base de datos para obtener los CUITs activos.
    """
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        query = """
        SELECT CLIENTE_ID
        FROM LK_CLIENTES
        WHERE ESTADO = 'A' AND AFIP_CATEGORIA <> 'INQUI'
        """
        cursor = conn.cursor()
        cursor.execute(query)
        resultados = [row[0] for row in cursor.fetchall()]
        conn.close()
        return resultados
    except Exception as e:
        raise Exception(f"Error al consultar la base de datos: {e}")


def validate_and_transform(data):
    """
    Valida y transforma los datos para la inserción.
    """
    try:
        return {
            'Cliente_ID': int(data.get('Cliente_ID')) if data.get('Cliente_ID') else None,
            'Estado': data.get('Estado', '').strip(),
            'Fecha_ID': datetime.strptime(data.get('Fecha_ID'), '%Y-%m-%d').date() if data.get('Fecha_ID') else None
        }
    except KeyError as ke:
        print(f"Clave faltante en los datos: {ke}")
        return None
    except ValueError as ve:
        print(f"Valor inválido: {ve}")
        return None
    except Exception as e:
        print(f"Error transformando datos: {e}")
        return None


 