import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.db.base import engine, Base
from app.api.v1.api import api_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# 挂载聊天文件上传目录为静态资源
uploads_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
if os.path.isdir(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


@app.get("/", tags=["健康检查"])
def root():
    return {"code": 200, "message": f"{settings.PROJECT_NAME} 服务运行中", "version": settings.VERSION}


@app.get("/health", tags=["健康检查"])
def health():
    return {"status": "ok"}
