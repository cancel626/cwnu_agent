from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta

from app.db.base import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, SendCodeRequest, UserInDB, AdminUserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token
from app.core.email import send_verify_code_email
from app.core.verify_code import generate_code, set_code, verify_code, clear_code
from app.core.config import settings
from app.api.v1.endpoints.admin import get_current_active_superuser
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/user/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的凭证")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的凭证")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="用户不存在或已禁用")
    return user


@router.post("/send-code", response_model=UserResponse, summary="发送邮箱验证码")
def send_code(data: SendCodeRequest, db: Session = Depends(get_db)):
    # 检查邮箱是否已被注册
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="该邮箱已被注册")

    code = generate_code()
    set_code(data.email, code)
    ok = send_verify_code_email(data.email, code)

    if not ok:
        # 开发环境 fallback：直接返回验证码
        return UserResponse(
            code=200,
            message="邮件服务暂不可用，开发模式直接返回验证码",
            data={"code": code, "email": data.email}
        )

    return UserResponse(code=200, message="验证码已发送至您的邮箱，请查收", data={"email": data.email})


@router.post("/register", response_model=UserResponse, summary="用户注册")
def user_register(data: UserCreate, db: Session = Depends(get_db)):
    # 校验验证码
    if not verify_code(data.email, data.verify_code):
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    # 检查用户名
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 检查邮箱
    existing_email = db.query(User).filter(User.email == data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    user = User(
        username=data.username,
        password_hash=get_password_hash(data.password),
        nickname=data.nickname,
        email=data.email,
        phone=data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 注册成功后清除验证码
    clear_code(data.email)

    return UserResponse(
        code=200,
        message="注册成功",
        data={"id": user.id, "username": user.username}
    )


@router.post("/login", response_model=UserResponse, summary="用户登录")
def user_login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    # 更新在线状态
    user.is_online = True
    db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "type": "user"},
        expires_delta=access_token_expires
    )

    return UserResponse(
        code=200,
        message="登录成功",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "email": user.email,
            }
        }
    )


@router.post("/logout", response_model=UserResponse, summary="用户退出登录")
def user_logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.is_online = False
    db.commit()
    return UserResponse(code=200, message="退出成功")


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        code=200,
        message="success",
        data=UserInDB.model_validate(current_user).model_dump(mode='json')
    )


@router.get("/list", response_model=UserResponse, summary="普通用户列表（需超级管理员）")
def list_users(
    skip: int = 0,
    limit: int = 20,
    keyword: str = "",
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    query = db.query(User)
    if keyword:
        query = query.filter(
            or_(
                User.username.contains(keyword),
                User.nickname.contains(keyword),
                User.email.contains(keyword)
            )
        )
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    return UserResponse(
        code=200,
        message="success",
        data={
            "total": total,
            "items": [UserInDB.model_validate(u).model_dump(mode='json') for u in users]
        }
    )


@router.post("/create", response_model=UserResponse, summary="管理员创建普通用户（需超级管理员）")
def create_user(
    data: AdminUserCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    existing_email = db.query(User).filter(User.email == data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    user = User(
        username=data.username,
        password_hash=get_password_hash(data.password),
        nickname=data.nickname,
        email=data.email,
        phone=data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(
        code=200,
        message="创建成功",
        data=UserInDB.model_validate(user).model_dump(mode='json')
    )


@router.put("/{user_id}", response_model=UserResponse, summary="修改普通用户（需超级管理员）")
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    update_data = data.model_dump(exclude_unset=True)

    # 如果修改用户名，检查是否冲突
    if "username" in update_data and update_data["username"] != user.username:
        existing = db.query(User).filter(User.username == update_data["username"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="用户名已存在")

    # 如果修改邮箱，检查是否冲突
    if "email" in update_data and update_data["email"] != user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="邮箱已被注册")

    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserResponse(code=200, message="更新成功", data=UserInDB.model_validate(user).model_dump(mode='json'))


@router.delete("/{user_id}", response_model=UserResponse, summary="删除普通用户（需超级管理员）")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    return UserResponse(code=200, message="删除成功")
