import asyncio
import httpx
from app.db.base import SessionLocal
from app.models.model_config import ModelConfig

async def test():
    db = SessionLocal()
    m = db.query(ModelConfig).filter(ModelConfig.is_default == True).first()
    db.close()
    if not m:
        print("ERROR: 没有默认模型")
        return
    print("Model:", m.name)
    print("API Base:", m.api_base)
    print("Model Name:", m.model_name)
    print("Key prefix:", m.api_key[:10] + "..." if m.api_key else "EMPTY")
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            url = m.api_base.rstrip("/") + "/chat/completions"
            print("URL:", url)
            resp = await client.post(
                url,
                headers={"Authorization": f"Bearer {m.api_key}", "Content-Type": "application/json"},
                json={"model": m.model_name, "messages": [{"role":"user","content":"hi"}], "stream": False, "temperature": 0.3}
            )
            print("HTTP Status:", resp.status_code)
            print("Body:", resp.text[:500])
    except Exception as e:
        print("Exception:", type(e).__name__, str(e))

asyncio.run(test())
