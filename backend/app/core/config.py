from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    项目全局配置类，自动从 backend/.env 文件和环境变量加载配置。
    """

    # 应用信息
    APP_NAME: str = "CollabW"
    APP_VERSION: str = "0.1.0"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./db/database.db"  # 指向 backend/db/database.db

    # 安全配置
    SECRET_KEY: str  # 在 .env 中设置
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = "./.env"  # 指向 backend/.env
        env_file_encoding = "utf-8"

settings = Settings()