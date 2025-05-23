<template>
  <nav class="sidebar">
    <ul>
      <li>
        <router-link to="/dashboard" active-class="active-link">Dashboard</router-link>
      </li>
      <li>
        <router-link to="/projects" active-class="active-link">Projects</router-link>
      </li>
      <li>
        <router-link to="/tasks" active-class="active-link">Tasks</router-link>
      </li>
      <li>
        <router-link to="/profile" active-class="active-link">Profile</router-link>
      </li>
    </ul>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Sidebar',
});
</script>

<style scoped>
.sidebar {
  width: 220px;
  min-height: 100vh;
  background: linear-gradient(135deg, #42b983 60%, #3498db 100%);
  color: #fff;
  padding: 32px 12px 18px 12px;
  box-shadow: 2px 0 8px rgba(52, 152, 219, 0.08);
  display: flex;
  flex-direction: column;
  position: relative;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}

.sidebar li {
  margin: 18px 0;
}

.sidebar a {
  color: #fff;
  text-decoration: none;
  font-size: 1.08em;
  padding: 8px 16px;
  border-radius: 5px;
  display: block;
  transition: background 0.18s, color 0.18s;
}

.sidebar a:hover,
.sidebar .active-link {
  background: rgba(255,255,255,0.18);
  color: #ffe082;
}

@media (max-width: 700px) {
  .sidebar {
    width: 100%;
    min-height: auto;
    flex-direction: row;
    padding: 10px 0;
    box-shadow: none;
    background: #42b983;
  }
  .sidebar ul {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
  }
  .sidebar li {
    margin: 0 8px;
  }
}
</style>