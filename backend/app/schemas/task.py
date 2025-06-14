from pydantic import BaseModel
from typing import Optional, List
from ..core.constants import TaskWorkload

class TaskBase(BaseModel):
    """任务基础字段"""
    name: str
    description: Optional[str] = None
    workload: TaskWorkload = TaskWorkload.light
    finished: bool = False
    project_id: int
    head_id: Optional[int] = None

class TaskCreate(TaskBase):
    """创建任务请求体"""
    pass

class TaskUpdate(BaseModel):
    """更新任务请求体，所有字段可选"""
    name: Optional[str] = None
    description: Optional[str] = None
    workload: Optional[TaskWorkload] = None
    finished: Optional[bool] = None
    project_id: Optional[int] = None
    head_id: Optional[int] = None

class Task(TaskBase):
    """任务输出模型"""
    id: int

    model_config = {"from_attributes": True}

class TaskList(BaseModel):
    """任务列表输出模型"""
    tasks: List[Task]