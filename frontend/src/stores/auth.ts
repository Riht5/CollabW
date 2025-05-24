import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import type { Register, LoginCredentials, User } from '@/types/index';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const token = ref('');

  // 初始化时检查本地存储的token
  const initAuth = () => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      token.value = storedToken;
      // 设置axios默认header
      axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
    }
  };

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await axios.post('/api/auth/login', credentials);
      token.value = response.data.access_token;
      localStorage.setItem('token', token.value);
      
      // 设置axios默认header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;

      // 登录后获取用户信息
      const userResp = await axios.get('/api/auth/me');
      user.value = userResp.data;
      
      return response.data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    user.value = null;
    token.value = '';
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const isAuthenticated = () => {
    return !!token.value || !!localStorage.getItem('token');
  };

  const register = async (userData: Register) => {
    try {
      const response = await axios.post('/api/auth/register', userData);
      return response.data;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  // 获取当前用户信息
  const getCurrentUser = async () => {
    if (!token.value) return null;
    
    try {
      const response = await axios.get('/api/auth/me');
      user.value = response.data;
      return user.value;
    } catch (error) {
      console.error('Failed to get current user:', error);
      logout(); // token可能已过期，清除登录状态
      return null;
    }
  };

  // 初始化认证状态
  initAuth();
  
  return { 
    user, 
    token, 
    login, 
    logout, 
    isAuthenticated, 
    register,
    getCurrentUser,
    initAuth
  };
});