from pydantic import BaseModel
from typing import List
from .project import ProjectProgress
from ..core.constants import RiskLevel


class BurnDownProjectBase(BaseModel):
    """燃尽图项目基础字段"""
    actual_progresses: List[ProjectProgress]
    ideal_progresses: List[ProjectProgress]
    risk_level: RiskLevel

class BurnDownProject(BurnDownProjectBase):
    """燃尽图项目输出模型"""
    model_config = {"from_attributes": True}