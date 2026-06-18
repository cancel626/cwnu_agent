import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

host = os.getenv("DB_HOST", "localhost")
port = int(os.getenv("DB_PORT", "3306"))
user = os.getenv("DB_USER", "root")
password = os.getenv("DB_PASSWORD", "")
database = os.getenv("DB_NAME", "zhishu_db")

print(f"尝试连接 MySQL: {host}:{port}/{database} (用户: {user})")

try:
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        connect_timeout=5
    )
    print("连接成功！")
    with conn.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"MySQL 版本: {version[0]}")
    conn.close()
except Exception as e:
    print(f"连接失败: {e}")
