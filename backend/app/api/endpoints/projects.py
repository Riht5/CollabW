from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List
from app.models.project import Project as ProjectModel, ProjectProgress as ProjectProgressModel
from app.models.task import Task as TaskModel
from app.models.user import User as UserModel
from app.schemas.project import ProjectCreate, Project, ProjectUpdate, ProjectProgress
from app.schemas.task import Task as TaskSchema
from app.schemas.user import User as UserSchema
from app.db.session import get_db
from app.services.project import update_project_progress
from sqlalchemy.orm import Session

# 创建路由
router = APIRouter()

@router.post("/", response_model=Project, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    创建新项目。
    """
    db_project = ProjectModel(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[Project])
def read_projects(db: Session = Depends(get_db)):
    """
    获取项目列表。
    """
    projects = db.query(ProjectModel).all()
    return projects

@router.get("/{project_id}", response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """
    获取指定ID的项目详情。
    """
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=Project)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    """
    更新指定ID的项目信息。
    - 参数: project_id（项目ID），project（更新数据），db（数据库会话）
    - 返回: 更新后的项目对象，若不存在则抛出404异常
    """
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    update_project_progress(project_id, db) # 更新项目进度
    return db_project

@router.delete("/{project_id}", response_model=Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """
    删除指定ID的项目。
    """
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return db_project

@router.post("/{project_id}/dependencies/", response_model=Project)
def add_dependencies(
    project_id: int,
    depends_on_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    为指定项目添加依赖关系。
    """
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    dependencies = db.query(ProjectModel).filter(ProjectModel.id.in_(depends_on_ids)).all()
    if len(dependencies) != len(depends_on_ids):
        raise HTTPException(status_code=404, detail="Some dependency projects not found")
    project.dependencies = dependencies
    db.commit()
    db.refresh(project)
    return project

@router.get("/{project_id}/progress/", response_model=List[ProjectProgress])
def read_all_project_progress(project_id: int, db: Session = Depends(get_db)):
    """
    获取指定项目ID的所有的进度记录（按日期升序返回）
    """
    progresses = (
        db
        .query(ProjectProgressModel)
        .filter(ProjectProgressModel.project_id == project_id)
        .order_by(ProjectProgressModel.date.asc())
        .all()
    )
    if not progresses:
        raise HTTPException(status_code=404, detail="No project progress found")

    return progresses
@router.get("/{project_id}/tasks", response_model=List[TaskSchema])
def get_project_tasks(project_id: int, db: Session = Depends(get_db)):
    """
    获取指定项目的所有任务
    """    
    # 验证项目是否存在
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 获取项目的所有任务
    tasks = db.query(TaskModel).filter(TaskModel.project_id == project_id).all()
    return tasks

@router.get("/{project_id}/members", response_model=List[UserSchema])
def get_project_members(project_id: int, db: Session = Depends(get_db)):
    """
    获取指定项目的所有成员
    """
    # 验证项目是否存在
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 通过任务获取项目成员
    task_ids = db.query(TaskModel.id).filter(TaskModel.project_id == project_id).subquery()
    members = db.query(UserModel).filter(UserModel.task_id.in_(task_ids)).distinct().all()
    
    return members
