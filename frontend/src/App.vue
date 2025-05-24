<template>
  <div id="app">
    <div v-if="!authStore.isAuthenticated()" class="auth-layout">
      <router-view />
    </div>
    <div v-else class="main-layout">
      <Header />
      <div class="layout-container">
        <Sidebar />
        <main class="main-content">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import Header from './components/common/Header.vue';
import Sidebar from './components/common/Sidebar.vue';

export default defineComponent({
  name: 'App',
  components: {
    Header,
    Sidebar,
  },
  setup() {
    const authStore = useAuthStore();

    onMounted(() => {
      authStore.initAuth();
    });

    return {
      authStore,
    };
  },
});
</script>

<style scoped>
.auth-layout {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  background: #f8f9fa;
}
</style>