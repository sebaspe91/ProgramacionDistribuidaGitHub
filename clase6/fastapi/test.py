import asyncio
import httpx

async def main():
    # crear cliente con timeout más largo
    timeout = httpx.Timeout(30.0)  # 30 segundos de timeout más largo
    async with httpx.AsyncClient(timeout=timeout) as client:
        await asyncio.gather(*[client.get("http://0.0.0.0:8000/incrementar") for _ in range(100)])

asyncio.run(main())