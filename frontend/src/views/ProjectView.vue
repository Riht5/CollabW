<template>
  <div class="project-view" v-if="project">
    <h1>{{ project.name }}</h1>
    <p>{{ project.description }}</p>
    <div class="project-details">
      <h2>Details</h2>
      <p><strong>Start Date:</strong> {{ project.start_time }}</p>
      <p><strong>End Date:</strong> {{ project.end_time }}</p>
      <p><strong>Status:</strong> {{ project.status }}</p>
    </div>
    <div class="tasks">
      <h2>Tasks</h2>
      <TaskList :tasks="project.tasks" />
      <TaskForm @task-added="fetchProject" :projectId="project.id" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import TaskList from '@/components/tasks/TaskList.vue';
import TaskForm from '@/components/tasks/TaskForm.vue';
import { useRoute } from 'vue-router';
import { useProjectStore } from '@/stores/project';

export default defineComponent({
  components: {
    TaskList,
    TaskForm,
  },
  setup() {
    const route = useRoute();
    const project = ref<any>(null);
    const projectStore = useProjectStore();

    const fetchProject = async () => {
      const projectId = route.params.id as string;
      project.value = await projectStore.fetchProjectById(projectId);
    };

    onMounted(fetchProject);

    return {
      project,
      fetchProject,
    };
  },
});
</script>

<style scoped>
.project-view {
  padding: 20px;
}
.project-details {
  margin-bottom: 20px;
}
</style>