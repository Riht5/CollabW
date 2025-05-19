import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import type { Task } from '@/types/index';

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchTasks = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/tasks');
      tasks.value = response.data;
    } catch (err: any) {
      error.value = err instanceof Error ? err.message : String(err) || 'Failed to fetch tasks';
    } finally {
      loading.value = false;
    }
  };

  const getTaskById = async (taskId: number | string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`/api/tasks/${taskId}`);
      return response.data as Task;
    } catch (err: any) {
      error.value = err instanceof Error ? err.message : String(err) || 'Failed to fetch task';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const addTask = async (task: Omit<Task, 'id'>) => {
    loading.value = true;
    error.value = null;
    try {
      await axios.post('/api/tasks', task);
      await fetchTasks();
    } catch (err: any) {
      error.value = err instanceof Error ? err.message : String(err) || 'Failed to add task';
    } finally {
      loading.value = false;
    }
  };

  const deleteTask = async (taskId: number) => {
    loading.value = true;
    error.value = null;
    try {
      await axios.delete(`/api/tasks/${taskId}`);
      await fetchTasks();
    } catch (err: any) {
      error.value = err instanceof Error ? err.message : String(err) || 'Failed to delete task';
    } finally {
      loading.value = false;
    }
  };

  return { tasks, loading, error, fetchTasks, getTaskById, addTask, deleteTask };
});