<template>
  <div class="gantt-wrapper" ref="wrapperRef">
    <div class="gantt-toolbar">
      <span class="gantt-title">📊 项目甘特图</span>
      <div class="toolbar-actions">
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
        <button class="btn btn-secondary" @click="refreshGantt" title="刷新数据" :disabled="ganttStore.loading">
          🔄 {{ ganttStore.loading ? '加载中...' : '刷新' }}
        </button>
      </div>
    </div>
    
    <div v-if="ganttStore.loading" class="loading">
      正在加载甘特图数据...
    </div>
    <div v-else-if="ganttStore.error" class="error">
      {{ ganttStore.error }}
      <br><small>请检查网络连接或联系管理员</small>
    </div>
    <div v-else-if="!ganttStore.ganttAllData.length" class="empty">
      📋 暂无项目数据
      <br><small>请先创建一些进行中或已完成的项目</small>
    </div>
    <div v-else class="gantt-scroll-container">
      <div 
        class="gantt-container gantt-container-main" 
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

// 优化的任务填充函数
const padGanttTasks = (tasks: GanttTask[], minRows = 6): GanttTask[] => {
  if (tasks.length >= minRows) return tasks;
  
  const baseDate = tasks.length > 0 ? tasks[0].start : new Date().toISOString().split('T')[0];
  const placeholders = Array.from({ length: minRows - tasks.length }).map((_, i) => ({
    id: `__placeholder_${i}`,
    name: '',
    start: baseDate,
    end: baseDate,
    progress: 0,
    dependencies: '',
    custom_class: 'placeholder-task'
  }));
  
  return [...tasks, ...placeholders];
};

// 动态计算容器高度
const containerHeight = computed(() => {
  const taskCount = Math.max(6, ganttStore.ganttAllData.length);
  const rowHeight = 50; // 增加行高以改善视觉效果
  const headerHeight = 120;
  const minHeight = 400;
  
  return Math.max(minHeight, taskCount * rowHeight + headerHeight);
});

// 获取时间轴范围
const getTimelineRange = () => {
  if (!ganttStore.ganttAllData.length) {
    const currentYear = new Date().getFullYear();
    return { startDate: `${currentYear}-01-01`, endDate: `${currentYear}-12-31` };
  }
  
  const dates = ganttStore.ganttAllData.flatMap(task => [
    new Date(task.start),
    new Date(task.end)
  ]);
  
  const minDate = new Date(Math.min(...dates.map(d => d.getTime())));
  const maxDate = new Date(Math.max(...dates.map(d => d.getTime())));
  
  // 添加一些缓冲时间
  minDate.setMonth(minDate.getMonth() - 1);
  maxDate.setMonth(maxDate.getMonth() + 1);
  
  return {
    startDate: minDate.toISOString().split('T')[0],
    endDate: maxDate.toISOString().split('T')[0]
  };
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
      gantt.value.refresh(padGanttTasks(ganttStore.ganttAllData));
    } catch (err) {
      console.error('Failed to change view mode:', err);
    }
  } else {
    console.warn('Gantt instance not initialized');
  }
};

const refreshGantt = async () => {
  if (gantt.value) {
    await ganttStore.fetchGanttData();
    if (ganttStore.ganttAllData.length > 0) {
      gantt.value.refresh(padGanttTasks(ganttStore.ganttAllData));
      console.log('Gantt refreshed:', ganttStore.ganttAllData);
    }
  }
};

// 优化的甘特图初始化
const initializeGantt = () => {
  if (!ganttContainer.value || !ganttStore.ganttAllData.length) {
    console.warn('Gantt container or data not ready');
    return;
  }
  
  ganttContainer.value.innerHTML = '';
  
  try {
    const { startDate } = getTimelineRange();
    const tasksWithPadding = padGanttTasks(ganttStore.ganttAllData);
    
    gantt.value = new Gantt(ganttContainer.value, tasksWithPadding, {
      view_mode: currentViewMode.value,
      date_format: 'YYYY-MM-DD',
      bar_height: 32,
      padding: 24,
      column_width: 120,
      scroll_to: startDate,
      language: 'zh-cn',
      custom_popup_html: (task: GanttTask) => {
        if (task.custom_class?.includes('placeholder')) return '';
        
        const startDate = new Date(task.start).toLocaleDateString('zh-CN');
        const endDate = new Date(task.end).toLocaleDateString('zh-CN');
        const duration = Math.ceil((new Date(task.end).getTime() - new Date(task.start).getTime()) / (1000 * 60 * 60 * 24));
        
        return `
          <div style="padding: 12px; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <h4 style="margin: 0 0 8px 0; color: #1f2937;">${task.name}</h4>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">开始: ${startDate}</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">结束: ${endDate}</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">工期: ${duration} 天</p>
            <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">进度: ${task.progress}%</p>
          </div>
        `;
      },
      on_click: (task: GanttTask) => {
        if (!task.custom_class?.includes('placeholder')) {
          console.log('点击任务:', task);
        }
      },
      on_date_change: (task: GanttTask, start: string, end: string) => {
        console.log('日期变更:', task.name, start, end);
      },
      on_progress_change: (task: GanttTask, progress: number) => {
        console.log('进度变更:', task.name, progress);
      }
    });
    
    console.log('甘特图初始化成功');
  } catch (err) {
    console.error('甘特图初始化失败:', err);
    ganttStore.error = '甘特图初始化失败，请刷新页面重试';
  }
};

onMounted(async () => {
  console.log('GanttChartTest mounted');
  await nextTick();
  await ganttStore.fetchGanttData();
});

watchEffect(() => {
  if (ganttStore.ganttAllData.length && ganttContainer.value) {
    initializeGantt();
  }
});

onUnmounted(() => {
  gantt.value = null;
  if (ganttContainer.value) {
    ganttContainer.value.innerHTML = '';
  }
  console.log('GanttChartTest unmounted');
});
</script>

<style scoped>
@import '@/assets/styles/gantt.css';

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