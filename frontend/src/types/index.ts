export interface Project {
  id: number;
  name: string;
  description?: string;
  status?: 'pending' | 'in_progress' | 'completed';
  estimated_duration?: number;
  start_time?: string;
  end_time?: string;
  head_id?: number;
  users?: User[];
  tasks?: Task[];
  dependencies?: Project[];
  dependents?: Project[];
}

export interface Task {
  id: number;
  name: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  status: boolean;
  project_id: number;
  head_id?: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'director' | 'manager' | 'user';
  profile?: string;
  project_id?: number;
}

export interface ProjectProgress {
  id: number;
  project_id: number;
  date: string;
  progress: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}