<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h3>分配成员</h3>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">

        <div class="current-assignees" v-if="currentAssignees.length > 0">
          <h5>当前分配成员 ({{ currentAssignees.length }})</h5>
          <div class="assignee-list">
            <div v-for="user in currentAssignees" :key="user.id" class="assignee-item current">
              <div class="user-avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
              <div class="user-info">
                <span class="user-name">{{ user.username }}</span>
                <span class="user-email">{{ user.email }}</span>
                <div class="user-badges">
                  <span class="user-role" :class="user.role">{{ getRoleText(user.role) }}</span>
                  <span v-if="isTaskHead(user)" class="head-badge">负责人</span>
                </div>
              </div>
              <button @click="removeAssignee(user)" class="remove-btn" title="移除">×</button>
            </div>
          </div>
        </div>

        <div class="available-users">
          <h5>可分配成员</h5>
          <div v-if="loading" class="loading-state">加载中...</div>
          <div v-else-if="availableUsers.length === 0" class="empty-state">暂无可分配成员</div>
          <div v-else>
            <div class="user-search">
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="搜索成员..."
                class="search-input"
              />
            </div>
            
            <div class="user-list">
              <div 
                v-for="user in filteredUsers" 
                :key="user.id"
                class="user-item"
                @click="addAssignee(user)"
              >
                <div class="user-avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
                <div class="user-info">
                  <span class="user-name">{{ user.username }}</span>
                  <span class="user-email">{{ user.email }}</span>
                  <span class="user-role" :class="user.role">{{ getRoleText(user.role) }}</span>
                </div>
                <button class="add-btn" title="添加">+</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn btn-secondary">取消</button>
        <button @click="saveAssignments" class="btn btn-primary" :disabled="saving">
          {{ saving ? '保存中...' : '保存分配' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useTaskStore } from '@/stores/task';
import { useUserStore } from '@/stores/user';
import type { User, Task } from '@/types/index';

export default defineComponent({
  name: 'UserAssignModal',
  props: {
    projectId: {
      type: [String, Number],
      required: true
    },
    assignedUsers: {
      type: Array as () => User[],
      required: true
    },
    preSelectedTask: {
      type: Object as () => Task,
      required: true
    }
  },
  emits: ['close', 'assigned'],
  setup(props, { emit }) {
    const taskStore = useTaskStore();
    const userStore = useUserStore();
    
    const searchQuery = ref('');
    const saving = ref(false);
    const loading = ref(false);
    const currentAssignees = ref<User[]>([]);
    const setAsHead = ref(false);

    // 使用用户store中的用户数据，如果为空则使用传入的项目成员
    const availableUsers = computed(() => {
      return userStore.users.length > 0 ? userStore.users : props.assignedUsers;
    });

    // 初始化当前分配的成员
    onMounted(async () => {
      loading.value = true;
      try {
        // 如果用户store为空，则获取用户数据
        if (userStore.users.length === 0) {
          await userStore.fetchUsers();
        }
        
        // 获取任务当前分配的成员
        const taskMembers = await taskStore.getTaskMembers(props.preSelectedTask.id);
        currentAssignees.value = [...(taskMembers || [])];
        
        // 如果任务有负责人但不在分配成员中，找到负责人用户对象并添加到列表
        if (props.preSelectedTask?.head_id && !currentAssignees.value.find(u => u.id === props.preSelectedTask.head_id)) {
          const headUser = userStore.users.find(u => u.id === props.preSelectedTask.head_id);
          if (headUser) {
            currentAssignees.value.push(headUser);
          }
        }
      } catch (error) {
        console.error('获取任务成员失败:', error);
      } finally {
        loading.value = false;
      }
    });

    const filteredUsers = computed(() => {
      const query = searchQuery.value.toLowerCase();
      const assignedIds = currentAssignees.value.map(u => u.id);
      
      return availableUsers.value.filter(user => 
        !assignedIds.includes(user.id) &&
        (user.username.toLowerCase().includes(query) || 
         user.email.toLowerCase().includes(query))
      );
    });

    const getRoleText = (role: string) => {
      const roleMap: Record<string, string> = {
        'director': '总监',
        'manager': '经理', 
        'user': '员工'
      };
      return roleMap[role] || role;
    };

    const isTaskHead = (user: User) => {
      return props.preSelectedTask?.head_id === user.id;
    };

    const addAssignee = (user: User) => {
      if (!currentAssignees.value.find(u => u.id === user.id)) {
        currentAssignees.value.push(user);
      }
    };

    const removeAssignee = async (user: User) => {
      try {  
        // 从任务中移除用户
        await taskStore.unassignUserFromTask(props.preSelectedTask.id, user.id);
        
        // 从本地列表中移除
        currentAssignees.value = currentAssignees.value.filter(u => u.id !== user.id);
      } catch (error) {
        console.error('移除成员失败:', error);
      }
    };

    const saveAssignments = async () => {
      saving.value = true;
      try {
        // 获取所有要分配的用户ID
        const memberIds = currentAssignees.value.map(u => u.id);
        
        // 分配用户到任务
        if (memberIds.length > 0) {
          await taskStore.assignUsersToTask(props.preSelectedTask.id, memberIds);
        }
        
        // 如果选择了设置负责人，设置最后添加的用户为负责人
        if (setAsHead.value && currentAssignees.value.length > 0) {
          const lastUser = currentAssignees.value[currentAssignees.value.length - 1];
          await taskStore.updateTask(props.preSelectedTask.id, {
            head_id: lastUser.id
          });
        }

        emit('assigned');
      } catch (error) {
        console.error('分配成员失败:', error);
      } finally {
        saving.value = false;
      }
    };

    const closeModal = () => {
      emit('close');
    };

    return {
      searchQuery,
      saving,
      loading,
      currentAssignees,
      setAsHead,
      availableUsers,
      filteredUsers,
      getRoleText,
      isTaskHead,
      addAssignee,
      removeAssignee,
      saveAssignments,
      closeModal
    };
  }
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

.modal-container {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.task-info {
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.task-info h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.task-info p {
  margin: 0;
  color: #6c757d;
  font-size: 14px;
}

.current-assignees {
  margin-bottom: 20px;
}

.current-assignees h5,
.available-users h5 {
  margin: 0 0 12px 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.assignee-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.assignee-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #e8f5e8;
  border-radius: 6px;
  border: 1px solid #c3e6c3;
}

.user-search {
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #eee;
}

.user-item:hover {
  background: #e9ecef;
  border-color: var(--primary-color);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 500;
  color: #2c3e50;
}

.user-email {
  font-size: 12px;
  color: #6c757d;
}

.user-role {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
  color: white;
  align-self: flex-start;
}

.user-role.director {
  background: #e74c3c;
}

.user-role.manager {
  background: #3498db;
}

.user-role.user {
  background: #95a5a6;
}

.user-badges {
  display: flex;
  gap: 6px;
  align-items: center;
  margin-top: 2px;
}

.head-badge {
  background: #e74c3c;
  color: white;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 500;
}

.add-btn,
.remove-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
  flex-shrink: 0;
}

.add-btn {
  background: var(--success-color);
  color: white;
}

.add-btn:hover {
  background: var(--success-hover);
}

.remove-btn {
  background: var(--danger-color);
  color: white;
}

.remove-btn:hover {
  background: var(--danger-hover);
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading-state,
.empty-state {
  padding: 20px;
  text-align: center;
  color: #6c757d;
  font-style: italic;
}

.assignment-mode {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.assignment-mode h5 {
  margin: 0 0 12px 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.checkbox-option {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #2c3e50;
}

.checkbox-option input[type="checkbox"] {
  margin-right: 8px;
}
</style>