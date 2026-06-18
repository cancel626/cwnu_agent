from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class StaffBase(BaseModel):
    name: str = Field(..., max_length=100, description="员工名称")
    model_type: Optional[str] = Field(None, max_length=50, description="模型类型")
    model_config_id: Optional[int] = Field(None, description="关联模型配置ID")
    role: Optional[str] = Field(None, max_length=100, description="角色/职责")
    desc: Optional[str] = Field(None, description="描述")
    tag: Optional[str] = Field(None, max_length=50, description="标签")
    status: Optional[str] = Field("待命中", max_length=20, description="状态")
    skills: Optional[str] = Field(None, max_length=255, description="核心技能")
    system_prompt: Optional[str] = Field(None, description="系统提示词")
    current_task: Optional[str] = Field(None, description="当前任务")
    avatar: Optional[str] = Field(None, description="头像URL")
    is_active: Optional[bool] = True


class StaffCreate(StaffBase):
    pass


class StaffUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    model_type: Optional[str] = Field(None, max_length=50)
    model_config_id: Optional[int] = Field(None)
    role: Optional[str] = Field(None, max_length=100)
    desc: Optional[str] = None
    tag: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)
    skills: Optional[str] = Field(None, max_length=255)
    system_prompt: Optional[str] = None
    current_task: Optional[str] = None
    avatar: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class StaffInDB(StaffBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StaffListResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[dict] = None
