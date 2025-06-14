<template>
  <div class="register-view container">
    <div class="card" style="max-width: 400px; margin: 40px auto;">
      <div class="card-body">
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label class="form-label required" for="username">用户名</label>
            <input 
              class="form-input"
              v-model="formData.username" 
              id="username" 
              required 
              autocomplete="username" 
              placeholder="请输入用户名"
            />
          </div>
          <div class="form-group">
            <label class="form-label required" for="email">邮箱</label>
            <input 
              class="form-input"
              v-model="formData.email" 
              id="email" 
              type="email" 
              required 
              autocomplete="email" 
              placeholder="请输入邮箱地址"
            />
          </div>
          <div class="form-group">
            <label class="form-label" for="profile">简介（可选）</label>
            <textarea 
              class="form-textarea"
              v-model="formData.profile" 
              id="profile" 
              rows="3" 
              placeholder="请输入个人简介"
            ></textarea>
          </div>
          <div class="form-group">
            <label class="form-label required" for="password">密码</label>
            <input 
              class="form-input"
              v-model="formData.password" 
              id="password" 
              type="password" 
              required 
              autocomplete="new-password" 
              placeholder="请输入密码（至少8位）"
            />
          </div>
          <div class="form-group">
            <label class="form-label required" for="confirm_password">确认密码</label>
            <input 
              class="form-input"
              v-model="formData.confirm_password" 
              id="confirm_password" 
              type="password" 
              required 
              autocomplete="new-password" 
              placeholder="请再次输入密码"
            />
          </div>
          <div class="form-group">
            <label class="form-label required" for="register_key">注册密钥</label>
            <input 
              class="form-input"
              v-model="formData.register_key" 
              id="register_key" 
              required 
              placeholder="请输入注册密钥"
            />
            <div class="form-help">不同的注册密钥对应不同的用户角色</div>
          </div>
          <button 
            class="btn btn-primary" 
            type="submit" 
            style="width:100%;" 
            :disabled="loading"
          >
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>
        <div v-if="errorMessage" class="error-message mt-md">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message mt-md">{{ successMessage }}</div>
      </div>
      <div class="card-footer text-center">
        <router-link to="/login">已有账号？点击登录</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import type { Register } from '@/types/index';

export default defineComponent({
  name: 'RegisterView',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const errorMessage = ref('');
    const successMessage = ref('');
    const loading = ref(false);

    const formData = reactive<Register>({
      username: '',
      email: '',
      password: '',
      confirm_password: '',
      profile: '',
      register_key: '',
    });

    const validateForm = (): boolean => {
      if (!formData.username || !formData.email || !formData.password || 
          !formData.confirm_password || !formData.register_key) {
        errorMessage.value = '请填写所有必需字段';
        return false;
      }

      if (formData.password !== formData.confirm_password) {
        errorMessage.value = '两次输入的密码不一致';
        return false;
      }

      if (formData.password.length < 8) {
        errorMessage.value = '密码至少需要8位字符';
        return false;
      }

      return true;
    };

    const handleRegister = async () => {
      errorMessage.value = '';
      successMessage.value = '';

      if (!validateForm()) {
        return;
      }

      loading.value = true;

      try {
        await authStore.register(formData);
        successMessage.value = '注册成功！正在跳转到登录页面...';
        
        // 延迟跳转，让用户看到成功消息
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } catch (error: any) {
        errorMessage.value = error.response?.data?.detail || '注册失败，请检查输入信息';
      } finally {
        loading.value = false;
      }
    };

    return { 
      formData,
      errorMessage, 
      successMessage, 
      loading,
      handleRegister 
    };
  },
});
</script>

<style scoped>
.register-view {
  padding: var(--spacing-xl);
}
</style>