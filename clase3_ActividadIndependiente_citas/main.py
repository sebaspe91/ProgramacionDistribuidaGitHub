# ---- IMPORTACIONES ------
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any 
import asyncio 
from datetime import datetime, timedelta, date

# creacion de aplicacion
app = FastAPI()

# Base de datos
citas = []

# enpoints

# Benveidos a la cita
@app.get("/")
def home():
    return {"mensaje" : "Bienvenidos a la citas FORMATO DE FECHA 'AÑO-MES-DIA-HORA'"}

# crear cita
@app.post("/crear_citas")
async def crear_cita(nombre : str, cedula : str, fecha : str):

    # 5. Simulación de delay asíncrono de 2 segundos
    await asyncio.sleep(2)

    # validar campos
    if not nombre or nombre.strip() == "" or not cedula or cedula.strip() == "" or not fecha or fecha.strip() == "":
        raise HTTPException(
            status_code = 400,
            detail = "Todos los campos son obligatorios"
        )
    
    # validar que la cedula no sean la misma
    for citaX in citas :
        if citaX["cedula"] == cedula :
            raise HTTPException(
                status_code = 400,
                detail = f"La cedula {cedula} ya existe, registro denegado"
            )


    # citas
    fecha_actual = datetime.now().strftime("%Y-%m-%d-%H:%M")
    ano, mes, dia, hora = fecha_actual.split('-')

    # datos ingresados
    anoCita, mesCita, diaCita, horaCita = fecha.split('-')

    if ano <= anoCita :
        if mes <= mesCita :
            if dia <= diaCita :                
                # se puede crear la cita
                    # Objeto
                cita = {
                    "id" : len(citas) + 1,
                    "nombre" : nombre,
                    "cedula" : cedula,
                    "fecha" : fecha
                }

                # Agregar a la base de datos
                citas.append(cita)

                return {
                    "Cita": cita["id"],
                    "nombre": nombre,
                    "cedula" : cedula,
                    "fecha" : fecha,
                    "mensaje": f"La Cita del cliente {nombre} creado exitosamente en 2 segundo para la fecha: {fecha}"
                }
                
    raise HTTPException(
        status_code = 400,
        detail = "Fecha no apta para agendar verifique"
    )

# Listar citas
@app.get("/listar_citas", response_model = Dict[str, Any])
def listar_citas():
    return {
        "citas": citas,
        "total_registrados" : len(citas)
    }



# BUSCAR CITAS POR PACIENTE
@app.get("/cita_paciente/{cedula}")
def cita_paciente(cedula : str) :
    for cita in citas :
        if cita["cedula"] == cedula :
            return cita
    
    # Manejo de cliente no encontrado
    raise HTTPException(
        status_code = 404, # No encontrado
        detail=f"Cita con cedula N. {cedula} no encontrado"
    )


# Cancelar Cita
@app.delete("/cancelar_cita/{cedula}")
def cancelar_cita(cedula : str) :
    for i, cita in enumerate(citas) :
        if cita["cedula"] == cedula :
            cita_cancelada = citas.pop(i)

            return {
                "mensaje": f"La cita del cliente {cita_cancelada['nombre']} se cancelo exitosamente",
                "cita_cancelada": cita_cancelada,
                "citas_restantes": len(citas)
            }
    # si no hay coicidencia
    raise HTTPException(
        status_code=404, # No encontrado
        detail=f"La cita con cedula N. {cedula} no se ha encontrado para cancelar"
    )


# Actualizar o modificar un cliente
@app.put("/modificar_cita/{cedula}")
def modificar_cita(cedula : str, nombre : str, fecha : str) :

    # validar campos
    if not nombre or nombre.strip() == "" or not cedula or cedula.strip() == "" or not fecha or fecha.strip() == "":
        raise HTTPException(
            status_code = 400,
            detail = "Todos los campos son obligatorios"
        )
    
    # citas
    fecha_actual = datetime.now().strftime("%Y-%m-%d-%H:%M")
    ano, mes, dia, hora = fecha_actual.split('-')

    # datos ingresados
    anoCita, mesCita, diaCita, horaCita = fecha.split('-')

    if ano <= anoCita :
        if mes <= mesCita :
            if dia <= diaCita :                
                # se puede crear la cita
                for citaX in citas:
                    if citaX["cedula"] == cedula:
                        nombre_anterior = citaX["nombre"]
                        citaX["nombre"] = nombre.strip()
                        citaX["fecha"] = fecha
                        return {
                            "mensaje": f"Cita actualizado exitosamente",
                            "nombre_anterior": nombre_anterior,
                            "nombre_nuevo": citaX["nombre"],
                            "cita": citaX
                        }
                
                raise HTTPException(
                    status_code=404,
                    detail=f"Cliente con cedula N. {cedula} no encontrado para actualizar"
                )

                
    raise HTTPException(
        status_code = 400,
        detail = "Fecha no apta para agendar verifique"
    )



    