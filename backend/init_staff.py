from app.db.base import SessionLocal, engine, Base
from app.models.staff import DigitalStaff

# 确保表已创建
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 检查是否已有数据
existing = db.query(DigitalStaff).first()
if existing:
    print("员工数据已存在，跳过初始化")
    db.close()
    exit(0)

staff_list = [
    DigitalStaff(
        name="灵感数据天才",
        model_type="GPT-4o",
        role="逻辑优化专家",
        desc="负责学生成绩指标和预测模型的首席研究员。",
        tag="核心智脑",
        status="处理中",
        skills="统计分析,PYTHON执行,可视化生成",
        current_task="正在分析计算机学院第三季度的招生趋势...",
        avatar="https://lh3.googleusercontent.com/aida-public/AB6AXuCcIOPfOJcqrNEcWd0E6gddMlbPLxk_rq82zKZo7_NFEvG9q051GA7SfdxEQSq0cziRpvjPLvwCZMfKqm4JGaaUAgtYL4XpQu_65TZ4fm73XuvX-dPvG4RodmhboXP4SS735Qu42PdrDZQHhx_EmGgxVIoXrjoY83GHNnbOBUurCtjWfzEFYg_PmdN3VZz-coKqaOEn95fwBzOZPFaehXSyiLVLxPKsSqlrlgmmDktpA_b_3o61g2V11cRT0DaSVVSUjQ_joqTzjpzM",
        is_active=True
    ),
    DigitalStaff(
        name="档案馆连接者 01",
        model_type="Llama-3-70B",
        role="数据合成核心",
        desc="管理大学数字资产库和历史文献资料。",
        tag="知识中心",
        status="待命中",
        skills="语义检索,实体抽取,安全归档",
        current_task="正在为教务处整理1990-2020年的历史学籍档案...",
        avatar="https://lh3.googleusercontent.com/aida-public/AB6AXuCGsqKt6LGy-apNYCuNsBniJrweev6_5xSHxT1jqHboD8E0VYrPiDuk4DYIukyGLAh6MGBubSYMKSgA1gP7cRbQfyaQYPu-7OMiRfcUIoquGuTyflont4Wz02WR_G2HnhgyF8eSXhMoSJdv6t9mHVkomnjuU8tF6n6XNxulNXjUlsDRfxt-PI22vV-q86NwVUwJkBs3OK6f1bfv7Lk_bkBUPSr2jgwW0ugr1QwqH_17LyMxuXAr29tMFy2ptvDJuWF-tTI1R3dtH8-v",
        is_active=True
    ),
    DigitalStaff(
        name="系统哨兵",
        model_type="Claude-3.5",
        role="安全哨兵",
        desc="主机结构完整性维护与校园网络节点编排优化。",
        tag="底层架构",
        status="活跃",
        skills="网络监控,漏洞扫描,自动修复",
        current_task="正在扫描防火墙7区的异常访问模式...",
        avatar="https://lh3.googleusercontent.com/aida-public/AB6AXuD9OykPPIuIcO-FvWl-8z6tN_FgJnvyAKZyV6sJHJCsN-Z6NHb6BafH0c25EDjHKVb2DmCXI_jQj2bOVS1AkIV5bep_BysTeP1tqHBYDPnTYchudB3otWbgwAInUPwJ_C9W5FKxkegADldnmRKPf1i4G9Nz9kEALo6-DQT8YaFk5T9QZfrg7afmBamJx9_6UyrRdfI6RF_uSDqS_WtPY2ORsfxfgdyW52V12buZkE-8GlGe1kL84BQpOpRX9Y3NYZiGKdt97xL9l_4G",
        is_active=True
    ),
    DigitalStaff(
        name="学术助手",
        model_type="GPT-4",
        role="逻辑优化专家",
        desc="用于课程映射和研究引用数据的神经接口，支持跨库检索。",
        tag="核心智脑",
        status="活跃",
        skills="跨库检索,引用分析,课程映射",
        current_task="正在整理教育学部最新的论文引用数据...",
        is_active=True
    ),
    DigitalStaff(
        name="人事分析师",
        model_type="GPT-4o",
        role="数据合成核心",
        desc="优化人力资本分配，处理人才流向诊断与效能评估。",
        tag="管理枢纽",
        status="活跃",
        skills="效能评估,人才分析,流向诊断",
        current_task="正在生成第三季度人事效能评估报告...",
        is_active=True
    ),
    DigitalStaff(
        name="数字馆员",
        model_type="Llama-3-70B",
        role="知识中心",
        desc="档案数据检索与跨维度知识索引，支持多模态数据查询。",
        tag="知识中心",
        status="活跃",
        skills="多模态查询,知识索引,数据检索",
        current_task="正在建立跨学科知识图谱索引...",
        is_active=True
    ),
]

for staff in staff_list:
    db.add(staff)

db.commit()
print(f"成功初始化 {len(staff_list)} 个数字员工")
db.close()
