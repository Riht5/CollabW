<!-- frontend/src/components/projects/CriticalPathChart.vue -->
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
import { onMounted, onUnmounted, onActivated, ref, computed, watch } from 'vue';
import Gantt from 'frappe-gantt';
import { useGanttStore } from '@/stores/gantt';
import { getGanttViewModeText } from '@/utils/helpers';
import type { GanttTask } from '@/types/index';

const ganttStore = useGanttStore();
const gantt = ref<Gantt | null>(null);
const ganttContainer = ref<HTMLElement | null>(null);
const wrapperRef = ref<HTMLElement | null>(null);
const currentViewMode = ref<Gantt.viewMode>('Day'); // 默认 Day
const showViewModeDropdown = ref<boolean>(false);
const viewModes: Gantt.viewMode[] = ['Day', 'Week', 'Month', 'Year'];

// 视图模式文本映射
const getViewModeText = (mode: string): string => {
  return getGanttViewModeText(mode);
};

// 添加空白任务填充，动态计算时间范围
const padGanttTasks = (tasks: GanttTask[], minRows = 4): GanttTask[] => {
  if (tasks.length >= minRows) return tasks;
  const validTasks = tasks.filter(task => task.id && !task.id.startsWith('__placeholder_'));
  const minDate = validTasks.length ? validTasks.reduce((min, task) => {
    const start = new Date(task.start);
    return start < min ? start : min;
  }, new Date(validTasks[0].start)) : new Date('2025-01-01');
  const placeholders = Array.from({ length: minRows - validTasks.length }).map((_, i) => ({
    id: `__placeholder_${i}`,
    name: '',
    start: minDate.toISOString().split('T')[0],
    end: minDate.toISOString().split('T')[0],
    progress: 0,
    dependencies: '',
    custom_class: 'placeholder-task'
  }));
  return [...validTasks, ...placeholders];
};

// 动态计算容器高度
const containerHeight = computed(() => {
  const taskCount = Math.max(4, ganttStore.criticalPathGanttData.length);
  const rowHeight = 50;
  const headerHeight = 120;
  const minHeight = 350;
  return Math.max(minHeight, taskCount * rowHeight + headerHeight);
});

const getTimelineRange = (viewMode: Gantt.viewMode) => {
  const tasks = ganttStore.criticalPathGanttData;
  if (!tasks.length) {
    const currentYear = new Date().getFullYear();
    return { startDate: `${currentYear}-01-01`, endDate: `${currentYear}-12-31` };
  }
  const dates = tasks.flatMap(task => [new Date(task.start), new Date(task.end)]);
  const minDate = new Date(Math.min(...dates.map(d => d.getTime())));
  const maxDate = new Date(Math.max(...dates.map(d => d.getTime())));
  if (viewMode === 'Day') {
    minDate.setDate(minDate.getDate() - 7);
    maxDate.setDate(maxDate.getDate() + 7);
  } else if (viewMode === 'Week') {
    minDate.setDate(minDate.getDate() - 14);
    maxDate.setDate(maxDate.getDate() + 14);
  } else if (viewMode === 'Month') {
    minDate.setMonth(minDate.getMonth() - 1);
    maxDate.setMonth(maxDate.getMonth() + 1);
  } else if (viewMode === 'Year') {
    minDate.setFullYear(minDate.getFullYear() - 1);
    maxDate.setFullYear(maxDate.getFullYear() + 1);
  }
  return {
    startDate: minDate.toISOString().split('T')[0],
    endDate: maxDate.toISOString().split('T')[0]
  };
};

const scrollToToday = () => {
  if (gantt.value) {
    // 使用重新初始化的方式来滚动到今天
    try {
      initializeGantt();
      console.log('Scrolled to today');
    } catch (err) {
      console.error('滚动失败:', err);
    }
  }
};

const toggleViewModeDropdown = () => {
  showViewModeDropdown.value = !showViewModeDropdown.value;
};

// 获取任务权重信息
const getTaskWeight = (taskId: string): number => {
  if (!ganttStore.criticalPathMeta) return 0;
  const numericId = parseInt(taskId.replace('project_', ''));
  return ganttStore.criticalPathMeta.weights[numericId] || 0;
};

