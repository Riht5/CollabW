<template>
  <div class="task-list">
    <!-- Loading state -->
    <div v-if="userStore.loading" class="loading-state">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
    <!-- Single task display -->
    <div class="task-card">
      <div class="task-card-body">
        <div class="task-header">
          <h4>{{ task.name }}</h4>
          <div class="task-badges">
            <span class="workload-badge" :class="task.workload">
              {{ getWorkloadText(task.workload) }}
            </span>
          </div>
        </div>

        <p v-if="task.description" class="task-description">
          {{ task.description }}
        </p>

        <div class="task-info">
          <div v-if="task.head_id && getHeadUser(task.head_id)" class="head-info">
            <span>负责人:</span>
            <span>{{ getHeadUser(task.head_id)?.username }}</span>
          </div>
          <div v-else-if="task.head_id" class="head-info">
            <span>负责人:</span>
            <span>加载中...</span>
          </div>
        </div>

        <!-- Todo list for this task -->
        <div class="todo-section">
          <div class="todo-header">
            <h5>Todo 清单</h5>
            <span class="todo-count">{{ getTodoStats(task.id) }}</span>
          </div>
          
          <div class="todo-input-group">
            <input
              ref="inputRef"
              v-model.trim="newTodoText"
              class="todo-input"
              placeholder="添加新的 Todo 项..."
              @keyup.enter="handleAddTodo(task.id)"
              @input="handleInput"
            />
            <button
              ref="buttonRef"
              type="button"
              class="btn btn-primary"
              @click="handleAddTodo(task.id)"
              :disabled="!newTodoText || !newTodoText.trim()"
            >
              <span class="btn-icon">+</span>
              添加
            </button>
          </div>
          
          <div v-if="todoError" class="error-message">{{ todoError }}</div>
          <div v-if="todoSuccess" class="success-message">{{ todoSuccess }}</div>
          
          <div class="todo-list">
            <template v-if="todos[task.id] && todos[task.id].length > 0">
              <!-- 未完成的todos -->
              <div v-if="getIncompleteTodos(task.id).length > 0" class="todo-group">
                <h6 class="todo-group-title">待完成 ({{ getIncompleteTodos(task.id).length }})</h6>
                <div class="todo-items">
                  <div v-for="todo in getIncompleteTodos(task.id)" :key="todo.id" class="todo-item">
                    <input
                      type="checkbox"
                      class="todo-checkbox"
                      :checked="todo.completed"
                      @change="updateTodo(task.id, todo.id)"
                    />
                    <div v-if="editingTodo === todo.id" class="todo-edit-form">
                      <input
                        v-model="editingText"
                        class="todo-edit-input"
                        @keyup.enter="saveEdit(task.id, todo.id)"
                        @keyup.esc="cancelEdit"
                        @blur="saveEdit(task.id, todo.id)"
                        ref="editInput"
                      />
                    </div>
                    <span v-else class="todo-text" @dblclick="startEdit(todo)">
                      {{ todo.text }}
                    </span>
                    <div class="todo-actions">
                      <button
                        v-if="editingTodo !== todo.id"
                        @click="startEdit(todo)"
                        class="todo-action-btn edit-btn"
                        title="编辑"
                      >
                        ✏️
                      </button>
                      <button
                        @click="deleteTodo(task.id, todo.id)"
                        class="todo-action-btn delete-btn"
                        title="删除"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 已完成的todos -->
              <div v-if="getCompletedTodos(task.id).length > 0" class="todo-group completed-group">
                <h6 class="todo-group-title">已完成 ({{ getCompletedTodos(task.id).length }})</h6>
                <div class="todo-items">
                  <div v-for="todo in getCompletedTodos(task.id)" :key="todo.id" class="todo-item completed">
                    <input
                      type="checkbox"
                      class="todo-checkbox"
                      :checked="todo.completed"
                      @change="updateTodo(task.id, todo.id)"
                    />
                    <span class="todo-text todo-completed">{{ todo.text }}</span>
                    <div class="todo-actions">
                      <button
                        @click="deleteTodo(task.id, todo.id)"
                        class="todo-action-btn delete-btn"
                        title="删除"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </template>
            <div v-else class="no-todos">
              <div class="no-todos-icon">📝</div>
              <p>暂无 Todo 项</p>
              <p class="no-todos-hint">添加第一个 Todo 来开始工作吧！</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, nextTick } from 'vue';
import type { Task } from '@/types/index';
import { useUserStore } from '@/stores/user';

/**
 * Todo 项接口定义
 */
interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

/**
 * Todos 数据结构接口定义
 */
interface Todos {
  [key: number]: Todo[];
}

