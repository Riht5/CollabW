# 通用工具函数
from typing import Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.constants import StatusCode, ErrorMessage

def create_error_response(status_code: int, detail: str) -> HTTPException:
    """创建标准错误响应"""
    return HTTPException(status_code=status_code, detail=detail)

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> None:
    """验证必填字段"""
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise create_error_response(
            StatusCode.BAD_REQUEST, 
            f"Missing required fields: {', '.join(missing_fields)}"
        )

def get_or_404(db: Session, model, **kwargs):
    """获取对象，不存在则返回404"""
    obj = db.query(model).filter_by(**kwargs).first()
    if not obj:
        model_name = model.__name__.lower()
        raise create_error_response(
            StatusCode.NOT_FOUND, 
            f"{model_name.capitalize()} not found"
        )
    return obj

def paginate_query(query, page: int = 1, per_page: int = 20):
    """分页查询"""
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def safe_commit(db: Session, operation_name: str = "operation"):
    """安全提交数据库事务"""
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise create_error_response(
            StatusCode.INTERNAL_SERVER_ERROR,
            f"Failed to {operation_name}: {str(e)}"
        )
