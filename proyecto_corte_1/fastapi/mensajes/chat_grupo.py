from fastapi import FastAPI, HTTPException
import requests
import asyncio
from database import get_connection

app = FastAPI()


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
        
        # VERIFICAR SI ES UNA LISTA (como muestra tu error)
        if isinstance(datos_usuario, list):
         
            if len(datos_usuario) > 0:
                # Tomar el primer elemento de la lista (asumiendo que es un diccionario)
                primer_usuario = datos_usuario[0]
           
                return primer_usuario
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"El {msm_error} no tiene datos válidos"
                )
        
        # Si es un diccionario directamente
        elif isinstance(datos_usuario, dict):
            id_usuario = datos_usuario.get("id_usuario")
            print("ID USUARIO EXTRAÍDO (dict):", id_usuario)
            return id_usuario
        
        # Si es otro tipo de dato
        else:
            print(f"Tipo de dato no esperado: {type(datos_usuario)}")
            raise HTTPException(
                status_code=500,
                detail=f"Formato de datos no esperado para {msm_error}"
            )

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Servicio de Consulta de mensajes no disponible"
        )



# Crear cita
@app.post("/mensajes")
async def crear_mensaje_publico(numero_cel_origen : str, mensaje : str, ):    
    
    id_usuario_origen = validarExistencia(numero_cel_origen, "usuario origen")

    await asyncio.sleep(2)

    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = "INSERT INTO mensajes (usuario_origen_id, usuario_destino_id, mensaje, estado_mensaje, tipo_mensaje) VALUES (%s, %s, %s, %s, %s)"
        # Corregido: execute (no excecute) y solo 2 parámetros para 3 placeholders
        await cursor.execute(query, (id_usuario_origen, 1, mensaje, 'ver', 'publico',))
        await conn.commit()

        await cursor.close()
        conn.close()

        return {"mensaje": "Mensaje publico creado correctamente"}
    except Exception as e:
        # Manejo de errores básico
        raise HTTPException(status_code=500, detail=f"Error al registrar el mensaje publico: {str(e)}")


# --- INICIO DEL SERVIDOR (UNIFICADO EN PUERTO 8006) ---
if __name__ == "__main__":
    import uvicorn
    # Ahora todo corre en el puerto 8004
    uvicorn.run(app, host="0.0.0.0", port=8006)







