import asyncio
import json
import httpx
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, or_

from app.db.base import get_db, SessionLocal
from app.models.crawler import CrawledData
from app.models.chat import Message
from app.models.model_config import ModelConfig
from app.models.admin import Admin
from app.schemas.user import UserResponse
from app.api.v1.endpoints.admin import get_current_admin

router = APIRouter()

# 违规类型中文映射
VIOLATION_TYPE_LABELS = {
    "PORN": "色情低俗",
    "VIOLENCE": "暴力血腥",
    "POLITICAL": "政治敏感",
    "ILLEGAL": "违法违规",
    "HATE": "仇恨言论",
    "SPAM": "垃圾广告",
    "SENSITIVE_INFO": "敏感信息泄露",
    "OTHER": "其他违规",
}


async def _call_default_model(system_prompt: str, user_content: str) -> str:
    """调用默认大模型进行内容审核"""
    db = SessionLocal()
    try:
        model = db.query(ModelConfig).filter(ModelConfig.is_default == True, ModelConfig.is_active == True).first()
        if not model:
            raise HTTPException(status_code=404, detail="未设置默认模型或默认模型未启用")

        url = f"{model.api_base.rstrip('/')}/chat/completions"
        payload = {
            "model": model.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "stream": False,
            "temperature": 0.1,
            "max_tokens": 1024
        }
        async with httpx.AsyncClient(timeout=model.timeout or 60, follow_redirects=True) as client:
            resp = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {model.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=502, detail=f"模型接口错误: HTTP {resp.status_code}")

            result = resp.json()
            choices = result.get("choices", [])
            if choices and isinstance(choices, list):
                msg = choices[0].get("message", {})
                content = msg.get("content", "")
            else:
                content = result.get("content", "")
            return content or ""
    finally:
        db.close()


SYSTEM_PROMPT = """你是一名内容安全审核专家。请对用户提供的内容进行合规性审查，判断是否存在色情、暴力、政治敏感、违法违规、仇恨言论、垃圾广告、敏感信息泄露等问题。

请严格按以下 JSON 格式返回，不要输出任何其他文字：
{
  "is_violation": true 或 false,
  "type": "PORN|VIOLENCE|POLITICAL|ILLEGAL|HATE|SPAM|SENSITIVE_INFO|OTHER|PASS",
  "reason": "简要说明判定理由（50字以内）",
  "confidence": 0-1 之间的浮点数
}

字段说明：
- is_violation: 是否存在违规内容
- type: 违规类型，如无违规则填 PASS
- reason: 判定理由
- confidence: 置信度，越接近1表示越确定

注意：只需返回 JSON，不要添加 markdown 代码块或其他解释。"""


def _parse_audit_result(raw_text: str) -> Dict[str, Any]:
    """解析模型返回的审核结果"""
    text = raw_text.strip()
    # 去掉可能的 markdown 代码块
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        data = json.loads(text)
        is_violation = bool(data.get("is_violation", False))
        vtype = data.get("type", "PASS")
        if not is_violation:
            vtype = "PASS"
        elif vtype not in VIOLATION_TYPE_LABELS:
            vtype = "OTHER"
        conf = abs(float(data.get("confidence", 0.5)))
        if conf > 1:
            conf = conf / 100
        conf = max(0.0, min(1.0, conf))
        return {
            "is_violation": is_violation,
            "type": vtype,
            "reason": data.get("reason", "")[:200],
            "confidence": conf
        }
    except Exception:
        return {
            "is_violation": False,
            "type": "PASS",
            "reason": "模型返回格式异常，默认通过",
            "confidence": 0.0
        }


async def _audit_single(content: str, title: str = "") -> Dict[str, Any]:
    """审核单条内容"""
    user_content = f"标题：{title}\n\n内容：{content[:4000]}"
    raw = await _call_default_model(SYSTEM_PROMPT, user_content)
    return _parse_audit_result(raw)


# ========== 爬取数据审核 ==========

