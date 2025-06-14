import { UserRole, ProjectStatus, TaskWorkload, RiskLevel } from '@/utils/constants';

export interface Project {
  id: number;
  name: string;
  description?: string;
  status: ProjectStatus;
  estimated_duration?: number;
  start_time?: string;
  end_time?: string;
  tasks?: Task[];
  dependencies?: Project[];
}

export interface Task {
  id: number;
  name: string;
  description?: string;
  workload: TaskWorkload;
  finished: boolean;
  project_id: number;
  head_id?: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: UserRole;
  profile?: string;
  performance?: number;
  outstanding?: boolean;
  task_id?: number;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  status?: ProjectStatus;
  estimated_duration?: number;
  start_time?: string;
  end_time?: string;
}

export interface TaskCreate {
  name: string;
  description?: string;
  workload: TaskWorkload;
  finished: boolean;
  project_id: number;
  head_id?: number;
}

export interface LoginCredentials {
  identifier: string;
  password: string;
}

export interface Register {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
  profile?: string;
  register_key: string;
  role?: UserRole;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface UserUpdate {
  username: string;
  email: string;
}

export interface PasswordChange {
  current_password: string;
  new_password: string;
}

export interface GanttTask {
  id: string;
  name: string;
  start: string;
  end: string;
  progress: number;
  dependencies: string;
  custom_class: string;
}

export interface ProjectProgress {
  date: string;
  progress: number;
}

export interface BurnDownProject {
  actual_progresses: ProjectProgress[];
  ideal_progresses: ProjectProgress[];
  risk_level: RiskLevel;
}

// 导出枚举
export { UserRole, ProjectStatus, TaskWorkload, RiskLevel };