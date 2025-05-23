from pydantic import BaseModel
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
    role: UserRole = UserRole.user
    profile: Optional[str] = None
    project_id: Optional[int] = None

class UserCreate(BaseModel):
    """用户注册请求体"""
    username: str
    email: str
    password: str
    confirm_password: str
    profile: Optional[str] = None
    register_key: str

class UserOut(BaseModel):
    """用于输出的用户信息（不包含敏感字段）"""
    id: int
    username: str
    email: str
    role: UserRole
    profile: Optional[str] = None
    project_id: Optional[int] = None

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    """用户登录请求体"""
    username: str
    password: str

class UserUpdate(BaseModel):
    """用户信息更新请求体，所有字段可选"""
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    profile: Optional[str] = None
    project_id: Optional[int] = None

class User(BaseModel):
    """用户模型"""
    id: int
    username: str
    email: str
    role: UserRole
    profile: Optional[str] = None
    project_id: Optional[int] = None

    model_config = {"from_attributes": True}

class UserList(BaseModel):
    """用户列表输出模型"""
    users: List[User]