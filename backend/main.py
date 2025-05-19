from fastapi import FastAPI
from app.api.router import router

# 创建 FastAPI 应用实例，添加元数据
app = FastAPI(
    title="CollabW",
    description="后端 API",
    version="0.1.0"
)

# 注册所有 API 路由
app.include_router(router)

@app.get("/")
def read_root():
    """根路径欢迎信息"""
    return {"message": "Welcome to CollabW API"}