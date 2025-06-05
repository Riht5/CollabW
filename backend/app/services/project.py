from sqlalchemy.orm import Session
from app.models.project import Project, ProjectProgress
from app.models.task import Task
from datetime import date

def update_project_progress(project_id: int, db: Session) -> float:
    """
    计算、更新并返回当天项目的进度。需要在每次项目状态变更时调用！
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ValueError("Project not found")
    
    # 计算项目进度
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    if not tasks:
        return 0.0
    total_weight = sum(task.workload.weight for task in tasks)
    completed_weight = sum(task.workload.weight for task in tasks if task.finished)
    progress = completed_weight / total_weight if total_weight > 0 else 0.0
    if progress == 0.0:
        project.status = "pending"
    elif progress < 1.0:
        project.status = "in_progress"
    else:
        project.status = "completed"
    today = date.today()
    
    # 检查今天是否已有进度记录
    existing_progress = db.query(ProjectProgress).filter(
        ProjectProgress.project_id == project_id,
        ProjectProgress.date == today
    ).first()
    
    if existing_progress:
        # 更新现有记录
        existing_progress.progress = progress
        db.commit()
        db.refresh(existing_progress)
        return existing_progress
    else:
        # 创建新记录
        progress_record = ProjectProgress(
            project_id=project_id,
            date=today,
            progress=progress
        )
        db.add(progress_record)
        db.commit()
        db.refresh(progress_record)
        return progress_record
