import re
import httpx
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.db.base import get_db, SessionLocal
from app.models.admin import Admin
from app.models.crawler import CrawledData
from app.models.model_config import ModelConfig
from app.schemas.user import UserResponse
from app.api.v1.endpoints.admin import get_current_admin

router = APIRouter()

# 简单停用词
STOP_WORDS = {
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也",
    "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这", "那",
    "什么", "怎么", "为什么", "吗", "呢", "吧", "啊", "哦", "嗯", "请问", "请", "帮", "帮我",
    "分析", "查询", "告诉我", "关于", "一下", "一些", "最近", "最新", "数据", "信息", "情况",
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might", "must", "can",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them", "my",
    "your", "his", "its", "our", "their", "this", "that", "these", "those", "and", "or", "but",
    "if", "then", "else", "when", "where", "why", "how", "what", "who", "which", "with", "for",
    "from", "to", "of", "in", "on", "at", "by", "about", "into", "through", "during", "before",
    "after", "above", "below", "between", "under", "again", "further", "then", "once"
}


def _extract_keywords(question: str) -> List[str]:
    """从问题中提取候选关键词"""
    # 去掉标点，按非中文/非字母数字分割
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", " ", question)
    tokens = text.split()
    keywords = []
    for t in tokens:
        t = t.strip().lower()
        if not t or t in STOP_WORDS:
            continue
        if re.fullmatch(r"[a-zA-Z0-9]+", t):
            # 英文/数字直接作为关键词
            if len(t) >= 2:
                keywords.append(t)
        else:
            # 中文按字切分，每个字都可能成为检索关键词
            for ch in t:
                ch = ch.strip()
                if ch and ch not in STOP_WORDS and len(ch) >= 1:
                    keywords.append(ch)
    # 去重并保留顺序
    seen = set()
    result = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            result.append(k)
    return result


def _retrieve_documents(db: Session, question: str, limit: int = 10) -> List[CrawledData]:
    """基于关键词从数据仓库中检索相关文档"""
    keywords = _extract_keywords(question)

    base_query = db.query(CrawledData).filter(CrawledData.is_saved == True)

    if not keywords:
        # 没有关键词时返回最近保存的文档
        return base_query.order_by(desc(CrawledData.created_at)).limit(limit).all()

    # 构造 or 条件：title / content / summary / keywords 任一字段匹配
    conditions = []
    for kw in keywords:
        like_pattern = f"%{kw}%"
        conditions.append(CrawledData.title.ilike(like_pattern))
        conditions.append(CrawledData.content.ilike(like_pattern))
        conditions.append(CrawledData.summary.ilike(like_pattern))
        conditions.append(CrawledData.keywords.ilike(like_pattern))

    return base_query.filter(or_(*conditions)).order_by(desc(CrawledData.created_at)).limit(limit).all()


async def _call_default_model(system_prompt: str, user_prompt: str) -> str:
    """调用默认大模型"""
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
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "temperature": model.temperature or 0.3,
            "max_tokens": model.max_tokens or 2048
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
            return content or "（模型返回空内容）"
    finally:
        db.close()


SYSTEM_PROMPT = """你是西华师范大学数智校园系统的 AI 问讯助手。请仅根据下面提供的「数据仓库资料」回答用户问题。

要求：
1. 如果资料中有与问题相关的内容，请基于这些资料给出准确、简洁、自然的回答，并说明数据依据。
2. 如果资料中没有与问题相关的内容，请诚恳地向用户道歉，说明数据仓库中暂未收录相关信息，并建议用户换个关键词或稍后再试。
3. 回答以对话方式呈现，语气友好、专业。
4. 不要编造资料中没有的信息。"""


@router.post("/inquiry", response_model=UserResponse, summary="AI 问讯")
async def ai_inquiry(
    data: dict,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    接收用户问题，从数据仓库（已保存的 crawled_data）中检索相关内容，
    调用默认大模型生成回答。若未检索到相关内容，则回复歉意。
    """
    question = (data.get("question", "") or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="请输入问题")

    docs = _retrieve_documents(db, question, limit=10)

    if docs:
        context_parts = []
        for idx, d in enumerate(docs, 1):
            text = d.summary or d.content or d.title or ""
            title = d.title or "无标题"
            context_parts.append(f"【资料 {idx}】{title}\n{text[:800]}")
        context = "\n\n".join(context_parts)
        user_prompt = f"""数据仓库资料：
{context}

用户问题：{question}

请根据以上资料回答用户问题。"""
    else:
        user_prompt = f"""数据仓库资料：（未检索到与问题相关的资料）

用户问题：{question}

请向用户表示歉意，并说明数据仓库中暂未收录相关信息。"""

    answer = await _call_default_model(SYSTEM_PROMPT, user_prompt)

    return UserResponse(
        code=200,
        message="success",
        data={
            "question": question,
            "answer": answer,
            "sources_count": len(docs),
            "sources": [
                {"id": d.id, "title": d.title or "", "url": d.url or ""}
                for d in docs
            ]
        }
    )
