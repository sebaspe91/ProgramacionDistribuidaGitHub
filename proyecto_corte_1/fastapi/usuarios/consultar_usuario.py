from fastapi import FastAPI, HTTPException
import requests
import asyncio
from database import get_connection

app = FastAPI()

ip_local = "127.0.0.1"

# listar usuarios
@app.get("/usuarios/{numero_cel}")
async def listar_usaurios(numero_cel : int):
    try:
        await asyncio.sleep(2)  # simulación de proceso lento
        conn = await get_connection()
        cursor = await conn.cursor()
        
        query = "SELECT * FROM usuarios WHERE numero_cel=%s"
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query, (numero_cel,))
        
        usuarios = await cursor.fetchone()

        await cursor.close()
        conn.close()

        

        if not usuarios:
            
            raise HTTPException(
                status_code=404,
                detail="usuario no encontrado"
            )

        return usuarios
    except Exception as e:
        
        # Manejo de errores básico
        raise HTTPException(status_code=500, detail=f"Error al encontrar el usuarios: {str(e)}")

# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8003) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8003
    uvicorn.run(app, host="0.0.0.0", port=8003)