<template>
  <div class="project-list">
    <div v-if="projects.length === 0">
      <p class="empty-tip">暂无项目。</p>
    </div>
    <ul>
      <li v-for="project in projects" :key="project.id">
        <ProjectCard :project="project" @view-project="handleViewProject" />
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ProjectCard from './ProjectCard.vue';
import { useProjectStore } from '@/stores/project';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'ProjectList',
  components: {
    ProjectCard,
  },
  setup() {
    const projectStore = useProjectStore();
    const projects = projectStore.projects;
    const router = useRouter();

    const handleViewProject = (id: number) => {
      router.push(`/projects/${id}`);
    };

    return {
      projects,
      handleViewProject,
    };
  },
});
</script>

<style scoped>
.project-list {
  padding: 10px 0;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
li {
  margin-bottom: 18px;
}
.empty-tip {
  color: #aaa;
  text-align: center;
  margin: 24px 0;
}
</style>