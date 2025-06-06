<template>
  <div class="task-list">
    <div v-if="tasks.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <h3>暂无任务</h3>
      <p>开始为项目添加任务吧！</p>
    </div>
    <div v-else class="d-flex flex-column gap-md">
      <div v-for="task in tasks" :key="task.id" class="card">
        <div class="card-body">
          <div class="d-flex justify-between align-start mb-md">
            <h4 class="mb-0">{{ task.name }}</h4>
            <div class="d-flex gap-sm">
              <span class="workload-badge" :class="task.workload">
                {{ getWorkloadText(task.workload) }}
              </span>
              <span class="status-badge" :class="{ completed: task.finished, pending: !task.finished }">
                {{ task.finished ? '已完成' : '进行中' }}
              </span>
            </div>
          </div>
          
          <p v-if="task.description" class="text-secondary mb-md">
            {{ task.description }}
          </p>
          
          <div class="d-flex justify-between text-sm mb-md">
            <div v-if="task.head">
              <span class="text-muted">负责人:</span>
              <span class="ml-sm">{{ task.head.username }}</span>
            </div>
            <div>
              <span class="text-muted">工作量权重:</span>
              <span class="ml-sm">{{ getWorkloadWeight(task.workload) }}</span>
            </div>
          </div>

          <div v-if="showActions" class="d-flex gap-sm">
            <button @click="$emit('edit', task)" class="btn btn-primary btn-sm">
              编辑
            </button>
            <button @click="$emit('assign-members', task)" class="btn btn-success btn-sm">
              分配成员
            </button>
            <button @click="$emit('toggle-status', task.id)" class="btn btn-secondary btn-sm">
              {{ task.finished ? '标记未完成' : '标记完成' }}
            </button>
            <button @click="$emit('delete', task.id)" class="btn btn-danger btn-sm">
              删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { Task } from '@/types/index';

export default defineComponent({
  name: 'TaskList',
  props: {
    tasks: {
      type: Array as () => Task[],
      required: true
    },
    showActions: {
      type: Boolean,
      default: true
    }
  },
  emits: ['edit', 'delete', 'toggle-status', 'assign-members'],
  setup() {
    const getWorkloadText = (workload: string) => {
      const workloadMap: Record<string, string> = {
        'light': '轻量',
        'medium': '中等',
        'heavy': '重量'
      };
      return workloadMap[workload] || workload;
    };

    const getWorkloadWeight = (workload: string) => {
      const weightMap: Record<string, number> = {
        'light': 1,
        'medium': 2,
        'heavy': 3
      };
      return weightMap[workload] || 1;
    };

    return {
      getWorkloadText,
      getWorkloadWeight,
    };
  },
});
</script>

<style scoped>
.task-list {
  width: 100%;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 48px;
  color: #007bff;
  margin-bottom: 16px;
}

.card {
  background: white;
  border-radius: 8px;
  border: 1px solid #eee;
  transition: all 0.2s;
}

.card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.1);
}

.workload-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.text-secondary {
  color: #6c757d;
}

.text-muted {
  color: #868e96;
}

.ml-sm {
  margin-left: 8px;
}

.mb-md {
  margin-bottom: 16px;
}

.gap-md {
  gap: 16px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  border: none;
}

.btn-success {
  background-color: #28a745;
  color: white;
  border: none;
}
</style>