<template>
  <div class="my-projects-view container">
    <div v-if="loading" class="loading-state text-center p-md">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
    
    <div v-else-if="error" class="error-message text-danger p-md">
      {{ error }}
    </div>
    
    <div v-else class="empty-state text-center p-xl">
      <div class="empty-icon">📁</div>
      <h3>暂未参与任何项目</h3>
      <p class="text-muted">等待项目分配</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import { useTaskStore } from '@/stores/task';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
  name: 'MyProjectsView',
  setup() {
    const router = useRouter();
    const projectStore = useProjectStore();
    const taskStore = useTaskStore();
    const authStore = useAuthStore();
    
    const loading = ref(true);
    const error = ref('');

    const currentUser = computed(() => authStore.user);

    const viewProject = (projectId: number) => {
      router.push(`/projects/${projectId}`);
    };

    const loadData = async () => {
      loading.value = true;
      error.value = '';
      try {
        await Promise.all([
          projectStore.fetchProjects(),
          taskStore.fetchTasks()
        ]);
        
        // 数据加载完成后立即检查并跳转
        const currentUserId = currentUser.value?.id;
        if (currentUserId) {
          // 获取用户的任务
          const userTasks = taskStore.tasks.filter(task => 
            task.id === currentUserId
          );
          
          if (userTasks.length > 0) {
            // 获取第一个任务的项目ID并立即跳转
            const projectId = userTasks[0].project_id;
            const project = projectStore.projects.find(p => p.id === projectId);
            
            if (project) {
              viewProject(projectId);
              return; // 跳转后直接返回，不需要设置loading为false
            }
          }
        }
      } catch (err: any) {
        error.value = err.message || '加载数据失败';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadData();
    });

    return {
      loading,
      error
    };
  }
});
</script>

<style scoped>
@import '@/assets/styles/main.css';

.my-project-view {
  padding: 16px;
}

.page-header h1 {
  color: #2c3e50;
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 24px 0;
}

.single-project {
  text-align: center;
  padding: 60px 20px;
}

.auto-redirect {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.redirect-icon {
  font-size: 48px;
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.loading-state,
.empty-state,
.error-message {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #3498db;
}
</style>