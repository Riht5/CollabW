from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
import enum

class UserRole(str, enum.Enum):
    director = "director"
    manager = "manager"
    user = "user"

class UserBase(BaseModel):
    """用户基础信息"""
    username: str
    email: str
    role: UserRole
    profile: Optional[str] = None
    outstanding: Optional[bool] = False
    task_id: Optional[int] = None

class UserCreate(BaseModel):
    """用户创建/注册请求体"""
    username: str
    email: str
    password: str
    confirm_password: str
    register_key: str
    profile: Optional[str] = None

class UserLogin(BaseModel):
    """用户登录请求体"""
    identifier: str  # 用户名或邮箱
    password: str

class UserUpdate(BaseModel):
    """用户信息更新请求体"""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: Optional[str] = None
    role: Optional[UserRole] = None
    profile: Optional[str] = None
    task_id: Optional[int] = None
    performance: Optional[float] = None
    outstanding: Optional[bool] = None

class PasswordChange(BaseModel):
    """密码更改请求体"""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)

class User(UserBase):
    """用户完整信息"""
    id: int
    hashed_password: str
    performance: Optional[float] = None
    
    model_config = {"from_attributes": True}

class UserList(BaseModel):
    """用户列表输出模型"""
    users: List[User]