export default defineComponent({
  name: 'Todolist',
  props: {
    task: {
      type: Object as () => Task,
      required: true
    }
  },
  setup(props) {
    const userStore = useUserStore();
    const todos = ref<Todos>({});
    const newTodoText = ref('');
    const todoError = ref('');
    const todoSuccess = ref('');
    const inputRef = ref<HTMLInputElement | null>(null);
    const editingTodo = ref<number | null>(null);
    const editingText = ref('');
    const editInput = ref<HTMLInputElement | null>(null);

    const saveTodos = () => {
      try {
        const todosToSave: Todos = {};
        Object.keys(todos.value).forEach(key => {
          const numKey = parseInt(key, 10);
          if (!isNaN(numKey)) {
            todosToSave[numKey] = todos.value[numKey];
          }
        });
        localStorage.setItem('todos', JSON.stringify(todosToSave));
      } catch (error) {
        console.error('保存 todos 失败:', error);
      }
    };

    const loadTodos = () => {
      try {
        const savedTodos = localStorage.getItem('todos');
        if (savedTodos) {
          todos.value = JSON.parse(savedTodos);
        }
      } catch (error) {
        console.error('加载 todos 失败:', error);
        todos.value = {};
      }
    };

    const clearInput = async () => {
      if (inputRef.value) {
        newTodoText.value = '';
        inputRef.value.value = '';
        await nextTick();
      }
    };

    const handleInput = (event: Event) => {
      const target = event.target as HTMLInputElement;
      newTodoText.value = target.value;
    };

    const handleAddTodo = async (taskId: number) => {
      const todoText = newTodoText.value.trim();
      
      if (!todoText) {
        return;
      }

      const newTodo: Todo = {
        id: Date.now(),
        text: todoText,
        completed: false
      };

      const newTodos: Todos = { ...todos.value };
      if (!newTodos[taskId]) {
        newTodos[taskId] = [];
      }
      
      newTodos[taskId] = [...newTodos[taskId], newTodo];
      todos.value = newTodos;
      
      saveTodos();
      await clearInput();
    };

    const updateTodo = (taskId: number, todoId: number) => {
      try {
        const taskTodos = todos.value[taskId] || [];
        const todoIndex = taskTodos.findIndex((t: Todo) => t.id === todoId);
        
        if (todoIndex === -1) {
          console.error('Todo not found:', { taskId, todoId });
          return;
        }

        const updatedTodo = {
          ...taskTodos[todoIndex],
          completed: !taskTodos[todoIndex].completed
        };

        const newTodos = [...taskTodos];
        newTodos[todoIndex] = updatedTodo;

        todos.value = {
          ...todos.value,
          [taskId]: newTodos
        };

        saveTodos();
      } catch (error) {
        console.error('更新 Todo 失败:', error);
        todoError.value = '更新 Todo 失败';
        setTimeout(() => {
          todoError.value = '';
        }, 3000);
      }
    };

    const getWorkloadText = (workload: string): string => {
      const workloadMap: Record<string, string> = {
        light: '轻量',
        medium: '中等',
        heavy: '重量'
      };
      return workloadMap[workload] || workload;
    };

    const getHeadUser = (headId: number | null | undefined) => {
      if (!headId || !userStore.users || userStore.users.length === 0) return null;
      return userStore.users.find(user => user.id === headId);
    };

    const getTodoStats = (taskId: number) => {
      const taskTodos = todos.value[taskId] || [];
      const completed = taskTodos.filter(t => t.completed).length;
      const total = taskTodos.length;
      return total > 0 ? `${completed}/${total} 完成` : '0 项';
    };

    const getIncompleteTodos = (taskId: number) => {
      return (todos.value[taskId] || []).filter(t => !t.completed);
    };

    const getCompletedTodos = (taskId: number) => {
      return (todos.value[taskId] || []).filter(t => t.completed);
    };

    const startEdit = (todo: Todo) => {
      editingTodo.value = todo.id;
      editingText.value = todo.text;
      nextTick(() => {
        if (editInput.value) {
          editInput.value.focus();
          editInput.value.select();
        }
      });
    };

    const cancelEdit = () => {
      editingTodo.value = null;
      editingText.value = '';
    };

    const saveEdit = (taskId: number, todoId: number) => {
      const newText = editingText.value.trim();
      if (!newText || newText === '') {
        cancelEdit();
        return;
      }

      try {
        const taskTodos = todos.value[taskId] || [];
        const todoIndex = taskTodos.findIndex(t => t.id === todoId);
        
        if (todoIndex !== -1) {
          const updatedTodo = {
            ...taskTodos[todoIndex],
            text: newText
          };

          const newTodos = [...taskTodos];
          newTodos[todoIndex] = updatedTodo;

          todos.value = {
            ...todos.value,
            [taskId]: newTodos
          };

          saveTodos();
        }
      } catch (error) {
        console.error('编辑 Todo 失败:', error);
        todoError.value = '编辑 Todo 失败';
        setTimeout(() => {
          todoError.value = '';
        }, 3000);
      }

      cancelEdit();
    };

    const deleteTodo = (taskId: number, todoId: number) => {
      if (!confirm('确定要删除这个 Todo 吗？')) {
        return;
      }

      try {
        const taskTodos = todos.value[taskId] || [];
        const newTodos = taskTodos.filter(t => t.id !== todoId);

        todos.value = {
          ...todos.value,
          [taskId]: newTodos
        };

        saveTodos();
        
        todoSuccess.value = 'Todo 已删除';
        setTimeout(() => {
          todoSuccess.value = '';
        }, 2000);
      } catch (error) {
        console.error('删除 Todo 失败:', error);
        todoError.value = '删除 Todo 失败';
        setTimeout(() => {
          todoError.value = '';
        }, 3000);
      }
    };

    onMounted(async () => {
      loadTodos();
      // 确保用户数据已加载
      try {
        if (userStore.users.length === 0) {
          await userStore.fetchUsers();
        }
      } catch (error) {
        console.error('Failed to load users:', error);
      }
    });

    return {
      userStore,
      todos,
      newTodoText,
      todoError,
      todoSuccess,
      inputRef,
      editingTodo,
      editingText,
      editInput,
      handleAddTodo,
      updateTodo,
      handleInput,
      getWorkloadText,
      getHeadUser,
      getTodoStats,
      getIncompleteTodos,
      getCompletedTodos,
      startEdit,
      cancelEdit,
      saveEdit,
      deleteTodo
    };
  }
});
</script>

