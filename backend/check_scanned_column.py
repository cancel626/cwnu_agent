from app.db.base import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT COUNT(*) FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'messages'
          AND COLUMN_NAME = 'is_scanned'
    """))
    print('is_scanned exists:', result.scalar())
