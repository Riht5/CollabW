<template>
  <header class="app-header">
    <div class="header-brand">
      <h1>项目协作管理平台</h1>
    </div>
    <div class="header-actions">
      <div class="user-menu">
        <div class="user-avatar">{{ userInitial }}</div>
        <span class="username">{{ authStore.user?.username }}</span>
        <div class="dropdown">
          <button @click="logout" class="btn btn-danger btn-sm">
            <i class="icon">🚪</i> 退出登录
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
  name: 'Header',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();

    const userInitial = computed(() => {
      return authStore.user?.username?.charAt(0).toUpperCase() || 'U';
    });

    const logout = () => {
      authStore.logout();
      router.push('/login');
    };

    return {
      authStore,
      userInitial,
      logout,
    };
  },
});
</script>

<style scoped>
.app-header {
  background: white;
  border-bottom: 1px solid #e0e0e0;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-brand h1 {
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.username {
  color: #2c3e50;
  font-weight: 500;
}

</style>