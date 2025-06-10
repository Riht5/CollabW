<!-- frontend/src/views/GanttView.vue -->
<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>项目总览</h1>
      <div class="header-actions">
        <!-- 仅 Manager 可见关键路径分析按钮 -->
        <button 
          v-if="isManager"
          class="btn btn-secondary" 
          @click="toggleView" 
          :disabled="ganttStore.loading"
        >
          {{ showCriticalPath ? '返回项目甘特图' : '计算关键路径' }}
          <i class="icon">{{ showCriticalPath ? '📊' : '🎯' }}</i>
        </button>
      </div>
    </div>    <div class="dashboard-content">
      <div v-if="!showCriticalPath" class="content-section">
        <GanttChart />
      </div>
      <div v-if="showCriticalPath && isManager" class="content-section">
        <Suspense>
          <template #default>
            <CriticalPathChart />
          </template>
          <template #fallback>
            <div class="loading">加载关键路径数据...</div>
          </template>
        </Suspense>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import GanttChart from '../components/gantt/GanttChart.vue';
import CriticalPathChart from '../components/gantt/CriticalPathChart.vue';
import { useGanttStore } from '@/stores/gantt';
import { useAuthStore } from '@/stores/auth';
import { onMounted } from 'vue';

const ganttStore = useGanttStore();
const authStore = useAuthStore();
const showCriticalPath = ref(false);

// 用户角色判断
const isManager = computed(() => authStore.user?.role === 'manager');

const toggleView = async () => {
  if (!isManager.value) return; // Manager专属功能
  
  if (showCriticalPath.value) {
    // 返回项目甘特图
    showCriticalPath.value = false;
    console.log('返回项目甘特图');
  } else {
    // 计算并显示关键路径
    try {
      ganttStore.loading = true;
      await ganttStore.fetchCriticalPath();
      console.log('获取关键路径数据:', ganttStore.criticalPathGanttData);
      showCriticalPath.value = true; // 切换到关键路径视图
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
    // 页面初始化时获取项目甘特图数据
    await ganttStore.fetchGanttData();
    console.log('获取甘特图数据:', ganttStore.ganttAllData);
  } catch (err) {
    console.error('获取甘特图数据失败:', err);
    ganttStore.error = '加载甘特图数据失败，请检查网络';
  }
});
</script>

<style scoped>
@import '@/assets/styles/gantt.css';
</style>