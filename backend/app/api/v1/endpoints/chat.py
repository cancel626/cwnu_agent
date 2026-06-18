import json
import asyncio
import re
import os
import uuid
import httpx
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc

from app.db.base import get_db
from app.models.user import User
from app.models.staff import DigitalStaff
from app.models.model_config import ModelConfig
from app.models.chat import Friendship, ChatGroup, GroupMember, Message
from app.schemas.user import UserResponse
from app.api.v1.endpoints.user import get_current_user
router = APIRouter()

# 聊天文件上传目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
CHAT_UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "chat")
os.makedirs(CHAT_UPLOAD_DIR, exist_ok=True)

# WebSocket 连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id: int, message: dict):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_json(message)

    async def broadcast_to_group(self, user_ids: List[int], message: dict):
        for uid in user_ids:
            ws = self.active_connections.get(uid)
            if ws:
                await ws.send_json(message)


manager = ConnectionManager()


# ==================== 好友管理 ====================

@router.post("/friend/request", response_model=UserResponse, summary="添加好友")
def add_friend(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    username = data.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="请输入用户名")

    friend = db.query(User).filter(User.username == username).first()
    if not friend:
        raise HTTPException(status_code=404, detail="用户不存在")
    if friend.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能添加自己为好友")

    existing = db.query(Friendship).filter(
        or_(
            and_(Friendship.user_id == current_user.id, Friendship.friend_id == friend.id),
            and_(Friendship.user_id == friend.id, Friendship.friend_id == current_user.id)
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="已经是好友或已发送请求")

    friendship = Friendship(user_id=current_user.id, friend_id=friend.id, status="accepted")
    db.add(friendship)
    db.commit()

    return UserResponse(code=200, message="添加成功", data={"friend_id": friend.id, "friend_name": friend.nickname or friend.username})


@router.get("/friend/list", response_model=UserResponse, summary="好友列表")
def friend_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendships = db.query(Friendship).filter(
        or_(Friendship.user_id == current_user.id, Friendship.friend_id == current_user.id)
    ).all()

    result = []
    for f in friendships:
        fid = f.friend_id if f.user_id == current_user.id else f.user_id
        friend = db.query(User).filter(User.id == fid).first()
        if friend:
            result.append({
                "id": f.id,
                "friend_id": friend.id,
                "friend_name": friend.nickname or friend.username,
                "friend_avatar": friend.avatar,
                "status": f.status,
                "created_at": f.created_at.isoformat() if f.created_at else None
            })

    return UserResponse(code=200, message="success", data=result)


@router.delete("/friend/{friend_id}", response_model=UserResponse, summary="删除好友")
def delete_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendship = db.query(Friendship).filter(
        or_(
            and_(Friendship.user_id == current_user.id, Friendship.friend_id == friend_id),
            and_(Friendship.user_id == friend_id, Friendship.friend_id == current_user.id)
        )
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="好友关系不存在")

    db.delete(friendship)
    db.commit()
    return UserResponse(code=200, message="删除成功", data=None)


# ==================== 群聊管理 ====================

@router.post("/group", response_model=UserResponse, summary="创建群聊")
def create_group(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    name = data.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="请输入群名称")

    group = ChatGroup(
        name=name,
        desc=data.get("desc"),
        owner_id=current_user.id
    )
    db.add(group)
    db.commit()
    db.refresh(group)

    # 群主加入群
    member = GroupMember(group_id=group.id, member_type="user", member_id=current_user.id)
    db.add(member)
    db.commit()

    return UserResponse(code=200, message="创建成功", data={"group_id": group.id, "name": group.name})


@router.get("/group/list", response_model=UserResponse, summary="群聊列表")
def group_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    members = db.query(GroupMember).filter(
        GroupMember.member_type == "user",
        GroupMember.member_id == current_user.id
    ).all()

    result = []
    for m in members:
        group = db.query(ChatGroup).filter(ChatGroup.id == m.group_id, ChatGroup.is_active == True).first()
        if group:
            owner = db.query(User).filter(User.id == group.owner_id).first()
            result.append({
                "id": group.id,
                "name": group.name,
                "desc": group.desc,
                "avatar": group.avatar,
                "owner_name": owner.nickname or owner.username if owner else "",
                "created_at": group.created_at.isoformat() if group.created_at else None
            })

    return UserResponse(code=200, message="success", data=result)


@router.get("/group/{group_id}/members", response_model=UserResponse, summary="群成员列表")
def group_members(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 检查当前用户是否在群中
    is_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.member_type == "user",
        GroupMember.member_id == current_user.id
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="你不是该群成员")

    members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    result = []
    for m in members:
        if m.member_type == "user":
            user = db.query(User).filter(User.id == m.member_id).first()
            if user:
                result.append({
                    "id": m.id,
                    "type": "user",
                    "user_id": user.id,
                    "name": user.nickname or user.username,
                    "avatar": user.avatar,
                    "joined_at": m.joined_at.isoformat() if m.joined_at else None
                })
        elif m.member_type == "staff":
            staff = db.query(DigitalStaff).filter(DigitalStaff.id == m.member_id).first()
            if staff:
                result.append({
                    "id": m.id,
                    "type": "staff",
                    "staff_id": staff.id,
                    "name": staff.name,
                    "avatar": staff.avatar,
                    "tag": staff.tag,
                    "joined_at": m.joined_at.isoformat() if m.joined_at else None
                })

    return UserResponse(code=200, message="success", data=result)


@router.post("/group/{group_id}/invite", response_model=UserResponse, summary="邀请成员")
def invite_member(
    group_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    member_type = data.get("member_type")
    member_id = data.get("member_id")

    if not member_type or not member_id:
        raise HTTPException(status_code=400, detail="参数错误")

    group = db.query(ChatGroup).filter(ChatGroup.id == group_id, ChatGroup.is_active == True).first()
    if not group:
        raise HTTPException(status_code=404, detail="群聊不存在")

    # 检查邀请者是否在群中
    is_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.member_type == "user",
        GroupMember.member_id == current_user.id
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="你不是该群成员")

    # 检查是否已在群中
    existing = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.member_type == member_type,
        GroupMember.member_id == member_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="该成员已在群中")

    gm = GroupMember(group_id=group_id, member_type=member_type, member_id=member_id)
    db.add(gm)
    db.commit()

    return UserResponse(code=200, message="邀请成功", data=None)


