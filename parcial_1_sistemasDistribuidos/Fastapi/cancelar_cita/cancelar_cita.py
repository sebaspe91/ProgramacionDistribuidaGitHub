from fastapi import FastAPI, HTTPException
import requests
import asyncio
from database import get_connection

app = FastAPI()

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


# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8005) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8005
    uvicorn.run(app, host="0.0.0.0", port=8005)