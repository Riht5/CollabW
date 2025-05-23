<template>
  <div class="task-list">
    <ul>
      <li v-for="task in tasks" :key="task.id">
        <div class="task-item">
          <h3>{{ task.name }}</h3>
          <p>{{ task.description }}</p>
          <p>优先级: {{ priorityLabel(task.priority) }}</p>
          <p>状态: <span :style="{color: task.status ? '#27ae60' : '#e67e22'}">{{ task.status ? '已完成' : '未完成' }}</span></p>
          <p v-if="task.head_id">负责人ID: {{ task.head_id }}</p>
        </div>
      </li>
    </ul>
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
    }
  },
  methods: {
    priorityLabel(priority: string) {
      switch (priority) {
        case 'high': return '高';
        case 'medium': return '中';
        case 'low': return '低';
        default: return priority;
      }
    }
  }
});
</script>

<style scoped>
.task-list {
  margin: 20px;
}

.task-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}
</style>