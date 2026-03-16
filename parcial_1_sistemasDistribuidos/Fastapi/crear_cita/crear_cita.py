from fastapi import FastAPI, HTTPException
import requests
import asyncio
from database import get_connection

app = FastAPI()

# Crear cita
@app.post("/citas")
async def crear_cita(paciente_id : int, fecha : str):

    try:
        # consultamos la base de datos por medio de api
        r = requests.get(
            f"http://192.168.101.9:8002/pacientes/{paciente_id}",
            timeout=5
        )

        if r.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503, 
            detail="Servicio de Consulta de Pacientes no disponible")
    
    await asyncio.sleep(2)

    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = "INSERT INTO citas (paciente_id, fecha, estado) VALUES (%s, %s, %s)"
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query, (paciente_id, fecha, 'activa'))
        await conn.commit()

        await cursor.close()
        conn.close()

        return {"mensaje": "Citas creada correctamente"}
    except Exception as e:
        # Manejo de errores básico
        raise HTTPException(status_code=500, detail=f"Error al registrar la cita: {str(e)}")


# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8003) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8001
    uvicorn.run(app, host="0.0.0.0", port=8003)







