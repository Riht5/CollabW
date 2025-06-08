<template>
  <div class="personal-table container">
    <div v-if="loading" class="loading-state text-center p-md">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
    <div v-else-if="error" class="error-message text-danger p-md">
      {{ error }}
    </div>
    <div v-else-if="inProgressTasks.length === 0" class="empty-state text-center p-xl">
      <div class="empty-icon">📝</div>
      <h3>暂无进行中的任务</h3>
      <p class="text-muted">等待任务分配</p>
    </div>
    <div v-else class="todolist-container">
      <Todolist v-for="task in inProgressTasks" :key="task.id" :task="task" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useTaskStore } from '@/stores/task';
import { useUserStore } from '@/stores/user';
import Todolist from '@/components/tasks/TodoList.vue';

export default defineComponent({
  name: 'PersonalTable',
  components: {
    Todolist
  },
  setup() {
    const taskStore = useTaskStore();
    const userStore = useUserStore();
    const loading = ref(true);
    const error = ref('');

    const inProgressTasks = computed(() => {
      const currentUserTaskId = userStore.currentUser?.task_id;
      if (!currentUserTaskId) return [];
      
      return taskStore.tasks.filter(task => 
        !task.finished && 
        task.id === currentUserTaskId
      );
    });

    const loadUserTasks = async () => {
      loading.value = true;
      error.value = '';
      try {
        // 确保当前用户信息已加载
        if (!userStore.currentUser) {
          await userStore.fetchCurrentUser();
        }
        // 然后获取任务列表
        await taskStore.fetchTasks();
      } catch (err: any) {
        error.value = err.message || '加载任务失败';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadUserTasks();
    });

    return {
      loading,
      error,
      inProgressTasks
    };
  }
});
</script>

<style scoped>
@import '@/assets/styles/main.css';
.personal-table {
  padding: 16px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 24px;
}

.empty-icon {
  font-size: 40px;
  margin-bottom: 12px;
  color: #3498db;
}

.error-message {
  text-align: center;
  color: #dc3545;
  padding: 12px;
}

.todolist-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>