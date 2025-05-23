from sqlalchemy import Column, Integer, Float, String, Enum, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..db.base import Base
import enum

class ProjectStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

project_dependencies = Table(
    "project_dependencies",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("depends_on_id", Integer, ForeignKey("projects.id"), primary_key=True)
)

class Project(Base):
    """
    项目表模型，描述项目的基本信息和与用户、任务、依赖的关系。
    """
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, doc="项目名称")
    description = Column(String, nullable=True, doc="项目描述")
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.pending, doc="项目状态")
    estimated_duration = Column(Integer, nullable=True, doc="预计时长（单位：小时）")
    start_time = Column(DateTime, nullable=True, doc="项目开始时间")
    end_time = Column(DateTime, nullable=True, doc="项目结束时间")
    head_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, doc="项目负责人ID")

    # 项目有多个成员（指定外键）
    users = relationship(
        "User",
        back_populates="project",
        foreign_keys='User.project_id'
    )

    # 项目有一个负责人（指定外键）
    head = relationship(
        "User",
        back_populates="headed_projects",
        foreign_keys=[head_id]
    )

    # 关系：项目下有多个任务，删除项目时级联删除任务
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    # 关系：项目依赖的其他项目
    dependencies = relationship(
        "Project",
        secondary=project_dependencies,
        primaryjoin=id == project_dependencies.c.project_id,
        secondaryjoin=id == project_dependencies.c.depends_on_id,
        backref="dependents"
    )

class ProjectProgress(Base):
    """
    项目进度表模型，记录项目的每日进度。
    """
    __tablename__ = 'project_progress'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), index=True)
    date = Column(Date, index=True)
    progress = Column(Float, nullable=False)
