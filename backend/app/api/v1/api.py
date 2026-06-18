from fastapi import APIRouter
from app.api.v1.endpoints import admin, dashboard, user, user_dashboard, staff, model_config, skill, chat, crawler, audit, ai_inquiry, bigscreen

api_router = APIRouter()
api_router.include_router(admin.router, prefix="/admin", tags=["管理员管理"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["仪表盘"])
api_router.include_router(user.router, prefix="/user", tags=["用户管理"])
api_router.include_router(user_dashboard.router, prefix="/user", tags=["用户仪表盘"])
api_router.include_router(staff.router, prefix="/staff", tags=["数字员工管理"])
api_router.include_router(model_config.router, prefix="/model", tags=["模型管理"])
api_router.include_router(skill.router, prefix="/skill", tags=["技能管理"])
api_router.include_router(chat.router, prefix="/chat", tags=["聊天管理"])
api_router.include_router(crawler.router, prefix="/crawler", tags=["数据采集"])
api_router.include_router(audit.router, prefix="/audit", tags=["内容审核"])
api_router.include_router(ai_inquiry.router, prefix="/ai", tags=["AI 问讯"])
api_router.include_router(bigscreen.router, prefix="/bigscreen", tags=["大屏监控"])
