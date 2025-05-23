<template>
  <div class="dashboard container">
    <div class="dashboard-header">
      <h1>仪表盘</h1>
      <p class="dashboard-welcome">欢迎来到项目协作管理平台！</p>
    </div>
    <div class="dashboard-content">
      <div class="dashboard-section card">
        <h2>我的项目</h2>
        <project-list />
      </div>
      <div class="dashboard-section card">
        <h2>我的任务</h2>
        <task-list :tasks="tasks" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import TaskList from '@/components/tasks/TaskList.vue';
import { useTaskStore } from '@/stores/task';

export default defineComponent({
  name: 'DashboardView',
  components: {
    ProjectList,
    TaskList,
  },
  setup() {
    const taskStore = useTaskStore();
    // 确保 taskStore.tasks 是响应式的任务数组
    return {
      tasks: taskStore.tasks,
    };
  },
});
</script>

<style scoped>
.dashboard {
  padding: 32px 0;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 32px;
}

.dashboard-welcome {
  color: #666;
  font-size: 1.1em;
  margin-top: 8px;
}

.dashboard-content {
  display: flex;
  flex-wrap: wrap;
  gap: 32px;
  justify-content: center;
}

.dashboard-section {
  flex: 1 1 350px;
  min-width: 320px;
  max-width: 500px;
  margin: 0 auto;
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.08);
  padding: 24px 20px 20px 20px;
}

@media (max-width: 900px) {
  .dashboard-content {
    flex-direction: column;
    gap: 24px;
  }
  .dashboard-section {
    max-width: 100%;
  }
}
</style>