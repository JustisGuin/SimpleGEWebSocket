import asyncio
import websockets

connectedClients = set()

async def broadcast(message):
    for websocket in connectedClients:
        await websocket.send(message)

async def handler(websocket, path):
    connectedClients.add(websocket)
    try: 
        async for message in websocket:
            print(f"Received message: {message}")
            await broadcast(message)
    finally:
        connectedClients.remove(websocket)

async def main():
    startServer = websockets.serve(handler, "localhost", 5000)
    await startServer
    await asyncio.Future()  # Run forever

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())