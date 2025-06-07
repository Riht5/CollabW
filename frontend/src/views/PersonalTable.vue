<template>
  <div class="personal-table container">
    <div v-if="loading" class="loading-state text-center p-md">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
    <div v-else-if="error" class="error-message text-danger p-md">
      {{ error }}
    </div>
    <div v-else-if="!currentTask" class="empty-state text-center p-xl">
      <div class="empty-icon">📝</div>
      <h3>暂无任务</h3>
      <p class="text-muted">等待任务分配</p>
    </div>
    <Todolist v-else :task="currentTask" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useTaskStore } from '@/stores/task';
import Todolist from '@/components/tasks/Todolist.vue';
import type { Task } from '@/types/index';

export default defineComponent({
  name: 'PersonalTable',
  components: {
    Todolist
  },
  setup() {
    const taskStore = useTaskStore();
    const loading = ref(true);
    const error = ref('');
    const currentTask = ref<Task | null>(null);

    const loadUserTask = async () => {
      loading.value = true;
      error.value = '';
      try {
        await taskStore.fetchTasks();
        // 获取第一个未完成的任务
        const unfinishedTask = taskStore.tasks.find(task => !task.finished);
        currentTask.value = unfinishedTask || null;
      } catch (err: any) {
        error.value = err.message || '加载任务失败';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadUserTask();
    });

    return {
      loading,
      error,
      currentTask
    };
  }
});
</script>

<style scoped>
@import '@/assets/styles/main.css';
.personal-table {
  padding: var(--spacing-lg);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xl);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
}

.error-message {
  text-align: center;
  color: var(--danger-color);
}
</style>