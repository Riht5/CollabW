// 前端应用常量定义

// 用户角色枚举
export enum UserRole {
  DIRECTOR = 'director',
  MANAGER = 'manager',
  USER = 'user'
}

// 项目状态枚举
export enum ProjectStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed'
}

// 任务工作量枚举
export enum TaskWorkload {
  LIGHT = 'light',
  MEDIUM = 'medium',
  HEAVY = 'heavy'
}

// 风险等级枚举
export enum RiskLevel {
  NONE = "NONE",
  LOW = "LOW",
  MEDIUM = "MEDIUM",
  HIGH = "HIGH",
  CRITICAL = "CRITICAL"
}

// 状态文本映射
export const STATUS_TEXT_MAP = {
  [ProjectStatus.PENDING]: '待开始',
  [ProjectStatus.IN_PROGRESS]: '进行中',
  [ProjectStatus.COMPLETED]: '已完成'
} as const;

// 角色文本映射
export const ROLE_TEXT_MAP = {
  [UserRole.DIRECTOR]: '总监',
  [UserRole.MANAGER]: '经理',
  [UserRole.USER]: '员工'
} as const;

// 工作量文本映射
export const WORKLOAD_TEXT_MAP = {
  [TaskWorkload.LIGHT]: '轻量',
  [TaskWorkload.MEDIUM]: '中等',
  [TaskWorkload.HEAVY]: '繁重'
} as const;

// 风险等级文本映射
export const RISK_LEVEL_TEXT_MAP = {
  [RiskLevel.NONE]: '无风险',
  [RiskLevel.LOW]: '低风险',
  [RiskLevel.MEDIUM]: '中等风险',
  [RiskLevel.HIGH]: '高风险',
  [RiskLevel.CRITICAL]: '严重风险'
} as const;

// 甘特图视图模式
export const GANTT_VIEW_MODES = ['Day', 'Week', 'Month', 'Year'] as const;

// 甘特图视图模式文本映射
export const GANTT_VIEW_MODE_TEXT_MAP = {
  'Day': '日视图',
  'Week': '周视图',
  'Month': '月视图',
  'Year': '年视图'
} as const;

// API路径常量
export const API_PATHS = {
  AUTH: {
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
    ME: '/api/auth/me',
    UPDATE_PROFILE: '/api/auth/update-profile',
    CHANGE_PASSWORD: '/api/auth/change-password'
  },
  PROJECTS: {
    LIST: '/api/projects/',
    CREATE: '/api/projects/',
    DETAIL: (id: number) => `/api/projects/${id}`,
    UPDATE: (id: number) => `/api/projects/${id}`,
    DELETE: (id: number) => `/api/projects/${id}`,
    DEPENDENCIES: (id: number) => `/api/projects/${id}/dependencies/`,
    ASSIGN_USERS: (id: number) => `/api/projects/${id}/assign-users/`,
    BURNDOWN: (id: number) => `/api/projects/${id}/burndown/`
  },
  TASKS: {
    LIST: '/api/tasks/',
    CREATE: '/api/tasks/',
    DETAIL: (id: number) => `/api/tasks/${id}`,
    UPDATE: (id: number) => `/api/tasks/${id}`,
    DELETE: (id: number) => `/api/tasks/${id}`
  },
  USERS: {
    LIST: '/api/users/',
    OUTSTANDING: '/api/users/outstanding',
    CALCULATE_PERFORMANCE: '/api/users/calculate-performance'
  },
  GANTT: {
    PROJECT_DATA: '/api/gantt/project-data',
    CRITICAL_PATH: '/api/gantt/critical-path'
  }
} as const;

// 错误信息常量
export const ERROR_MESSAGES = {
  NETWORK_ERROR: '网络连接失败，请检查网络设置',
  UNAUTHORIZED: '未授权访问，请重新登录',
  FORBIDDEN: '权限不足，无法执行此操作',
  NOT_FOUND: '请求的资源不存在',
  SERVER_ERROR: '服务器内部错误，请稍后重试',
  VALIDATION_ERROR: '输入数据验证失败',
  PASSWORD_MISMATCH: '两次输入的密码不一致',
  PASSWORD_TOO_SHORT: '密码长度至少8位',
  REQUIRED_FIELDS: '请填写所有必填字段'
} as const;

// 成功信息常量
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: '登录成功',
  REGISTER_SUCCESS: '注册成功',
  UPDATE_SUCCESS: '更新成功',
  DELETE_SUCCESS: '删除成功',
  CREATE_SUCCESS: '创建成功'
} as const;
