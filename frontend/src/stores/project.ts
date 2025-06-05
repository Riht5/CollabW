import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import type { Project, ProjectCreate } from '@/types/index';

interface GanttTask {
  id: string;
  name: string;
  start: string;
  end: string;
  progress: number;
  dependencies: string;
  custom_class: string;
}

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([]);
  const ganttAllData = ref<GanttTask[]>([]);
  const criticalPathGanttData = ref<GanttTask[]>([]);
  const criticalPathMeta = ref<{
    critical_path: number[];
    total_duration_days: number;
    weights: { [key: number]: number };
  } | null>(null);
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

  const createProject = async (project: ProjectCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post('/api/projects/', project);
      await fetchProjects();
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

  const fetchGanttData = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/gantt-data');
      ganttAllData.value = response.data.map((project: any) => ({
        id: `project_${project.id}`,
        name: project.name,
        start: project.start_time,
        end: project.end_time,
        progress: project.progress,
        dependencies: project.dependencies.map((depId: number) => `project_${depId}`).join(','),
        custom_class: `status-${project.status.replace('_', '-')}`
      }));
      console.log('Gantt data fetched:', ganttAllData.value);
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch gantt data';
      console.error('Gantt data fetch failed:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchCriticalPath = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/critical-path');
      criticalPathMeta.value = response.data;
      if (criticalPathMeta.value && ganttAllData.value.length) {
        const { critical_path } = criticalPathMeta.value;
        criticalPathGanttData.value = ganttAllData.value.filter(task => {
          const taskId = parseInt(task.id.replace('project_', ''));
          return critical_path.includes(taskId);
        });
      }
      console.log('Critical path fetched:', criticalPathMeta.value);
      console.log('Critical path gantt data:', criticalPathGanttData.value);
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch critical path';
      console.error('Critical path fetch failed:', err);
    } finally {
      loading.value = false;
    }
  };

  return {
    projects,
    ganttAllData,
    criticalPathGanttData,
    criticalPathMeta,
    loading,
    error,
    fetchProjects,
    fetchProjectById,
    createProject,
    updateProject,
    deleteProject,
    addDependencies,
    assignUsersToProject,
    removeUserFromProject,
    fetchGanttData,
    fetchCriticalPath
  };
});