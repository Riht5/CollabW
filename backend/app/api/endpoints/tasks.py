from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate, Task as TaskSchema
from app.models.project import Project as ProjectModel
from app.models.task import Task as TaskModel
from app.models.user import User as UserModel
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=TaskSchema, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    创建新任务
    """
    # 验证项目是否存在
    project = db.query(ProjectModel).filter(ProjectModel.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 验证负责人是否存在（如果指定了）
    if task.head_id:
        head = db.query(UserModel).filter(UserModel.id == task.head_id).first()
        if not head:
            raise HTTPException(status_code=404, detail="Head user not found")
    
    db_task = TaskModel(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskSchema])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取任务列表
    """
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=TaskSchema)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    获取指定ID的任务详情
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    更新指定ID的任务
    """
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 验证更新数据的有效性
    update_data = task.model_dump(exclude_unset=True)
    if "project_id" in update_data:
        project = db.query(ProjectModel).filter(ProjectModel.id == update_data["project_id"]).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
    
    if "head_id" in update_data and update_data["head_id"]:
        head = db.query(UserModel).filter(UserModel.id == update_data["head_id"]).first()
        if not head:
            raise HTTPException(status_code=404, detail="Head user not found")
    
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", response_model=TaskSchema)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    删除指定ID的任务
    """
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 清除关联用户的 task_id
    users = db.query(UserModel).filter(UserModel.task_id == task_id).all()
    for user in users:
        user.task_id = None
    
    db.delete(db_task)
    db.commit()
    return db_task

@router.post("/{task_id}/assign")
def assign_users_to_task(
    task_id: int, 
    user_ids: List[int], 
    db: Session = Depends(get_db)
):
    """
    将用户分配到任务
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 验证用户是否存在
    users = db.query(UserModel).filter(UserModel.id.in_(user_ids)).all()
    if len(users) != len(user_ids):
        raise HTTPException(status_code=404, detail="Some users not found")
    
    # 分配用户到任务
    for user in users:
        user.task_id = task_id
    
    db.commit()
    return {"message": f"Successfully assigned {len(users)} users to task {task_id}"}

@router.delete("/{task_id}/unassign/{user_id}")
def unassign_user_from_task(
    task_id: int, 
    user_id: int, 
    db: Session = Depends(get_db)
):
    """
    从任务中移除用户
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    user = db.query(UserModel).filter(
        UserModel.id == user_id, 
        UserModel.task_id == task_id
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not assigned to this task")
    
    user.task_id = None
    db.commit()
    return {"message": f"Successfully unassigned user {user_id} from task {task_id}"}