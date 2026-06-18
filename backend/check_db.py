from app.db.base import SessionLocal
from app.models.admin import Admin

db = SessionLocal()
admins = db.query(Admin).all()
for a in admins:
    h = a.password_hash or ""
    print("id=%s username=%r active=%s hash_len=%s" % (a.id, a.username, a.is_active, len(h)))
db.close()
