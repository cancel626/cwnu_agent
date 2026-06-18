import asyncio
import json
import requests
import websockets

# 登录两个用户
r1 = requests.post('http://127.0.0.1:8000/api/v1/user/login', json={'username':'testuser','password':'123456'})
token1 = r1.json()['data']['access_token']

r2 = requests.post('http://127.0.0.1:8000/api/v1/user/login', json={'username':'yuyunzhe','password':'123456'})
token2 = r2.json()['data']['access_token']

async def receiver():
    uri = f"ws://127.0.0.1:8000/api/v1/chat/ws/chat?token={token1}"
    async with websockets.connect(uri) as ws:
        print("[testuser] connected")
        try:
            msg = await asyncio.wait_for(ws.recv(), timeout=15)
            print("[testuser] received:", msg)
        except asyncio.TimeoutError:
            print("[testuser] timeout")

async def sender():
    uri = f"ws://127.0.0.1:8000/api/v1/chat/ws/chat?token={token2}"
    async with websockets.connect(uri) as ws:
        print("[yuyunzhe] connected")
        await asyncio.sleep(0.5)
        payload = {
            'action': 'send_private',
            'receiver_id': 1,
            'content': json.dumps({
                'url': '/uploads/chat/20260618/f4aa707bbd7640918ee80a1ec7ebcd13.txt',
                'name': 'test.txt',
                'size': 11,
                'ext': '.txt'
            }),
            'msg_type': 'file'
        }
        await ws.send(json.dumps(payload))
        print("[yuyunzhe] sent file msg")
        try:
            msg = await asyncio.wait_for(ws.recv(), timeout=5)
            print("[yuyunzhe] received:", msg)
        except asyncio.TimeoutError:
            print("[yuyunzhe] timeout")

async def main():
    r_task = asyncio.create_task(receiver())
    s_task = asyncio.create_task(sender())
    await asyncio.gather(r_task, s_task)

asyncio.run(main())
