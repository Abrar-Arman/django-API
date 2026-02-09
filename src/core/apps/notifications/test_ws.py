import asyncio
import websockets
import json

async def listen():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcwNjQ1NzE1LCJpYXQiOjE3NzA2NDU0MTUsImp0aSI6ImU2YmM1NDg5NTlkMjQ1ZDlhNGZiYjdiNDk4MDE0N2NjIiwidXNlcl9pZCI6IjEifQ.1GgK-s_wujvcYEeSW8w6mtAOwYl33fo9Vp4VKw9FDd4"  
    url = f"ws://127.0.0.1:8000/ws/notifications/?token={token}"

    async with websockets.connect(url) as ws:
        print("Connected to WebSocket. Waiting for notifications...")
        while True:
            message = await ws.recv()
            data = json.loads(message)
            print("Notification received:", data)

asyncio.run(listen())
