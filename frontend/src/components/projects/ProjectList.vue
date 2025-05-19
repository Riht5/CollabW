<template>
  <div class="project-list">
    <h2>Project List</h2>
    <div v-if="projects.length === 0">
      <p>No projects available.</p>
    </div>
    <ul>
      <li v-for="project in projects" :key="project.id">
        <ProjectCard :project="project" />
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ProjectCard from './ProjectCard.vue';
import { useProjectStore } from '@/stores/project';

export default defineComponent({
  name: 'ProjectList',
  components: {
    ProjectCard,
  },
  setup() {
    const projectStore = useProjectStore();
    const projects = projectStore.projects;

    return {
      projects,
    };
  },
});
</script>

<style scoped>
.project-list {
  padding: 20px;
}
</style>