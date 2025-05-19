<template>
  <div class="sidebar">
    <h2>CollabW</h2>
    <ul>
      <li><router-link to="/dashboard">Dashboard</router-link></li>
      <li><router-link to="/projects">Projects</router-link></li>
      <li><router-link to="/tasks">Tasks</router-link></li>
      <li><router-link to="/profile">Profile</router-link></li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Sidebar',
});
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #f4f4f4;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h2 {
  margin-bottom: 20px;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  margin: 10px 0;
}

.sidebar a {
  text-decoration: none;
  color: #333;
}

.sidebar a:hover {
  color: #007bff;
}
</style>