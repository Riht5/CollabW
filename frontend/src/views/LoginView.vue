<template>
  <div class="login-view container">
    <div class="card" style="max-width: 400px; margin: 60px auto;">
      <h1 style="text-align:center; margin-bottom: 1em;">登录</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="username" required autocomplete="username" />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" required autocomplete="current-password" />
        </div>
        <button class="button" type="submit" style="width:100%;">登录</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
  name: 'LoginView',
  setup() {
    const authStore = useAuthStore();
    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');

    const handleLogin = async () => {
      try {
        await authStore.login({ username: username.value, password: password.value });
        // 登录成功后的跳转或其他操作
      } catch (error) {
        errorMessage.value = 'Invalid username or password';
      }
    };

    return {
      username,
      password,
      errorMessage,
      handleLogin,
    };
  },
});
</script>

<style scoped>
.login-view {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.error {
  color: red;
}
</style>