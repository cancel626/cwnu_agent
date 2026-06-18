from app.db.base import SessionLocal
from app.models.user import User

db = SessionLocal()
for u in db.query(User).limit(10).all():
    print(u.id, u.username, u.nickname)
db.close()
