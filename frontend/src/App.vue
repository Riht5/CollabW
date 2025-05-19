<template>
  <div id="app">
    <AppHeader />
    <Sidebar />
    <router-view />
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
  display: flex;
  flex-direction: column;
  height: 100vh;
}
</style>