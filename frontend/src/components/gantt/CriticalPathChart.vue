<template>
  <div class="gantt-wrapper" ref="wrapperRef">
    <div class="gantt-toolbar">
      <span class="gantt-title">🎯 关键路径分析</span>
      <div class="toolbar-actions">
        <div v-if="ganttStore.criticalPathMeta" class="critical-path-info">
          <span>总工期: {{ ganttStore.criticalPathMeta.total_duration_days }} 天</span>
        </div>
        <button class="btn btn-secondary" @click="scrollToToday" title="定位到今天">
          📅 今天
        </button>
        <div class="view-mode-dropdown">
          <button class="btn btn-secondary" @click="toggleViewModeDropdown" title="切换视图模式">
            {{ getViewModeText(currentViewMode) }} <span class="dropdown-icon">▼</span>
          </button>
          <div v-if="showViewModeDropdown" class="dropdown-menu">
            <button
              v-for="mode in viewModes"
              :key="mode"
              class="dropdown-item"
              @click="changeViewMode(mode)"
            >
              {{ getViewModeText(mode) }}
            </button>
          </div>
        </div>
        <button class="btn btn-secondary" @click="refreshCriticalPath" title="刷新关键路径" :disabled="ganttStore.loading">
          🔄 {{ ganttStore.loading ? '分析中...' : '刷新' }}
        </button>
      </div>
    </div>
    
    <div v-if="ganttStore.loading" class="loading">
      正在分析关键路径...
    </div>
    <div v-else-if="ganttStore.error" class="error">
      {{ ganttStore.error }}
      <br><small>请检查网络连接或联系管理员</small>
    </div>
    <div v-else-if="!ganttStore.criticalPathGanttData.length" class="empty">
      🎯 暂无关键路径数据
      <br><small>请确保项目间存在依赖关系</small>
    </div>
    <div v-else class="gantt-scroll-container">
      <div 
        class="gantt-container gantt-container-critical" 
        ref="ganttContainer" 
        :style="{ height: containerHeight + 'px' }"
      ></div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, onUnmounted, nextTick, ref, watchEffect, computed } from 'vue';
import Gantt from 'frappe-gantt';
import { useGanttStore } from '@/stores/gantt';
import type { GanttTask } from '@/types/index';

const ganttStore = useGanttStore();
const gantt = ref<Gantt | null>(null);
const ganttContainer = ref<HTMLElement | null>(null);
const wrapperRef = ref<HTMLElement | null>(null);
const currentViewMode = ref<string>('Week');
const showViewModeDropdown = ref<boolean>(false);
const viewModes: string[] = ['Day', 'Week', 'Month', 'Year'];

// 视图模式文本映射
const getViewModeText = (mode: string): string => {
  const modeMap: Record<string, string> = {
    'Day': '日视图',
    'Week': '周视图',
    'Month': '月视图', 
    'Year': '年视图'
  };
  return modeMap[mode] || mode;
};

// 添加空白任务填充
const padGanttTasks = (tasks: GanttTask[], minRows = 8): GanttTask[] => {
  if (tasks.length >= minRows) return tasks;
  const placeholders = Array.from({ length: minRows - tasks.length }).map((_, i) => ({
    id: `__placeholder_${i}`,
    name: '',
    start: tasks[0]?.start || '2025-01-01',
    end: tasks[0]?.start || '2025-01-01',
    progress: 0,
    dependencies: '',
    custom_class: 'placeholder-task'
  }));
  return [...tasks, ...placeholders];
};

// 动态计算容器高度
const containerHeight = computed(() => {
  const taskCount = Math.max(4, ganttStore.criticalPathGanttData.length);
  const rowHeight = 50;
  const headerHeight = 120;
  const minHeight = 350;
  
  return Math.max(minHeight, taskCount * rowHeight + headerHeight);
});

const getTimelineRange = () => {
  const taskYears = ganttStore.criticalPathGanttData.map((task: GanttTask) => new Date(task.start).getFullYear());
  const year = taskYears.length ? Math.min(...taskYears) : 2025;
  return { startDate: `${year}-01-01`, endDate: `${year}-12-31` };
};

const scrollToToday = () => {
  if (gantt.value) {
    gantt.value.scroll_current();
    console.log('Scrolled to today');
  }
};

const toggleViewModeDropdown = () => {
  showViewModeDropdown.value = !showViewModeDropdown.value;
};

const changeViewMode = (mode: string) => {
  if (gantt.value) {
    try {
      gantt.value.change_view_mode(mode);
      currentViewMode.value = mode;
      showViewModeDropdown.value = false;
      console.log('View changed to:', mode);
      gantt.value.refresh(padGanttTasks(ganttStore.criticalPathGanttData));
    } catch (err) {
      console.error('Failed to change view mode:', err);
    }
  } else {
    console.warn('Gantt instance not initialized');
  }
};

const refreshCriticalPath = async () => {
  if (gantt.value) {
    await ganttStore.fetchCriticalPath();
    if (ganttStore.criticalPathGanttData.length > 0) {
      gantt.value.refresh(padGanttTasks(ganttStore.criticalPathGanttData));
      console.log('Critical path refreshed:', ganttStore.criticalPathGanttData);
    }
  }
};

// 获取任务权重信息
const getTaskWeight = (taskId: string): number => {
  if (!ganttStore.criticalPathMeta) return 0;
  const numericId = parseInt(taskId.replace('project_', ''));
  return ganttStore.criticalPathMeta.weights[numericId] || 0;
};

