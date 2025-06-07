from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.project import Project as ProjectModel

def get_dependency_end_time(project: ProjectModel, db: Session, current_path=None) -> datetime:
    """
    获取项目依赖中最晚的结束时间，递归处理依赖，精确检测循环依赖。
    
    Args:
        project: 项目对象
        db: 数据库会话
        current_path: 当前递归路径的已访问项目 ID 集合
    
    Returns:
        项目或其依赖的最晚结束时间
    
    Raises:
        ValueError: 检测到循环依赖
    """
    if current_path is None:
        current_path = set()
    
    # 检测当前路径中的循环依赖
    if project.id in current_path:
        raise ValueError(f"Circular dependency detected for project {project.id}")
    
    # 添加当前项目到路径
    current_path.add(project.id)
    
    # 无依赖时，返回项目本身的结束时间
    if not project.dependencies:
        end_time = project.end_time or (
            project.start_time + timedelta(days=(project.estimated_duration or 0))
            if project.start_time
            else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # 使用当前日期，时间归零
        )
        current_path.remove(project.id)  # 回溯
        return end_time
    
    # 遍历依赖（InstrumentedList，包含 Project 对象）
    end_times = []
    for dep in project.dependencies:
        if not dep:
            continue
        # 递归获取依赖的结束时间
        dep_end_time = get_dependency_end_time(dep, db, current_path.copy())
        end_times.append(dep_end_time)
    
    # 回溯，移除当前项目
    current_path.remove(project.id)
    
    # 返回依赖中最晚的结束时间，或项目本身结束时间
    result = max(end_times) if end_times else (
        project.end_time or (
            project.start_time + timedelta(days=(project.estimated_duration or 0))
            if project.start_time
            else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # 使用当前日期，时间归零
        )
    )
    return result