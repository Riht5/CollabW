import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/utils/axios';
import { API_PATHS } from '@/utils/constants';
import type { Project, ProjectCreate, Task, BurnDownProject} from '@/types/index';

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const fetchProjects = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(API_PATHS.PROJECTS.LIST);
      projects.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch projects';
    } finally {
      loading.value = false;
    }
  };

  const fetchProjectById = async (projectId: string | number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/projects/${projectId}`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch project';
      throw err;
    } finally {
      loading.value = false;
    }
  };
  const fetchBurnDown = async (id: number | string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/projects/${id}/burn-down/`);
      const data = response.data as BurnDownProject;   
      return data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch burn down chart data';
      console.error('获取燃尽图数据失败:', err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  const createProject = async (project: ProjectCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/api/projects/', project);
      await fetchProjects(); // 重新获取项目列表
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateProject = async (projectId: number, project: Partial<ProjectCreate>) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/api/projects/${projectId}`, project);
      await fetchProjects();
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deleteProject = async (projectId: number) => {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/api/projects/${projectId}`);
      await fetchProjects();
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const addDependencies = async (projectId: number, dependsOnIds: number[]) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post(`/api/projects/${projectId}/dependencies/`, {
        depends_on_ids: dependsOnIds
      });
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to add dependencies';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const assignUsersToProject = async (projectId: number, userIds: number[]) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post(`/api/projects/${projectId}/assign-users/`, {
        user_ids: userIds
      });
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to assign users to project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const removeUserFromProject = async (projectId: number, userId: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.delete(`/api/projects/${projectId}/remove-user/${userId}`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to remove user from project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchProjectTasks = async (projectId: string | number): Promise<Task[]> => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/projects/${projectId}/tasks`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch project tasks';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchProjectMembers = async (projectId: string | number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/projects/${projectId}/members`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch project members';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return { 
    projects, 
    loading, 
    error, 
    fetchProjects, 
    fetchProjectById, 
    fetchBurnDown, 
    createProject, 
    updateProject, 
    deleteProject,
    addDependencies,
    assignUsersToProject,
    removeUserFromProject,
    fetchProjectTasks,
    fetchProjectMembers,
  };
});
