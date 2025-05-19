from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base import Base
import enum

class UserRole(enum.Enum):
    director = "director"
    manager = "manager"
    user = "user"

class User(Base):
    """
    用户表模型，描述用户的基本信息。
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False, doc="用户名")
    hashed_password = Column(String(200), nullable=False, doc="加密后的密码")
    email = Column(String(100), unique=True, index=True, nullable=False, doc="邮箱")
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user, doc="用户角色")
    profile = Column(String, nullable=True, doc="用户简介")
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True, index=True, doc="所属项目ID")

    # 关系：用户属于一个项目
    project = relationship("Project", back_populates="users")

    # 关系：用户作为负责人负责的项目（反向）
    headed_projects = relationship("Project", back_populates="head", foreign_keys='Project.head_id')

    # 关系：用户作为负责人负责的任务（反向）
    headed_tasks = relationship("Task", back_populates="head", foreign_keys='Task.head_id')