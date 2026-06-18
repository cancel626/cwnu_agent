import asyncio
import json
import requests
import websockets

# 1. 登录 testuser（接收方）
r = requests.post('http://127.0.0.1:8000/api/v1/user/login', json={'username':'testuser','password':'123456'})
token = r.json()['data']['access_token']

async def receive():
    uri = f"ws://127.0.0.1:8000/api/v1/chat/ws/chat?token={token}"
    async with websockets.connect(uri) as ws:
        print("[testuser] WebSocket connected")
        try:
            msg = await asyncio.wait_for(ws.recv(), timeout=15)
            print("[testuser] received:", msg)
        except asyncio.TimeoutError:
            print("[testuser] timeout, no message received")

# 2. 登录 yuyunzhe（发送方），发送文件消息
def send_file_msg():
    r2 = requests.post('http://127.0.0.1:8000/api/v1/user/login', json={'username':'yuyunzhe','password':'123456'})
    token2 = r2.json()['data']['access_token']
    payload = {
        'receiver_id': 1,
        'content': json.dumps({
            'url': '/uploads/chat/20260618/f4aa707bbd7640918ee80a1ec7ebcd13.txt',
            'name': 'test.txt',
            'size': 11,
            'ext': '.txt'
        }),
        'msg_type': 'file'
    }
    q = requests.post(
        'http://127.0.0.1:8000/api/v1/chat/message/send',
        json=payload,
        headers={'Authorization': f'Bearer {token2}', 'Content-Type': 'application/json'}
    )
    print("[yuyunzhe] send result:", q.status_code, q.text)

async def main():
    task = asyncio.create_task(receive())
    await asyncio.sleep(1)
    send_file_msg()
    await task

asyncio.run(main())
