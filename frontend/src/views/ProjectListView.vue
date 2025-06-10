<template>
  <div class="container" style="margin-top: 32px;">
    <div class="page-header">
      <h1>项目管理</h1>
      <div class="header-actions">
        <!-- 仅 Manager 可见创建项目按钮 -->
        <router-link 
          v-if="isManager"
          to="/projects/create" 
          class="btn btn-primary"
        >
          <i class="icon">➕</i> 创建项目
        </router-link>
      </div>
    </div>

    <div class="card mb-lg">
      <div class="card-body">
        <div class="d-flex gap-lg align-center">
          <div class="form-group mb-0">
            <label class="form-label">状态筛选:</label>
            <select class="form-select" v-model="statusFilter" @change="filterProjects">
              <option value="">全部状态</option>
              <option value="pending">待开始</option>
              <option value="in_progress">进行中</option>
              <option value="completed">已完成</option>
            </select>
          </div>
          <div class="form-group mb-0 flex-1">
            <label class="form-label">搜索项目:</label>
            <div class="search-input">
              <input 
                class="form-input"
                type="text" 
                v-model="searchQuery" 
                @input="filterProjects"
                placeholder="搜索项目名称..."
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <ProjectList 
      :projects="filteredProjects" 
      :show-actions="isManager"
      @edit="editProject"
      @delete="deleteProject"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import { useAuthStore } from '@/stores/auth';
import ProjectList from '@/components/projects/ProjectList.vue';
import type { Project } from '@/types/index';

export default defineComponent({
  name: 'ProjectListView',
  components: {
    ProjectList,
  },
  setup() {
    const router = useRouter();
    const projectStore = useProjectStore();
    const authStore = useAuthStore();
    
    const statusFilter = ref('');
    const searchQuery = ref('');

    // 用户角色判断
    const isManager = computed(() => authStore.user?.role === 'manager');

    const filteredProjects = computed(() => {
      let projects = projectStore.projects;
      
      if (statusFilter.value) {
        projects = projects.filter(p => p.status === statusFilter.value);
      }
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        projects = projects.filter(p => 
          p.name.toLowerCase().includes(query) ||
          p.description?.toLowerCase().includes(query)
        );
      }
      
      return projects;
    });

    const filterProjects = () => {
      // 触发响应式更新
    };

    const editProject = (project: Project) => {
      router.push(`/projects/${project.id}`);
    };

    const deleteProject = async (projectId: number) => {
      if (confirm('确定要删除此项目吗？此操作不可恢复。')) {
        try {
          await projectStore.deleteProject(projectId);
        } catch (error) {
          console.error('删除项目失败:', error);
        }
      }
    };

    onMounted(() => {
      projectStore.fetchProjects();
    });

    return {
      statusFilter,
      searchQuery,
      filteredProjects,
      filterProjects,
      editProject,
      deleteProject,
      isManager,
    };
  },
});
</script>

<style scoped>
@media (max-width: 768px) {
  .card-body .d-flex {
    flex-direction: column;
    gap: var(--spacing-md);
  }
}
</style>