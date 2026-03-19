import asyncio
import httpx

# semaforo global que permite maximo 10 peticiones concurrentes
semaphore = asyncio.Semaphore(10)

async def peticion(client):
    async with semaphore: # Solo se agrega esta linea
        try:
            await client.get("http://0.0.0.0:8000/incrementar")
        except Exception as e:
            print("Error: ", e)

async def main():
    # crear cliente con timeout más largo
    # timeout = httpx.Timeout(30.0)  # 30 segundos de timeout más largo
    async with httpx.AsyncClient(timeout=10.0) as client:
        await asyncio.gather(*[ 
            peticion(client) for _ in range(100)
        ])

asyncio.run(main())