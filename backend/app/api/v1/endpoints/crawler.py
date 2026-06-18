from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
import asyncio
import time
import threading
import httpx

from app.db.base import get_db
from app.models.crawler import CrawlSource, CrawlTask, CrawledData
from app.models.admin import Admin
from app.models.model_config import ModelConfig
from app.schemas.user import UserResponse
from app.api.v1.endpoints.admin import get_current_admin
from app.services.crawler_service import CrawlerService

router = APIRouter()

# ========== 内存缓存：任务结果暂存（未保存到数据库前） ==========
# 结构: { task_id: { "items": [...], "created_at": timestamp } }
_task_result_cache = {}
_cache_lock = threading.Lock()
_CACHE_TTL = 3600 * 2  # 缓存保留2小时


def _clean_expired_cache():
    """清理过期缓存"""
    now = time.time()
    expired = [k for k, v in _task_result_cache.items() if now - v.get("created_at", 0) > _CACHE_TTL]
    for k in expired:
        del _task_result_cache[k]


def _set_task_cache(task_id: int, items: list):
    with _cache_lock:
        _clean_expired_cache()
        _task_result_cache[task_id] = {
            "items": items,
            "created_at": time.time()
        }


def _get_task_cache(task_id: int):
    with _cache_lock:
        _clean_expired_cache()
        return _task_result_cache.get(task_id, {}).get("items", [])


def _clear_task_cache(task_id: int):
    with _cache_lock:
        if task_id in _task_result_cache:
            del _task_result_cache[task_id]


# ========== 数据源管理 ==========

