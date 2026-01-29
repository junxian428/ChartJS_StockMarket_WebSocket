import asyncio
import websockets

connected_clients = set()

async def handler(websocket):
    # Register client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")

            # Publish / broadcast to all connected clients
            await asyncio.gather(
                *[client.send(message) for client in connected_clients]
            )
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
