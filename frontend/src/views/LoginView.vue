<template>
  <div class="login-view">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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