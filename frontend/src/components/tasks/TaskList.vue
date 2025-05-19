<template>
  <div class="task-list">
    <h2>Task List</h2>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        <div class="task-item">
          <h3>{{ task.title }}</h3>
          <p>{{ task.description }}</p>
          <span>Status: {{ task.status }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Task } from '@/types/index';

export default defineComponent({
  name: 'TaskList',
  props: {
    tasks: {
      type: Array as () => Task[],
      required: true
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