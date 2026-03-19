from fastapi import FastAPI, HTTPException
import requests
import asyncio
from database import get_connection

app = FastAPI()

ip_local = "127.0.0.1"

# Crear usuario
@app.post("/usuarios")
async def crear_usuario(nombre : str, numero_cel : str):
    global ip_local

    try:
        # validar si el numero de celular ya esta registrado
        conn = await get_connection()
        cursor = await conn.cursor()

        query_num_cel = "SELECT numero_cel FROM usuarios WHERE numero_cel=%s"
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query_num_cel, (numero_cel))
        
        resultado = await cursor.fetchone()  # Obtener el resultado

        await cursor.close()
        conn.close()
        
        if resultado:
            return {"mensaje" : "El numero de celular ya se encuentra registrado"}
    except:
        raise HTTPException(
            status_code=503, 
            detail="Servicio de Consulta de Usuarios no disponible")


    try:
        await asyncio.sleep(2)  # simulación de proceso lento
        conn = await get_connection()
        cursor = await conn.cursor()

        query = """
        INSERT INTO usuarios (nombre, numero_cel) VALUES (%s, %s)
        """
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query, (nombre, numero_cel))
        await conn.commit()

        await cursor.close()
        conn.close()

        return {"mensaje": "Usuario registrado correctamente"}
    except Exception as e:
        # Manejo de errores básico
        raise HTTPException(status_code=500, detail=f"Error al registrar el paciente: {str(e)}")

# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8001) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)