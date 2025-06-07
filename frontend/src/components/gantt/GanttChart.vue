<!-- frontend/src/components/gantt/GanttChart.vue -->
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
import { onMounted, onUnmounted, onActivated, ref, computed, watch } from 'vue';
import Gantt from 'frappe-gantt';
import { useGanttStore } from '@/stores/gantt';
import type { GanttTask } from '@/types/index';

const ganttStore = useGanttStore();
const gantt = ref<Gantt | null>(null);
const ganttContainer = ref<HTMLElement | null>(null);
const wrapperRef = ref<HTMLElement | null>(null);
const currentViewMode = ref<string>('Day'); // 默认 Day
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
  const validTasks = tasks.filter(task => task.id && !task.id.startsWith('__placeholder_'));
  const minDate = validTasks.length ? validTasks.reduce((min, task) => {
    const start = new Date(task.start);
    return start < min ? start : min;
  }, new Date(validTasks[0].start)) : new Date();
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
  const taskCount = Math.max(6, ganttStore.ganttAllData.length);
  const rowHeight = 50;
  const headerHeight = 120;
  const minHeight = 400;
  return Math.max(minHeight, taskCount * rowHeight + headerHeight);
});

// 获取时间轴范围，参考旧版固定年度
const getTimelineRange = () => {
  const tasks = ganttStore.ganttAllData;
  if (!tasks.length) {
    const currentYear = new Date().getFullYear();
    return { startDate: `${currentYear}-01-01`, endDate: `${currentYear}-12-31` };
  }
  const taskYears = tasks.map((task: GanttTask) => new Date(task.start).getFullYear());
  const minYear = Math.min(...taskYears);
  return { startDate: `${minYear}-01-01`, endDate: `${minYear}-12-31` };
};

const scrollToToday = () => {
  if (gantt.value) {
    gantt.value.scroll_current();
    console.log('滚动至今天');
  }
};

const toggleViewModeDropdown = () => {
  showViewModeDropdown.value = !showViewModeDropdown.value;
};

const changeViewMode = (mode: string) => {
  if (!ganttContainer.value || !ganttStore.ganttAllData.length) {
    console.warn('甘特图容器或数据未就绪');
    return;
  }
  try {
    ganttContainer.value.innerHTML = '';
    gantt.value = null;
    const { startDate } = getTimelineRange();
    const tasksWithPadding = padGanttTasks(ganttStore.ganttAllData);
    gantt.value = new Gantt(ganttContainer.value, tasksWithPadding, {
      view_mode: mode,
      date_format: 'YYYY-MM-DD',
      bar_height: 32,
      padding: 24,
      column_width: mode === 'Day' ? 30 : mode === 'Week' ? 50 : mode === 'Month' ? 100 : 150,
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
    currentViewMode.value = mode;
    showViewModeDropdown.value = false;
    console.log('视图切换至:', mode);
  } catch (err) {
    console.error('视图切换失败:', err);
    ganttStore.error = '视图切换失败，请刷新页面重试';
  }
};

const refreshGantt = async () => {
  try {
    await ganttStore.fetchGanttData();
    console.log('刷新甘特图数据:', ganttStore.ganttAllData);
    if (ganttStore.ganttAllData.length > 0) {
      if (gantt.value) {
        gantt.value.refresh(padGanttTasks(ganttStore.ganttAllData));
        console.log('甘特图刷新成功:', ganttStore.ganttAllData);
      } else {
        console.warn('Gantt 实例未初始化，重新初始化');
        initializeGantt();
      }
    }
  } catch (err) {
    console.error('刷新甘特图数据失败:', err);
    ganttStore.error = '刷新甘特图数据失败，请重试';
  }
};

// 优化的甘特图初始化
const initializeGantt = () => {
  if (!ganttContainer.value || !ganttStore.ganttAllData.length) {
    console.warn('甘特图容器或数据未就绪');
    return;
  }
  ganttContainer.value.innerHTML = '';
  gantt.value = null;
  try {
    const { startDate } = getTimelineRange();
    const tasksWithPadding = padGanttTasks(ganttStore.ganttAllData);
    gantt.value = new Gantt(ganttContainer.value, tasksWithPadding, {
      view_mode: currentViewMode.value,
      date_format: 'YYYY-MM-DD',
      bar_height: 32,
      padding: 24,
      column_width: currentViewMode.value === 'Day' ? 30 : currentViewMode.value === 'Week' ? 50 : currentViewMode.value === 'Month' ? 100 : 150,
      scroll_to: startDate,
      language: 'zh-cn',
      infinite_padding: false, // 限制无限扩展
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
  console.log('项目甘特图组件挂载');
  try {
    await ganttStore.fetchGanttData();
    console.log('获取甘特图数据:', ganttStore.ganttAllData);
  } catch (err) {
    console.error('获取甘特图数据失败:', err);
    ganttStore.error = '加载甘特图数据失败，请检查网络';
  }
});

onActivated(async () => {
  console.log('项目甘特图组件激活');
  try {
    await ganttStore.fetchGanttData();
    console.log('激活时获取甘特图数据:', ganttStore.ganttAllData);
  } catch (err) {
    console.error('激活时获取甘特图数据失败:', err);
    ganttStore.error = '加载甘特图数据失败，请检查网络';
  }
});

watch(
  () => [ganttStore.ganttAllData, ganttContainer.value],
  ([newData, container]) => {
    console.log('Watch 触发，数据长度:', newData.length, '容器:', !!container, 'Gantt 实例:', !!gantt.value);
    if (newData.length && container) {
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
  console.log('项目甘特图组件卸载');
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