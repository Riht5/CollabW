import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import type { Project, ProjectCreate, ProjectProgress} from '@/types/index';

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchProjects = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/projects/');
      projects.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch projects';
    } finally {
      loading.value = false;
    }
  };

  const fetchProjectById = async (id: number | string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`/api/projects/${id}`);
      return response.data as Project;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch project';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const fetchProjectProgress = async (id: number | string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`/api/projects/${id}/progress/`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch project progress';
      return null;
    } finally {
      loading.value = false;
    }
    };

  const createProject = async (project: ProjectCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post('/api/projects/', project);
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
      const response = await axios.put(`/api/projects/${projectId}`, project);
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
      await axios.delete(`/api/projects/${projectId}`);
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
      const response = await axios.post(`/api/projects/${projectId}/dependencies/`, {
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
      const response = await axios.post(`/api/projects/${projectId}/assign-users/`, {
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
      const response = await axios.delete(`/api/projects/${projectId}/remove-user/${userId}`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to remove user from project';
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
    fetchProjectProgress, 
    createProject, 
    updateProject, 
    deleteProject,
    addDependencies,
    assignUsersToProject,
    removeUserFromProject
  };
});