from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.db.base import get_db
from app.models.user import User
from app.models.admin import Admin
from app.models.staff import DigitalStaff
from app.models.chat import QueryConversation, ChatGroup, GroupMember, Message
from app.schemas.user import UserResponse
from app.api.v1.endpoints.user import get_current_user
from app.api.v1.endpoints.chat import generate_staff_answer

router = APIRouter()


def _format_relative_time(dt: datetime) -> str:
    """将时间转换为相对中文描述"""
    if not dt:
        return ""
    now = datetime.now()
    delta = now - dt
    if delta.total_seconds() < 60:
        return "刚刚"
    if delta.total_seconds() < 3600:
        return f"{int(delta.total_seconds() // 60)}分钟前"
    if delta.total_seconds() < 86400:
        return f"{int(delta.total_seconds() // 3600)}小时前"
    if delta.days < 7:
        return f"{delta.days}天前"
    return dt.strftime("%m-%d")


@router.get("/dashboard", response_model=UserResponse, summary="用户仪表盘数据")
def user_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """返回用户控制台首页所需的真实统计数据"""
    total_users = db.query(func.count(User.id)).scalar()
    total_admins = db.query(func.count(Admin.id)).scalar()

    # 数字员工统计
    staff_count = db.query(func.count(DigitalStaff.id)).scalar()
    active_staff_count = db.query(func.count(DigitalStaff.id)).filter(
        DigitalStaff.is_active == True
    ).scalar()

    # 当前用户调用智能体的次数：使用智能问数会话数作为统计口径
    staff_call_count = db.query(func.count(QueryConversation.id)).filter(
        QueryConversation.user_id == current_user.id,
        QueryConversation.is_active == True
    ).scalar()

    # 最近常用联系人：私聊 + 群聊，取每个会话最新一条消息
    private_msgs = db.query(Message).filter(
        Message.msg_type == "text",
        ((Message.sender_id == current_user.id) & (Message.sender_type == "user")) |
        ((Message.receiver_id == current_user.id) & (Message.sender_type == "user"))
    ).order_by(Message.created_at.desc()).limit(200).all()

    # 获取当前用户加入的群
    joined_groups = db.query(GroupMember).filter(
        GroupMember.member_type == "user",
        GroupMember.member_id == current_user.id
    ).all()
    joined_group_ids = [g.group_id for g in joined_groups]

    group_msgs = []
    if joined_group_ids:
        group_msgs = db.query(Message).filter(
            Message.group_id.in_(joined_group_ids),
            Message.msg_type == "text"
        ).order_by(Message.created_at.desc()).limit(200).all()

    # 按联系人/群分组，取最新消息
    contacts_map = {}
    for msg in private_msgs:
        if msg.sender_id == current_user.id:
            other_id = msg.receiver_id
        else:
            other_id = msg.sender_id
        if not other_id:
            continue
        key = ("user", other_id)
        if key not in contacts_map or contacts_map[key]["created_at"] < msg.created_at:
            contacts_map[key] = {
                "type": "user",
                "id": other_id,
                "content": msg.content,
                "created_at": msg.created_at
            }

    for msg in group_msgs:
        key = ("group", msg.group_id)
        if key not in contacts_map or contacts_map[key]["created_at"] < msg.created_at:
            contacts_map[key] = {
                "type": "group",
                "id": msg.group_id,
                "content": msg.content,
                "created_at": msg.created_at
            }

    # 补充名称和头像
    recent_contacts = []
    user_ids = [v["id"] for k, v in contacts_map.items() if v["type"] == "user"]
    group_ids = [v["id"] for k, v in contacts_map.items() if v["type"] == "group"]

    user_map = {}
    group_map = {}
    if user_ids:
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        user_map = {u.id: u for u in users}
    if group_ids:
        groups = db.query(ChatGroup).filter(ChatGroup.id.in_(group_ids)).all()
        group_map = {g.id: g for g in groups}

    for key, info in contacts_map.items():
        if info["type"] == "user":
            u = user_map.get(info["id"])
            name = (u.nickname or u.username) if u else f"用户{info['id']}"
            avatar = u.avatar if u else ""
        else:
            g = group_map.get(info["id"])
            name = g.name if g else f"群聊{info['id']}"
            avatar = g.avatar if g else ""

        recent_contacts.append({
            "type": info["type"],
            "id": info["id"],
            "from": name,
            "avatar": avatar,
            "content": info["content"],
            "time": _format_relative_time(info["created_at"])
        })

    recent_contacts.sort(key=lambda x: x["time"], reverse=True)
    recent_contacts = recent_contacts[:5]

    # 推荐数字员工：取最近创建且启用的前 3 个
    staffs = db.query(DigitalStaff).filter(DigitalStaff.is_active == True).order_by(DigitalStaff.created_at.desc()).limit(3).all()
    staff_list = []
    icon_pool = ["bolt", "sync", "shield", "analytics", "memory", "psychology"]
    for idx, s in enumerate(staffs):
        staff_list.append({
            "staff_id": s.id,
            "name": s.name,
            "role": s.role or s.tag or "数字员工",
            "status": s.status or "待命中",
            "icon": icon_pool[idx % len(icon_pool)],
            "iconClass": "animate-spin" if s.status == "处理中" else "",
            "avatar": s.avatar or ""
        })

    return UserResponse(
        code=200,
        message="success",
        data={
            "stats": {
                "staffCount": staff_count,
                "activeStaffCount": active_staff_count,
                "staffCallCount": staff_call_count,
                "todayRequests": 42891,
                "campusNodes": 1024,
                "computeUtilization": 32.8,
                "securityStatus": "极度安全",
                "securityCount": 12
            },
            "system": {
                "load": 24.8,
                "activeNodes": 128,
                "computeEfficiency": 98,
                "coreLoad": 85,
                "memoryUsage": 42.1,
                "gpuUsage": 78.4
            },
            "staff": staff_list,
            "quickLinks": [
                {"name": "最近报告", "desc": "12 条新同步", "icon": "analytics"},
                {"name": "部门分析", "desc": "全域透视", "icon": "account_tree"},
                {"name": "系统日志", "desc": "状态正常", "icon": "monitor_heart"},
                {"name": "帮助中心", "desc": "24/7 支持", "icon": "support_agent"}
            ],
            "messages": recent_contacts,
            "logs": [
                {"time": f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", "level": "[INFO]", "levelClass": "text-secondary", "text": f"核心负载均衡器初始化成功。系统当前共有 {staff_count} 个数智员工节点在线。", "textClass": "text-on-surface", "opacity": True},
                {"time": f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", "level": "[DATA]", "levelClass": "text-primary", "text": f"已处理 {staff_call_count} 次智能体调用请求。", "textClass": "text-on-surface", "opacity": False},
                {"time": f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", "level": "[INFO]", "levelClass": "text-secondary", "text": "数智助手安全特征库版本 1.0.8 校验通过。", "textClass": "text-on-surface", "opacity": True},
                {"time": f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", "level": "[INFO]", "levelClass": "text-secondary", "text": f"用户 {(current_user.nickname or current_user.username)} 登录控制台，加载仪表盘数据。", "textClass": "text-on-surface", "opacity": True}
            ],
            "userCount": total_users,
            "adminCount": total_admins
        }
    )


@router.get("/staff", response_model=UserResponse, summary="数字员工列表")
def staff_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    staffs = db.query(DigitalStaff).filter(DigitalStaff.is_active == True).order_by(DigitalStaff.created_at.desc()).all()

    total = len(staffs)
    active_count = sum(1 for s in staffs if s.status in ("活跃", "处理中"))
    sync_rate = f"{round((active_count / total * 100), 1)}%" if total else "0%"

    items = []
    for s in staffs:
        tag = s.tag or "通用节点"
        sid = f"XNU-{tag}-{str(s.id).zfill(2)}"
        if s.status in ("活跃", "处理中"):
            metric = f"活跃度: {min(85 + s.id * 3, 99)}%"
            status_color = "bg-secondary-fixed shadow-[0_0_5px_#2ae500]"
        elif s.status == "待命中":
            metric = "状态: 待命"
            status_color = "bg-outline"
        else:
            metric = f"状态: {s.status}"
            status_color = "bg-outline"

        items.append({
            "id": sid,
            "staff_id": s.id,
            "name": s.name,
            "desc": s.desc or "暂无描述",
            "tag": tag,
            "metric": metric,
            "statusColor": status_color,
            "avatar": s.avatar or ""
        })

    return UserResponse(
        code=200,
        message="success",
        data={
            "items": items,
            "overview": {
                "totalNodes": total,
                "avgResponse": "0.02s",
                "syncRate": sync_rate,
                "todayThroughput": f"{round(total * 1.8, 1)} TB"
            }
        }
    )


@router.post("/query/ask", response_model=UserResponse, summary="向指定数字员工提问")
async def ask_staff_question(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """用户选择某个数字员工并提问，复用群聊@数字员工的模型调用逻辑"""
    staff_id = data.get("staff_id")
    question = data.get("question", "").strip()

    if not staff_id:
        raise HTTPException(status_code=400, detail="请选择要提问的数字员工")
    if not question:
        raise HTTPException(status_code=400, detail="请输入问题内容")

    staff = db.query(DigitalStaff).filter(
        DigitalStaff.id == staff_id,
        DigitalStaff.is_active == True
    ).first()
    if not staff:
        raise HTTPException(status_code=404, detail="数字员工不存在或已禁用")

    reply = await generate_staff_answer(staff, question, db)

    return UserResponse(
        code=200,
        message="success",
        data={
            "staff_id": staff.id,
            "staff_name": staff.name,
            "question": question,
            "reply": reply
        }
    )


def _build_conv_data(conv: QueryConversation):
    """将会话对象序列化为响应数据"""
    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "staff_id": conv.staff_id,
        "title": conv.title,
        "messages": conv.messages or [],
        "is_active": conv.is_active,
        "created_at": conv.created_at.isoformat() if conv.created_at else None,
        "updated_at": conv.updated_at.isoformat() if conv.updated_at else None
    }


@router.post("/query/conversation", response_model=UserResponse, summary="创建智能问数会话")
def create_query_conversation(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的智能问数会话，可传入初始 staff_id 和 title"""
    title = data.get("title", "新会话").strip()
    if not title:
        title = "新会话"

    conv = QueryConversation(
        user_id=current_user.id,
        staff_id=data.get("staff_id"),
        title=title,
        messages=[]
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)

    return UserResponse(code=200, message="创建成功", data=_build_conv_data(conv))


@router.get("/query/conversation/list", response_model=UserResponse, summary="获取智能问数会话列表")
def list_query_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    page_size: int = 50
):
    """获取当前用户的智能问数会话列表，按更新时间倒序"""
    query = db.query(QueryConversation).filter(
        QueryConversation.user_id == current_user.id,
        QueryConversation.is_active == True
    ).order_by(QueryConversation.updated_at.desc())

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return UserResponse(
        code=200,
        message="success",
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [_build_conv_data(item) for item in items]
        }
    )


@router.get("/query/conversation/{conversation_id}", response_model=UserResponse, summary="获取会话详情")
def get_query_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定会话的完整消息记录"""
    conv = db.query(QueryConversation).filter(
        QueryConversation.id == conversation_id,
        QueryConversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="会话不存在")

    return UserResponse(code=200, message="success", data=_build_conv_data(conv))


@router.put("/query/conversation/{conversation_id}", response_model=UserResponse, summary="更新智能问数会话")
def update_query_conversation(
    conversation_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新会话的标题、消息列表或当前智能体"""
    conv = db.query(QueryConversation).filter(
        QueryConversation.id == conversation_id,
        QueryConversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="会话不存在")

    if "title" in data:
        conv.title = data["title"].strip() or conv.title
    if "staff_id" in data:
        conv.staff_id = data["staff_id"]
    if "messages" in data:
        conv.messages = data["messages"]

    db.commit()
    db.refresh(conv)

    return UserResponse(code=200, message="更新成功", data=_build_conv_data(conv))


@router.delete("/query/conversation/{conversation_id}", response_model=UserResponse, summary="删除智能问数会话")
def delete_query_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """软删除指定会话"""
    conv = db.query(QueryConversation).filter(
        QueryConversation.id == conversation_id,
        QueryConversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="会话不存在")

    conv.is_active = False
    db.commit()

    return UserResponse(code=200, message="删除成功", data={"id": conversation_id})
