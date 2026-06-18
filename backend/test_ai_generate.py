import asyncio
import httpx
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

token = jwt.encode({"sub": "1", "exp": datetime.utcnow() + timedelta(days=1)}, settings.SECRET_KEY, algorithm="HS256")

async def test():
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            resp = await client.post(
                "http://127.0.0.1:8000/api/v1/skill/ai-generate",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={"skill_type": "functioncall", "description": "计算两个数的和"}
            )
            print("HTTP Status:", resp.status_code)
            data = resp.json()
            print("Response code:", data.get("code"))
            print("Message:", data.get("message"))
            print("Data:", data.get("data"))
        except Exception as e:
            print("Exception:", type(e).__name__, str(e))

asyncio.run(test())
