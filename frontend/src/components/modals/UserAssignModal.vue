<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>为任务"{{ preSelectedTask.name }}"分配成员</h2>
        <button @click="closeModal" class="close-btn">×</button>
      </div>
      
      <div class="modal-body">
        <!-- 显示当前选中的任务信息 -->
        <div class="selected-task-info">
          <h3>任务信息</h3>
          <div class="task-info-card">
            <h4>{{ preSelectedTask.name }}</h4>
            <p>{{ preSelectedTask.description || '无描述' }}</p>
            <span class="workload-badge" :class="preSelectedTask.workload">
              {{ getWorkloadText(preSelectedTask.workload) }}
            </span>
          </div>
        </div>

        <div class="search-section">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索用户..."
            class="search-input"
          />
        </div>
        
        <div class="users-section">
          <h3>可分配用户</h3>
          <div class="user-list">
            <div 
              v-for="user in filteredUsers" 
              :key="user.id"
              class="user-item"
              :class="{ selected: isUserSelected(user.id) }"
              @click="toggleUser(user.id)"
            >
              <div class="user-avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
              <div class="user-info">
                <h4>{{ user.username }}</h4>
                <p>{{ user.email }}</p>
                <span class="role-badge" :class="user.role">{{ getRoleText(user.role) }}</span>
              </div>
              <div class="checkbox" @click.stop>
                <input 
                  type="checkbox" 
                  :checked="isUserSelected(user.id)"
                  @change="toggleUser(user.id)"
                />
              </div>
            </div>
          </div>
        </div>
        
        <div class="selected-section">
          <h3>已选择用户 ({{ selectedUsers.length }})</h3>
          <div class="selected-users">
            <div 
              v-for="userId in selectedUsers" 
              :key="userId"
              class="selected-user"
            >
              <span>{{ getUserById(userId)?.username }}</span>
              <button @click="removeUser(userId)" class="remove-btn">×</button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn btn-secondary">取消</button>
        <button 
          @click="assignUsers" 
          class="btn btn-primary" 
          :disabled="loading || selectedUsers.length === 0"
        >
          {{ loading ? '分配中...' : `分配到任务 (${selectedUsers.length})` }}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, toRef } from 'vue';
import { useUserStore } from '@/stores/user';
import { useTaskStore } from '@/stores/task';
import { useProjectStore } from '@/stores/project';
import type { User, Task } from '@/types/index';

export default defineComponent({
  name: 'UserAssignModal',
  props: {
    projectId: {
      type: Number,
      required: true,
    },
    assignedUsers: {
      type: Array as () => User[],
      default: () => [],
    },
    preSelectedTask: {
      type: Object as () => Task,
      required: true,
    },
  },
  emits: ['close', 'assigned'],
  setup(props, { emit }) {
    const userStore = useUserStore();
    const taskStore = useTaskStore();
    const projectStore = useProjectStore();
    
    const loading = ref(false);
    const searchQuery = ref('');
    const selectedUsers = ref<number[]>([]);

    const filteredUsers = computed(() => {
      let users = userStore.users.filter(user => 
        !props.assignedUsers.find(assigned => assigned.id === user.id)
      );
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        users = users.filter(user => 
          user.username.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        );
      }
      
      return users;
    });

    const getRoleText = (role: string) => {
      const roleMap: Record<string, string> = {
        'director': '总监',
        'manager': '经理',
        'user': '员工'
      };
      return roleMap[role] || role;
    };

    const getWorkloadText = (workload: string) => {
      const workloadMap: Record<string, string> = {
        'light': '轻量',
        'medium': '中等',
        'heavy': '重量'
      };
      return workloadMap[workload] || workload;
    };

    const isUserSelected = (userId: number) => {
      return selectedUsers.value.includes(userId);
    };

    const toggleUser = (userId: number) => {
      const index = selectedUsers.value.indexOf(userId);
      if (index > -1) {
        selectedUsers.value.splice(index, 1);
      } else {
        selectedUsers.value.push(userId);
      }
    };

    const removeUser = (userId: number) => {
      const index = selectedUsers.value.indexOf(userId);
      if (index > -1) {
        selectedUsers.value.splice(index, 1);
      }
    };

    const getUserById = (userId: number) => {
      return userStore.users.find(user => user.id === userId);
    };

    const assignUsers = async () => {
      if (selectedUsers.value.length === 0) return;
      
      loading.value = true;
      try {
        // 直接使用预选任务的ID
        await taskStore.assignUsersToTask(props.preSelectedTask.id, selectedUsers.value);
        emit('assigned');
      } catch (error) {
        console.error('分配用户到任务失败:', error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      userStore.fetchUsers();
    });

    const closeModal = () => {
      emit('close');
    };

    return {
      loading,
      searchQuery,
      selectedUsers,
      preSelectedTask: toRef(props, 'preSelectedTask'),
      filteredUsers,
      getRoleText,
      getWorkloadText,
      isUserSelected,
      toggleUser,
      removeUser,
      getUserById,
      assignUsers,
      closeModal,
    };
  },
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  background: #f0f0f0;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.selected-task-info {
  margin-bottom: 24px;
}

.task-info-card {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.task-info-card h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.task-info-card p {
  margin: 0 0 12px 0;
  color: #666;
  font-size: 14px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
}

.users-section h3,
.selected-section h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 16px;
}

.user-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 8px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.2s;
}

.user-item:hover,
.user-item.selected {
  background: #f8f9fa;
}

.user-item:last-child {
  border-bottom: none;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.user-info {
  flex: 1;
}

.user-info h4 {
  margin: 0 0 4px 0;
  color: #2c3e50;
  font-size: 14px;
}

.user-info p {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 12px;
}

.role-badge {
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 500;
}

.role-badge.director {
  background: #ff6b6b;
  color: white;
}

.role-badge.manager {
  background: #4ecdc4;
  color: white;
}

.role-badge.user {
  background: #95a5a6;
  color: white;
}

.checkbox input {
  width: 16px;
  height: 16px;
}

.selected-users {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.selected-user {
  background: #e3f2fd;
  color: #1976d2;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.remove-btn {
  background: #f44336;
  color: white;
  border: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #eee;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
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
</style>