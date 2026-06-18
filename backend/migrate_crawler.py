"""为 crawled_data 表添加新列"""
import sys
sys.path.insert(0, "d:/Trae/Code/shixun/backend")

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

with engine.connect() as conn:
    # 检查表是否存在
    result = conn.execute(text("SHOW TABLES LIKE 'crawled_data'"))
    if result.fetchone():
        # 添加新列
        columns_to_add = [
            ("markdown_content", "LONGTEXT", "Markdown原始内容"),
            ("summary", "LONGTEXT", "内容摘要"),
            ("keywords", "JSON", "关键词列表"),
            ("entities", "JSON", "实体信息"),
        ]
        for col_name, col_type, comment in columns_to_add:
            # 检查列是否已存在
            r = conn.execute(text(f"SHOW COLUMNS FROM crawled_data LIKE '{col_name}'"))
            if not r.fetchone():
                conn.execute(text(f"ALTER TABLE crawled_data ADD COLUMN {col_name} {col_type} NULL COMMENT '{comment}'"))
                print(f"Added column: {col_name}")
            else:
                print(f"Column already exists: {col_name}")
        conn.commit()
        print("Migration completed.")
    else:
        print("Table crawled_data does not exist yet, it will be created by SQLAlchemy.")
