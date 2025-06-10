<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>仪表盘</h1>
    </div>

    <div class="dashboard-stats">
      <div class="stat-card">
        <div class="stat-icon">📁</div>
        <div class="stat-content">
          <h3>总项目数</h3>
          <div class="stat-number">{{ projects.length }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🚀</div>
        <div class="stat-content">
          <h3>进行中项目</h3>
          <div class="stat-number">{{ inProgressProjects }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <h3>已完成项目</h3>
          <div class="stat-number">{{ completedProjects }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-content">
          <h3>总任务数</h3>
          <div class="stat-number">{{ tasks.length }}</div>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="content-section">
        <div class="section-header">
          <h2>最近项目</h2>
          <router-link to="/projects" class="view-all-link">查看全部</router-link>
        </div>
        <ProjectList :projects="projects.slice(0, 4)" :show-actions="false" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { useProjectStore } from '@/stores/project';
import { useTaskStore } from '@/stores/task';
import { useAuthStore } from '@/stores/auth';
import ProjectList from '@/components/projects/ProjectList.vue';

export default defineComponent({
  name: 'DashboardView',
  components: {
    ProjectList,
  },
  setup() {
    const projectStore = useProjectStore();
    const taskStore = useTaskStore();
    const authStore = useAuthStore();

    const projects = computed(() => projectStore.projects);
    const tasks = computed(() => taskStore.tasks);

    const inProgressProjects = computed(() => 
      projects.value.filter(p => p.status === 'in_progress').length
    );

    const completedProjects = computed(() => 
      projects.value.filter(p => p.status === 'completed').length
    );

    // 用户角色判断 - 参考Sidebar的实现
    const isManager = computed(() => authStore.user?.role === 'manager');
    const isDirectorOrManager = computed(() => 
      ['director', 'manager'].includes(authStore.user?.role || '')
    );

    onMounted(() => {
      projectStore.fetchProjects();
      taskStore.fetchTasks();
    });

    return {
      projects,
      tasks,
      inProgressProjects,
      completedProjects,
      isManager,
      isDirectorOrManager,
    };
  },
});
</script>

<style scoped>
.dashboard {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.dashboard-header h1 {
  color: #2c3e50;
  font-size: 32px;
  font-weight: 600;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 48px;
}

.stat-content h3 {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.content-section {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

.view-all-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.view-all-link:hover {
  text-decoration: underline;
}

.btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.icon {
  font-style: normal;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .dashboard-stats {
    grid-template-columns: 1fr;
  }
  
  .content-section {
    padding: 24px;
  }
}
</style>