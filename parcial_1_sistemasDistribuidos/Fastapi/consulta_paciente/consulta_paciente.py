# CODIGO CORREGIDO

from fastapi import FastAPI, HTTPException
import asyncio
from database import get_connection

app = FastAPI()

# consultar paciente
@app.get("/pacientes/{id}")
async def consultar_paciente(id: int):
    
    try:
        await asyncio.sleep(2)  # simulación de proceso lento
        conn = await get_connection()
        cursor = await conn.cursor()
        
        query = "SELECT * FROM pacientes WHERE id=%s"
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query, (id,))
        
        paciente = await cursor.fetchone()

        await cursor.close()
        conn.close()

        

        if not paciente:
            
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        return paciente
    except Exception as e:
        
        # Manejo de errores básico
        raise HTTPException(status_code=500, detail=f"Error al registrar el paciente: {str(e)}")

# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8003) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8001
    uvicorn.run(app, host="0.0.0.0", port=8002)

