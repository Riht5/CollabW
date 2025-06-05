from pydantic import BaseModel
from typing import List, Dict

class GanttProjectBase(BaseModel):
    """甘特图项目基础字段"""
    id: int
    name: str
    status: str
    start_time: str
    end_time: str
    progress: float
    dependencies: List[int]

class GanttProject(GanttProjectBase):
    """甘特图项目输出模型"""
    model_config = {"from_attributes": True}

class CriticalPathResponse(BaseModel):
    """关键路径响应模型"""
    critical_path: List[int]
    total_duration_days: float
    weights: Dict[int, float]

    model_config = {"from_attributes": True}