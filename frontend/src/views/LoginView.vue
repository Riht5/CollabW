<template>
  <div class="login-view container">
    <div class="card" style="max-width: 400px; margin: 60px auto;">
      <div class="card-header text-center">
        <h1>登录</h1>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label class="form-label required" for="identifier">用户名或邮箱</label>
            <input 
              class="form-input"
              type="text" 
              id="identifier" 
              v-model="identifier" 
              required 
              autocomplete="username" 
              placeholder="请输入用户名或邮箱"
            />
          </div>
          <div class="form-group">
            <label class="form-label required" for="password">密码</label>
            <input 
              class="form-input"
              type="password" 
              id="password" 
              v-model="password" 
              required 
              autocomplete="current-password" 
              placeholder="请输入密码"
            />
          </div>
          <button 
            class="btn btn-primary" 
            type="submit" 
            style="width:100%;" 
            :disabled="loading"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
        <div v-if="errorMessage" class="error-message mt-md">{{ errorMessage }}</div>
      </div>
      <div class="card-footer text-center">
        <router-link to="/register">还没有账号？点击注册</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
  name: 'LoginView',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const identifier = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const loading = ref(false);

    const handleLogin = async () => {
      if (!identifier.value || !password.value) {
        errorMessage.value = '请填写所有字段';
        return;
      }

      loading.value = true;
      errorMessage.value = '';

      try {
        await authStore.login({ 
          identifier: identifier.value, 
          password: password.value 
        });
        router.push('/'); // 登录成功后跳转到首页
      } catch (error: any) {
        errorMessage.value = error.response?.data?.detail || '登录失败，请检查用户名和密码';
      } finally {
        loading.value = false;
      }
    };

    return {
      identifier,
      password,
      errorMessage,
      loading,
      handleLogin,
    };
  },
});
</script>

<style scoped>
.login-view {
  padding: var(--spacing-xl);
}
</style>