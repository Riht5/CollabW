<!-- frontend/src/views/GanttView.vue -->
<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>多项目甘特图</h1>
      <div class="header-actions">
        <button class="btn btn-secondary" @click="toggleCriticalPath" :disabled="ganttStore.loading">
          {{ showCriticalPath ? '隐藏关键路径' : '显示关键路径' }}
          <i class="icon">{{ showCriticalPath ? '🙈' : '🎯' }}</i>
        </button>
        <router-link to="/" class="btn btn-secondary">
          <i class="icon">📊</i> 返回仪表盘
        </router-link>
      </div>
    </div>
    <div class="dashboard-content">
      <div class="content-section">
        <h2>项目总览</h2>
        <GanttChartTest />
      </div>
      <Suspense v-if="showCriticalPath">
        <template #default>
          <div class="content-section">
            <h2>关键路径</h2>
            <CriticalPathChart />
          </div>
        </template>
        <template #fallback>
          <div class="loading">加载关键路径数据...</div>
        </template>
      </Suspense>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import GanttChartTest from '../components/gantt/GanttChart.vue';
import CriticalPathChart from '../components/gantt/CriticalPathChart.vue';
import { useGanttStore } from '@/stores/gantt';
import { onMounted } from 'vue';

const ganttStore = useGanttStore();
const showCriticalPath = ref(false); // 控制关键路径显示

const toggleCriticalPath = async () => {
  if (showCriticalPath.value) {
    showCriticalPath.value = false; // 隐藏关键路径
    console.log('隐藏关键路径');
  } else {
    try {
      ganttStore.loading = true; // 设置加载状态
      await ganttStore.fetchCriticalPath();
      console.log('获取关键路径数据:', ganttStore.criticalPathGanttData);
      showCriticalPath.value = true; // 显示关键路径
    } catch (err) {
      console.error('获取关键路径数据失败:', err);
      ganttStore.error = '加载关键路径数据失败，请检查网络';
    } finally {
      ganttStore.loading = false;
    }
  }
};

onMounted(async () => {
  try {
    await ganttStore.fetchGanttData();
    console.log('获取甘特图数据:', ganttStore.ganttAllData);
  } catch (err) {
    console.error('获取甘特图数据失败:', err);
    ganttStore.error = '加载甘特图数据失败，请检查网络';
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
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.icon {
  font-style: normal;
}
.loading {
  padding: 20px;
  text-align: center;
  color: #3b82f6;
  font-size: 16px;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border-radius: 8px;
  margin: 20px;
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
    flex-wrap: wrap;
  }
  .btn {
    padding: 10px 16px;
    font-size: 14px;
  }
}
</style>