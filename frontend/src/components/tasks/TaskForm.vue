<template>
  <div class="task-form">
    <h2>{{ isEdit ? '编辑任务' : '创建任务' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="name">任务名称:</label>
        <input type="text" v-model="task.name" id="name" required />
      </div>
      <div>
        <label for="description">描述:</label>
        <textarea v-model="task.description" id="description"></textarea>
      </div>
      <div>
        <label for="priority">优先级:</label>
        <select v-model="task.priority" id="priority">
          <option value="low">低</option>
          <option value="medium">中</option>
          <option value="high">高</option>
        </select>
      </div>
      <div>
        <label>
          <input type="checkbox" v-model="task.status" />
          已完成
        </label>
      </div>
      <!-- project_id 和 head_id 通常由父组件传递或自动赋值，这里可选填 -->
      <div>
        <label for="head_id">负责人ID:</label>
        <input type="number" v-model.number="task.head_id" id="head_id" />
      </div>
      <div>
        <button type="submit">{{ isEdit ? '更新任务' : '创建任务' }}</button>
        <button type="button" @click="cancel">取消</button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue';
import type { Task } from '@/types/index';

export default defineComponent({
  name: 'TaskForm',
  props: {
    initialTask: {
      type: Object as PropType<Partial<Task>>,
      default: () => ({
        name: '',
        description: '',
        priority: 'low',
        status: false,
        project_id: undefined,
        head_id: undefined,
      }),
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const task = ref({ ...props.initialTask });

    const submitForm = () => {
      emit('submit', { ...task.value });
    };

    const cancel = () => {
      emit('cancel');
    };

    return {
      task,
      submitForm,
      cancel,
    };
  },
});
</script>

<style scoped>
.task-form {
  max-width: 400px;
  margin: auto;
}
.task-form h2 {
  text-align: center;
}
.task-form div {
  margin-bottom: 1em;
}
.task-form label {
  display: block;
  margin-bottom: 0.5em;
}
.task-form input,
.task-form textarea,
.task-form select {
  width: 100%;
  padding: 0.5em;
}
.task-form button {
  margin-right: 0.5em;
}
</style>