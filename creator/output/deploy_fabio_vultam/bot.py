import asyncio
from gateway_bot import gateway_runner

if __name__ == "__main__":
    try:
        asyncio.run(gateway_runner())
    except KeyboardInterrupt:
        print("\nGateway detenido por el usuario.")
