from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router

# 创建 FastAPI 应用实例，添加元数据
app = FastAPI(
    title="CollabW",
    description="后端 API",
    version="0.1.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:5173", 
        "http://127.0.0.1:5173"
    ],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

# 注册所有 API 路由
app.include_router(router, prefix="/api", tags=["api"])

@app.get("/")
def read_root():
    """根路径欢迎信息"""
    return {"message": "Welcome to CollabW API"}