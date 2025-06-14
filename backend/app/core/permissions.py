# 权限检查装饰器和函数
from functools import wraps
from typing import List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.constants import UserRole, StatusCode, ErrorMessage
from app.models.user import User as UserModel
from app.api.dependencies import get_current_user

class PermissionChecker:
    """权限检查类"""
    
    @staticmethod
    def check_role(required_roles: List[UserRole], current_user: UserModel) -> bool:
        """检查用户角色"""
        return current_user.role in required_roles
    
    @staticmethod
    def require_roles(required_roles: List[UserRole]):
        """要求特定角色的装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 从kwargs中获取current_user
                current_user = kwargs.get('current_user')
                if not current_user:
                    raise HTTPException(
                        status_code=StatusCode.UNAUTHORIZED,
                        detail=ErrorMessage.UNAUTHORIZED
                    )
                
                if not PermissionChecker.check_role(required_roles, current_user):
                    raise HTTPException(
                        status_code=StatusCode.FORBIDDEN,
                        detail=ErrorMessage.FORBIDDEN
                    )
                
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def require_director():
        """要求总监权限"""
        return PermissionChecker.require_roles([UserRole.director])
    
    @staticmethod
    def require_manager_or_director():
        """要求经理或总监权限"""
        return PermissionChecker.require_roles([UserRole.manager, UserRole.director])
    
    @staticmethod
    def require_any_role():
        """要求任意角色（已登录）"""
        return PermissionChecker.require_roles([UserRole.user, UserRole.manager, UserRole.director])

# 权限依赖项
def get_director_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """获取总监用户"""
    if current_user.role != UserRole.director:
        raise HTTPException(
            status_code=StatusCode.FORBIDDEN,
            detail=ErrorMessage.FORBIDDEN
        )
    return current_user

def get_manager_or_director_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """获取经理或总监用户"""
    if current_user.role not in [UserRole.manager, UserRole.director]:
        raise HTTPException(
            status_code=StatusCode.FORBIDDEN,
            detail=ErrorMessage.FORBIDDEN
        )
    return current_user
