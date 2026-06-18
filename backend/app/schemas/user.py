from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户账号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    email: str = Field(..., max_length=100, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128, description="密码")
    verify_code: str = Field(..., min_length=6, max_length=6, description="邮箱验证码")


class AdminUserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128, description="密码")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户账号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    email: Optional[str] = Field(None, max_length=100, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    is_active: Optional[bool] = Field(None, description="是否启用")
    is_online: Optional[bool] = Field(None, description="是否在线")


class UserLogin(BaseModel):
    username: str = Field(..., description="账号")
    password: str = Field(..., description="密码")


class UserInDB(UserBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool
    is_online: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SendCodeRequest(BaseModel):
    email: str = Field(..., max_length=100, description="接收验证码的邮箱")


class UserResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None
