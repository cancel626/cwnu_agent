from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from datetime import datetime, timedelta

from app.db.base import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate, AdminInDB, AdminResponse, AdminLogin, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token
from app.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/admin/login")


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Admin:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的凭证")
    admin_id = payload.get("sub")
    if not admin_id:
        raise HTTPException(status_code=401, detail="无效的凭证")
    admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
    if not admin or not admin.is_active:
        raise HTTPException(status_code=401, detail="用户不存在或已禁用")
    return admin


def get_current_active_superuser(current_admin: Admin = Depends(get_current_admin)) -> Admin:
    if not current_admin.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足，需要超级管理员")
    return current_admin


@router.post("/register", response_model=AdminResponse, summary="管理员注册")
def admin_register(data: AdminCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    existing = db.query(Admin).filter(Admin.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="账号已存在")

    # 检查邮箱/手机是否被占用
    if data.email:
        email_exists = db.query(Admin).filter(Admin.email == data.email).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="邮箱已被使用")

    admin = Admin(
        username=data.username,
        password_hash=get_password_hash(data.password),
        nickname=data.nickname,
        email=data.email,
        phone=data.phone,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    return AdminResponse(
        code=200,
        message="注册成功",
        data={"id": admin.id, "username": admin.username}
    )


@router.post("/login", response_model=TokenResponse, summary="管理员登录")
def admin_login(data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == data.username).first()
    if not admin or not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    if not admin.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    # 更新最后登录时间和在线状态
    admin.last_login = datetime.now()
    admin.is_online = True
    db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(admin.id), "username": admin.username, "is_superuser": admin.is_superuser},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        code=200,
        message="登录成功",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "admin": {
                "id": admin.id,
                "username": admin.username,
                "nickname": admin.nickname,
                "avatar": admin.avatar,
                "is_superuser": admin.is_superuser,
            }
        }
    )


@router.post("/logout", response_model=AdminResponse, summary="管理员退出登录")
def admin_logout(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    current_admin.is_online = False
    db.commit()
    return AdminResponse(code=200, message="退出成功")


@router.get("/me", response_model=AdminResponse, summary="获取当前管理员信息")
def get_me(current_admin: Admin = Depends(get_current_admin)):
    return AdminResponse(
        code=200,
        message="success",
        data=AdminInDB.model_validate(current_admin).model_dump(mode='json')
    )


@router.put("/me", response_model=AdminResponse, summary="修改个人信息")
def update_me(data: AdminUpdate, current_admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(current_admin, field, value)
    db.commit()
    db.refresh(current_admin)
    return AdminResponse(code=200, message="更新成功", data=AdminInDB.model_validate(current_admin).model_dump(mode='json'))


@router.get("/list", response_model=AdminResponse, summary="管理员列表（需超级管理员）")
def list_admins(
    skip: int = 0,
    limit: int = 20,
    keyword: str = "",
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_superuser)
):
    query = db.query(Admin)
    if keyword:
        query = query.filter(
            or_(
                Admin.username.contains(keyword),
                Admin.nickname.contains(keyword),
                Admin.email.contains(keyword)
            )
        )
    total = query.count()
    admins = query.offset(skip).limit(limit).all()
    return AdminResponse(
        code=200,
        message="success",
        data={
            "total": total,
            "items": [AdminInDB.model_validate(a).model_dump(mode='json') for a in admins]
        }
    )


@router.put("/{admin_id}", response_model=AdminResponse, summary="修改管理员（需超级管理员）")
def update_admin(
    admin_id: int,
    data: AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_superuser)
):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="管理员不存在")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(admin, field, value)
    db.commit()
    db.refresh(admin)
    return AdminResponse(code=200, message="更新成功", data=AdminInDB.model_validate(admin).model_dump(mode='json'))


@router.delete("/{admin_id}", response_model=AdminResponse, summary="删除管理员（需超级管理员）")
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_superuser)
):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="管理员不存在")
    if admin.id == current_admin.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    db.delete(admin)
    db.commit()
    return AdminResponse(code=200, message="删除成功")
