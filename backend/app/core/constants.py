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
    USER_NOT_FOUND = "用户不存在"
    PROJECT_NOT_FOUND = "项目不存在"
    TASK_NOT_FOUND = "任务不存在"
    UNAUTHORIZED = "未授权访问"
    FORBIDDEN = "权限不足"
    USERNAME_EXISTS = "用户名已被注册"
    EMAIL_EXISTS = "邮箱已被注册"
    INVALID_CREDENTIALS = "用户名或密码错误"
    PASSWORDS_NOT_MATCH = "两次输入的密码不一致"
    PASSWORD_TOO_SHORT = "密码需要至少8位"
    INVALID_REGISTER_KEY = "注册密钥无效"
    CURRENT_PASSWORD_INCORRECT = "当前密码不正确"
    NEW_PASSWORD_TOO_SHORT = "新密码需要至少8位"
    NEW_PASSWORD_SAME_AS_CURRENT = "新密码不能与当前密码相同"
    INVALID_TOKEN_PAYLOAD = "无效的令牌数据"
    COULD_NOT_VALIDATE_CREDENTIALS = "无法验证身份凭证"

# 成功信息常量
class SuccessMessage:
    USER_CREATED = "用户创建成功"
    PROJECT_CREATED = "项目创建成功"
    TASK_CREATED = "任务创建成功"
    UPDATED_SUCCESSFULLY = "更新成功"
    DELETED_SUCCESSFULLY = "删除成功"
    PASSWORD_CHANGED_SUCCESSFULLY = "密码修改成功"
