<template>
  <div class="task-list">
    <div v-if="tasks.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <h3>暂无任务</h3>
      <p>开始为项目添加任务吧！</p>
    </div>
    <div v-else class="d-flex flex-column gap-sm">
      <div v-for="task in sortedTasks" :key="task.id" class="task-item" :class="`workload-${task.workload}`">
        <!-- 左侧工作量指示竖线 -->
        <div class="workload-indicator" :class="task.workload"></div>
        
        <!-- 左侧复选框 -->
        <div class="task-checkbox">
          <input 
            type="checkbox" 
            :checked="task.finished" 
            @change="$emit('toggle-status', task)"
            class="checkbox-input"
          />
        </div>
        
        <!-- 任务内容 -->
        <div class="task-content">
          <div class="task-header">
            <h4 class="task-title" :class="{ completed: task.finished }">{{ task.name }}</h4>
          </div>
          
          <p v-if="task.description" class="task-description">{{ task.description }}</p>
        </div>
        
        <!-- 负责人信息 -->
        <div class="task-assignee">
          <div v-if="task.head_id && getHeadUser(task.head_id)" class="assignee-info">
            <div class="assignee-avatar">
              {{ getHeadUser(task.head_id)?.username?.charAt(0)?.toUpperCase() || '' }}
            </div>
            <div class="assignee-details">
              <span class="assignee-name">负责人：{{ getHeadUser(task.head_id)?.username }}</span>
              <span class="assignee-email">{{ getHeadUser(task.head_id)?.email }}</span>
            </div>
          </div>
          <div v-else class="no-assignee">
            <div class="no-assignee-avatar">?</div>
            <div class="assignee-details">
              <span class="assignee-name">未分配负责人</span>
              <span class="assignee-email"></span>
            </div>
          </div>
        </div>
        
        <!-- 右侧操作按钮 -->
        <div v-if="showActions" class="task-actions">
          <button @click="$emit('assign-members', task)" class="action-btn edit-btn" title="分配成员">
            <i class="icon">👥</i>
          </button>
          <button @click="$emit('edit', task)" class="action-btn edit-btn" title="编辑任务">
            <i class="icon">✏️</i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { getWorkloadText } from '@/utils/helpers';
import type { Task, User } from '@/types/index';

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
  setup(props) {
    const userStore = useUserStore();
    const users = ref<User[]>([]);

    const sortedTasks = computed(() => {
      return [...props.tasks].sort((a, b) => {
        // 未完成的任务排在前面，已完成的任务排在后面
        if (a.finished && !b.finished) return 1;
        if (!a.finished && b.finished) return -1;
        // 同样状态的任务保持原有顺序
        return 0;
      });
    });

    const getHeadUser = (headId: number) => {
      return users.value.find(user => user.id === headId);
    };

    onMounted(async () => {
      try {
        await userStore.fetchUsers();
        users.value = userStore.users;
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    });

    return {
      sortedTasks,
      getHeadUser,
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

.gap-sm {
  gap: 8px;
}

.task-item {
  display: flex;
  align-items: flex-start;
  background: white;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  padding: 16px;
  transition: all 0.2s;
  position: relative;
  gap: 16px;
}

.task-item:hover {
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.15);
  transform: translateY(-1px);
}

/* 工作量指示竖线 */
.workload-indicator {
  width: 4px;
  min-height: 60px;
  border-radius: 2px;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
}

.workload-indicator.light {
  background: var(--success-color);
}

.workload-indicator.medium {
  background: var(--warning-color);
}

.workload-indicator.heavy {
  background: var(--danger-color);
}

/* 复选框样式 */
.task-checkbox {
  display: flex;
  align-items: center;
  margin-left: 8px;
  align-self: center;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #007bff;
}

/* 任务内容区域 */
.task-content {
  flex: 1;
  min-width: 0;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.task-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  transition: all 0.2s;
}

.task-title.completed {
  text-decoration: line-through;
  color: #6c757d;
}

.workload-badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  color: white;
}

.workload-badge.light {
  background: #28a745;
}

.workload-badge.medium {
  background: #ffc107;
}

.workload-badge.heavy {
  background: #dc3545;
}

.task-description {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #6c757d;
  line-height: 1.4;
}

/* 负责人信息 */
.task-assignee {
  display: flex;
  align-items: center;
  min-width: 140px;
  align-self: center;
  margin-right: 8px;
}

.assignee-info,
.no-assignee {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.no-assignee {
  cursor: pointer;
  transition: all 0.2s;
}

.no-assignee:hover {
  opacity: 0.7;
}

.assignee-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--success-color));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.no-assignee-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e9ecef;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.assignee-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.assignee-name {
  font-weight: 500;
  font-size: 13px;
  color: #2c3e50;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.assignee-email {
  font-size: 11px;
  color: #6c757d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-assignee .assignee-name {
  color: #6c757d;
  font-style: italic;
}

.no-assignee .assignee-email {
  color: #adb5bd;
  font-size: 10px;
}

/* 右侧操作按钮 */
.task-actions {
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  align-self: center;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 14px;
}

.edit-btn {
  background: #c4c7c9;
  color: white;
}

.edit-btn:hover {
  background: #5a6268;
  transform: scale(1.05);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .task-item {
    padding: 12px;
    gap: 8px;
    flex-wrap: wrap;
  }
  
  .task-assignee {
    min-width: 100px;
    order: 2;
    flex: 1;
  }
  
  .task-actions {
    flex-direction: row;
    gap: 4px;
    order: 3;
    width: auto;
    justify-content: flex-end;
  }
  
  .assignee-avatar,
  .no-assignee-avatar {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
  
  .assignee-name {
    font-size: 12px;
  }
  
  .assignee-email {
    font-size: 10px;
  }
  
  .action-btn {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
  
  .task-title {
    font-size: 14px;
  }
}

.task-item.completed {
  opacity: 0.8;
}
</style>