from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base import Base
import enum

class TaskWorkload(enum.Enum):
    light = "light"
    medium = "medium"
    heavy = "heavy"
    
    @property
    def weight(self):
        """返回任务工作量对应的权重值"""
        weights = {
            TaskWorkload.light: 1,
            TaskWorkload.medium: 2,
            TaskWorkload.heavy: 3
        }
        return weights[self]

class Task(Base):
    """
    任务表模型，描述任务的基本信息和与项目的关系。
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, doc="任务名称")
    description = Column(String, nullable=True, doc="任务描述")
    workload = Column(Enum(TaskWorkload), nullable=False, default=TaskWorkload.light, doc="任务工作量")
    finished = Column(Boolean, nullable=False, default=False, doc="任务是否完成")
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False, index=True, doc="所属项目ID")
    head_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True, doc="任务负责人ID")

    # 任务属于一个项目
    project = relationship("Project", back_populates="tasks")

    # 任务的所有成员
    users = relationship(
        "User",
        back_populates="task",
        foreign_keys="User.task_id"
    )

    # 任务负责人
    head = relationship(
        "User",
        back_populates="headed_task",
        foreign_keys=[head_id]
    )