<!-- frontend/src/views/GanttView.vue -->
<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>多项目甘特图</h1>
      <div class="header-actions">
        <router-link to="/" class="btn btn-secondary">
          <i class="icon">📊</i> 返回仪表盘
        </router-link>
      </div>
    </div>
    <div class="dashboard-content">
      <div class="content-section">
        <h2>固定数据甘特图</h2>
        <GanttChart />
      </div>
      <div class="content-section">
        <h2>API 数据甘特图</h2>
        <GanttChartTest />
      </div>
      <div class="content-section">
        <h2>关键路径甘特图</h2>
        <CriticalPathChart />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import GanttChart from '../components/projects/GanttChart.vue';
import GanttChartTest from '../components/projects/GanttChartTest.vue';
import CriticalPathChart from '../components/projects/CriticalPathChart.vue';
import { useProjectStore } from '@/stores/project';
import { onMounted } from 'vue';

const projectStore = useProjectStore();

onMounted(async () => {
  await projectStore.fetchGanttData();
  try {
    await projectStore.fetchCriticalPath();
  } catch (err) {
    console.error('Failed to fetch critical path:', err);
  }
});
</script>

<style scoped>
.dashboard {
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}
.dashboard-header h1 {
  color: #2c3e50;
  font-size: 32px;
  font-weight: 600;
  margin: 0;
}
.header-actions {
  display: flex;
  gap: 12px;
}
.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}
.content-section {
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}
.content-section h2 {
  margin: 0 0 8px;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}
.btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}
.btn-secondary {
  background: #95a5a6;
  color: white;
}
.btn-secondary:hover {
  background: #7f8c8d;
}
.icon {
  font-style: normal;
}
@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }
  .dashboard-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  .header-actions {
    justify-content: center;
  }
}
</style>