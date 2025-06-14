import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/utils/axios';
import { API_PATHS } from '@/utils/constants';
import type { Register, LoginCredentials, User } from '@/types/index';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const token = ref('');

  // 初始化时检查本地存储的token
  const initAuth = async () => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      token.value = storedToken;
      // 设置axios默认header
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
      
      // 尝试获取当前用户信息
      try {
        await getCurrentUser();
      } catch (error) {
        console.error('Failed to get user info on init:', error);
        // 如果获取用户信息失败，清除无效token
        logout();
      }
    }
  };

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await apiClient.post('/api/auth/login', credentials);
      token.value = response.data.access_token;
      localStorage.setItem('token', token.value);
      // 设置axios默认header
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;

      // 登录后获取用户信息
      const userResp = await apiClient.get('/api/auth/me');
      user.value = userResp.data;
      
      return response.data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    user.value = null;    token.value = '';
    localStorage.removeItem('token');
    delete apiClient.defaults.headers.common['Authorization'];
  };

  const isAuthenticated = () => {
    return !!token.value || !!localStorage.getItem('token');
  };

  const register = async (userData: Register) => {
    try {
      const response = await apiClient.post('/api/auth/register', userData);
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
      const response = await apiClient.get('/api/auth/me');
      user.value = response.data;
      return user.value;
    } catch (error) {
      console.error('Failed to get current user:', error);
      logout(); // token可能已过期，清除登录状态
      return null;
    }
  };

  const updateUserInfo = async (userData: { username: string; email: string }) => {
    try {
      // 添加数据验证
      if (!userData.username || !userData.email) {
        throw new Error('用户名和邮箱不能为空');
      }

      // 确保数据格式正确
      const requestData = {
        username: userData.username.trim(),
        email: userData.email.trim()
      };

      console.log('Sending update request:', requestData); // 调试日志

      const response = await apiClient.put('/api/auth/update-profile', requestData);
      
      if (response.data.success) {
        // Update the user data in store
        if (user.value) {
          user.value.username = userData.username;
          user.value.email = userData.email;
        }
        
        return response.data;
      } else {
        throw new Error(response.data.message || '更新失败');
      }
    } catch (error: any) {
      console.error('Update user info error:', error);
      // 添加更详细的错误信息
      if (error.response?.status === 422) {
        const detail = error.response.data?.detail;
        if (Array.isArray(detail)) {
          const fieldErrors = detail.map(err => `${err.loc?.join('.')}: ${err.msg}`).join(', ');
          throw new Error(`数据验证失败: ${fieldErrors}`);
        }
        throw new Error(detail || '数据格式错误');
      }
      throw new Error(error.response?.data?.message || error.message || '更新用户信息失败');
    }
  };

  const changePassword = async (passwordData: { currentPassword: string; newPassword: string }) => {
    try {
      // Convert frontend field names to backend field names
      const backendData = {
        current_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      };
      
      const response = await apiClient.put('/api/auth/change-password', backendData);
      
      if (response.data.success) {
        return response.data;
      } else {
        throw new Error(response.data.message || '密码修改失败');
      }
    } catch (error: any) {
      console.error('Change password error:', error);
      throw new Error(error.response?.data?.message || '密码修改失败');
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
    initAuth,
    updateUserInfo,
    changePassword
  };
});
