from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.project import Project as ProjectModel

def get_dependency_end_time(project: ProjectModel, db: Session, visited=None) -> datetime:
    """
    获取项目依赖中最晚的结束时间，递归处理依赖。
    """
    if visited is None:
        visited = set()
    if project.id in visited:
        raise ValueError(f"Circular dependency detected for project {project.id}")
    visited.add(project.id)

    if not project.dependencies:
        return project.end_time or (
            project.start_time + timedelta(days=(project.estimated_duration or 0))
            if project.start_time
            else datetime.strptime("2025-06-01", "%Y-%m-%d")
        )

    end_times = []
    for dep in project.dependencies:
        dep_end_time = dep.end_time
        if not dep_end_time:
            # 递归计算依赖的 start_time 和 end_time
            dep_start_time = get_dependency_end_time(dep, db, visited)
            dep_end_time = dep_start_time + timedelta(days=(dep.estimated_duration or 0))
        end_times.append(dep_end_time)
    
    visited.remove(project.id)
    return max(end_times) if end_times else datetime.strptime("2025-06-01", "%Y-%m-%d")