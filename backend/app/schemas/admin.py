from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AdminBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="管理员账号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    email: Optional[str] = Field(None, max_length=100, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class AdminCreate(AdminBase):
    password: str = Field(..., min_length=6, max_length=128, description="密码")


class AdminUpdate(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    is_online: Optional[bool] = None


class AdminInDB(AdminBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool
    is_online: bool
    is_superuser: bool
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AdminResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[dict] = None


class AdminLogin(BaseModel):
    username: str = Field(..., description="账号")
    password: str = Field(..., description="密码")


class TokenResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: dict
