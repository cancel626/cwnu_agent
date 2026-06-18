from app.db.base import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS digital_staff"))
    conn.commit()
    print("digital_staff 表已删除")
