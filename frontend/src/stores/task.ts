import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/utils/axios';
import { API_PATHS } from '@/utils/constants';
import type { Task, TaskCreate } from '@/types/index';

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchTasks = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/tasks/');
      tasks.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch tasks';
    } finally {
      loading.value = false;
    }
  };
  //获取当前用户任务
   const fetchUserTasks = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/users/me/tasks');
      tasks.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch user tasks';
    } finally {
      loading.value = false;
    }
  };

  const getTaskById = async (taskId: number | string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/tasks/${taskId}`);
      return response.data as Task;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch task';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const createTask = async (task: TaskCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/api/tasks/', task);
      await fetchTasks(); // 重新获取任务列表
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create task';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateTask = async (taskId: number, updateData: Partial<Task>) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/api/tasks/${taskId}`, updateData);
      
      // 更新本地状态中的任务
      const index = tasks.value.findIndex(task => task.id === taskId);
      if (index !== -1) {
        tasks.value[index] = response.data;
      }
      
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update task';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deleteTask = async (taskId: number) => {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/api/tasks/${taskId}`);
      await fetchTasks(); // 重新获取任务列表
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete task';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 分配用户到任务
  const assignUsersToTask = async (taskId: number, userIds: number[]) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post(`/api/tasks/${taskId}/assign`, userIds);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to assign users';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 获取任务成员
  const getTaskMembers = async (taskId: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/tasks/${taskId}/users`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch task members';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 从任务中移除用户
  const unassignUserFromTask = async (taskId: number, userId: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.delete(`/api/tasks/${taskId}/unassign/${userId}`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to unassign user';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return { 
    tasks, 
    loading, 
    error, 
    fetchTasks, 
    getTaskById, 
    createTask, 
    updateTask, 
    deleteTask,
    assignUsersToTask,
    getTaskMembers,
    unassignUserFromTask
  };
});




