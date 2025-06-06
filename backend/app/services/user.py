from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User as UserModel
from app.models.task import Task as TaskModel
from app.models.project import Project as ProjectModel
from app.schemas.user import UserCreate, User as UserSchema
from app.core.security import hash_password

def create_user(user: UserCreate, db: Session, role=None) -> UserSchema:
    """
    创建用户业务逻辑
    """
    # 检查用户名是否已存在
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already registered"
        )
    
    # 检查邮箱是否已存在
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    try:
        hashed_pw = hash_password(user.password)
        new_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pw,
            role=role,  # 使用传入的role参数
            profile=user.profile or "",  # 提供默认值
            task_id=None  # 新用户默认没有任务
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

def calculate_user_performance(user_id: int, db: Session) -> float:
    """
    计算用户绩效
    """
    # 获取用户参与的所有任务
    user_tasks = db.query(TaskModel).join(UserModel, TaskModel.id == UserModel.task_id)\
                   .filter(UserModel.id == user_id).all()
    
    if not user_tasks:
        return 0.0
    
    total_performance = 0.0
    
    for task in user_tasks:
        # 获取项目信息
        project = db.query(ProjectModel).filter(ProjectModel.id == task.project_id).first()
        if not project:
            continue
        
        # 第一次加权：根据任务工作量
        workload_score = task.workload.weight
        
        # 计算参与该任务的人数
        task_participants = db.query(UserModel).filter(UserModel.task_id == task.id).count()
        
        # 按人数平分
        user_task_score = workload_score / task_participants
        
        # 如果是任务负责人，乘以120%
        if task.head_id == user_id:
            user_task_score *= 1.2
        
        # 第二次加权：根据所属项目预期工期
        if project.estimated_duration:
            duration_weight = project.estimated_duration
        else:
            duration_weight = 1  # 默认权重
        
        final_task_score = user_task_score * duration_weight
        total_performance += final_task_score
    
    return total_performance

def calculate_all_users_performance(db: Session) -> None:
    """
    计算所有用户的绩效，并更新outstanding字段
    """
    # 获取所有用户
    all_users = db.query(UserModel).all()
    user_performances = []
    
    # 计算每个用户的performance
    for user in all_users:
        if user.role == "user":
            performance = calculate_user_performance(user.id, db)
            user.performance = performance
            user_performances.append((user.id, performance))
    
    # 按performance降序排序
    user_performances.sort(key=lambda x: x[1], reverse=True)
    
    # 计算前20%的用户数量
    total_users = len(user_performances)
    top_20_percent_count = max(1, int(total_users * 0.2))
    
    # 重置所有用户的outstanding状态
    db.query(UserModel).update({"outstanding": False})
    
    # 设置前20%用户为优秀员工
    if user_performances:
        top_user_ids = [user_performances[i][0] for i in range(min(top_20_percent_count, len(user_performances)))]
        db.query(UserModel).filter(UserModel.id.in_(top_user_ids)).update({"outstanding": True})