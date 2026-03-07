
# CODIGO CORREGIDO

from fastapi import FastAPI, HTTPException
import asyncio
from database import get_connection

app = FastAPI()

# Crear cita
@app.post("/citas")
async def crear_cita(paciente: str, fecha: str):
    try:
        await asyncio.sleep(2)  # simulación de proceso lento
        conn = await get_connection()
        cursor = await conn.cursor()

        query = """
        INSERT INTO citas (paciente, fecha, estado) VALUES (%s, %s, %s)
        """
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query, (paciente, fecha, "activo"))
        await conn.commit()

        await cursor.close()
        conn.close()

        return {"mensaje": "Cita creada correctamente"}
    except Exception as e:
        # Manejo de errores básico
        raise HTTPException(status_code=500, detail=f"Error al crear cita: {str(e)}")

# Obtener todos los registros
@app.get("/citas")
async def listar_citas():
    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = "SELECT * FROM citas"
        await cursor.execute(query)
        citas = await cursor.fetchall()

        await cursor.close()
        conn.close()

        return citas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar citas: {str(e)}")

# Buscar citas por paciente - CORREGIDO: quitado el "7"
@app.get("/citas/{paciente}")
async def buscar_cita(paciente: str):
    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = "SELECT * FROM citas WHERE paciente = %s"
        await cursor.execute(query, (paciente,))
        cita = await cursor.fetchone()

        await cursor.close()
        conn.close()

        if not cita:
            raise HTTPException(
                status_code=404,
                detail="Cita no encontrada"
            )

        return cita
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar cita: {str(e)}")

# Cancelar cita
@app.delete("/citas/{id}")
async def cancelar_cita(id: int):
    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = "UPDATE citas SET estado='cancelada' WHERE id=%s"
        await cursor.execute(query, (id,))
        await conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        await cursor.close()
        conn.close()

        return {"mensaje": "Cita cancelada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cancelar cita: {str(e)}")