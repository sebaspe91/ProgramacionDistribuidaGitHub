
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

# Buscar citas por paciente 
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

# Listar citas activas
@app.get("/citas_activas")
async def citasActivas():
    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = "SELECT * FROM citas WHERE estado='activo'"
        await cursor.execute(query)

        citas = await cursor.fetchall() # se agrega los datos que se trae de la base de datos ya tratados para q lo entienda python lo trae con varios resultado como una dubla o listas

        await cursor.close()
        conn.close()

        return citas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar citas: {str(e)}")

# lista todas las citas tanto activas como canceladas
@app.get("/conteo_citas")
async def conteo_citas():
    try:
        conn = await get_connection() 
        cursor = await conn.cursor()

        query = "SELECT COUNT(*) AS total_citas FROM citas"
        await cursor.execute(query)

        resultado = await cursor.fetchone() # se agrega los datos que se trae de la base de datos ya tratados para q lo entienda python
        # .fetchone()===> trae solo un resultado

        # extrae el primer elemento si no hay resultado develve 0
        total = resultado[0] if resultado else 0

        await cursor.close()
        conn.close()

        return {"mensaje": f"El total de citas es: {total}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar citas: {str(e)}")
    

# lista todas las citas activas o canceladas
@app.get("/conteo_citas_estado/{estado}")
async def conteo_citas_estado(estado : str):
    try:
        # if not estado == 'activo' or not estado == 'cancelada' :
        #     raise HTTPException(
        #         status_code=400, 
        #         detail=f"El estado {estado} no es permito en el programa, Solo se aceptan activo o cancelada"
        #     )
        
        conn = await get_connection() 
        cursor = await conn.cursor()

        query = "SELECT COUNT(*) AS total_citas FROM citas WHERE estado=%s"
        await cursor.execute(query, (estado,))

        resultado = await cursor.fetchone() # se agrega los datos que se trae de la base de datos ya tratados para q lo entienda python
        # .fetchone()===> trae solo un resultado

        # extrae el primer elemento si no hay resultado develve 0
        total = resultado[0] if resultado else 0

        await cursor.close()
        conn.close()

        return {"mensaje": f"El total de citas {estado} es: {total}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar citas: {str(e)}")
    

# Reactivar cita cancelada
@app.put("/reactivar_cita/{id}")
async def reactiva_cita(id : int):
    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = "UPDATE citas SET estado='activo' WHERE id=%s"

        await cursor.execute(query, (id,))
        await conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, 
                detail="Cita no encontrada"
            )

        await cursor.close()
        conn.close()

        return {"mensaje": "Cita reactivada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al reactivar cita: {str(e)}")
    
############  TRABAJO INDEPENDIENTE ##############################

# actualizar fecha
@app.put("/actualizar_fecha/{id}")
async def actualizar_fecha(id : int, fehca : str):
    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = f"UPDATE citas SET fecha='{fehca}' WHERE id={id}"
        await cursor.execute(query)
        await conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, 
                detail="Cita no encontrada"
            )
        
        await cursor.close()
        conn.close()

        return {"mensaje" : "Fecha actualizada correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar fecha de la cita: {str(e)}")
    

# NOTA: CANCELAR CITA YA ESTA MAS ARRIBA

# listar cita por fecha
@app.get("/listar_fecha/{fecha}")
async def listar_cita_fecha(fecha: str):
    try:
        conn = await get_connection()
        cursor = await conn.cursor()

        query = "SELECT * FROM citas WHERE fecha = %s"
        await cursor.execute(query, (fecha,))
        citas = await cursor.fetchall()

        await cursor.close()
        conn.close()

        if not citas:
            raise HTTPException(status_code=404, detail="No se encontraron citas para esta fecha")
        
        return citas

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al encontrar la fecha de la cita: {str(e)}")