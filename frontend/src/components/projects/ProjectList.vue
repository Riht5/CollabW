<template>
  <div class="project-list">
    <div v-if="projects.length === 0" class="empty-state">
      <div class="empty-icon">📁</div>
      <h3>暂无项目</h3>
      <p>开始创建您的第一个项目吧！</p>
    </div>
    <div v-else class="grid grid-3">
      <div 
        v-for="project in projects" 
        :key="project.id" 
        class="card project-card"
        @click="viewProject(project.id)"
      >
        <div class="card-header d-flex justify-between align-start">
          <h4 class="mb-0">{{ project.name }}</h4>
          <span class="status-badge" :class="project.status">
            {{ getStatusText(project.status) }}
          </span>
        </div>
        
        <div class="card-body">
          <p v-if="project.description" class="text-secondary mb-md">
            {{ project.description }}
          </p>
          
          <div class="d-flex flex-column gap-sm">
            <div class="d-flex justify-between">
              <span class="text-muted">工期:</span>
              <span>{{ project.estimated_duration || '未设置' }} 天</span>
            </div>
            <div class="d-flex justify-between">
              <span class="text-muted">任务:</span>
              <span>{{ project.tasks?.length || 0 }} 个</span>
            </div>
            <div class="d-flex justify-between">
              <span class="text-muted">成员:</span>
              <span>{{ project.assigned_users?.length || 0 }} 人</span>
            </div>
          </div>
        </div>

        <div v-if="showActions" class="card-footer d-flex gap-sm" @click.stop>
          <button @click="$emit('edit', project)" class="btn btn-primary btn-sm flex-1">
            编辑
          </button>
          <button @click="$emit('delete', project.id)" class="btn btn-danger btn-sm">
            删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import type { Project } from '@/types/index';

export default defineComponent({
  name: 'ProjectList',
  props: {
    projects: {
      type: Array as () => Project[],
      required: true
    },
    showActions: {
      type: Boolean,
      default: false
    }
  },
  emits: ['edit', 'delete'],
  setup() {
    const router = useRouter();

    const getStatusText = (status: string) => {
      const statusMap: Record<string, string> = {
        'pending': '待开始',
        'in_progress': '进行中',
        'completed': '已完成'
      };
      return statusMap[status] || status;
    };

    const viewProject = (projectId: number) => {
      router.push(`/projects/${projectId}`);
    };

    return {
      getStatusText,
      viewProject,
    };
  },
});
</script>

<style scoped>
.project-card {
  cursor: pointer;
  transition: all 0.2s ease;
}

.project-card:hover {
  transform: translateY(-2px);
}
</style>