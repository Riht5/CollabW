<template>
  <div id="app">
    <AppHeader />
    <div class="main-layout">
      <Sidebar />
      <div class="main-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AppHeader from './components/common/AppHeader.vue';
import Sidebar from './components/common/Sidebar.vue';

export default defineComponent({
  name: 'App',
  components: {
    AppHeader,
    Sidebar,
  },
});
</script>

<style>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-layout {
  display: flex;
  flex: 1 1 0;
  min-height: 0;
}
.main-content {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #f7f9fb;
}
</style>