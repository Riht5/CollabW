from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserLogin, User as UserSchema, UserUpdate, PasswordChange
from app.core.config import settings
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.constants import UserRole, StatusCode, ErrorMessage, SuccessMessage
from app.core.utils import create_error_response
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
        raise HTTPException(status_code=400, detail=ErrorMessage.INVALID_CREDENTIALS)
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册，支持简介、两次密码校验、key控制角色
    """
    # 密码一致性校验
    if user.password != user.confirm_password:
        raise create_error_response(StatusCode.BAD_REQUEST, ErrorMessage.PASSWORDS_NOT_MATCH)
    
    # 密码强度校验
    if len(user.password) < 8:
        raise create_error_response(StatusCode.BAD_REQUEST, ErrorMessage.PASSWORD_TOO_SHORT)
    
    # 注册密钥控制角色
    role_mapping = {
        settings.DIRECTOR_REGISTER_KEY: UserRole.director,
        settings.MANAGER_REGISTER_KEY: UserRole.manager,
        settings.USER_REGISTER_KEY: UserRole.user
    }
    
    role = role_mapping.get(user.register_key)
    if not role:
        raise create_error_response(StatusCode.BAD_REQUEST, ErrorMessage.INVALID_REGISTER_KEY)
    
    return create_user(user, db, role=role)

@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """
    获取当前登录用户信息
    """
    return current_user

@router.put("/update-profile")
def update_profile(
    user_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新用户资料
    """
    try:
        # 检查用户名是否已被其他用户使用
        if user_data.username and user_data.username != current_user.username:
            existing_user = db.query(UserModel).filter(
                UserModel.username == user_data.username,
                UserModel.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail=ErrorMessage.USERNAME_EXISTS
                )

        # 检查邮箱是否已被其他用户使用
        if user_data.email and user_data.email != current_user.email:
            existing_user = db.query(UserModel).filter(
                UserModel.email == user_data.email,
                UserModel.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail=ErrorMessage.EMAIL_EXISTS
                )

        # 更新用户信息
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(current_user, key):
                setattr(current_user, key, value)

        db.commit()
        db.refresh(current_user)

        return {
            "success": True,
            "message": "Profile updated successfully",
            "user": current_user
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update profile: {str(e)}"
        )

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
        raise HTTPException(status_code=400, detail=ErrorMessage.CURRENT_PASSWORD_INCORRECT)
    
    # 密码强度校验
    if len(password_change.new_password) < 6:
        raise HTTPException(status_code=400, detail=ErrorMessage.NEW_PASSWORD_TOO_SHORT)
    
    # 检查新密码是否与当前密码相同
    if verify_password(password_change.new_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail=ErrorMessage.NEW_PASSWORD_SAME_AS_CURRENT)
    
    # 更新密码
    current_user.hashed_password = get_password_hash(password_change.new_password)
    
    db.commit()
    
    return {"success": True, "message": SuccessMessage.PASSWORD_CHANGED_SUCCESSFULLY}