// 优化的关键路径甘特图初始化
const initializeGantt = () => {
  if (!ganttContainer.value || !ganttStore.criticalPathGanttData.length) {
    console.warn('Critical path gantt container or data not ready');
    return;
  }
  
  ganttContainer.value.innerHTML = '';
  
  try {
    const { startDate } = getTimelineRange();
    const tasksWithPadding = padGanttTasks(ganttStore.criticalPathGanttData, 4);
    
    gantt.value = new Gantt(ganttContainer.value, tasksWithPadding, {
      view_mode: currentViewMode.value,
      date_format: 'YYYY-MM-DD',
      bar_height: 36,
      padding: 24,
      column_width: 120,
      scroll_to: startDate,
      language: 'zh-cn',
      custom_popup_html: (task: GanttTask) => {
        if (task.custom_class?.includes('placeholder')) return '';
        
        const startDate = new Date(task.start).toLocaleDateString('zh-CN');
        const endDate = new Date(task.end).toLocaleDateString('zh-CN');
        const duration = Math.ceil((new Date(task.end).getTime() - new Date(task.start).getTime()) / (1000 * 60 * 60 * 24));
        const weight = getTaskWeight(task.id);
        
        return `
          <div style="padding: 12px; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-left: 4px solid #ef4444;">
            <h4 style="margin: 0 0 8px 0; color: #dc2626; font-weight: bold;">🎯 ${task.name}</h4>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">开始: ${startDate}</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">结束: ${endDate}</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">工期: ${duration} 天</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">进度: ${task.progress}%</p>
            <p style="margin: 4px 0; color: #dc2626; font-size: 14px; font-weight: bold;">权重: ${weight.toFixed(2)} 天</p>
            <small style="color: #ef4444;">⚠️ 关键路径任务，延期将影响整体进度</small>
          </div>
        `;
      },
      on_click: (task: GanttTask) => {
        if (!task.custom_class?.includes('placeholder')) {
          const weight = getTaskWeight(task.id);
          console.log('点击关键任务:', task.name, '权重:', weight);
          
          // 显示详细信息
          alert(`关键任务: ${task.name}\n权重: ${weight.toFixed(2)} 天\n\n此任务在关键路径上，任何延期都会影响项目整体进度！`);
        }
      },
      on_date_change: (task: GanttTask, start: string, end: string) => {
        console.log('关键任务日期变更:', task.name, start, end);
      },
      on_progress_change: (task: GanttTask, progress: number) => {
        console.log('关键任务进度变更:', task.name, progress);
      }
    });
    
    console.log('关键路径甘特图初始化成功');
  } catch (err) {
    console.error('关键路径甘特图初始化失败:', err);
    ganttStore.error = '关键路径甘特图初始化失败，请刷新页面重试';
  }
};

onMounted(async () => {
  console.log('CriticalPathChart mounted');
  await nextTick();
  await ganttStore.fetchGanttData();
  await ganttStore.fetchCriticalPath();
});

watchEffect(() => {
  if (ganttStore.criticalPathGanttData.length && ganttContainer.value) {
    initializeGantt();
  }
});

onUnmounted(() => {
  gantt.value = null;
  if (ganttContainer.value) {
    ganttContainer.value.innerHTML = '';
  }
  console.log('CriticalPathChart unmounted');
});
</script>

<style scoped>
@import '@/assets/styles/gantt.css';

.critical-path-info {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn:disabled:hover {
  background: rgba(255, 255, 255, 0.2) !important;
  transform: none !important;
}

.status-in-progress .bar {
  fill: #3498db;
}
.status-completed .bar {
  fill: #2ecc71;
}
.status-pending .bar {
  fill: #95a5a6;
}
.placeholder-task .bar {
  display: none !important; /* Hide placeholder tasks */
}
.gantt-wrapper {
  display: flex;
  flex-direction: column;
  background: #f4f6f8;
  border-radius: 8px;
  border: 1px solid #ccc;
  height: 100%; /* Fill card */
}
.gantt-toolbar {
  padding: 12px 16px;
  background: #2c3e50;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #ccc;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.toolbar-actions {
  display: flex;
  gap: 10px;
}
.view-mode-dropdown {
  position: relative;
}
.dropdown-icon {
  margin-left: 5px;
  font-size: 12px;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 120px;
}
.dropdown-item {
  display: block;
  width: 100%;
  padding: 8px 16px;
  background: none;
  border: none;
  text-align: left;
  font-size: 14px;
  color: #2c3e50;
  cursor: pointer;
}
.dropdown-item:hover {
  background: #f4f6f8;
}
.btn.btn-secondary {
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 4px;
  background: #95a5a6;
  color: white;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}
.btn.btn-secondary:hover {
  background: #7f8c8d;
}
.gantt-scroll-container {
  overflow-x: auto;
  overflow-y: hidden;
  flex-grow: 1; /* Fill remaining space */
}
.gantt-container {
  width: 100%;
  min-width: 1200px;
  height: 100%; /* Fill scroll container */
  position: relative;
}
.gantt-scroll-container::-webkit-scrollbar {
  height: 10px;
}
.gantt-scroll-container::-webkit-scrollbar-track {
  background: #ecf0f1;
  border-radius: 5px;
}
.gantt-scroll-container::-webkit-scrollbar-thumb {
  background: #bdc3c7;
  border-radius: 5px;
}
.gantt {
  background-color: #ffffff !important;
  font-family: 'Arial', sans-serif;
}
.loading, .error, .empty {
  padding: 20px;
  text-align: center;
  color: #2c3e50;
  font-size: 16px;
}
.error {
  color: #e74c3c;
}
</style>