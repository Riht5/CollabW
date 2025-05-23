<template>
  <div class="project-card">
    <h3>{{ project.name }}</h3>
    <p v-if="project.description">{{ project.description }}</p>
    <div class="project-details">
      <span>状态: {{ statusLabel(project.status) }}</span>
      <span v-if="project.estimated_duration">预计周期: {{ project.estimated_duration }} 天</span>
      <span v-if="project.start_time">开始: {{ formatDate(project.start_time) }}</span>
      <span v-if="project.end_time">结束: {{ formatDate(project.end_time) }}</span>
    </div>
    <button class="button" @click="viewProject">查看详情</button>
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
    },
    statusLabel(status: string) {
      switch (status) {
        case 'pending': return '未开始';
        case 'in_progress': return '进行中';
        case 'completed': return '已完成';
        default: return status;
      }
    },
    formatDate(dateStr: string) {
      if (!dateStr) return '';
      return dateStr.split('T')[0];
    }
  }
});
</script>

<style scoped>
.project-card {
  border: 1px solid #d0d7de;
  border-radius: 8px;
  padding: 18px 16px 14px 16px;
  margin: 16px 0;
  background: #fff;
  transition: box-shadow 0.3s;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.06);
}
.project-card:hover {
  box-shadow: 0 4px 16px rgba(52, 152, 219, 0.15);
}
.project-details {
  margin-top: 10px;
  color: #666;
  font-size: 0.98em;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.button {
  margin-top: 14px;
  background: #3498db;
  color: #fff;
  border: none;
  padding: 8px 18px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background 0.2s;
}
.button:hover {
  background: #217dbb;
}
</style>