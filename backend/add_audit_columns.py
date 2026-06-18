import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', password='2005626', database='zhishu_warehouse')
cursor = conn.cursor()

# crawled_data 表添加审核字段
cursor.execute("""
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema='zhishu_warehouse' AND table_name='crawled_data' AND column_name='audit_status'
""")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE crawled_data ADD COLUMN audit_status VARCHAR(20) DEFAULT 'pending' COMMENT '审核状态: pending/pass/rejected'")
    print('Added audit_status to crawled_data')
else:
    print('audit_status already exists in crawled_data')

cursor.execute("""
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema='zhishu_warehouse' AND table_name='crawled_data' AND column_name='audit_result'
""")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE crawled_data ADD COLUMN audit_result JSON DEFAULT NULL COMMENT '审核结果JSON'")
    print('Added audit_result to crawled_data')
else:
    print('audit_result already exists in crawled_data')

cursor.execute("""
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema='zhishu_warehouse' AND table_name='crawled_data' AND column_name='audited_at'
""")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE crawled_data ADD COLUMN audited_at DATETIME DEFAULT NULL COMMENT '审核时间'")
    print('Added audited_at to crawled_data')
else:
    print('audited_at already exists in crawled_data')

# messages 表添加审核字段
cursor.execute("""
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema='zhishu_warehouse' AND table_name='messages' AND column_name='audit_status'
""")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE messages ADD COLUMN audit_status VARCHAR(20) DEFAULT 'pending' COMMENT '审核状态: pending/pass/rejected'")
    print('Added audit_status to messages')
else:
    print('audit_status already exists in messages')

cursor.execute("""
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema='zhishu_warehouse' AND table_name='messages' AND column_name='audit_result'
""")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE messages ADD COLUMN audit_result JSON DEFAULT NULL COMMENT '审核结果JSON'")
    print('Added audit_result to messages')
else:
    print('audit_result already exists in messages')

cursor.execute("""
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema='zhishu_warehouse' AND table_name='messages' AND column_name='audited_at'
""")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE messages ADD COLUMN audited_at DATETIME DEFAULT NULL COMMENT '审核时间'")
    print('Added audited_at to messages')
else:
    print('audited_at already exists in messages')

conn.commit()
conn.close()
print('Done')