# ==================== 消息管理 ====================

@router.get("/message/private/{friend_id}", response_model=UserResponse, summary="私聊历史")
def private_history(
    friend_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * page_size
    messages = db.query(Message).filter(
        Message.group_id.is_(None),
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == friend_id),
            and_(Message.sender_id == friend_id, Message.receiver_id == current_user.id)
        )
    ).order_by(desc(Message.created_at)).offset(offset).limit(page_size).all()

    # 标记为已读
    unread = db.query(Message).filter(
        Message.group_id.is_(None),
        Message.sender_id == friend_id,
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).all()
    for m in unread:
        m.is_read = True
    db.commit()

    result = []
    for m in reversed(messages):
        sender = db.query(User).filter(User.id == m.sender_id).first()
        result.append({
            "id": m.id,
            "sender_id": m.sender_id,
            "sender_name": sender.nickname or sender.username if sender else "未知",
            "sender_avatar": sender.avatar if sender else "",
            "content": m.content,
            "msg_type": m.msg_type,
            "is_read": m.is_read,
            "created_at": m.created_at.isoformat() if m.created_at else None
        })

    return UserResponse(code=200, message="success", data=result)


@router.get("/message/group/{group_id}", response_model=UserResponse, summary="群聊历史")
def group_history(
    group_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 检查成员
    is_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.member_type == "user",
        GroupMember.member_id == current_user.id
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="你不是该群成员")

    offset = (page - 1) * page_size
    messages = db.query(Message).filter(
        Message.group_id == group_id
    ).order_by(desc(Message.created_at)).offset(offset).limit(page_size).all()

    result = []
    for m in reversed(messages):
        item = {
            "id": m.id,
            "sender_id": m.sender_id,
            "sender_type": m.sender_type,
            "content": m.content,
            "msg_type": m.msg_type,
            "at_staff_ids": m.at_staff_ids,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        if m.sender_type == "user":
            sender = db.query(User).filter(User.id == m.sender_id).first()
            item["sender_name"] = sender.nickname or sender.username if sender else "未知"
            item["sender_avatar"] = sender.avatar if sender else ""
        elif m.sender_type == "staff":
            staff = db.query(DigitalStaff).filter(DigitalStaff.id == m.sender_id).first()
            item["sender_name"] = staff.name if staff else "数字员工"
            item["sender_avatar"] = staff.avatar if staff else ""
            item["tag"] = staff.tag if staff else ""
        else:
            item["sender_name"] = "系统"
            item["sender_avatar"] = ""
        result.append(item)

    return UserResponse(code=200, message="success", data=result)


@router.post("/message/send", response_model=UserResponse, summary="发送消息")
async def send_message(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    msg_type = data.get("msg_type", "text")
    content = data.get("content", "").strip()
    receiver_id = data.get("receiver_id")
    group_id = data.get("group_id")
    at_staff_ids = data.get("at_staff_ids", "")

    if not content:
        raise HTTPException(status_code=400, detail="消息内容不能为空")

    msg = Message(
        msg_type=msg_type,
        sender_type="user",
        sender_id=current_user.id,
        receiver_id=receiver_id,
        group_id=group_id,
        content=content,
        at_staff_ids=at_staff_ids if at_staff_ids else None
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    sender_name = current_user.nickname or current_user.username
    base_payload = {
        "id": msg.id,
        "sender_id": current_user.id,
        "sender_type": "user",
        "sender_name": sender_name,
        "sender_avatar": current_user.avatar or "",
        "content": content,
        "msg_type": msg_type,
        "created_at": msg.created_at.isoformat() if msg.created_at else None
    }

    if receiver_id:
        # 私聊：推送给接收者，同时回推给发送者
        payload = {
            "type": "private_message",
            "data": {**base_payload, "receiver_id": receiver_id}
        }
        await manager.send_to_user(receiver_id, payload)
        await manager.send_to_user(current_user.id, payload)
    elif group_id:
        # 群聊：广播给所有在线成员
        payload = {
            "type": "group_message",
            "data": {**base_payload, "group_id": group_id, "at_staff_ids": at_staff_ids}
        }
        members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
        user_ids = [m.member_id for m in members if m.member_type == "user"]
        await manager.broadcast_to_group(user_ids, payload)

    # 异步触发数字员工响应（实际中可以用后台任务）
    if group_id and at_staff_ids:
        staff_ids = [int(x) for x in at_staff_ids.split(",") if x.strip().isdigit()]
        for sid in staff_ids:
            asyncio.create_task(staff_reply(group_id, sid, content, current_user.id))

    return UserResponse(code=200, message="发送成功", data={"message_id": msg.id})


# 允许上传的文件扩展名
ALLOWED_CHAT_EXTENSIONS = {".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                         ".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".mp3", ".zip", ".rar"}
MAX_CHAT_FILE_SIZE = 20 * 1024 * 1024  # 20MB


@router.post("/upload", response_model=UserResponse, summary="上传聊天文件")
async def upload_chat_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传聊天文件，返回可访问 URL"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名为空")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_CHAT_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}")

    # 读取内容校验大小
    content = await file.read()
    if len(content) > MAX_CHAT_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过 20MB 限制")

    # 生成唯一文件名并保存
    today = datetime.now().strftime("%Y%m%d")
    save_dir = os.path.join(CHAT_UPLOAD_DIR, today)
    os.makedirs(save_dir, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(save_dir, unique_name)
    with open(save_path, "wb") as f:
        f.write(content)

    # 返回相对 URL，前端通过 /uploads/chat/... 访问
    file_url = f"/uploads/chat/{today}/{unique_name}"
    return UserResponse(code=200, message="上传成功", data={
        "url": file_url,
        "name": file.filename,
        "size": len(content),
        "ext": ext
    })


async def generate_staff_answer(staff: DigitalStaff, prompt: str, db: Session):
    """根据数字员工配置调用模型生成回复（与群聊@复用同一套逻辑）"""
    model_cfg = None
    if staff.model_config_id:
        model_cfg = db.query(ModelConfig).filter(
            ModelConfig.id == staff.model_config_id,
            ModelConfig.is_active == True
        ).first()

    if model_cfg:
        messages_for_model = []
        if staff.system_prompt:
            messages_for_model.append({"role": "system", "content": staff.system_prompt})
        messages_for_model.append({"role": "user", "content": prompt})

        url = f"{model_cfg.api_base.rstrip('/')}/chat/completions"
        payload = {
            "model": model_cfg.model_name,
            "messages": messages_for_model,
            "stream": False,
            "temperature": model_cfg.temperature or 0.7
        }
        if model_cfg.max_tokens:
            payload["max_tokens"] = model_cfg.max_tokens

        try:
            async with httpx.AsyncClient(timeout=model_cfg.timeout or 30, follow_redirects=True) as client:
                resp = await client.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {model_cfg.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                if resp.status_code == 200:
                    raw_text = resp.text
                    result = {}
                    if raw_text.strip().startswith("data:"):
                        lines = raw_text.strip().split("\n")
                        for line in lines:
                            line = line.strip()
                            if line.startswith("data:"):
                                json_str = line[5:].strip()
                                if json_str == "[DONE]":
                                    continue
                                try:
                                    chunk = json.loads(json_str)
                                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                                    if delta.get("content"):
                                        result.setdefault("_sse_content", "")
                                        result["_sse_content"] += delta["content"]
                                    result = chunk
                                except Exception:
                                    pass
                        content = result.get("_sse_content", "")
                        if not content:
                            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    else:
                        try:
                            result = resp.json()
                        except Exception:
                            result = {"_raw_text": raw_text}
                        content = ""
                        try:
                            choices = result.get("choices", [])
                            if choices and isinstance(choices, list):
                                msg = choices[0].get("message", {})
                                if msg:
                                    content = msg.get("content", "")
                                else:
                                    content = choices[0].get("text", "")
                            else:
                                content = result.get("content", "")
                        except Exception:
                            content = ""
                    return content or f"【{staff.name}】模型未返回有效内容。"
                else:
                    return f"【{staff.name}】模型调用失败（状态码 {resp.status_code}），请检查模型配置。"
        except httpx.TimeoutException:
            return f"【{staff.name}】模型调用超时，请稍后重试。"
        except Exception as e:
            return f"【{staff.name}】模型调用异常: {str(e)[:200]}"

    return f"我是 {staff.name}，已收到您的请求: '{prompt[:50]}'。\n\n基于我的能力({staff.skills or '通用处理'})，这是处理结果:\n\n[模拟响应数据] 任务已处理完成。"


async def staff_reply(group_id: int, staff_id: int, user_content: str, user_id: int):
    """数字员工流式回复：优先调用配置模型生成真实回复"""
    from app.db.base import SessionLocal
    db = SessionLocal()
    try:
        staff = db.query(DigitalStaff).filter(DigitalStaff.id == staff_id).first()
        if not staff:
            return

        gm = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.member_type == "staff",
            GroupMember.member_id == staff_id
        ).first()
        if not gm:
            # 被 @ 的数字员工不在群中，自动邀请入群以便响应
            gm = GroupMember(
                group_id=group_id,
                member_type="staff",
                member_id=staff_id
            )
            db.add(gm)
            db.commit()

        # 提取有效提示词：去掉 @员工名称 前缀
        prompt = re.sub(r"^@[^\s]+\s+", "", user_content).strip()
        if not prompt:
            prompt = user_content

        # 广播思考中状态
        async def broadcast_step(content: str, msg_type: str = "system"):
            sys_msg = Message(
                msg_type=msg_type,
                sender_type="staff",
                sender_id=staff_id,
                group_id=group_id,
                content=content
            )
            db.add(sys_msg)
            db.commit()
            db.refresh(sys_msg)
            members = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.member_type == "user"
            ).all()
            user_ids = [m.member_id for m in members]
            await manager.broadcast_to_group(user_ids, {
                "type": "message",
                "data": {
                    "id": sys_msg.id,
                    "sender_id": staff_id,
                    "sender_type": "staff",
                    "sender_name": staff.name,
                    "sender_avatar": staff.avatar or "",
                    "tag": staff.tag or "",
                    "content": content,
                    "msg_type": msg_type,
                    "group_id": group_id,
                    "created_at": sys_msg.created_at.isoformat() if sys_msg.created_at else None
                }
            })

        await broadcast_step(f"【{staff.name}】正在分析您的请求...")
        await asyncio.sleep(0.5)
        await broadcast_step(f"正在调用相关能力: {staff.skills or '通用处理'}...")
        await asyncio.sleep(0.5)
        await broadcast_step("正在生成响应...")

        reply_content = await generate_staff_answer(staff, prompt, db)

        # 广播最终回复
        final_msg = Message(
            msg_type="text",
            sender_type="staff",
            sender_id=staff_id,
            group_id=group_id,
            content=reply_content
        )
        db.add(final_msg)
        db.commit()
        db.refresh(final_msg)

        members = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.member_type == "user"
        ).all()
        user_ids = [m.member_id for m in members]
        await manager.broadcast_to_group(user_ids, {
            "type": "message",
            "data": {
                "id": final_msg.id,
                "sender_id": staff_id,
                "sender_type": "staff",
                "sender_name": staff.name,
                "sender_avatar": staff.avatar or "",
                "tag": staff.tag or "",
                "content": reply_content,
                "msg_type": "text",
                "group_id": group_id,
                "created_at": final_msg.created_at.isoformat() if final_msg.created_at else None
            }
        })
    finally:
        db.close()


