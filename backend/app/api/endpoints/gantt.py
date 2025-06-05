from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import networkx as nx

from app.db.session import get_db
from app.models.project import Project as ProjectModel, ProjectStatus
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.gantt import GanttProject, CriticalPathResponse

router = APIRouter()

def get_dependency_end_time(project: ProjectModel, db: Session, visited=None) -> datetime:
    """获取项目依赖中最晚的结束时间，递归处理依赖"""
    if visited is None:
        visited = set()
    if project.id in visited:  # 防止循环依赖
        return datetime.strptime("2025-06-01", "%Y-%m-%d")
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

@router.get("/gantt-data", response_model=List[GanttProject])
def get_gantt_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(ProjectModel).all()
    gantt_data = []

    for project in projects:
        valid_dependencies = True
        dependencies = []

        if project.dependencies:
            for dep in project.dependencies:
                if dep.status.value != ProjectStatus.completed.value:
                    valid_dependencies = False
                if dep.progress_records:
                    latest_progress = sorted(dep.progress_records, key=lambda x: x.date, reverse=True)[0].progress
                else:
                    latest_progress = 0.0
                if latest_progress < 1.0:
                    valid_dependencies = False
                dependencies.append(dep.id)

        start_time = project.start_time
        if not start_time:
            start_time = get_dependency_end_time(project, db)
        
        end_time = project.end_time or (
            start_time + timedelta(days=(project.estimated_duration or 0))
        )

        if project.status.value == ProjectStatus.completed.value:
            progress = 100.0
        elif project.progress_records:
            progress = sorted(project.progress_records, key=lambda x: x.date, reverse=True)[0].progress * 100
        else:
            progress = 0.0

        gantt_data.append({
            "id": project.id,
            "name": project.name,
            "status": project.status.value,
            "start_time": start_time.strftime("%Y-%m-%d"),
            "end_time": end_time.strftime("%Y-%m-%d"),
            "progress": progress,
            "dependencies": dependencies
        })

    return gantt_data

@router.get("/critical-path", response_model=CriticalPathResponse)
def get_critical_path(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(ProjectModel).all()
    
    G = nx.DiGraph()
    G.add_node("start", duration=0)
    G.add_node("end", duration=0)
    weights = {}

    for project in projects:
        progress = 0.0
        if project.progress_records:
            progress = sorted(project.progress_records, key=lambda x: x.date, reverse=True)[0].progress
        elif project.status.value == ProjectStatus.completed.value:
            progress = 1.0
        
        duration_days = project.estimated_duration or 0
        weight = duration_days * (1 - progress)
        G.add_node(project.id, duration=weight)
        weights[project.id] = float(weight)
    
    for project in projects:
        for dep in project.dependencies:
            G.add_edge(dep.id, project.id)
    
    for project in projects:
        if G.in_degree(project.id) == 0 and project.id != "start":
            G.add_edge("start", project.id)
        if G.out_degree(project.id) == 0 and project.id != "end":
            G.add_edge(project.id, "end")
    
    try:
        critical_path = nx.dag_longest_path(G, weight="duration")
        total_duration = sum(G.nodes[node]["duration"] for node in critical_path)
        critical_path_ids = [node for node in critical_path if node not in ["start", "end"]]
        
        return CriticalPathResponse(
            critical_path=critical_path_ids,
            total_duration_days=total_duration,
            weights=weights
        )
    except nx.NetworkXUnfeasible:
        return CriticalPathResponse(
            critical_path=[],
            total_duration_days=0,
            weights=weights
        )