

import aiomysql

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "db": "citas_db",
    "autocommit": False  # Recomendado para tener control sobre commits
}

async def get_connection():
    try:
        # crea una conexion async con la base de datos
        conn = await aiomysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise e