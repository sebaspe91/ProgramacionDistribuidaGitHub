# CODIGO CORREGIDO

from fastapi import FastAPI, HTTPException
import asyncio
from database import get_connection

app = FastAPI()

# Crear cita
@app.post("/pacientes")
async def registrar_paciente(nombre: str, email: str):
    try:
        await asyncio.sleep(2)  # simulación de proceso lento
        conn = await get_connection()
        cursor = await conn.cursor()

        query = """
        INSERT INTO pacientes (nombre, email) VALUES (%s, %s)
        """
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query, (nombre, email))
        await conn.commit()

        await cursor.close()
        conn.close()

        return {"mensaje": "Paciente registrado correctamente"}
    except Exception as e:
        # Manejo de errores básico
        raise HTTPException(status_code=500, detail=f"Error al registrar el paciente: {str(e)}")

# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8003) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)

# import asyncio
# import sys
# import os

# Agregar el directorio padre al path si es necesario
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from database import get_connection

# async def main():
#     try:
#         # Conexión a la base de datos
#         conn = await get_connection()
#         cursor = await conn.cursor()
        
#         # Ejecutar consulta
#         await cursor.execute("SHOW TABLES")
        
#         # Obtener y mostrar resultados
#         print("\n=== 📊 TABLAS EN LA BASE DE DATOS ===")
#         async for tabla in cursor:
#             print(f"{tabla[0]}")
        
#         # Cerrar conexión
#         await cursor.close()
#         await conn.close()
#         print("\n✅ Conexión cerrada correctamente")
        
#     except Exception as e:
#         print(f"\n❌ Error: {e}")

# # Ejecutar la función asíncrona
# if __name__ == "__main__":
#     asyncio.run(main())