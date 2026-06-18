import json
from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.api.v1.endpoints.admin import get_current_admin
from app.db.base import get_db
from app.models.admin import Admin
from app.models.crawler import CrawledData, CrawlSource, CrawlTask
from app.schemas.user import UserResponse

router = APIRouter()

# 简单城市 -> 经纬度映射（供 3D 地球使用）
CITY_COORDS = {
    "北京": [116.4074, 39.9042],
    "上海": [121.4737, 31.2304],
    "广州": [113.2644, 23.1291],
    "深圳": [114.0579, 22.5431],
    "成都": [104.0668, 30.5728],
    "杭州": [120.1551, 30.2741],
    "武汉": [114.3054, 30.5928],
    "西安": [108.9398, 34.3416],
    "南京": [118.7969, 32.0603],
    "重庆": [106.5516, 29.5630],
    "天津": [117.2009, 39.0842],
    "苏州": [120.5853, 31.2989],
    "南充": [106.1107, 30.8378],
    "郑州": [113.6253, 34.7466],
    "长沙": [112.9388, 28.2282],
    "沈阳": [123.4315, 41.8057],
    "青岛": [120.3826, 36.0671],
    "宁波": [121.5500, 29.8750],
    "东莞": [113.7518, 23.0207],
    "哈尔滨": [126.5350, 45.8038],
    "纽约": [-74.0060, 40.7128],
    "伦敦": [-0.1276, 51.5074],
    "东京": [139.6917, 35.6895],
    "巴黎": [2.3522, 48.8566],
    "悉尼": [151.2093, -33.8688],
    "新加坡": [103.8198, 1.3521],
}


def _parse_keywords(kw_value) -> List[str]:
    """兼容 JSON 字符串与列表"""
    if not kw_value:
        return []
    if isinstance(kw_value, list):
        return kw_value
    try:
        obj = json.loads(kw_value)
        return obj if isinstance(obj, list) else []
    except Exception:
        return []


@router.get("/warehouse", response_model=UserResponse, summary="数据仓库大屏统计")
def bigscreen_warehouse(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    聚合数据仓库多维统计，供大屏监控模块使用。
    返回：基础指标、来源分布、关键词词云、地点 3D 分布、时间趋势、最新日志。
    """
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today_start - timedelta(days=6)

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
    source_distribution = [{"name": name or "未知", "value": count} for name, count in source_rows]

    # 3. 关键词频率（词云，全部关键词，Top 50）
    keyword_counter = Counter()
    rows = db.query(CrawledData.keywords).filter(CrawledData.is_saved == True).all()
    for (kw_value,) in rows:
        for kw in _parse_keywords(kw_value):
            if kw and len(str(kw).strip()) > 0:
                keyword_counter[str(kw).strip()] += 1
    wordcloud_data = [{"name": k, "value": v} for k, v in keyword_counter.most_common(50)]

    # 4. 地点 3D 分布（从 entities.地点、keywords、title、summary 中识别已知城市）
    def _collect_locations(item: CrawledData) -> List[str]:
        found = set()
        # entities 中的地点
        if item.entities and isinstance(item.entities, dict):
            for loc in item.entities.get("地点", []):
                if loc:
                    found.add(str(loc))
        # 从 title / summary / keywords 文本中匹配城市
        texts = []
        if item.title:
            texts.append(str(item.title))
        if item.summary:
            texts.append(str(item.summary))
        for kw in _parse_keywords(item.keywords):
            texts.append(str(kw))
        text = " ".join(texts)
        for city in CITY_COORDS.keys():
            if city in text:
                found.add(city)
        return list(found)

    location_counter = Counter()
    rows = db.query(CrawledData).filter(CrawledData.is_saved == True).all()
    for item in rows:
        for loc in _collect_locations(item):
            location_counter[loc] += 1

    globe_data = []
    for loc, count in location_counter.most_common(30):
        coord = CITY_COORDS.get(loc)
        if coord:
            globe_data.append({"name": loc, "value": coord + [count]})

    # 5. 时间趋势（最近 7 天，每天保存量）
    trend_map: Dict[str, int] = {}
    for i in range(7):
        day = (week_ago + timedelta(days=i)).strftime("%m-%d")
        trend_map[day] = 0

    rows = db.query(
        func.date_format(CrawledData.created_at, "%m-%d").label("day"),
        func.count(CrawledData.id)
    ).filter(
        CrawledData.is_saved == True,
        CrawledData.created_at >= week_ago
    ).group_by("day").all()
    for day, count in rows:
        if day in trend_map:
            trend_map[day] = count
    trend_data = [{"date": k, "count": v} for k, v in sorted(trend_map.items(), key=lambda x: x[0])]

    # 6. 最新活动日志
    recent_items = db.query(CrawledData).filter(
        CrawledData.is_saved == True
    ).order_by(desc(CrawledData.created_at)).limit(8).all()
    recent_logs = []
    for d in recent_items:
        source = db.query(CrawlSource).filter(CrawlSource.id == d.source_id).first()
        recent_logs.append({
            "id": d.id,
            "title": d.title or "无标题",
            "source": source.name if source else "未知来源",
            "created_at": d.created_at.isoformat() if d.created_at else None
        })

    return UserResponse(code=200, message="success", data={
        "stats": {
            "total_saved": total_saved,
            "today_saved": today_saved,
            "total_sources": total_sources,
            "running_tasks": running_tasks
        },
        "source_distribution": source_distribution,
        "wordcloud": wordcloud_data,
        "globe": globe_data,
        "trend": trend_data,
        "recent_logs": recent_logs
    })
