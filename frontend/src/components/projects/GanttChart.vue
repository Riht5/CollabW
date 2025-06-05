<!-- frontend/src/components/projects/GanttChart.vue -->
<template>
  <div class="gantt-wrapper">
    <div class="gantt-toolbar">
      <span class="gantt-title">📅 Project Gantt Chart</span>
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
        <button class="btn btn-secondary" @click="refreshGantt">Refresh Gantt</button>
      </div>
    </div>
    <div class="gantt-scroll-container">
      <div class="gantt-container" id="gantt-container"></div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, nextTick, ref } from 'vue'
import Gantt from 'frappe-gantt'

// 模拟项目数据
const projects = [
  {
    id: 1,
    name: 'Website Redesign',
    status: 'in_progress',
    start_time: '2025-06-01T00:00:00',
    end_time: '2025-07-15T23:59:59',
    progress_records: [{ date: '2025-06-30', progress: 0.4 }],
    dependencies: []
  },
  {
    id: 2,
    name: 'Mobile App Development',
    status: 'completed',
    start_time: '2025-05-01T00:00:00',
    end_time: '2025-06-30T23:59:59',
    progress_records: [{ date: '2025-06-30', progress: 1.0 }],
    dependencies: [1]
  },
  {
    id: 3,
    name: 'Database Migration',
    status: 'in_progress',
    start_time: '2025-07-01T00:00:00',
    end_time: '2025-08-15T23:59:59',
    progress_records: [{ date: '2025-07-15', progress: 0.2 }],
    dependencies: [2]
  },
  {
    id: 4,
    name: 'Marketing Campaign',
    status: 'in_progress',
    start_time: '2025-06-15T00:00:00',
    end_time: '2025-09-30T23:59:59',
    progress_records: [{ date: '2025-07-15', progress: 0.3 }],
    dependencies: []
  },
  {
    id: 5,
    name: 'Cloud Infrastructure Setup',
    status: 'pending',
    start_time: null,
    end_time: null,
    progress_records: [],
    dependencies: [3]
  },
  {
    id: 6,
    name: 'User Training Program',
    status: 'in_progress',
    start_time: '2025-08-01T00:00:00',
    end_time: '2025-10-31T23:59:59',
    progress_records: [{ date: '2025-08-15', progress: 0.1 }],
    dependencies: [4]
  },
  {
    id: 7,
    name: 'Security Audit',
    status: 'in_progress',
    start_time: '2025-09-01T00:00:00',
    end_time: '2025-10-15T23:59:59',
    progress_records: [{ date: '2025-09-15', progress: 0.25 }],
    dependencies: [6]
  },
  {
    id: 8,
    name: 'Final Deployment',
    status: 'pending',
    start_time: null,
    end_time: null,
    progress_records: [],
    dependencies: [3, 6, 7]
  }
]

// 映射到 Frappe Gantt 任务格式
const tasks = projects
  .filter(p => p.start_time && p.end_time)
  .map(p => ({
    id: `project_${p.id}`,
    name: p.name,
    start: p.start_time!.split('T')[0],
    end: p.end_time!.split('T')[0],
    progress: p.progress_records.length
      ? Math.round(
          p.progress_records.reduce((sum: number, r: any) => sum + r.progress, 0) /
            p.progress_records.length * 100
        )
      : 0,
    dependencies: p.dependencies.map(d => `project_${d}`).join(','),
    custom_class: `status-${p.status.replace('_', '-')}`
  }))

// 计算时间轴范围（整年）
const taskYears = tasks.map(task => new Date(task.start).getFullYear())
const year = taskYears.length ? Math.min(...taskYears) : 2025
const startDate = `${year}-01-01`

const gantt = ref(null)
const currentViewMode = ref('Month')
const showViewModeDropdown = ref(false)
const viewModes = ['Day', 'Week', 'Month', 'Year']

const scrollToToday = () => {
  if (gantt.value) {
    gantt.value.scroll_current()
    console.log('Scrolled to today')
  }
}

const toggleViewModeDropdown = () => {
  showViewModeDropdown.value = !showViewModeDropdown.value
}

const changeViewMode = (mode: string) => {
  if (gantt.value) {
    gantt.value.change_view_mode(mode)
    currentViewMode.value = mode
    showViewModeDropdown.value = false
    console.log('View changed to:', mode)
  }
}

const refreshGantt = () => {
  if (gantt.value) {
    gantt.value.refresh(tasks)
    console.log('Gantt refreshed')
  }
}

onMounted(async () => {
  console.log('GanttChart mounted, tasks:', tasks)
  await nextTick()
  try {
    gantt.value = new Gantt('#gantt-container', tasks, {
      view_mode: 'Month',
      date_format: 'YYYY-MM-DD',
      bar_height: 25,
      padding: 15,
      column_width: 100,
      scroll_to: startDate,
      infinite_padding: false,
      today_button: false,
      view_mode_select: false,
      on_click: (task: any) => console.log('Clicked task:', task),
      on_date_change: (task: any, start: string, end: string) => console.log('Date changed:', task, start, end),
      on_progress_change: (task: any, progress: number) => console.log('Progress:', task, progress)
    })
    console.log('Gantt initialized')
  } catch (err) {
    console.error('Gantt init failed:', err)
  }
})
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
.gantt-wrapper {
  display: flex;
  flex-direction: column;
  background: #f4f6f8;
  border-radius: 8px;
  border: 1px solid #ccc;
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
}
.gantt-container {
  width: 100%;
  min-width: 1200px;
  height: 700px;
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
</style>