
import asyncio # Importa la libreria para programacion asincrona
# import time

# contador del cliente
contador_clientes = 0  # recurso compartido

# Funcion que maneja cada cliente (coroutine)
async def handle_client(reader, writer):

    global contador_clientes



    # print(f"Cliente {contador_clientes} atencion desde {reader}")

    await asyncio.sleep(10) # probar el tiempo delay
    
    # Espera datos del cliente (maximo 1024 bytes)
    data = await reader.read(1024)
    
    # Convierte los bytes recibidos en texto
    name = data.decode()

    # Incrlemento contador
    contador_clientes += 1
    
    # Construye el mensaje de respuesta
    response = f"Hola {name} eres el cliente numero: {contador_clientes}"

    # envia la respuesta al cliente (en bytes)
    writer.write(response.encode())

    # Espera a que los datos se envien completamente
    await writer.drain()
    
    # cierra la conexion con el cliente
    writer.close()
    


# Funcion principal del servidor
async def main():
    # Crea el servidor en la IP 127.0.0.1 y puerto 5000
    # hendle_client sera ejecutado por cada nuevo conexion
    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 5000
    )

    # Mantiene el servidor activo
    async with server:
        # El servidor queda escuchando indefinidamente
        await server.serve_forever()

# ejecuta el event loop principal
asyncio.run(main())
