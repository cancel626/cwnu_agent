import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', password='2005626', database='zhishu_warehouse')
cursor = conn.cursor()

# Check if column exists in admins
cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='zhishu_warehouse' AND table_name='admins' AND column_name='is_online'")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE admins ADD COLUMN is_online TINYINT(1) DEFAULT 0 COMMENT '是否在线'")
    print('Added is_online to admins')
else:
    print('is_online already exists in admins')

# Check if column exists in users
cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='zhishu_warehouse' AND table_name='users' AND column_name='is_online'")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE users ADD COLUMN is_online TINYINT(1) DEFAULT 0 COMMENT '是否在线'")
    print('Added is_online to users')
else:
    print('is_online already exists in users')

conn.commit()
conn.close()
print('Done')
