<template>
  <div>调试：Todolist 组件已加载</div>
  <div class="task-list" v-if="taskStore">
    <!-- Error message -->
    <div v-if="error" class="text-danger mt-md">{{ error }}</div>
    <!-- Success message -->
    <div v-if="success" class="text-success mt-md">{{ success }}</div>
    <!-- Loading state -->
    <div v-if="taskStore.loading" class="loading-state text-center p-md">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
    <!-- Empty state -->
    <div v-else-if="taskStore.tasks.length === 0" class="empty-state text-center p-xl">
      <div class="empty-icon">📝</div>
      <h3>暂无任务</h3>
      <p class="text-muted">等待任务分配或添加 Todo</p>
    </div>
    <!-- Task list -->
    <div v-else class="d-flex flex-column gap-md">
      <div v-for="task in taskStore.tasks" :key="task.id" class="card">
        <div class="card-body p-md">
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

          <div class="d-flex justify-between text-muted mb-md">
            <div v-if="task.head">
              <span>负责人:</span>
              <span class="m-sm">{{ task.head.username }}</span>
            </div>
            <div>
              <span>工作量权重:</span>
              <span class="m-sm">{{ getWorkloadWeight(task.workload) }}</span>
            </div>
          </div>

          <!-- Todo list for this task -->
          <div class="todo-section mb-md">
            <h5>Todo 清单</h5>
            <div class="todo-input-group d-flex gap-sm mb-sm">
              <input
                ref="inputRef"
                v-model.trim="newTodoText"
                class="todo-input"
                placeholder="添加 Todo"
                @keyup.enter="handleAddTodo(task.id)"
                @input="handleInput"
              />
              <button
                ref="buttonRef"
                type="button"
                class="btn-primary"
                @click="handleAddTodo(task.id)"
                :disabled="!newTodoText || !newTodoText.trim()"
              >
                确认
              </button>
            </div>
            <div v-if="todoError" class="text-danger mt-sm">{{ todoError }}</div>
            <div v-if="todoSuccess" class="text-success mt-sm">{{ todoSuccess }}</div>
            <div class="todo-list">
              <template v-if="todos[task.id] && todos[task.id].length > 0">
                <ul>
                  <li v-for="todo in todos[task.id].filter(t => !t.completed)" :key="todo.id" class="todo-item">
                    <input
                      type="checkbox"
                      class="todo-checkbox"
                      :checked="todo.completed"
                      @change="updateTodo(task.id, todo.id)"
                    />
                    <span>{{ todo.text }}</span>
                  </li>
                  <li v-for="todo in todos[task.id].filter(t => t.completed)" :key="todo.id" class="todo-item completed">
                    <input
                      type="checkbox"
                      class="todo-checkbox"
                      :checked="todo.completed"
                      @change="updateTodo(task.id, todo.id)"
                    />
                    <span class="todo-completed">{{ todo.text }}</span>
                  </li>
                </ul>
              </template>
              <div v-else class="no-todos">
                暂无 Todo
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="text-danger p-md">任务数据加载失败</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch, getCurrentInstance, nextTick } from 'vue';
import type { Task } from '@/types/index';
import { useTaskStore } from '@/stores/task';

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
    const taskStore = useTaskStore();
    const todos = ref<Todos>({});
    const newTodoText = ref('');
    const todoError = ref('');
    const todoSuccess = ref('');
    const error = ref('');
    const success = ref('');
    const buttonRef = ref<HTMLButtonElement | null>(null);
    const inputRef = ref<HTMLInputElement | null>(null);
    const instance = getCurrentInstance();

    const forceUpdate = () => {
      const newTodos: Todos = {};
      Object.entries(todos.value).forEach(([key, value]) => {
        newTodos[parseInt(key, 10)] = [...value];
      });
      todos.value = newTodos;
    };

    const isButtonDisabled = computed(() => {
      return !newTodoText.value || !newTodoText.value.trim();
    });

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
      forceUpdate();
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

        const newTodosState = {
          ...todos.value,
          [taskId]: newTodos
        };

        todos.value = newTodosState;
        saveTodos();
        forceUpdate();
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

    const getWorkloadWeight = (workload: string): number => {
      const weightMap: Record<string, number> = {
        light: 1,
        medium: 2,
        heavy: 3
      };
      return weightMap[workload] || 1;
    };

    watch(todos, () => {
      saveTodos();
    }, { deep: true });

    onMounted(() => {
      loadTodos();
    });

    return {
      taskStore,
      todos,
      newTodoText,
      todoError,
      todoSuccess,
      error,
      success,
      buttonRef,
      inputRef,
      isButtonDisabled,
      handleAddTodo,
      updateTodo,
      handleInput,
      getWorkloadText,
      getWorkloadWeight
    };
  }
});
</script>

<style scoped>
@import '@/assets/styles/main.css';

.task-list {
  width: 100%;
  visibility: visible !important;
}

.empty-state {
  padding: var(--spacing-xl);
}

.empty-icon {
  font-size: var(--font-size-4xl);
  color: var(--primary-color);
  margin-bottom: var(--spacing-md);
}

.loading-state {
  padding: var(--spacing-md);
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid var(--primary-color);
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  margin-right: var(--spacing-sm);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.card {
  background: var(--bg-primary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: var(--spacing-md);
}

.workload-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.workload-badge.light {
  background-color: var(--success-color);
  color: white;
}

.workload-badge.medium {
  background-color: var(--warning-color);
  color: black;
}

.workload-badge.heavy {
  background-color: var(--danger-color);
  color: white;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.status-badge.completed {
  background-color: var(--success-color);
  color: white;
}

.status-badge.pending {
  background-color: var(--warning-color);
  color: black;
}

.todo-section {
  border-top: none;
  padding-top: var(--spacing-md);
}

.todo-list {
  list-style: none;
  padding: 0;
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  z-index: 1 !important;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.todo-item:last-child {
  border-bottom: none;
}

.todo-item.completed {
  opacity: 0.6;
}

.todo-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.todo-completed {
  text-decoration: line-through;
  color: #999;
}

.no-todos {
  color: #999;
  text-align: center;
  padding: 16px 0;
}

.todo-input-group {
  align-items: center;
}

.todo-input {
  flex: 1;
  padding: var(--spacing-sm);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: var(--font-size-base);
  outline: none;
}

.todo-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.btn-primary {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: var(--font-size-base);
  font-weight: 500;
  background-color: var(--primary-color);
  color: white;
  border: none;
  cursor: pointer !important;
  -webkit-user-select: none;
  user-select: none;
  transition: opacity 0.2s;
  pointer-events: auto !important;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
}

.btn-link {
  background: none;
  border: none;
  color: var(--primary-color);
  font-size: var(--font-size-sm);
  cursor: pointer;
  padding: 0;
  -webkit-user-select: none;
  user-select: none;
}

.btn-link:hover {
  text-decoration: underline;
}
</style>