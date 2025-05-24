<template>
  <div class="project-create-view">
    <div class="page-header">
      <h1>创建新项目</h1>
      <router-link to="/projects" class="btn btn-secondary">
        <i class="icon">←</i> 返回项目列表
      </router-link>
    </div>

    <div class="create-form">
      <form @submit.prevent="handleSubmit">
        <div class="form-section">
          <h2>基本信息</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="name">项目名称 *</label>
              <input
                type="text"
                id="name"
                v-model="form.name"
                required
                placeholder="请输入项目名称"
              />
            </div>
            <div class="form-group">
              <label for="status">项目状态</label>
              <select id="status" v-model="form.status">
                <option value="pending">待开始</option>
                <option value="in_progress">进行中</option>
                <option value="completed">已完成</option>
              </select>
            </div>
            <div class="form-group">
              <label for="estimated_duration">预计工期（天）</label>
              <input
                type="number"
                id="estimated_duration"
                v-model.number="form.estimated_duration"
                min="1"
                placeholder="预计工期"
              />
            </div>
          </div>
          <div class="form-group">
            <label for="description">项目描述</label>
            <textarea
              id="description"
              v-model="form.description"
              rows="4"
              placeholder="请输入项目描述"
            ></textarea>
          </div>
        </div>

        <div class="form-section">
          <h2>项目依赖</h2>
          <div class="dependencies-section">
            <div class="selected-dependencies">
              <h3>已选依赖项目</h3>
              <div v-if="selectedDependencies.length === 0" class="empty-state">
                暂无依赖项目
              </div>
              <div v-else class="dependency-list">
                <div 
                  v-for="dep in selectedDependencies" 
                  :key="dep.id"
                  class="dependency-item"
                >
                  <span>{{ dep.name }}</span>
                  <button 
                    type="button" 
                    @click="removeDependency(dep.id)"
                    class="remove-btn"
                  >
                    ×
                  </button>
                </div>
              </div>
            </div>
            <div class="available-projects">
              <h3>可选择的项目</h3>
              <div class="project-selector">
                <div 
                  v-for="project in availableProjects" 
                  :key="project.id"
                  class="project-option"
                  @click="addDependency(project)"
                >
                  <span>{{ project.name }}</span>
                  <span class="project-status" :class="project.status">
                    {{ getStatusText(project.status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? '创建中...' : '创建项目' }}
          </button>
          <router-link to="/projects" class="btn btn-secondary">
            取消
          </router-link>
        </div>
      </form>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import type { ProjectCreate, Project } from '@/types/index';

export default defineComponent({
  name: 'ProjectCreateView',
  setup() {
    const router = useRouter();
    const projectStore = useProjectStore();
    
    const loading = ref(false);
    const error = ref('');
    const selectedDependencies = ref<Project[]>([]);

    const form = reactive<ProjectCreate>({
      name: '',
      description: '',
      status: 'pending',
      estimated_duration: undefined,
    });

    const availableProjects = computed(() => 
      projectStore.projects.filter(p => 
        !selectedDependencies.value.find(dep => dep.id === p.id)
      )
    );

    const getStatusText = (status: string) => {
      const statusMap: Record<string, string> = {
        'pending': '待开始',
        'in_progress': '进行中',
        'completed': '已完成'
      };
      return statusMap[status] || status;
    };

    const addDependency = (project: Project) => {
      if (!selectedDependencies.value.find(dep => dep.id === project.id)) {
        selectedDependencies.value.push(project);
      }
    };

    const removeDependency = (projectId: number) => {
      selectedDependencies.value = selectedDependencies.value.filter(
        dep => dep.id !== projectId
      );
    };

    const handleSubmit = async () => {
      if (!form.name.trim()) {
        error.value = '请输入项目名称';
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        const project = await projectStore.createProject(form);
        
        // 如果有依赖项目，添加依赖关系
        if (selectedDependencies.value.length > 0) {
          const dependencyIds = selectedDependencies.value.map(dep => dep.id);
          await projectStore.addDependencies(project.id, dependencyIds);
        }

        router.push(`/projects/${project.id}`);
      } catch (err: any) {
        error.value = err.response?.data?.detail || '创建项目失败';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      projectStore.fetchProjects();
    });

    return {
      form,
      loading,
      error,
      selectedDependencies,
      availableProjects,
      getStatusText,
      addDependency,
      removeDependency,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.project-create-view {
  padding: 32px;
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.page-header h1 {
  color: #2c3e50;
  font-size: 32px;
  font-weight: 600;
  margin: 0;
}

.create-form {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.form-section {
  margin-bottom: 32px;
}

.form-section h2 {
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 20px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
}

.dependencies-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.selected-dependencies,
.available-projects {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 16px;
}

.selected-dependencies h3,
.available-projects h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 16px;
}

.empty-state {
  color: #999;
  text-align: center;
  padding: 20px;
}

.dependency-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dependency-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.remove-btn {
  background: #e74c3c;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.project-selector {
  max-height: 200px;
  overflow-y: auto;
}

.project-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.2s;
}

.project-option:hover {
  background: #f8f9fa;
}

.project-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.project-status.pending {
  background: #fff3cd;
  color: #856404;
}

.project-status.in_progress {
  background: #d1ecf1;
  color: #0c5460;
}

.project-status.completed {
  background: #d4edda;
  color: #155724;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn {
  padding: 12px 24px;
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

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px 16px;
  border-radius: 6px;
  margin-top: 16px;
}

.icon {
  font-style: normal;
}

@media (max-width: 768px) {
  .project-create-view {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .dependencies-section {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>