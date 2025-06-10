<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>添加新任务</h2>
        <button @click="closeModal" class="modal-close-btn">×</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="createTask">
          <div class="form-group">
            <label class="form-label required" for="name">任务名称</label>
            <input
              class="form-input"
              type="text"
              id="name"
              v-model="form.name"
              required
              placeholder="请输入任务名称"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label" for="description">任务描述</label>
            <textarea
              class="form-textarea"
              id="description"
              v-model="form.description"
              rows="3"
              placeholder="请输入任务描述"
            ></textarea>
          </div>
          
          <div class="form-row cols-2">
            <div class="form-group">
              <label class="form-label required" for="workload">工作量</label>
              <select class="form-select" id="workload" v-model="form.workload" required>
                <option value="">请选择工作量</option>
                <option value="light">轻量</option>
                <option value="medium">中等</option>
                <option value="heavy">困难</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label" for="head">任务负责人</label>
              <select class="form-select" id="head" v-model="form.head_id">
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
            <label class="form-checkbox">
              <input type="checkbox" v-model="form.finished" />
              任务已完成
            </label>
          </div>
        </form>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn btn-secondary">取消</button>
        <button @click="createTask" class="btn btn-primary" :disabled="loading || !form.name || !form.workload">
          {{ loading ? '创建中...' : '创建任务' }}
        </button>
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
import { TaskWorkload } from '@/utils/constants';
import type { TaskCreate } from '@/types/index';

export default defineComponent({
  name: 'TaskCreateModal',
  props: {
    projectId: {
      type: Number,
      required: true,
    },
  },
  emits: ['close', 'created'],
  setup(props, { emit }) {
    const taskStore = useTaskStore();
    const userStore = useUserStore();
    
    const loading = ref(false);
    const error = ref('');    const form = reactive<TaskCreate>({
      name: '',
      description: '',
      workload: TaskWorkload.LIGHT,
      finished: false,
      project_id: props.projectId,
      head_id: undefined,
    });const availableUsers = userStore.users;

    const getRoleTextDisplay = (role: string) => {
      return getRoleText(role);
    };

    const createTask = async () => {
      if (!form.name.trim() || !form.workload) {
        error.value = '请填写必填字段';
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        await taskStore.createTask(form);
        emit('created');
      } catch (err: any) {
        error.value = err.response?.data?.detail || '创建任务失败';
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
      createTask,
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

.modal-close-btn {
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

.modal-close-btn:hover {
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

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #3498db;
}

.form-checkbox {
  display: flex;
  align-items: center;
}

.form-checkbox input[type="checkbox"] {
  margin-right: 8px;
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

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px 16px;
  margin: 0 24px 24px;
  border-radius: 6px;
}
</style>