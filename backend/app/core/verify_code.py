import random
import time
from threading import Lock

# 内存验证码缓存 {email: {"code": "123456", "expire": 1234567890}}
_code_cache = {}
_lock = Lock()
CODE_EXPIRE_SECONDS = 300  # 5分钟
CODE_LENGTH = 6


def generate_code() -> str:
    return "".join(random.choices("0123456789", k=CODE_LENGTH))


def set_code(email: str, code: str):
    with _lock:
        _code_cache[email] = {
            "code": code,
            "expire": time.time() + CODE_EXPIRE_SECONDS
        }


def get_code(email: str) -> str:
    with _lock:
        item = _code_cache.get(email)
        if not item:
            return ""
        if time.time() > item["expire"]:
            del _code_cache[email]
            return ""
        return item["code"]


def verify_code(email: str, code: str) -> bool:
    if not code:
        return False
    stored = get_code(email)
    if not stored:
        return False
    return stored.lower() == code.lower()


def clear_code(email: str):
    with _lock:
        _code_cache.pop(email, None)
