<template>
  <aside class="sidebar">
    <nav class="nav-menu">
      <router-link to="/" class="nav-item" :class="{ active: $route.name === 'Dashboard' }">
        <i class="icon">📊</i>
        <span>仪表盘</span>
      </router-link>
      <router-link to="/projects" class="nav-item" :class="{ active: $route.path.startsWith('/projects') }">
        <i class="icon">📁</i>
        <span>项目管理</span>
      </router-link>
      <router-link to="/performance" class="nav-item" :class="{ active: $route.name === 'Performance' }">
        <i class="icon">🏆</i>
        <span>绩效看板</span>
      </router-link>
      <router-link to="/gantt" class="nav-item" :class="{ active: $route.name === 'Gantt' }">
        <i class="icon">📅</i>
        <span>甘特图</span>
      </router-link>
      <router-link to="/personal" class="nav-item" :class="{ active: $route.name === 'PersonalTable' }">
        <i class="icon">👤</i>
        <span>个人工作台</span>
      </router-link>
    </nav>
  </aside>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
  name: 'Sidebar',
  setup() {
    const authStore = useAuthStore();
    const isDirectorOrManager = computed(() => {
      return ['director', 'manager'].includes(authStore.userRole);
    });

    return {
      isDirectorOrManager
    };
  }
});
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: white;
  border-right: 1px solid #e0e0e0;
  padding: 24px 0;
}

.nav-menu {
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  color: #666;
  text-decoration: none;
  transition: all 0.2s;
  border-right: 3px solid transparent;
}

.nav-item:hover {
  background: #f8f9fa;
  color: #3498db;
}

.nav-item.active {
  background: #e3f2fd;
  color: #3498db;
  border-right-color: #3498db;
  font-weight: 500;
}

.icon {
  font-style: normal;
  font-size: 18px;
}
</style>