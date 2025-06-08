from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User as UserModel, UserRole
from app.schemas.user import UserCreate, UserLogin, User as UserSchema, UserUpdate, PasswordChange
from app.core.config import settings
from app.core.security import create_access_token, verify_password, get_password_hash
from app.api.dependencies import get_current_user
from app.services.user import create_user

router = APIRouter()

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录，返回访问令牌
    支持用户名或邮箱登录
    """
    db_user = db.query(UserModel).filter(
        (UserModel.username == user.identifier) | (UserModel.email == user.identifier)
    ).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册，支持简介、两次密码校验、key控制角色
    """
    # 密码一致性校验
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # 密码强度校验
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    # 注册密钥控制角色
    role_mapping = {
        settings.DIRECTOR_REGISTER_KEY: UserRole.director,
        settings.MANAGER_REGISTER_KEY: UserRole.manager,
        settings.USER_REGISTER_KEY: UserRole.user
    }
    
    role = role_mapping.get(user.register_key)
    if not role:
        raise HTTPException(status_code=400, detail="Invalid registration key")
    
    return create_user(user, db, role=role)

@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """
    获取当前登录用户信息
    """
    return current_user

@router.put("/update-profile", response_model=UserSchema)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    更新用户基本信息（用户名和邮箱）
    """
    # 检查用户名是否已被其他用户使用
    if user_update.username != current_user.username:
        existing_user = db.query(UserModel).filter(
            UserModel.username == user_update.username,
            UserModel.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # 检查邮箱是否已被其他用户使用
    if user_update.email != current_user.email:
        existing_user = db.query(UserModel).filter(
            UserModel.email == user_update.email,
            UserModel.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already taken")
    
    # 更新用户信息
    current_user.username = user_update.username
    current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.put("/change-password")
def change_password(
    password_change: PasswordChange,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    修改用户密码
    """
    # 验证当前密码
    if not verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # 密码强度校验
    if len(password_change.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters long")
    
    # 检查新密码是否与当前密码相同
    if verify_password(password_change.new_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="New password must be different from current password")
    
    # 更新密码
    current_user.hashed_password = get_password_hash(password_change.new_password)
    
    db.commit()
    
    return {"success": True, "message": "Password changed successfully"}