from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base import Base
import enum

class TaskPriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    """
    任务表模型，描述任务的基本信息和与项目的关系。
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, doc="任务名称")
    description = Column(String, nullable=True, doc="任务描述")
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.low, doc="任务优先级")
    status = Column(Boolean, nullable=False, default=False, doc="任务状态")
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False, index=True, doc="所属项目ID")
    head_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True, doc="任务负责人ID")

    # 关系：任务属于一个项目
    project = relationship("Project", back_populates="tasks")

    # 关系：任务有一个负责人
    head = relationship("User", back_populates="headed_tasks", foreign_keys=[head_id])