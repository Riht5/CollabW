<template>
  <div class="personal-table container">
    <div class="page-header">
      <h1>个人工作台</h1>
    </div>

    <div v-if="loading" class="loading-state text-center p-md">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
    
    <div v-else-if="error" class="error-message text-danger p-md">
      {{ error }}
    </div>
    
    <div v-else class="personal-content">
      <!-- TodoList 区域 -->
      <div class="section">
        <h2>我的任务</h2>
        <div v-if="userTasks.length === 0" class="empty-state text-center p-xl">
          <div class="empty-icon">📝</div>
          <h3>暂无进行中的任务</h3>
          <p class="text-muted">等待任务分配</p>
        </div>
        <div v-else class="todolist-container">
          <Todolist v-for="task in userTasks" :key="task.id" :task="task" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useTaskStore } from '@/stores/task';
import { useUserStore } from '@/stores/user';
import { useProjectStore } from '@/stores/project';
import { useAuthStore } from '@/stores/auth';
import Todolist from '@/components/tasks/TodoList.vue';

export default defineComponent({
  name: 'PersonalTable',
  components: {
    Todolist
  },
  setup() {
    const router = useRouter();
    const taskStore = useTaskStore();
    const userStore = useUserStore();
    const projectStore = useProjectStore();
    const authStore = useAuthStore();
    
    const loading = ref(true);
    const error = ref('');

    const currentUser = computed(() => authStore.user);

    // 用户的任务
    const userTasks = computed(() => {
      const currentUserId = currentUser.value?.id;
      if (!currentUserId) return [];
      
      return taskStore.tasks.filter(task => 
        !task.finished && 
        task.id === currentUserId
      );
    });

    const loadUserData = async () => {
      loading.value = true;
      error.value = '';
      try {
        await taskStore.fetchTasks();
      } catch (err: any) {
        error.value = err.message || '加载数据失败';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadUserData();
    });

    return {
      loading,
      error,
      currentUser,
      userTasks
    };
  }
});
</script>

<style scoped>
.personal-table {
  padding: 16px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  color: #2c3e50;
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.personal-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.section h2 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
}

.todolist-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.project-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e9ecef;
  transition: all 0.2s;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.project-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.project-description {
  color: #6c757d;
  font-size: 14px;
  margin-bottom: 16px;
  line-height: 1.4;
}

.project-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
}

.stat-item .label {
  color: #6c757d;
  font-size: 13px;
}

.stat-item .value {
  color: #2c3e50;
  font-size: 13px;
  font-weight: 500;
}

.performance-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #dee2e6;
}

.performance-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 24px;
}

.user-info {
  flex: 1;
}

.user-info h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 18px;
}

.performance-score {
  text-align: center;
}

.performance-score .score {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #3498db;
  line-height: 1;
}

.performance-score .label {
  font-size: 12px;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.performance-rank {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rank-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.rank-label {
  font-size: 12px;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rank-value {
  font-size: 20px;
  font-weight: 700;
  color: #f39c12;
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

.btn-sm {
  padding: 8px 16px;
  font-size: 13px;
}

@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .performance-header {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .performance-rank {
    flex-direction: column;
    gap: 16px;
  }
}
</style>