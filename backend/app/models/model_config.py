from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.sql import func
from app.db.base import Base


class ModelConfig(Base):
    __tablename__ = "model_configs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="模型显示名称")
    provider = Column(String(50), default="openai", comment="提供商，如 openai/azure/local")
    api_base = Column(String(255), nullable=False, comment="API 基础地址")
    api_key = Column(String(255), nullable=False, comment="API 密钥")
    model_name = Column(String(100), nullable=False, comment="实际调用的模型名称，如 gpt-4o")
    is_default = Column(Boolean, default=False, comment="是否为默认模型")
    is_active = Column(Boolean, default=True, comment="是否启用")
    temperature = Column(Float, default=0.7, comment="温度参数")
    max_tokens = Column(Integer, default=2048, comment="最大 token 数")
    timeout = Column(Integer, default=30, comment="超时秒数")
    remark = Column(Text, nullable=True, comment="备注说明")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
