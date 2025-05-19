<template>
  <div class="project-card">
    <h3>{{ project.name }}</h3>
    <p>{{ project.description }}</p>
    <div class="project-details">
      <span>Status: {{ project.status }}</span>
      <span>Due Date: {{ project.dueDate }}</span>
    </div>
    <button @click="viewProject">View Project</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ProjectCard',
  props: {
    project: {
      type: Object,
      required: true
    }
  },
  methods: {
    viewProject() {
      this.$emit('view-project', this.project.id);
    }
  }
});
</script>

<style scoped>
.project-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  transition: box-shadow 0.3s;
}

.project-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.project-details {
  margin-top: 8px;
}
</style>