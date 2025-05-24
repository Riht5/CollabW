from sqlalchemy import Column, Integer, Float, String, Boolean, Enum, ForeignKey
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
    performance = Column(Float, nullable=True, doc="用户绩效评分")
    outstanding = Column(Boolean, nullable=True, default=False, doc="是否为优秀员工")
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True, index=True, doc="参与的任务ID")

    # 用户参与的任务
    task = relationship(
        "Task",
        back_populates="users",
        foreign_keys=[task_id]
    )

    # 用户作为负责人的任务
    headed_task = relationship(
        "Task",
        back_populates="head",
        foreign_keys="Task.head_id"
    )