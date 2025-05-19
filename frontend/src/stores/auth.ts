import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import type { LoginCredentials } from '@/types/index';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  const token = ref('');

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await axios.post('/api/auth/login', credentials);
      token.value = response.data.access_token;
      localStorage.setItem('token', token.value);

      // 登录后再获取用户信息
      const userResp = await axios.get('/api/auth/me', {
        headers: { Authorization: `Bearer ${token.value}` }
      });
      user.value = userResp.data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    user.value = null;
    token.value = '';
    localStorage.removeItem('token');
  };

  const isAuthenticated = () => {
    return !!token.value || !!localStorage.getItem('token');
  };

  return { user, token, login, logout, isAuthenticated };
});