// 统一的甘特图创建函数，消除重复代码
const createGanttChart = (viewMode?: Gantt.viewMode) => {
  const mode = viewMode || currentViewMode.value;
  
  if (!ganttContainer.value || !ganttStore.criticalPathGanttData.length) {
    console.warn('关键路径甘特图容器或数据未就绪');
    return;
  }
  
  // 清理现有实例
  ganttContainer.value.innerHTML = '';
  gantt.value = null;
  
  try {
    const { startDate } = getTimelineRange(mode);
    const tasksWithPadding = padGanttTasks(ganttStore.criticalPathGanttData, 4);
    
    gantt.value = new Gantt(ganttContainer.value, tasksWithPadding, {
      view_mode: mode,
      date_format: 'YYYY-MM-DD',
      bar_height: 36,
      padding: 24,
      column_width: mode === 'Day' ? 30 : mode === 'Week' ? 50 : mode === 'Month' ? 100 : 150,
      scroll_to: startDate,
      language: 'zh-cn',
      popup: (task: any) => {
        if (task.task?.custom_class?.includes('placeholder')) return '';
        const taskData = task.task || {};
        const startDate = taskData._start
          ? taskData._start.toLocaleDateString('zh-CN')
          : taskData.start
            ? new Date(taskData.start).toLocaleDateString('zh-CN')
            : '未知日期';
        const endDate = taskData._end
          ? taskData._end.toLocaleDateString('zh-CN')
          : taskData.end
            ? new Date(taskData.end).toLocaleDateString('zh-CN')
            : '未知日期';
        const duration = taskData._end && taskData._start
          ? Math.ceil((taskData._end.getTime() - taskData._start.getTime()) / (1000 * 60 * 60 * 24))
          : taskData.end && taskData.start
            ? Math.ceil((new Date(taskData.end).getTime() - new Date(taskData.start).getTime()) / (1000 * 60 * 60 * 24))
            : 0;
        const weight = getTaskWeight(taskData.id || '');
        return `
          <div style="padding: 12px; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-left: 4px solid #ef4444;">
            <h4 style="margin: 0 0 8px 0; color: #dc2626; font-weight: bold;">🎯 ${taskData.name || '未知任务'}</h4>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">开始: ${startDate}</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">结束: ${endDate}</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">工期: ${duration} 天</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">进度: ${taskData.progress !== undefined ? taskData.progress : 0}%</p>
          </div>
        `;
      },
      on_click: (task: any) => {
        if (!task.task?.custom_class?.includes('placeholder')) {
          const weight = getTaskWeight(task.task.id || '');
          console.log('点击关键任务:', task.task.name, '权重:', weight);
        }
      },
      on_date_change: (task: any, start: Date, end: Date) => {
        console.log('关键任务日期变更:', task.task.name, start.toISOString().split('T')[0], end.toISOString().split('T')[0]);
      },
      on_progress_change: (task: any, progress: number) => {
        console.log('关键任务进度变更:', task.task.name, progress);
      }
    });
    
    console.log('关键路径甘特图创建成功，视图模式:', mode);
    return true;
  } catch (err) {
    console.error('关键路径甘特图创建失败:', err);
    ganttStore.error = '关键路径甘特图创建失败，请刷新页面重试';
    return false;
  }
};

// 切换视图模式
const changeViewMode = (mode: Gantt.viewMode) => {
  if (createGanttChart(mode)) {
    currentViewMode.value = mode;
    showViewModeDropdown.value = false;
    console.log('视图切换至:', mode);
  }
};

// 初始化甘特图
const initializeGantt = () => {
  createGanttChart();
};

const refreshCriticalPath = async () => {
  try {
    await ganttStore.fetchCriticalPath();
    console.log('刷新关键路径数据:', ganttStore.criticalPathGanttData);
    if (ganttStore.criticalPathGanttData.length > 0) {
      if (gantt.value) {
        gantt.value.refresh(padGanttTasks(ganttStore.criticalPathGanttData));
        console.log('关键路径刷新成功:', ganttStore.criticalPathGanttData);
      } else {
        console.warn('Gantt 实例未初始化，重新初始化');
        initializeGantt();
      }
    }
  } catch (err) {
    console.error('刷新关键路径失败:', err);
    ganttStore.error = '刷新关键路径失败，请重试';
  }
};

onMounted(async () => {
  console.log('关键路径甘特图组件挂载');
  try {
    await ganttStore.fetchCriticalPath();
    console.log('获取关键路径数据:', ganttStore.criticalPathGanttData);
  } catch (err) {
    console.error('获取关键路径数据失败:', err);
    ganttStore.error = '加载关键路径数据失败，请检查网络';
  }
});

onActivated(async () => {
  console.log('关键路径甘特图组件激活');
  try {
    await ganttStore.fetchCriticalPath();
    console.log('激活时获取关键路径数据:', ganttStore.criticalPathGanttData);
  } catch (err) {
    console.error('激活时获取关键路径数据失败:', err);
    ganttStore.error = '加载关键路径数据失败，请检查网络';
  }
});

watch(
  () => [ganttStore.criticalPathGanttData, ganttContainer.value],
  ([newData, container]) => {
    console.log('Watch 触发，数据长度:', Array.isArray(newData) ? newData.length : '非数组', '容器:', !!container, 'Gantt 实例:', !!gantt.value);
    if (Array.isArray(newData) && newData.length && container) {
      initializeGantt();
    }
  },
  { immediate: true }
);

onUnmounted(() => {
  gantt.value = null;
  if (ganttContainer.value) {
    ganttContainer.value.innerHTML = '';
  }
  console.log('关键路径甘特图组件卸载');
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
  position: relative;
}
.gantt-container {
  width: 100%;
  min-width: 1200px;
  height: 100%; /* Fill scroll container */
  position: relative;
  overflow: hidden; /* 防止内部溢出 */
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