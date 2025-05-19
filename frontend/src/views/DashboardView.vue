<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="dashboard-content">
      <p>Welcome to your project management dashboard!</p>
      <project-list />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import TaskList from '@/components/tasks/TaskList.vue';

export default defineComponent({
  name: 'DashboardView',
  components: {
    ProjectList,
    TaskList,
  },
});
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>