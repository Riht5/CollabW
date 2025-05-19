<template>
  <div class="task-form">
    <h2>{{ isEdit ? 'Edit Task' : 'Create Task' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="title">Title:</label>
        <input type="text" v-model="task.title" required />
      </div>
      <div>
        <label for="description">Description:</label>
        <textarea v-model="task.description" required></textarea>
      </div>
      <div>
        <label for="dueDate">Due Date:</label>
        <input type="date" v-model="task.dueDate" />
      </div>
      <div>
        <button type="submit">{{ isEdit ? 'Update Task' : 'Create Task' }}</button>
        <button type="button" @click="cancel">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue';
import { Task } from '@/types/index';

export default defineComponent({
  name: 'TaskForm',
  props: {
    initialTask: {
      type: Object as PropType<Task>,
      default: () => ({ title: '', description: '', dueDate: '' }),
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const task = ref({ ...props.initialTask });

    const submitForm = () => {
      // Logic to submit the form (create or update task)
      console.log('Form submitted:', task.value);
    };

    const cancel = () => {
      // Logic to cancel the form
      task.value = { title: '', description: '', dueDate: '' };
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
.task-form textarea {
  width: 100%;
  padding: 0.5em;
}
.task-form button {
  margin-right: 0.5em;
}
</style>