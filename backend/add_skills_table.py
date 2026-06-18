import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', password='2005626', database='zhishu_warehouse')
cursor = conn.cursor()

# Create skills table
cursor.execute("""
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    description TEXT,
    config JSON,
    content LONGTEXT,
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='技能管理'
""")

# Add model_config_id to digital_staff if not exists
cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='zhishu_warehouse' AND table_name='digital_staff' AND column_name='model_config_id'")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE digital_staff ADD COLUMN model_config_id INT NULL COMMENT '关联模型配置ID'")

# Add system_prompt to digital_staff if not exists
cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='zhishu_warehouse' AND table_name='digital_staff' AND column_name='system_prompt'")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE digital_staff ADD COLUMN system_prompt LONGTEXT NULL COMMENT '系统提示词'")

conn.commit()
conn.close()
print("Database migration completed.")
