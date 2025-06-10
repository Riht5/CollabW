// 通用工具函数
import { 
  STATUS_TEXT_MAP, 
  ROLE_TEXT_MAP, 
  WORKLOAD_TEXT_MAP, 
  RISK_LEVEL_TEXT_MAP,
  GANTT_VIEW_MODE_TEXT_MAP,
  ProjectStatus,
  UserRole,
  TaskWorkload,
  RiskLevel
} from './constants';

/**
 * 获取项目状态文本
 */
export const getStatusText = (status: string): string => {
  return STATUS_TEXT_MAP[status as ProjectStatus] || status;
};

/**
 * 获取用户角色文本
 */
export const getRoleText = (role: string | undefined): string => {
  return ROLE_TEXT_MAP[role as UserRole] || '员工';
};

/**
 * 获取任务工作量文本
 */
export const getWorkloadText = (workload: string): string => {
  return WORKLOAD_TEXT_MAP[workload as TaskWorkload] || workload;
};

/**
 * 获取风险等级文本
 */
export const getRiskLevelText = (riskLevel: string): string => {
  return RISK_LEVEL_TEXT_MAP[riskLevel as RiskLevel] || riskLevel;
};

/**
 * 获取甘特图视图模式文本
 */
export const getViewModeText = (mode: string): string => {
  return GANTT_VIEW_MODE_TEXT_MAP[mode as keyof typeof GANTT_VIEW_MODE_TEXT_MAP] || mode;
};

/**
 * 获取甘特图视图模式文本
 */
export const getGanttViewModeText = (mode: string): string => {
  return GANTT_VIEW_MODE_TEXT_MAP[mode as keyof typeof GANTT_VIEW_MODE_TEXT_MAP] || mode;
};

/**
 * 格式化日期
 */
export const formatDate = (date: string | Date | null | undefined): string => {
  if (!date) return '未设置';
  const d = new Date(date);
  if (isNaN(d.getTime())) return '无效日期';
  return d.toLocaleDateString('zh-CN');
};

/**
 * 格式化日期时间
 */
export const formatDateTime = (date: string | Date | null | undefined): string => {
  if (!date) return '未设置';
  const d = new Date(date);
  if (isNaN(d.getTime())) return '无效日期';
  return d.toLocaleString('zh-CN');
};

/**
 * 检查用户权限
 */
export class PermissionChecker {
  /**
   * 检查是否为总监
   */
  static isDirector(userRole?: string): boolean {
    return userRole === UserRole.DIRECTOR;
  }

  /**
   * 检查是否为经理
   */
  static isManager(userRole?: string): boolean {
    return userRole === UserRole.MANAGER;
  }

  /**
   * 检查是否为普通用户
   */
  static isUser(userRole?: string): boolean {
    return userRole === UserRole.USER;
  }

  /**
   * 检查是否为经理或总监
   */
  static isManagerOrDirector(userRole?: string): boolean {
    return userRole === UserRole.MANAGER || userRole === UserRole.DIRECTOR;
  }

  /**
   * 检查是否有管理权限（创建、编辑、删除）
   */
  static hasManagementPermission(userRole?: string): boolean {
    return this.isManagerOrDirector(userRole);
  }
}

/**
 * 防抖函数
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
};

/**
 * 节流函数
 */
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

/**
 * 深拷贝对象
 */
export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime()) as unknown as T;
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as unknown as T;
  if (typeof obj === 'object') {
    const clonedObj = {} as T;
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key]);
      }
    }
    return clonedObj;
  }
  return obj;
};

/**
 * 验证邮箱格式
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * 验证密码强度
 */
export const isValidPassword = (password: string): boolean => {
  return password.length >= 8;
};

/**
 * 生成随机ID
 */
export const generateId = (): string => {
  return Math.random().toString(36).substr(2, 9);
};

/**
 * 本地存储工具
 */
export class StorageUtil {
  /**
   * 获取本地存储项
   */
  static getItem<T>(key: string, defaultValue?: T): T | null {
    try {
      const item = localStorage.getItem(key);
      if (item === null) return defaultValue || null;
      return JSON.parse(item);
    } catch (error) {
      console.error(`Error getting item from localStorage: ${key}`, error);
      return defaultValue || null;
    }
  }

  /**
   * 设置本地存储项
   */
  static setItem<T>(key: string, value: T): void {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Error setting item to localStorage: ${key}`, error);
    }
  }

  /**
   * 删除本地存储项
   */
  static removeItem(key: string): void {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error(`Error removing item from localStorage: ${key}`, error);
    }
  }

  /**
   * 清空本地存储
   */
  static clear(): void {
    try {
      localStorage.clear();
    } catch (error) {
      console.error('Error clearing localStorage', error);
    }
  }
}
