from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.db.session import get_db
from app.models.user import User
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    从JWT token中获取当前用户
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    验证当前用户是否为管理员
    """
    if current_user.role not in ["director", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def get_director_user(current_user: User = Depends(get_current_user)) -> User:
    """
    验证当前用户是否为总监
    """
    if current_user.role != "director":
        raise HTTPException(status_code=403, detail="Director permissions required")
    return current_user