<!-- frontend/src/components/projects/CriticalPathChart.vue -->
<template>
  <div class="gantt-wrapper" ref="wrapperRef">
    <div class="gantt-toolbar">
      <span class="gantt-title">📅 Critical Path Chart</span>
      <div class="toolbar-actions">
        <button class="btn btn-secondary" @click="scrollToToday">Today</button>
        <div class="view-mode-dropdown">
          <button class="btn btn-secondary" @click="toggleViewModeDropdown">
            {{ currentViewMode }} <span class="dropdown-icon">▼</span>
          </button>
          <div v-if="showViewModeDropdown" class="dropdown-menu">
            <button
              v-for="mode in viewModes"
              :key="mode"
              class="dropdown-item"
              @click="changeViewMode(mode)"
            >
              {{ mode }}
            </button>
          </div>
        </div>
        <button class="btn btn-secondary" @click="refreshCriticalPath">Refresh Critical Path</button>
      </div>
    </div>
    <div v-if="projectStore.loading" class="loading">加载中...</div>
    <div v-else-if="projectStore.error" class="error">{{ projectStore.error }}（请确保登录并检查数据库数据）</div>
    <div v-else-if="!projectStore.criticalPathGanttData.length" class="empty">暂无关键路径数据</div>
    <div v-else class="gantt-scroll-container">
      <div class="gantt-container gantt-container-critical" ref="ganttContainer" :style="{ height: containerHeight + 'px' }"></div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, onUnmounted, nextTick, ref, watchEffect, computed } from 'vue';
import Gantt from 'frappe-gantt';
import { useProjectStore } from '@/stores/project';

interface GanttTask {
  id: string;
  name: string;
  start: string;
  end: string;
  progress: number;
  dependencies: string;
  custom_class: string;
}

const projectStore = useProjectStore();
const gantt = ref<Gantt | null>(null);
const ganttContainer = ref<HTMLElement | null>(null);
const wrapperRef = ref<HTMLElement | null>(null);
const currentViewMode = ref<string>('Week');
const showViewModeDropdown = ref<boolean>(false);
const viewModes: string[] = ['Day', 'Week', 'Month', 'Year'];

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

// 动态计算容器高度：基于实际卡片高度
const containerHeight = computed(() => {
  const taskCount = projectStore.criticalPathGanttData.length;
  const minRows = 8;
  const rowHeight = 30; // bar_height (20px) + padding (10px)
  const headerHeight = 100; // 标题和时间轴
  const wrapperHeight = wrapperRef.value?.clientHeight ?? 500; // 动态测量
  const toolbarHeight = 48; // .gantt-toolbar height
  const cardPadding = 32; // .content-section padding (16px * 2)
  const titleHeight = 32; // h2 height + margin
  const availableHeight = wrapperHeight - toolbarHeight - cardPadding - titleHeight;
  const taskHeight = Math.max(minRows, taskCount) * rowHeight + headerHeight;
  return Math.max(340, taskHeight, availableHeight); // Minimum 340px (8 rows)
});

const getTimelineRange = () => {
  const taskYears = projectStore.criticalPathGanttData.map((task: GanttTask) => new Date(task.start).getFullYear());
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
      gantt.value.refresh(padGanttTasks(projectStore.criticalPathGanttData));
    } catch (err) {
      console.error('Failed to change view mode:', err);
    }
  } else {
    console.warn('Gantt instance not initialized');
  }
};

const refreshCriticalPath = async () => {
  if (gantt.value) {
    await projectStore.fetchCriticalPath();
    if (projectStore.criticalPathGanttData.length > 0) {
      gantt.value.refresh(padGanttTasks(projectStore.criticalPathGanttData));
      console.log('Critical path refreshed:', projectStore.criticalPathGanttData);
    }
  }
};

const initializeGantt = () => {
  if (!ganttContainer.value || !projectStore.criticalPathGanttData.length) {
    console.warn('Gantt container or data not ready');
    return;
  }
  ganttContainer.value.innerHTML = '';
  try {
    const { startDate } = getTimelineRange();
    gantt.value = new Gantt(ganttContainer.value, padGanttTasks(projectStore.criticalPathGanttData), {
      view_mode: currentViewMode.value,
      date_format: 'YYYY-MM-DD',
      bar_height: 20,
      padding: 10,
      column_width: 100,
      scroll_to: startDate,
      infinite_padding: false,
      today_button: false,
      view_mode_select: false,
      on_click: (task: GanttTask) => {
        console.log('Clicked task:', task);
        if (projectStore.criticalPathMeta) {
          const weight = projectStore.criticalPathMeta.weights[parseInt(task.id.replace('project_', ''))];
          alert(`Task: ${task.name}, Weight: ${weight?.toFixed(2) || '0.00'} days`);
        }
      },
      on_date_change: (task: GanttTask, start: string, end: string) => console.log('Date changed:', task, start, end),
      on_progress_change: (task: GanttTask, progress: number) => console.log('Progress:', task, progress)
    });
    console.log('Critical path Gantt initialized');
  } catch (err) {
    console.error('Critical path Gantt init failed:', err);
    projectStore.error = '关键路径甘特图初始化失败，请检查数据或刷新页面';
  }
};

onMounted(async () => {
  console.log('CriticalPathChart mounted');
  await nextTick();
  await projectStore.fetchGanttData();
  await projectStore.fetchCriticalPath();
});

watchEffect(() => {
  if (projectStore.criticalPathGanttData.length && ganttContainer.value) {
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