@router.get("/source", response_model=UserResponse, summary="数据源列表")
def list_sources(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    items = db.query(CrawlSource).order_by(desc(CrawlSource.created_at)).all()
    data = []
    for s in items:
        data.append({
            "id": s.id,
            "name": s.name,
            "source_type": s.source_type,
            "base_url": s.base_url,
            "keyword_placeholder": s.keyword_placeholder,
            "description": s.description or "",
            "params": s.params or {},
            "rules": s.rules or [],
            "max_depth": s.max_depth,
            "is_active": s.is_active,
            "created_at": s.created_at.isoformat() if s.created_at else None
        })
    return UserResponse(code=200, message="success", data={"items": data, "total": len(data)})


@router.post("/source", response_model=UserResponse, summary="创建数据源")
def create_source(
    data: dict,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    source = CrawlSource(
        name=data.get("name", ""),
        source_type=data.get("source_type", "custom"),
        base_url=data.get("base_url", ""),
        keyword_placeholder=data.get("keyword_placeholder", "{keyword}"),
        description=data.get("description"),
        params=data.get("params") or {},
        rules=data.get("rules") or [],
        max_depth=data.get("max_depth", 1),
        is_active=data.get("is_active", True)
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return UserResponse(code=200, message="创建成功", data={"id": source.id})


@router.put("/source/{source_id}", response_model=UserResponse, summary="更新数据源")
def update_source(
    source_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    source = db.query(CrawlSource).filter(CrawlSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="数据源不存在")
    for field in ["name", "source_type", "base_url", "keyword_placeholder", "description", "params", "rules", "max_depth", "is_active"]:
        if field in data:
            setattr(source, field, data[field])
    db.commit()
    db.refresh(source)
    return UserResponse(code=200, message="更新成功")


@router.delete("/source/{source_id}", response_model=UserResponse, summary="删除数据源")
def delete_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    source = db.query(CrawlSource).filter(CrawlSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="数据源不存在")
    # 先删除关联的爬取数据和任务（避免外键约束错误）
    db.query(CrawledData).filter(CrawledData.source_id == source_id).delete(synchronize_session=False)
    db.query(CrawlTask).filter(CrawlTask.source_id == source_id).delete(synchronize_session=False)
    db.delete(source)
    db.commit()
    return UserResponse(code=200, message="删除成功")


# ========== 数据采集任务 ==========

@router.post("/task", response_model=UserResponse, summary="创建采集任务")
async def create_task(
    data: dict,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    source_id = data.get("source_id")
    keyword = data.get("keyword", "").strip()
    if not source_id or not keyword:
        raise HTTPException(status_code=400, detail="请选择数据源并输入关键词")

    source = db.query(CrawlSource).filter(CrawlSource.id == source_id, CrawlSource.is_active == True).first()
    if not source:
        raise HTTPException(status_code=404, detail="数据源不存在或未启用")

    task = CrawlTask(source_id=source_id, keyword=keyword, status="running")
    db.add(task)
    db.commit()
    db.refresh(task)

    # 异步执行爬取
    asyncio.create_task(_do_crawl(task.id, source_id, keyword))

    return UserResponse(code=200, message="任务已创建并开始爬取", data={"task_id": task.id})


async def _do_crawl(task_id: int, source_id: int, keyword: str):
    """后台执行爬取"""
    from app.db.base import SessionLocal
    db = SessionLocal()
    try:
        task = db.query(CrawlTask).filter(CrawlTask.id == task_id).first()
        source = db.query(CrawlSource).filter(CrawlSource.id == source_id).first()
        if not task or not source:
            return

        try:
            results = await CrawlerService.crawl(source, keyword, db)
            # 结果存入内存缓存，不写入数据库
            cache_items = []
            for idx, item in enumerate(results):
                cache_items.append({
                    "id": f"{task_id}_{idx}",  # 临时ID供前端勾选使用
                    "title": item.get("title", "")[:500],
                    "content": item.get("content", "")[:20000],
                    "url": item.get("url", ""),
                    "raw_data": item,
                    "markdown_content": item.get("markdown_content", ""),
                    "summary": item.get("summary", ""),
                    "keywords": item.get("keywords", []),
                    "entities": item.get("entities", {}),
                    "created_at": __import__("datetime").datetime.utcnow().isoformat()
                })
            _set_task_cache(task_id, cache_items)
            task.status = "completed"
            task.result_count = len(results)
        except Exception as e:
            task.status = "failed"
            task.error_msg = str(e)[:500]
        task.completed_at = __import__("datetime").datetime.utcnow()
        db.commit()
    finally:
        db.close()


@router.get("/task", response_model=UserResponse, summary="任务列表")
def list_tasks(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    items = db.query(CrawlTask).order_by(desc(CrawlTask.created_at)).all()
    data = []
    for t in items:
        source = db.query(CrawlSource).filter(CrawlSource.id == t.source_id).first()
        data.append({
            "id": t.id,
            "source_id": t.source_id,
            "source_name": source.name if source else "",
            "keyword": t.keyword,
            "status": t.status,
            "result_count": t.result_count,
            "error_msg": t.error_msg or "",
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "completed_at": t.completed_at.isoformat() if t.completed_at else None
        })
    return UserResponse(code=200, message="success", data={"items": data, "total": len(data)})


@router.get("/task/{task_id}/result", response_model=UserResponse, summary="任务结果")
def task_result(
    task_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    task = db.query(CrawlTask).filter(CrawlTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    # 优先从内存缓存读取
    items = _get_task_cache(task_id)
    if not items:
        # 回退到数据库（兼容旧数据）
        db_items = db.query(CrawledData).filter(CrawledData.task_id == task_id).order_by(desc(CrawledData.created_at)).all()
        items = []
        for d in db_items:
            items.append({
                "id": d.id,
                "title": d.title or "",
                "content": d.content or "",
                "url": d.url or "",
                "summary": d.summary or "",
                "keywords": d.keywords or [],
                "entities": d.entities or {},
                "markdown_content": d.markdown_content or "",
                "raw_data": d.raw_data or {},
                "is_saved": d.is_saved,
                "created_at": d.created_at.isoformat() if d.created_at else None
            })
    return UserResponse(code=200, message="success", data={"task": {"id": task.id, "status": task.status, "keyword": task.keyword}, "items": items, "total": len(items)})


# ========== 数据保存 ==========

@router.post("/data/save", response_model=UserResponse, summary="保存数据到仓库")
def save_data(
    data: dict,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    ids = data.get("ids", [])
    if not ids:
        raise HTTPException(status_code=400, detail="请选择要保存的数据")

    # 从各任务缓存中查找并写入数据库
    count = 0
    for temp_id in ids:
        # 解析 task_id: temp_id 格式为 "{task_id}_{index}"
        if isinstance(temp_id, str) and "_" in temp_id:
            try:
                task_id = int(temp_id.split("_", 1)[0])
            except ValueError:
                continue
        elif isinstance(temp_id, int):
            # 兼容旧数据（已是数据库ID）
            cd = db.query(CrawledData).filter(CrawledData.id == temp_id).first()
            if cd:
                cd.is_saved = True
                count += 1
            continue
        else:
            continue

        cache_items = _get_task_cache(task_id)
        item = None
        for ci in cache_items:
            if ci.get("id") == temp_id:
                item = ci
                break
        if not item:
            continue

        # 写入数据库
        task = db.query(CrawlTask).filter(CrawlTask.id == task_id).first()
        source_id = task.source_id if task else None
        cd = CrawledData(
            task_id=task_id,
            source_id=source_id,
            title=item.get("title", ""),
            content=item.get("content", ""),
            url=item.get("url", ""),
            raw_data=item.get("raw_data", {}),
            markdown_content=item.get("markdown_content", ""),
            summary=item.get("summary", ""),
            keywords=item.get("keywords", []),
            entities=item.get("entities", {}),
            is_saved=True
        )
        db.add(cd)
        count += 1

        # 从缓存中移除已保存项
        with _cache_lock:
            cache = _task_result_cache.get(task_id)
            if cache:
                cache["items"] = [ci for ci in cache["items"] if ci.get("id") != temp_id]

    db.commit()
    return UserResponse(code=200, message=f"已保存 {count} 条数据", data={"saved_count": count})


@router.get("/data/overview", response_model=UserResponse, summary="存储概览统计")
def data_overview(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """返回数据仓库的统计概览，供前端存储管理页面渲染"""
    from datetime import datetime, timedelta

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    # 1. 基础统计
    total_saved = db.query(func.count(CrawledData.id)).filter(CrawledData.is_saved == True).scalar() or 0
    today_saved = db.query(func.count(CrawledData.id)).filter(
        CrawledData.is_saved == True,
        CrawledData.created_at >= today_start
    ).scalar() or 0
    total_sources = db.query(func.count(CrawlSource.id)).scalar() or 0
    running_tasks = db.query(func.count(CrawlTask.id)).filter(CrawlTask.status == "running").scalar() or 0

    # 2. 来源分布
    source_rows = db.query(
        CrawlSource.name,
        func.count(CrawledData.id)
    ).join(CrawledData, CrawlSource.id == CrawledData.source_id).filter(
        CrawledData.is_saved == True
    ).group_by(CrawlSource.id).all()
    source_distribution = [{"name": name or "未知", "count": count} for name, count in source_rows]

    # 3. 关键词统计（Top 10）
    keyword_counts = {}
    all_keywords = db.query(CrawledData.keywords).filter(CrawledData.is_saved == True).all()
    for (kw_list,) in all_keywords:
            if kw_list:
                for kw in kw_list:
                    keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
    top_keywords = sorted(
        [{"name": k, "count": v} for k, v in keyword_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:10]

    # 4. 实体统计（地名 Top 10）
    location_counts = {}
    all_entities = db.query(CrawledData.entities).filter(CrawledData.is_saved == True).all()
    for (ent,) in all_entities:
        if ent and isinstance(ent, dict):
            for loc in ent.get("地点", []):
                location_counts[loc] = location_counts.get(loc, 0) + 1
    top_locations = sorted(
        [{"name": k, "count": v} for k, v in location_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:10]

    # 5. 数据仓库结构
    schema = [
        {"layer": "ODS_ENTITY_DATA", "name": "原始层", "fields": [
            {"name": "row_id", "type": "INT AUTO_INCREMENT PK"},
            {"name": "raw_payload", "type": "JSON"},
            {"name": "source_tag", "type": "VARCHAR(64)"},
            {"name": "ingest_ts", "type": "DATETIME"}
        ]},
        {"layer": "DWD_CRAWL_DETAIL", "name": "明细层", "fields": [
            {"name": "id", "type": "INT AUTO_INCREMENT PK"},
            {"name": "task_id", "type": "INT FK"},
            {"name": "source_id", "type": "INT FK"},
            {"name": "title", "type": "VARCHAR(500)"},
            {"name": "content", "type": "TEXT"},
            {"name": "url", "type": "VARCHAR(1000)"},
            {"name": "markdown_content", "type": "LONGTEXT"},
            {"name": "summary", "type": "TEXT"},
            {"name": "keywords", "type": "JSON"},
            {"name": "entities", "type": "JSON"},
            {"name": "is_saved", "type": "BOOLEAN"},
            {"name": "created_at", "type": "DATETIME"}
        ]},
        {"layer": "ADS_SMART_ANALYTICS", "name": "应用层", "fields": [
            {"name": "report_date", "type": "DATE"},
            {"name": "kpi_score", "type": "DECIMAL(5,2)"},
            {"name": "keyword_trend", "type": "JSON"},
            {"name": "entity_distribution", "type": "JSON"}
        ]}
    ]

    # 6. 集群节点状态（模拟）
    import random
    nodes = []
    for i in range(1, 9):
        status = random.choice(["healthy", "healthy", "healthy", "healthy", "error", "offline"])
        nodes.append({
            "id": f"NODE_{i:02d}",
            "status": status,
            "cpu": random.randint(10, 90) if status == "healthy" else 0,
            "memory": random.randint(20, 80) if status == "healthy" else 0
        })

    return UserResponse(code=200, message="success", data={
        "stats": {
            "total_saved": total_saved,
            "today_saved": today_saved,
            "total_sources": total_sources,
            "running_tasks": running_tasks
        },
        "source_distribution": source_distribution,
        "top_keywords": top_keywords,
        "top_locations": top_locations,
        "schema": schema,
        "nodes": nodes
    })


@router.get("/data/saved", response_model=UserResponse, summary="已保存的数据")
def list_saved_data(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    items = db.query(CrawledData).filter(CrawledData.is_saved == True).order_by(desc(CrawledData.created_at)).all()
    data = []
    for d in items:
        source = db.query(CrawlSource).filter(CrawlSource.id == d.source_id).first()
        data.append({
            "id": d.id,
            "title": d.title or "",
            "content": d.content or "",
            "url": d.url or "",
            "summary": d.summary or "",
            "keywords": d.keywords or [],
            "entities": d.entities or {},
            "source_name": source.name if source else "",
            "raw_data": d.raw_data or {},
            "created_at": d.created_at.isoformat() if d.created_at else None
        })
    return UserResponse(code=200, message="success", data={"items": data, "total": len(data)})


@router.delete("/data/{data_id}", response_model=UserResponse, summary="删除爬取数据")
def delete_data(
    data_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    cd = db.query(CrawledData).filter(CrawledData.id == data_id).first()
    if not cd:
        raise HTTPException(status_code=404, detail="数据不存在")
    db.delete(cd)
    db.commit()
    return UserResponse(code=200, message="删除成功")


# ========== 数据清洗（大模型） ==========

async def _call_default_model(prompt: str) -> str:
    """调用默认大模型进行文本处理"""
    from app.db.base import SessionLocal
    db = SessionLocal()
    try:
        model = db.query(ModelConfig).filter(ModelConfig.is_default == True, ModelConfig.is_active == True).first()
        if not model:
            raise HTTPException(status_code=404, detail="未设置默认模型或模型未启用")

        url = f"{model.api_base.rstrip('/')}/chat/completions"
        payload = {
            "model": model.model_name,
            "messages": [{"role": "user", "content": prompt}],
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


@router.post("/data/clean", response_model=UserResponse, summary="大模型数据清洗")
async def clean_data(
    data: dict,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    接收数据ID列表和清洗指令，调用默认大模型对每条数据的摘要进行清洗。
    返回清洗后的结果列表。
    """
    ids = data.get("ids", [])
    instruction = data.get("instruction", "对以下文本进行清洗、去噪、精炼，保留核心信息并输出一段通顺的中文摘要。").strip()
    if not ids:
        raise HTTPException(status_code=400, detail="请选择要清洗的数据")

    items = db.query(CrawledData).filter(
        CrawledData.id.in_(ids),
        CrawledData.is_saved == True
    ).all()
    if not items:
        raise HTTPException(status_code=404, detail="未找到可清洗的数据")

    results = []
    for item in items:
        original_summary = item.summary or item.content or ""
        if not original_summary:
            results.append({
                "id": item.id,
                "title": item.title or "",
                "original": "",
                "cleaned": "（原文为空，无法清洗）",
                "status": "skipped"
            })
            continue

        prompt = f"""{instruction}

原文标题：{item.title or '无标题'}
原文摘要：
{original_summary}

请直接输出清洗后的文本，不要添加额外解释。"""
        try:
            cleaned_text = await _call_default_model(prompt)
            results.append({
                "id": item.id,
                "title": item.title or "",
                "original": original_summary,
                "cleaned": cleaned_text,
                "status": "success"
            })
        except Exception as e:
            results.append({
                "id": item.id,
                "title": item.title or "",
                "original": original_summary,
                "cleaned": f"清洗失败: {str(e)}",
                "status": "failed"
            })

    return UserResponse(code=200, message="清洗完成", data={"results": results, "total": len(results)})
