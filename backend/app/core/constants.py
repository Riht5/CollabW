# 应用常量定义
from enum import Enum

class UserRole(str, Enum):
    """用户角色枚举"""
    director = "director"
    manager = "manager"
    user = "user"

class ProjectStatus(str, Enum):
    """项目状态枚举"""
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskWorkload(str, Enum):
    """任务工作量枚举"""
    light = "light"
    medium = "medium"
    heavy = "heavy"
    
    @property
    def weight(self) -> int:
        """获取工作量权重"""
        weights = {
            TaskWorkload.light: 1,
            TaskWorkload.medium: 2,
            TaskWorkload.heavy: 3
        }
        return weights[self]

class RiskLevel(str, Enum):
    """风险等级枚举"""
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

# HTTP状态码常量
class StatusCode:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

# 错误信息常量
class ErrorMessage:
    USER_NOT_FOUND = "User not found"
    PROJECT_NOT_FOUND = "Project not found"
    TASK_NOT_FOUND = "Task not found"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    USERNAME_EXISTS = "Username already registered"
    EMAIL_EXISTS = "Email already registered"
    INVALID_CREDENTIALS = "Invalid credentials"
    PASSWORDS_NOT_MATCH = "Passwords do not match"
    PASSWORD_TOO_SHORT = "Password must be at least 8 characters long"
    INVALID_REGISTER_KEY = "Invalid registration key"

# 成功信息常量
class SuccessMessage:
    USER_CREATED = "User created successfully"
    PROJECT_CREATED = "Project created successfully"
    TASK_CREATED = "Task created successfully"
    UPDATED_SUCCESSFULLY = "Updated successfully"
    DELETED_SUCCESSFULLY = "Deleted successfully"
