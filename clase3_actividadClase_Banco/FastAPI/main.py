# ----- IMPORTACIONES -------- #

# FestAPI => crear la api  ------ HTTPException => Enviar errores HTTP controlados
from fastapi import FastAPI, HTTPException

# tipado para mostrar mensajes --- List => listas tipadas --- Dict => diccionarios --- Any => 
from typing import List, Dict, Any 

# Para el delay asíncrono
import asyncio  

# ------ CREACION DE LA APLICACION --------- #
app = FastAPI()

# BASE DE DATOS SIMULADA  
clientes = []  # Variable global tipo lista almacenar clientes en memoria

# 4. Contador global de clientes creados
contador_clientes = 0  # Lleva la cuenta total de clientes creados

# ENDPOINT RAIZ
@app.get("/")
def home():
    return {"Mensaje": "API del Banco funcionando"}


# CREAR CLIENTE (CON DELAY ASÍNCRONO Y VALIDACIÓN)
@app.post("/clientes") # le dice a FastAPI q esta funcion responde a peticiones HTTP de tipo POST
async def crear_cliente(nombre: str):  # Cambiamos a async para poder usar await

    # global: Indica que vamos a modificar una variable definida FUERA de la función
    global contador_clientes
    
    # 3. Validación básica (no permitir nombre vacío)
    if not nombre or nombre.strip() == "":
        raise HTTPException( # raise HTTPException => lanza un error controlado
            status_code=400, # error del cliente
            detail="El nombre no puede estar vacío" # mensaje descriptivo del erro
        )
    
    # 5. Simulación de delay asíncrono de 3 segundos
    await asyncio.sleep(3)
    
    # Incrementar contador global
    contador_clientes += 1
    
    # Crear el cliente en el objeto
    cliente = {
        "id": len(clientes) + 1,
        "nombre": nombre.strip()  # Eliminamos espacios extras
    }

    # Guardar en base datos simulada
    clientes.append(cliente)
    
    # Retornamos cliente creado + información del contador tipo JSON
    return {
        "cliente": cliente,
        "total_clientes_creados": contador_clientes,
        "mensaje": f"Cliente {nombre} creado exitosamente después de 3 segundos"
    }

# LISTAR CLIENTES

# Dict => Esta función va a devolver un DICCIONARIO
# Las llaves serán de tipo str (texto)   ===== Los valores pueden ser de cualquier tipo (Any)
@app.get("/clientes", response_model=Dict[str, Any])
def listar_clientes(): # Función síncrona (no necesita async porque no espera nada)
    return {
        "clientes": clientes,
        "total_registrados": len(clientes),
        "total_creados_historicamente": contador_clientes
    }

# OBTENER CLIENTE POR ID
@app.get("/clientes/{cliente_id}")
def obtener_cliente(cliente_id: int):
    for cliente in clientes:
        if cliente["id"] == cliente_id: # en el objeto cliente solo id
            return cliente
    
    # Manejo de cliente no encontrado
    raise HTTPException(
        status_code=404, # No encontrado
        detail=f"Cliente con ID {cliente_id} no encontrado"
    )

# 1. Endpoint DELETE para eliminar cliente
@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    # enumerate(): Función que permite iterar obteniendo tanto el índice (i) como el valor (cliente)
    for i, cliente in enumerate(clientes):
        if cliente["id"] == cliente_id:
            cliente_eliminado = clientes.pop(i) # Elimina el cliente
            return {
                "mensaje": f"Cliente {cliente_eliminado['nombre']} eliminado exitosamente",
                "cliente_eliminado": cliente_eliminado,
                "clientes_restantes": len(clientes)
            }
    
    # si no hay coicidencia
    raise HTTPException(
        status_code=404, # No encontrado
        detail=f"Cliente con ID {cliente_id} no encontrado para eliminar"
    )

# 2. Endpoint PUT para actualizar nombre
@app.put("/clientes/{cliente_id}")
def actualizar_cliente(cliente_id: int, nombre: str):
    # Validación básica (no permitir nombre vacío)
    if not nombre or nombre.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="El nombre no puede estar vacío"
        )
    
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            nombre_anterior = cliente["nombre"]
            cliente["nombre"] = nombre.strip()
            return {
                "mensaje": f"Cliente actualizado exitosamente",
                "nombre_anterior": nombre_anterior,
                "nombre_nuevo": cliente["nombre"],
                "cliente": cliente
            }
    
    raise HTTPException(
        status_code=404,
        detail=f"Cliente con ID {cliente_id} no encontrado para actualizar"
    )

# Endpoint adicional para ver el contador global
@app.get("/estadisticas")
def obtener_estadisticas():
    return {
        "clientes_actuales": len(clientes),
        "total_clientes_creados_historicamente": contador_clientes,
        "capacidad_maxima_teorica": "ilimitada"
    }

# Endpoint para resetear (útil para pruebas)
@app.post("/reset")
def resetear_sistema():
    global clientes, contador_clientes
    clientes = []
    contador_clientes = 0
    return {"mensaje": "Sistema reseteado exitosamente"}