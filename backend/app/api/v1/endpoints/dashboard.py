from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db.base import get_db
from app.models.admin import Admin
from app.models.user import User
from app.models.staff import DigitalStaff
from app.schemas.admin import AdminResponse
from app.api.v1.endpoints.admin import get_current_admin

router = APIRouter()


@router.get("/stats", response_model=AdminResponse, summary="仪表盘统计数据")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """返回仪表盘所需的各项统计数据"""
    # 总管理员数
    total_admins = db.query(func.count(Admin.id)).scalar()

    # 活跃管理员数
    active_admins = db.query(func.count(Admin.id)).filter(Admin.is_active == True).scalar()

    # 超级管理员数
    super_admins = db.query(func.count(Admin.id)).filter(Admin.is_superuser == True).scalar()

    # 普通用户统计
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()

    # 今日新增（最近24小时）
    last_24h = datetime.now() - timedelta(hours=24)
    recent_admins = db.query(func.count(Admin.id)).filter(Admin.created_at > last_24h).scalar()
    recent_users = db.query(func.count(User.id)).filter(User.created_at > last_24h).scalar()
    recent = (recent_admins or 0) + (recent_users or 0)

    # 数字员工统计
    total_staff = db.query(func.count(DigitalStaff.id)).scalar()
    active_staff = db.query(func.count(DigitalStaff.id)).filter(DigitalStaff.is_active == True).scalar()

    return AdminResponse(
        code=200,
        message="success",
        data={
            "totalCollection": "1.2M+",
            "totalUsers": total_admins,
            "activeUsers": active_admins,
            "superUsers": super_admins,
            "todayNew": recent or 0,
            "cleaningRate": "99.2%",
            "activeStaff": active_staff or 0,
            "totalStaff": total_staff or 0,
            "systemLoad": "34%",
            "trend": {
                "collection": "+12.5%",
                "users": "+3.2%",
                "cleaning": "极佳",
                "staff": "在线"
            },
            "trafficData": [
                {"time": "00:00", "value": 12},
                {"time": "04:00", "value": 18},
                {"time": "08:00", "value": 16},
                {"time": "12:00", "value": 26},
                {"time": "16:00", "value": 34},
                {"time": "20:00", "value": 28},
                {"time": "23:59", "value": 22}
            ],
            "departmentDistribution": [
                {"name": "人文科学", "value": 25, "color": "primary"},
                {"name": "自然科学", "value": 35, "color": "tertiary-container"},
                {"name": "信息技术", "value": 40, "color": "secondary-fixed"}
            ],
            "recentTasks": [
                {
                    "id": "TASK-0001",
                    "name": "校园网络流量",
                    "source": "NOC 中心 API",
                    "frequency": "每 5 分钟",
                    "status": "success",
                    "statusText": "成功"
                },
                {
                    "id": "TASK-0002",
                    "name": "图书馆图书流通",
                    "source": "内部 SQL 服务器",
                    "frequency": "每日 00:00",
                    "status": "running",
                    "statusText": "运行中"
                },
                {
                    "id": "TASK-0003",
                    "name": "科研成果同步",
                    "source": "WCNU 科研门户",
                    "frequency": "实时钩子",
                    "status": "success",
                    "statusText": "成功"
                },
                {
                    "id": "TASK-0004",
                    "name": "智能能源使用",
                    "source": "IoT 网关 v2",
                    "frequency": "每 15 分钟",
                    "status": "running",
                    "statusText": "运行中"
                }
            ]
        }
    )
