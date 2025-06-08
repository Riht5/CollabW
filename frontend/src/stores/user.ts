import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import type { User } from '@/types/index';

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([]);
  const outstandingUsers = ref<User[]>([]);
  const currentUser = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchUsers = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/users/');
      users.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch users';
    } finally {
      loading.value = false;
    }
  };

  const fetchCurrentUser = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/auth/me');
      currentUser.value = response.data;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch current user';
      // 如果获取失败，清空当前用户信息
      currentUser.value = null;
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getUserById = async (userId: number | string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`/api/users/${userId}`);
      return response.data as User;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch user';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const fetchOutstandingUsers = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/users/outstanding');
      outstandingUsers.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch outstanding users';
    } finally {
      loading.value = false;
    }
  };

  const calculatePerformance = async () => {
    loading.value = true;
    error.value = null;
    try {
      await axios.post('/api/users/calculate-performance');
      // 重新获取用户列表和优秀员工列表
      await Promise.all([fetchUsers(), fetchOutstandingUsers()]);
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to calculate performance';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getUserTask = async (userId: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`/api/users/${userId}/task`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch user task';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getUserHeadedTask = async (userId: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`/api/users/${userId}/headed-task`);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch user headed task';
      return null;
    } finally {
      loading.value = false;
    }
  };

  return {
    users,
    outstandingUsers,
    currentUser,
    loading,
    error,
    fetchUsers,
    fetchCurrentUser,
    getUserById,
    fetchOutstandingUsers,
    calculatePerformance,
    getUserTask,
    getUserHeadedTask
  };
});