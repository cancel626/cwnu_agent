from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class SkillBase(BaseModel):
    name: str = Field(..., max_length=100, description="技能名称")
    type: str = Field(..., max_length=20, description="类型: functioncall/mcp/skill")
    description: Optional[str] = Field(None, description="技能描述")
    config: Optional[dict] = Field(None, description="类型相关参数配置")
    content: Optional[str] = Field(None, description="内容: Python代码 / MCP配置 / skill.md")
    is_active: bool = Field(default=True, description="是否启用")


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    type: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    config: Optional[dict] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None


class SkillInDB(SkillBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SkillResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None


class SkillAIGenerateRequest(BaseModel):
    skill_type: str = Field(..., description="技能类型")
    description: str = Field(..., description="自然语言描述")


class StaffSystemPromptRequest(BaseModel):
    skill_ids: list = Field(default=[], description="技能ID列表")
    extra_desc: Optional[str] = Field(None, description="额外描述")