# ==================== WebSocket ====================

@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, token: str = Query(...)):
    from app.core.security import decode_token
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=1008)
        return

    user_id = int(payload.get("sub"))
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "send_private":
                receiver_id = data.get("receiver_id")
                content = data.get("content", "").strip()
                msg_type = data.get("msg_type", "text")
                if receiver_id and content:
                    msg = Message(
                        msg_type=msg_type,
                        sender_type="user",
                        sender_id=user_id,
                        receiver_id=receiver_id,
                        content=content
                    )
                    db.add(msg)
                    db.commit()
                    db.refresh(msg)

                    sender_name = user.nickname or user.username
                    payload_msg = {
                        "type": "private_message",
                        "data": {
                            "id": msg.id,
                            "sender_id": user_id,
                            "sender_name": sender_name,
                            "sender_avatar": user.avatar or "",
                            "receiver_id": receiver_id,
                            "content": content,
                            "msg_type": msg_type,
                            "created_at": msg.created_at.isoformat() if msg.created_at else None
                        }
                    }
                    # 发给接收者
                    await manager.send_to_user(receiver_id, payload_msg)
                    # 发给自己（确认）
                    await websocket.send_json(payload_msg)

            elif action == "send_group":
                group_id = data.get("group_id")
                content = data.get("content", "").strip()
                msg_type = data.get("msg_type", "text")
                at_staff_ids = data.get("at_staff_ids", "")
                if group_id and content:
                    msg = Message(
                        msg_type=msg_type,
                        sender_type="user",
                        sender_id=user_id,
                        group_id=group_id,
                        content=content,
                        at_staff_ids=at_staff_ids if at_staff_ids else None
                    )
                    db.add(msg)
                    db.commit()
                    db.refresh(msg)

                    sender_name = user.nickname or user.username
                    payload_msg = {
                        "type": "group_message",
                        "data": {
                            "id": msg.id,
                            "sender_id": user_id,
                            "sender_type": "user",
                            "sender_name": sender_name,
                            "sender_avatar": user.avatar or "",
                            "group_id": group_id,
                            "content": content,
                            "msg_type": msg_type,
                            "at_staff_ids": at_staff_ids,
                            "created_at": msg.created_at.isoformat() if msg.created_at else None
                        }
                    }

                    # 广播给群成员
                    members = db.query(GroupMember).filter(
                        GroupMember.group_id == group_id,
                        GroupMember.member_type == "user"
                    ).all()
                    user_ids = [m.member_id for m in members]
                    await manager.broadcast_to_group(user_ids, payload_msg)

                    # 触发数字员工响应
                    if at_staff_ids:
                        staff_ids = [int(x) for x in at_staff_ids.split(",") if x.strip().isdigit()]
                        for sid in staff_ids:
                            asyncio.create_task(staff_reply(group_id, sid, content, user_id))

            elif action == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        manager.disconnect(user_id)
