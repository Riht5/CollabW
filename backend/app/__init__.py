# FastAPI 应用初始化与路由注册

from fastapi import FastAPI

# 创建 FastAPI 应用实例，并添加元数据
app = FastAPI(
    title="CollabW",
    description="后端 API",
    version="0.1.0"
)

# 导入并注册 API 路由
from .api.router import router as api_router
app.include_router(api_router)