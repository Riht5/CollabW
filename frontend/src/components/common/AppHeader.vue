<template>
  <header class="app-header">
    <div class="logo">
      <h1>CollabW</h1>
    </div>
    <nav>
      <ul>
        <li><router-link to="/">首页</router-link></li>
        <li><router-link to="/login">登录</router-link></li>
        <li><router-link to="/register">注册</router-link></li>
      </ul>
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AppHeader',
});
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #42b983;
  color: white;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.08);
}

.logo h1 {
  margin: 0;
  font-size: 2rem;
  letter-spacing: 2px;
  font-weight: bold;
}

nav ul {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

nav a {
  color: white;
  text-decoration: none;
  font-size: 1.08em;
  padding: 6px 14px;
  border-radius: 5px;
  transition: background 0.18s, color 0.18s;
}

nav a:hover,
nav .router-link-exact-active {
  background: rgba(255,255,255,0.18);
  color: #ffe082;
}
</style>