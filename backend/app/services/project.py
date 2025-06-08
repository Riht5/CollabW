from sqlalchemy.orm import Session
from app.models.project import Project as ProjectModel, ProjectProgress as ProjectProgressModel
from app.models.task import Task as TaskModel
from app.schemas.project import ProjectProgress
from app.schemas.burndown import RiskLevel
from datetime import date
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException

PROGRESS_DEVIATION_THRESHOLDS = {
    RiskLevel.LOW: 0.05,      # 5%
    RiskLevel.MEDIUM: 0.10,   # 10%
    RiskLevel.HIGH: 0.20,     # 20%
    RiskLevel.CRITICAL: 0.30, # 30%
}

EFFICIENCY_THRESHOLDS = {
    RiskLevel.LOW: 0.90,      # 90%
    RiskLevel.MEDIUM: 0.80,   # 80%
    RiskLevel.HIGH: 0.70,     # 70%
    RiskLevel.CRITICAL: 0.60, # 60%
}


def update_project_progress(project_id: int, db: Session) -> float:
    """
    计算、更新并返回当天项目的进度。需要在每次项目状态变更时调用！
    """
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise ValueError("Project not found")
    
    # 计算项目进度
    tasks = db.query(TaskModel).filter(TaskModel.project_id == project_id).all()
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
    existing_progress = db.query(ProjectProgressModel).filter(
        ProjectProgressModel.project_id == project_id,
        ProjectProgressModel.date == today
    ).first()
    
    if existing_progress:
        # 更新现有记录
        existing_progress.progress = progress
        db.commit()
        db.refresh(existing_progress)
        return existing_progress
    else:
        # 创建新记录
        progress_record = ProjectProgressModel(
            project_id=project_id,
            date=today,
            progress=progress
        )
        db.add(progress_record)
        db.commit()
        db.refresh(progress_record)
        return progress_record



def get_filled_project_progress(project_id: int, db: Session) -> List[ProjectProgress]:
    """
    查询项目的进度并对没有记录的日期填充进度
    """
    progresses = (
        db.query(ProjectProgressModel)
        .filter(ProjectProgressModel.project_id == project_id)
        .order_by(ProjectProgressModel.date.asc())
        .all()
    )

    if not progresses:
        return []

    # 获取最早和最晚的日期
    start_date = progresses[0].date
    end_date = datetime.today().date()

    # 填充缺失的日期
    filled_progresses = []
    last_progress = None

    # 遍历从start_date到今天的的每一天
    for day in range((end_date - start_date).days + 1):
        current_date = start_date + timedelta(days=day)

        # 找到该日期的进度数据
        progress_for_day = next((p for p in progresses if p.date == current_date), None)

        if progress_for_day:
            filled_progresses.append(progress_for_day)
            last_progress = progress_for_day
            # 任务结束则停止填充
            if progress_for_day.progress >= 1.0:
                break
        elif last_progress:
            # 如果没有当天的进度数据，使用最近一次的进度数据，并将日期更新为当前日期
            filled_progress = ProjectProgressModel(
                project_id=last_progress.project_id,
                date=current_date,
                progress=last_progress.progress
            )
            filled_progresses.append(filled_progress)
    return filled_progresses

def get_ideal_project_progress(project_id: int, db: Session) -> List[ProjectProgress]:
    """
    计算项目的每日理想进度
    """
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.start_time == None or project.estimated_duration == None:
        return []

    # 计算理想进度
    ideal_progresses = []
    # 理想进度的日期范围：从项目的 start_time 开始，持续 estimated_duration 天
    current_date = project.start_time
    for day in range(project.estimated_duration):
        progress = round(day / (project.estimated_duration - 1), 2)  # 计算当天的理想进度
        ideal_progresses.append(
            ProjectProgress(
                project_id=project_id,
                date=current_date,
                progress=progress
            )
        )
        # 增加一天
        current_date += timedelta(days=1)
    return ideal_progresses

def get_current_ideal(ideal_progresses: List[ProjectProgress], latest_progress: ProjectProgress) -> ProjectProgress:
    """
    找到最新日期对应或之前最近的理想进度
    """
    current_ideal: Optional[ProjectProgress] = None
    for prog in ideal_progresses:
        if prog.date <= latest_progress.date:
            current_ideal = prog
        else:
            break
    if current_ideal is None:
        current_ideal = ideal_progresses[0]
    return current_ideal

def analyse_warning_level(actual_progresses: List[ProjectProgress], ideal_progresses: List[ProjectProgress]) -> RiskLevel:
    """
    根据进度偏差和效率风险计算项目的预警等级
    """
    if not actual_progresses or not ideal_progresses:
        return RiskLevel.NONE

    # 按日期升序
    actual = sorted(actual_progresses, key=lambda p: p.date)
    ideal  = sorted(ideal_progresses,  key=lambda p: p.date)

    latest = actual[-1]


    current_ideal = get_current_ideal(ideal, latest)
    # 计算进度偏差
    deviation = current_ideal.progress - latest.progress

    # 计算平均每日实际进度
    days = (actual[-1].date - actual[0].date).days or 1
    total_done = actual[-1].progress - actual[0].progress
    avg_daily = total_done / days
    remaining = 1.0 - latest.progress
    # 剩余天数：从明天到理想最后一天
    remaining_days = (ideal[-1].date - latest.date).days
    remaining_days = max(remaining_days, 1)
    required_daily = remaining / remaining_days
    efficiency_ratio = avg_daily / (required_daily or 1e-6)

    # 根据阈值评估偏差风险和效率风险
    def eval_deviation_level(dev: float) -> RiskLevel:
        for level in [RiskLevel.CRITICAL, RiskLevel.HIGH, RiskLevel.MEDIUM, RiskLevel.LOW]:
            if dev > PROGRESS_DEVIATION_THRESHOLDS[level]:
                return level
        return RiskLevel.NONE

    def eval_efficiency_level(ratio: float) -> RiskLevel:
        for level in [RiskLevel.CRITICAL, RiskLevel.HIGH, RiskLevel.MEDIUM, RiskLevel.LOW]:
            if ratio < EFFICIENCY_THRESHOLDS[level]:
                return level
        return RiskLevel.NONE

    dev_level = eval_deviation_level(deviation)
    eff_level = eval_efficiency_level(efficiency_ratio)

    # 取更高（更严重）的等级
    order = [RiskLevel.NONE, RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
    return dev_level if order.index(dev_level) > order.index(eff_level) else eff_level