import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import type { GanttTask } from '@/types/index';

export const useGanttStore = defineStore('gantt', () => {
  const ganttAllData = ref<GanttTask[]>([]);
  const criticalPathGanttData = ref<GanttTask[]>([]);
  const criticalPathMeta = ref<{
    critical_path: number[];
    total_duration_days: number;
    weights: { [key: number]: number };
  } | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchGanttData = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/gantt/project-data');
      ganttAllData.value = response.data.map((project: any) => ({
        id: `project_${project.id}`,
        name: project.name,
        start: project.start_time,
        end: project.end_time,
        progress: project.progress,
        dependencies: project.dependencies.map((depId: number) => `project_${depId}`).join(','),
        custom_class: `status-${project.status.replace('_', '-')}`
      }));
      console.log('Gantt data fetched:', ganttAllData.value);
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch gantt data';
      console.error('Gantt data fetch failed:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchCriticalPath = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('/api/gantt/critical-path');
      criticalPathMeta.value = response.data;
      if (criticalPathMeta.value && ganttAllData.value.length) {
        const { critical_path } = criticalPathMeta.value;
        criticalPathGanttData.value = ganttAllData.value.filter(task => {
          const taskId = parseInt(task.id.replace('project_', ''));
          return critical_path.includes(taskId);
        });
      }
      console.log('Critical path fetched:', criticalPathMeta.value);
      console.log('Critical path gantt data:', criticalPathGanttData.value);
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch critical path';
      console.error('Critical path fetch failed:', err);
    } finally {
      loading.value = false;
    }
  };

  return {
    ganttAllData,
    criticalPathGanttData,
    criticalPathMeta,
    loading,
    error,
    fetchGanttData,
    fetchCriticalPath
  };
});
