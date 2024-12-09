import asyncio
import websockets

# Dictionary to hold client data
client_data = {}

# Set to hold connected clients
connected_clients = set()

async def broadcast():
    # Send all client data to all clients
    if client_data:
        message = "\n".join(f"{key}|{value}" for key, value in client_data.items())
        # Create tasks for sending messages to all clients
        tasks = [asyncio.create_task(client.send(message)) for client in connected_clients]
        await asyncio.gather(*tasks)  # Wait for all tasks to complete

async def handler(websocket):
    # Add the new client to the connected clients set
    connected_clients.add(websocket)
    print("New connection")

    try:
        async for message in websocket:
            print(f"Received: {message}")
            try:
                key, value = message.split("|", 1)  # Split the message into key and value
                client_data[key] = value  # Store the payload in client_data
                await broadcast()  # Broadcast updated data to all clients
                print("Current data:")
                print("\n".join(f"{k}|{v}" for k, v in client_data.items()))
                print("\n")
            except ValueError:
                print(f"Invalid message format: {message}. Expected format: 'key|value'")
                # Optionally, you can send an error message back to the client
                await websocket.send("Error: Invalid message format. Use 'key|value'.")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    finally:
        connected_clients.remove(websocket)  # Remove the client from the set
        # Safely remove the client's data if it exists
        if 'key' in locals() and key in client_data:
            del client_data[key]  # Remove the client's data
        await broadcast()  # Broadcast updated data to remaining clients

async def main():
    async with websockets.serve(handler, "localhost", 8001):
        print("WebSocket server started on ws://localhost:8001")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())