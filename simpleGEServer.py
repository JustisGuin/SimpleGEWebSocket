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
            print(f"Recieved message: {message}")
            await broadcast(message)

    finally:
        connectedClients.remove(websocket)

startServer = websockets.serve(handler, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(startServer)
asyncio.get_event_loop().run_forever()

