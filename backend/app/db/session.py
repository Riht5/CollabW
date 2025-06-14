from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.core.config import settings

# 根据数据库类型配置引擎（SQLite 需特殊参数）
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.DATABASE_URL)

# 创建数据库会话工厂，每个请求独立 session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 依赖注入：获取数据库会话，用完自动关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()