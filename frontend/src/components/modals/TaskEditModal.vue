<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>编辑任务</h2>
        <button @click="closeModal" class="close-btn">×</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="updateTask">
          <div class="form-group">
            <label for="name">任务名称 *</label>
            <input
              type="text"
              id="name"
              v-model="form.name"
              required
              placeholder="请输入任务名称"
            />
          </div>
          
          <div class="form-group">
            <label for="description">任务描述</label>
            <textarea
              id="description"
              v-model="form.description"
              rows="3"
              placeholder="请输入任务描述"
            ></textarea>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="workload">工作量 *</label>
              <select id="workload" v-model="form.workload" required>
                <option value="light">轻量</option>
                <option value="medium">中等</option>
                <option value="heavy">困难</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="head">任务负责人</label>
              <select id="head" v-model="form.head_id">
                <option :value="null">不分配负责人</option>
                <option 
                  v-for="user in availableUsers" 
                  :key="user.id" 
                  :value="user.id"
                >
                  {{ user.username }} ({{ getRoleTextDisplay(user.role) }})
                </option>
              </select>
            </div>
          </div>
          
          <div class="form-group">
            <label>
              <input type="checkbox" v-model="form.finished" />
              任务已完成
            </label>
          </div>
        </form>
      </div>
      
      <div class="modal-footer">
        <button @click="deleteTask" class="btn btn-danger" :disabled="loading">
          {{ loading ? '删除中...' : '删除任务' }}
        </button>
        <div class="footer-right">
          <button @click="closeModal" class="btn btn-secondary">取消</button>
          <button @click="updateTask" class="btn btn-primary" :disabled="loading || !form.name || !form.workload">
            {{ loading ? '更新中...' : '更新任务' }}
          </button>
        </div>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue';
import { useTaskStore } from '@/stores/task';
import { useUserStore } from '@/stores/user';
import { getRoleText } from '@/utils/helpers';
import type { Task } from '@/types/index';

export default defineComponent({
  name: 'TaskEditModal',
  props: {
    task: {
      type: Object as () => Task,
      required: true,
    },
  },
  emits: ['close', 'updated', 'deleted'],
  setup(props, { emit }) {
    const taskStore = useTaskStore();
    const userStore = useUserStore();
    
    const loading = ref(false);
    const error = ref('');

    const form = reactive({
      name: props.task.name,
      description: props.task.description || '',
      workload: props.task.workload,
      finished: props.task.finished,
      head_id: props.task.head_id || undefined,
    });    const availableUsers = userStore.users;

    const getRoleTextDisplay = (role: string) => {
      return getRoleText(role);
    };

    const updateTask = async () => {
      if (!form.name.trim() || !form.workload) {
        error.value = '请填写必填字段';
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        // 处理负责人ID，空字符串转为 undefined
        const updateData = {
          ...form,
          head_id: form.head_id || undefined
        };
        
        // 使用 update_task 接口更新任务信息，包括负责人
        await taskStore.updateTask(props.task.id, updateData);
        emit('updated');
      } catch (err: any) {
        error.value = err.response?.data?.detail || '更新任务失败';
      } finally {
        loading.value = false;
      }
    };

    const deleteTask = async () => {
      if (!confirm('确定要删除此任务吗？此操作不可撤销。')) {
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        await taskStore.deleteTask(props.task.id);
        emit('deleted');
      } catch (err: any) {
        error.value = err.response?.data?.detail || '删除任务失败';
      } finally {
        loading.value = false;
      }
    };

    const closeModal = () => {
      emit('close');
    };

    onMounted(() => {
      userStore.fetchUsers();
    });

    return {
      form,
      loading,      error,
      availableUsers,
      getRoleTextDisplay,
      updateTask,
      deleteTask,
      closeModal,
    };
  },
});
</script>

<style scoped>
/* 复用 TaskCreateModal 的样式 */
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
  max-width: 500px;
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
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-group input[type="text"],
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input[type="text"]:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
}

.form-group input[type="checkbox"] {
  margin-right: 8px;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-top: 1px solid #eee;
}

.footer-right {
  display: flex;
  gap: 12px;
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

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

.btn-danger:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px 16px;
  margin: 0 24px 24px;
  border-radius: 6px;
}
</style>