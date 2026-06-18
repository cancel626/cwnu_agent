from app.db.base import SessionLocal
from app.models.admin import Admin
from app.core.security import get_password_hash

db = SessionLocal()

# 测试数据
admins = [
    {
        "username": "admin",
        "password": "123456",
        "nickname": "超级管理员",
        "email": "admin@cwnu.edu.cn",
        "is_superuser": True,
        "is_active": True,
    },
    {
        "username": "zhangsan",
        "password": "123456",
        "nickname": "张三",
        "email": "zhangsan@cwnu.edu.cn",
        "is_superuser": False,
        "is_active": True,
    },
    {
        "username": "lisi",
        "password": "123456",
        "nickname": "李四",
        "email": "lisi@cwnu.edu.cn",
        "is_superuser": False,
        "is_active": True,
    },
    {
        "username": "wangwu",
        "password": "123456",
        "nickname": "王五",
        "email": "wangwu@cwnu.edu.cn",
        "is_superuser": False,
        "is_active": False,
    },
]

for item in admins:
    existing = db.query(Admin).filter(Admin.username == item["username"]).first()
    if existing:
        print(f"账号 {item['username']} 已存在，跳过")
        continue
    admin = Admin(
        username=item["username"],
        password_hash=get_password_hash(item["password"]),
        nickname=item["nickname"],
        email=item["email"],
        is_superuser=item["is_superuser"],
        is_active=item["is_active"],
    )
    db.add(admin)
    print(f"插入账号: {item['username']} ({item['nickname']})")

db.commit()
db.close()
print("测试数据插入完成")
