from app.db.base import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

db = SessionLocal()
u = db.query(User).filter(User.username == 'yuyunzhe').first()
if u:
    print(u.id, u.username)
    pwd = CryptContext(schemes=['bcrypt'], deprecated='auto').hash('123456')
    u.password_hash = pwd
    db.commit()
    print('password reset to 123456')
else:
    print('user not found')
db.close()
