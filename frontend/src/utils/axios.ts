import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import router from '@/router';

// 请求拦截器
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token过期或无效，清除登录状态
      const authStore = useAuthStore();
      authStore.logout();
      // 跳转到登录页
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default axios;