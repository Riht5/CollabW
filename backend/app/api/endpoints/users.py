from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User as UserModel
from app.models.task import Task as TaskModel
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.core.security import hash_password
from app.services.user import create_user, calculate_all_users_performance

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=201)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """
    创建用户。
    """
    return create_user(user, db)

@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    获取指定ID的用户信息。
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取用户列表。
    """
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    更新用户信息
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True)
    
    # 验证任务是否存在（如果要分配任务）
    if "task_id" in update_data and update_data["task_id"]:
        task = db.query(TaskModel).filter(TaskModel.id == update_data["task_id"]).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
    # 如果更新密码，需要加密
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}/task", response_model=dict)
def get_user_task(user_id: int, db: Session = Depends(get_db)):
    """
    获取用户参与的任务
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.task_id:
        return {"task": None}
    
    task = db.query(TaskModel).filter(TaskModel.id == user.task_id).first()
    return {"task": task}

@router.get("/{user_id}/headed-task", response_model=dict)
def get_user_headed_task(user_id: int, db: Session = Depends(get_db)):
    """
    获取用户负责的任务
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    task = db.query(TaskModel).filter(TaskModel.head_id == user_id).first()
    return {"headed_task": task}

@router.post("/calculate-performance")
def calculate_all_users_performance_endpoint(db: Session = Depends(get_db)):
    """
    计算所有用户的绩效，并更新outstanding字段
    """
    try:
        calculate_all_users_performance(db)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate performance: {str(e)}"
        )

@router.get("/outstanding")
def get_outstanding_users(db: Session = Depends(get_db)):
    """
    获取优秀员工列表
    """
    try:
        outstanding_users = db.query(UserModel).filter(UserModel.outstanding == True).all()
        return outstanding_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))