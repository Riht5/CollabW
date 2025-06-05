from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
import enum
from .task import Task

class ProjectStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class ProjectBase(BaseModel):
    """项目基础字段"""
    name: str
    description: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.pending
    estimated_duration: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    """创建项目请求体"""
    pass

class ProjectUpdate(BaseModel):
    """更新项目请求体，所有字段可选"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    estimated_duration: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class Project(ProjectBase):
    """项目输出模型"""
    id: int
    progress: Optional[float] = None
    tasks: Optional[List[Task]] = []
    progress: Optional[float] = None

    model_config = {"from_attributes": True}

class ProjectList(BaseModel):
    """项目列表输出模型"""
    projects: List[Project]

class ProjectProgress(BaseModel):
    """项目进度输出模型"""
    id: Optional[int] = None
    project_id: int
    date: date
    progress: float

    model_config = {"from_attributes": True}