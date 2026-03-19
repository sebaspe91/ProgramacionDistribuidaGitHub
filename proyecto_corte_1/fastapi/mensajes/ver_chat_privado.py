from fastapi import FastAPI, HTTPException
import requests
import asyncio
from database import get_connection

app = FastAPI()

ip_local = "127.0.0.1"

# funcion de validacion de usuario
def validarExistencia(numero_cel: str, msm_error: str):
    print(f"Validando existencia de {msm_error} con celular: {numero_cel}")
    try:
        # consultamos la base de datos por medio de api
        r = requests.get(
            f"http://127.0.0.1:8003/usuarios/{numero_cel}",
            timeout=5
        )

        if r.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontro el {msm_error} en la base de datos"
            )
        
        # Obtener los datos de la respuesta
        datos_usuario = r.json()
        
        return datos_usuario

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Servicio de Consulta de Pacientes no disponible"
        )


# ver mensajes privados
@app.get("/mensajes/{numero_cel_origen}/{numero_cel_destino}")
async def ver_chat_privado(numero_cel_origen : str, numero_cel_destino : str):

    usuario_origen = validarExistencia(numero_cel_origen, "usuario origen")
    usuario_destino = validarExistencia(numero_cel_destino, "usuario destino")

    id_user_origen = usuario_origen[0]
    nombre_origen = usuario_origen[1]

    id_user_destino = usuario_destino[0]
    nombre_destino = usuario_destino[1]

    try:
        await asyncio.sleep(2)  # simulación de proceso lento
        conn = await get_connection()
        cursor = await conn.cursor()
        
        query = f"""
            SELECT u.nombre, m.mensaje FROM mensajes m JOIN usuarios u ON m.usuario_origen_id = u.id_usuario WHERE (usuario_origen_id = {id_user_origen} AND usuario_destino_id={id_user_destino}) OR (usuario_origen_id = {id_user_destino} AND usuario_destino_id={id_user_origen}) AND tipo_mensaje='privado' AND estado_mensaje='ver'
            ORDER BY fecha_mensaje ASC;
        """
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query)
        
        mensajes = await cursor.fetchall()

        await cursor.close()
        conn.close()

        

        if not mensajes:
            
            raise HTTPException(
                status_code=404,
                detail="mensajes no encontrados"
            )

        return {f"Chat entre: {nombre_origen} y {nombre_destino}": mensajes}
    except Exception as e:
        
        # Manejo de errores básico
        raise HTTPException(status_code=500, detail=f"Error al encontrar los mensajes: {str(e)}")

# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8004) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8004
    uvicorn.run(app, host="0.0.0.0", port=8005)