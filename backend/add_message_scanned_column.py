"""
为 messages 表添加 is_scanned 字段，并将已有 audited_at 的记录设为已扫描。
"""
import pymysql
from app.core.config import settings

# 解析数据库连接信息
# URL 格式: mysql+pymysql://user:password@host:port/dbname
url = settings.SQLALCHEMY_DATABASE_URL
# 去掉 mysql+pymysql:// 前缀
body = url.split('://', 1)[1]
creds, rest = body.split('@', 1)
user, password = creds.split(':', 1)
host_port, db = rest.split('/', 1)
if ':' in host_port:
    host, port = host_port.split(':', 1)
    port = int(port)
else:
    host = host_port
    port = 3306

conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db)
try:
    with conn.cursor() as cur:
        # 添加字段（不存在则添加）
        cur.execute("""
            ALTER TABLE messages
            ADD COLUMN is_scanned TINYINT(1) NOT NULL DEFAULT 0
            COMMENT '是否已被大模型扫描过'
        """)
        print("已添加 messages.is_scanned 字段")
    conn.commit()
except pymysql.err.OperationalError as e:
    if 'Duplicate column name' in str(e):
        print("messages.is_scanned 字段已存在")
    else:
        raise

with conn.cursor() as cur:
    cur.execute("""
        UPDATE messages
        SET is_scanned = 1
        WHERE audited_at IS NOT NULL
    """)
    print(f"已更新 {cur.rowcount} 条已审核记录的 is_scanned 为 True")
conn.commit()
conn.close()
