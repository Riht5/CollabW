from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.task import TaskCreate, TaskUpdate, Task
from app.models.task import Task as TaskModel
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=Task, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    创建新任务
    """
    db_task = TaskModel(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取任务列表
    """
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    获取指定ID的任务详情
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    更新指定ID的任务
    """
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    删除指定ID的任务
    """
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task