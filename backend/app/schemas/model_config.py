from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ModelConfigBase(BaseModel):
    name: str = Field(..., max_length=100, description="模型显示名称")
    provider: str = Field(default="openai", max_length=50, description="提供商")
    api_base: str = Field(..., max_length=255, description="API 基础地址")
    model_name: str = Field(..., max_length=100, description="模型名称")
    is_default: bool = Field(default=False, description="是否为默认模型")
    is_active: bool = Field(default=True, description="是否启用")
    temperature: float = Field(default=0.7, description="温度参数")
    max_tokens: int = Field(default=2048, description="最大 token 数")
    timeout: int = Field(default=30, description="超时秒数")
    remark: Optional[str] = Field(None, description="备注")


class ModelConfigCreate(ModelConfigBase):
    api_key: str = Field(..., min_length=1, max_length=255, description="API 密钥")


class ModelConfigUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    provider: Optional[str] = Field(None, max_length=50)
    api_base: Optional[str] = Field(None, max_length=255)
    api_key: Optional[str] = Field(None, max_length=255)
    model_name: Optional[str] = Field(None, max_length=100)
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    remark: Optional[str] = None


class ModelConfigInDB(ModelConfigBase):
    id: int
    api_key_masked: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ModelConfigResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[dict] = None


class ModelTestRequest(BaseModel):
    message: str = Field(default="Hello, are you working?", description="测试消息")
