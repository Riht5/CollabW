<template>
  <div class="register-view container">
    <div class="card" style="max-width: 400px; margin: 40px auto;">
      <h1 style="text-align:center; margin-bottom: 1em;">注册新用户</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input v-model="username" id="username" required autocomplete="username" />
        </div>
        <div class="form-group">
          <label for="email">邮箱</label>
          <input v-model="email" id="email" type="email" required autocomplete="email" />
        </div>
        <div class="form-group">
          <label for="profile">简介</label>
          <textarea v-model="profile" id="profile" rows="3" ></textarea>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input v-model="password" id="password" type="password" required autocomplete="new-password" />
        </div>
        <div class="form-group">
          <label for="confirm_password">确认密码</label>
          <input v-model="confirmPassword" id="confirm_password" type="password" required autocomplete="new-password" />
        </div>
        <div class="form-group">
          <label for="register_key">注册密钥</label>
          <input v-model="registerKey" id="register_key" required />
        </div>
        <button class="button" type="submit" style="width:100%;">注册</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
  name: 'RegisterView',
  setup() {
    const username = ref('');
    const email = ref('');
    const profile = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const registerKey = ref('');
    const errorMessage = ref('');
    const successMessage = ref('');
    const authStore = useAuthStore();

    const handleRegister = async () => {
      errorMessage.value = '';
      successMessage.value = '';
      if (password.value !== confirmPassword.value) {
        errorMessage.value = '两次输入的密码不一致';
        return;
      }
      try {
        await authStore.register({
          username: username.value,
          email: email.value,
          password: password.value,
          confirm_password: confirmPassword.value,
          profile: profile.value,
          register_key: registerKey.value,
        });
        successMessage.value = '注册成功！请登录。';
      } catch (error: any) {
        errorMessage.value = error.response?.data?.detail || '注册失败';
      }
    };

    return { username, email, profile, password, confirmPassword, registerKey, errorMessage, successMessage, handleRegister };
  },
});
</script>