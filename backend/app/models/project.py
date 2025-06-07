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
    项目表模型，描述项目的基本信息和与任务、依赖的关系。
    """
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, doc="项目名称")
    description = Column(String, nullable=True, doc="项目描述")
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.pending, doc="项目状态")
    estimated_duration = Column(Integer, nullable=True, doc="预计时长（单位：小时）")
    start_time = Column(DateTime, nullable=True, doc="项目开始时间")
    end_time = Column(DateTime, nullable=True, doc="项目结束时间")

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

    @property
    def progress(self):
        """获取项目进度"""
        if self.progress_records:
            latest_record = max(self.progress_records, key=lambda x: x.date)
            return latest_record.progress
        return 0.0

class ProjectProgress(Base):
    """
    项目进度表模型，记录项目的每日进度。
    """
    __tablename__ = 'project_progress'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False, index=True, doc="所属项目ID")
    date = Column(Date, nullable=False, index=True, doc="日期")
    progress = Column(Float, nullable=False, doc="完成进度（0-1之间）")
    
    # 关系：进度记录属于某个项目
    project = relationship("Project", backref="progress_records")

