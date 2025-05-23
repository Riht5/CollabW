from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.core.config import settings
from app.core.security import create_access_token, verify_password, hash_password
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录，返回访问令牌
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册，支持简介、两次密码校验、key控制角色
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    # 密码一致性校验
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    # 注册密钥控制角色
    if user.register_key == settings.DIRECTOR_REGISTER_KEY:
        role = UserRole.director
    elif user.register_key == settings.MANAGER_REGISTER_KEY:
        role = UserRole.manager
    elif user.register_key == settings.USER_REGISTER_KEY:
        role = UserRole.user
    else:
        raise HTTPException(status_code=400, detail="Invalid registration key")
    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role=role,
        profile=user.profile
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户信息
    """
    return current_user