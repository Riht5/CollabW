from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class ProjectBase(BaseModel):
    """项目基础字段"""
    name: str
    description: Optional[str] = None
    status: Optional[str] = None
    estimated_duration: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    head_id: int = None

class ProjectCreate(ProjectBase):
    """创建项目请求体"""
    pass

class ProjectUpdate(BaseModel):
    """更新项目请求体，所有字段可选"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    estimated_duration: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    head_id: Optional[int] = None

class Project(ProjectBase):
    """项目输出模型"""
    id: int

    model_config = {"from_attributes": True}

class ProjectList(BaseModel):
    """项目列表输出模型"""
    projects: List[Project]

class ProjectProgress(BaseModel):
    """项目进度输出模型"""
    date: date
    progress: float

    model_config = {"from_attributes": True}