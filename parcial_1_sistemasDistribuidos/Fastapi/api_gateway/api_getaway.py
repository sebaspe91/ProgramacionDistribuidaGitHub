from fastapi import FastAPI, HTTPException
import requests
import asyncio
from database import get_connection

app = FastAPI()

# getaway cita
@app.post("/reservar-cita")
def reservar(paciente_id:int, fecha:str):
    r = requests.post(
        "http://192.168.101.9:8003/citas",
        params={"paciente_id": paciente_id, "fecha": fecha}
    )

    return r.json()


# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8000) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)