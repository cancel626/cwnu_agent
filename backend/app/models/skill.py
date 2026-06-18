from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="技能名称")
    type = Column(String(20), nullable=False, comment="类型: functioncall/mcp/skill")
    description = Column(Text, nullable=True, comment="技能描述")
    config = Column(JSON, nullable=True, comment="类型相关参数配置(JSON)")
    content = Column(Text, nullable=True, comment="内容: Python代码 / MCP配置 / skill.md")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
