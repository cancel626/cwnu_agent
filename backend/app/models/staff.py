from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class DigitalStaff(Base):
    __tablename__ = "digital_staff"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="员工名称")
    model_type = Column(String(50), nullable=True, comment="模型类型")
    model_config_id = Column(Integer, ForeignKey("model_configs.id"), nullable=True, comment="关联模型配置ID")
    role = Column(String(100), nullable=True, comment="角色/职责")
    desc = Column(Text, nullable=True, comment="描述")
    tag = Column(String(50), nullable=True, comment="标签")
    status = Column(String(20), default="待命中", comment="状态")
    skills = Column(String(255), nullable=True, comment="核心技能，逗号分隔")
    system_prompt = Column(Text, nullable=True, comment="系统提示词")
    current_task = Column(Text, nullable=True, comment="当前任务")
    avatar = Column(Text, nullable=True, comment="头像URL")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