@router.post("/crawl/scan", response_model=UserResponse, summary="扫描爬取数据违规内容")
async def scan_crawl_data(
    data: dict = None,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    对 crawled_data 表中未审核或待审核的数据进行 AI 审核。
    可传入 {"limit": 50} 控制每次扫描条数，默认 50。
    """
    if data is None:
        data = {}
    limit = min(int(data.get("limit", 50)), 200)

    items = db.query(CrawledData).filter(
        or_(CrawledData.audit_status == "pending", CrawledData.audit_status.is_(None))
    ).order_by(desc(CrawledData.created_at)).limit(limit).all()

    semaphore = asyncio.Semaphore(5)

    async def _audit_item(item):
        text = item.content or item.markdown_content or item.title or ""
        title = item.title or ""
        if not text.strip():
            return {
                "item": item,
                "result": {"is_violation": False, "type": "PASS", "reason": "内容为空", "confidence": 1.0}
            }
        async with semaphore:
            try:
                result = await _audit_single(text, title)
            except Exception:
                return None
        return {"item": item, "result": result}

    tasks = [_audit_item(item) for item in items]
    results = await asyncio.gather(*tasks)

    scanned = 0
    violations = 0
    for r in results:
        if r is None:
            continue
        item = r["item"]
        result = r["result"]
        item.audit_result = result
        item.audited_at = datetime.utcnow()
        scanned += 1
        if result.get("is_violation"):
            item.audit_status = "rejected"
            violations += 1
        else:
            item.audit_status = "pass"

    db.commit()
    return UserResponse(
        code=200,
        message=f"扫描完成：已审核 {scanned} 条，发现违规 {violations} 条",
        data={"scanned": scanned, "violations": violations}
    )


@router.get("/crawl/violations", response_model=UserResponse, summary="获取爬取数据违规列表")
def get_crawl_violations(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """返回 crawled_data 中审核状态为 rejected 的违规内容"""
    offset = (page - 1) * page_size
    query = db.query(CrawledData).filter(CrawledData.audit_status == "rejected").order_by(desc(CrawledData.audited_at))
    total = query.count()
    items = query.offset(offset).limit(page_size).all()

    data = []
    for item in items:
        result = item.audit_result or {}
        data.append({
            "id": item.id,
            "title": item.title or "",
            "content": (item.content or item.markdown_content or "")[:500],
            "url": item.url or "",
            "type": result.get("type", "OTHER"),
            "type_label": VIOLATION_TYPE_LABELS.get(result.get("type", "OTHER"), "其他违规"),
            "reason": result.get("reason", ""),
            "confidence": result.get("confidence", 0),
            "audited_at": item.audited_at.isoformat() if item.audited_at else None,
            "created_at": item.created_at.isoformat() if item.created_at else None
        })

    return UserResponse(code=200, message="success", data={"items": data, "total": total, "page": page, "page_size": page_size})


# ========== 违规用户管理 ==========

@router.get("/message/violators", response_model=UserResponse, summary="获取违规用户列表")
def get_violator_users(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    按发送者聚合 messages 中的违规记录，返回普通用户维度的违规统计。
    只包含有实际用户账号（sender_type=user）的发送者。
    """
    from app.models.user import User

    rows = db.query(
        Message.sender_id,
        func.count(Message.id).label("violation_count")
    ).filter(
        Message.audit_status == "rejected",
        Message.sender_type == "user"
    ).group_by(Message.sender_id).order_by(desc("violation_count")).all()

    data = []
    for sender_id, count in rows:
        user = db.query(User).filter(User.id == sender_id).first()
        if not user:
            continue
        # 最近一条违规消息
        latest_msg = db.query(Message).filter(
            Message.sender_id == sender_id,
            Message.sender_type == "user",
            Message.audit_status == "rejected"
        ).order_by(desc(Message.audited_at)).first()
        latest_type = "OTHER"
        if latest_msg and latest_msg.audit_result:
            latest_type = latest_msg.audit_result.get("type", "OTHER")

        data.append({
            "user_id": user.id,
            "username": user.username,
            "nickname": user.nickname or user.username,
            "avatar": user.avatar,
            "is_active": user.is_active,
            "violation_count": count,
            "latest_type": latest_type,
            "latest_type_label": VIOLATION_TYPE_LABELS.get(latest_type, "其他违规"),
            "latest_at": latest_msg.audited_at.isoformat() if latest_msg and latest_msg.audited_at else None
        })

    return UserResponse(code=200, message="success", data={"items": data, "total": len(data)})


# ========== 聊天消息审核 ==========

@router.post("/message/scan", response_model=UserResponse, summary="扫描聊天消息违规内容")
async def scan_messages(
    data: dict = None,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    对 messages 表中未审核或待审核的文本消息进行 AI 审核。
    可传入 {"limit": 100} 控制每次扫描条数，默认 100。
    """
    if data is None:
        data = {}
    limit = min(int(data.get("limit", 100)), 300)

    items = db.query(Message).filter(
        Message.msg_type == "text",
        or_(Message.is_scanned == False, Message.is_scanned.is_(None))
    ).order_by(desc(Message.created_at)).limit(limit).all()

    semaphore = asyncio.Semaphore(5)

    async def _audit_item(item):
        text = item.content or ""
        if not text.strip():
            return {
                "item": item,
                "result": {"is_violation": False, "type": "PASS", "reason": "内容为空", "confidence": 1.0}
            }
        async with semaphore:
            try:
                result = await _audit_single(text)
            except Exception:
                return None
        return {"item": item, "result": result}

    tasks = [_audit_item(item) for item in items]
    results = await asyncio.gather(*tasks)

    scanned = 0
    violations = 0
    for r in results:
        if r is None:
            continue
        item = r["item"]
        result = r["result"]
        item.audit_result = result
        item.audited_at = datetime.utcnow()
        item.is_scanned = True
        scanned += 1
        if result.get("is_violation"):
            item.audit_status = "rejected"
            violations += 1
        else:
            item.audit_status = "pass"

    db.commit()
    return UserResponse(
        code=200,
        message=f"扫描完成：已审核 {scanned} 条，发现违规 {violations} 条",
        data={"scanned": scanned, "violations": violations}
    )


@router.get("/message/violations", response_model=UserResponse, summary="获取聊天消息违规列表")
def get_message_violations(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """返回 messages 中审核状态为 rejected 的违规内容"""
    offset = (page - 1) * page_size
    query = db.query(Message).filter(Message.audit_status == "rejected").order_by(desc(Message.audited_at))
    total = query.count()
    items = query.offset(offset).limit(page_size).all()

    data = []
    for item in items:
        result = item.audit_result or {}
        sender_name = "未知"
        if item.sender_type == "user":
            from app.models.user import User
            user = db.query(User).filter(User.id == item.sender_id).first()
            sender_name = user.nickname or user.username if user else "未知用户"
        elif item.sender_type == "staff":
            from app.models.staff import DigitalStaff
            staff = db.query(DigitalStaff).filter(DigitalStaff.id == item.sender_id).first()
            sender_name = staff.name if staff else "未知员工"

        data.append({
            "id": item.id,
            "sender_type": item.sender_type,
            "sender_id": item.sender_id,
            "sender_name": sender_name,
            "content": item.content[:500],
            "type": result.get("type", "OTHER"),
            "type_label": VIOLATION_TYPE_LABELS.get(result.get("type", "OTHER"), "其他违规"),
            "reason": result.get("reason", ""),
            "confidence": result.get("confidence", 0),
            "audited_at": item.audited_at.isoformat() if item.audited_at else None,
            "created_at": item.created_at.isoformat() if item.created_at else None
        })

    return UserResponse(code=200, message="success", data={"items": data, "total": total, "page": page, "page_size": page_size})