<style scoped>
.task-list {
  width: 100%;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px 16px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #f5c6cb;
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 12px 16px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #c3e6cb;
}

.loading-state {
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #3498db;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 48px;
  color: #3498db;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.empty-state p {
  margin: 0;
  color: #6c757d;
}

.tasks-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.task-card {
  background: white;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  transition: all 0.2s;
}

.task-card:hover {
  border-color: #3498db;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.15);
}

.task-card-body {
  padding: 20px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.task-header h4 {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.task-badges {
  display: flex;
  gap: 8px;
}

.workload-badge {
  padding: 4px 8px;
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
  color: #000;
}

.workload-badge.heavy {
  background: #dc3545;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.status-badge.completed {
  background: #28a745;
  color: white;
}

.status-badge.pending {
  background: #ffc107;
  color: #000;
}

.task-description {
  margin: 0 0 12px 0;
  color: #6c757d;
  font-size: 14px;
  line-height: 1.4;
}

.task-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 14px;
  color: #6c757d;
}

.head-info,
.workload-info {
  display: flex;
  gap: 8px;
}

.todo-section {
  border-top: 1px solid #e9ecef;
  padding-top: 20px;
}

.todo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.todo-header h5 {
  margin: 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.todo-count {
  background: #f8f9fa;
  color: #6c757d;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.todo-input-group {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #dee2e6;
  transition: all 0.2s;
}

.todo-input-group:focus-within {
  border-color: #3498db;
  background: #fff;
}

.todo-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
}

.todo-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.btn {
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-icon {
  font-size: 16px;
  font-weight: bold;
}

.btn-primary {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #2980b9, #21618c);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.4);
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.todo-list {
  margin-top: 16px;
}

.todo-group {
  margin-bottom: 24px;
}

.todo-group-title {
  margin: 0 0 12px 0;
  color: #495057;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.completed-group .todo-group-title {
  color: #6c757d;
}

.todo-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  transition: all 0.2s;
}

.todo-item:hover {
  border-color: #3498db;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.1);
}

.todo-item.completed {
  background: #f8f9fa;
  border-color: #dee2e6;
}

.todo-checkbox {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #3498db;
  flex-shrink: 0;
}

.todo-text {
  flex: 1;
  font-size: 14px;
  line-height: 1.4;
  cursor: pointer;
  padding: 4px 0;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.todo-text:hover {
  background-color: #f8f9fa;
  padding-left: 8px;
  padding-right: 8px;
}

.todo-completed {
  text-decoration: line-through;
  color: #6c757d;
  opacity: 0.7;
}

.todo-edit-form {
  flex: 1;
}

.todo-edit-input {
  width: 100%;
  padding: 8px 12px;
  border: 2px solid #3498db;
  border-radius: 4px;
  font-size: 14px;
  background: #fff;
}

.todo-edit-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}

.todo-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

.todo-item:hover .todo-actions {
  opacity: 1;
}

.todo-action-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: all 0.2s;
  background: #f8f9fa;
}

.edit-btn:hover {
  background: #3498db;
  color: white;
  transform: scale(1.1);
}

.delete-btn:hover {
  background: #e74c3c;
  color: white;
  transform: scale(1.1);
}

.no-todos {
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
}

.no-todos-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-todos p {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 500;
}

.no-todos-hint {
  font-size: 14px;
  opacity: 0.8;
}
</style>