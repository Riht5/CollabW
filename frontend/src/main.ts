import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

// 导入全局样式
import '@/assets/styles/main.css';
// 导入甘特图样式
import '../node_modules/frappe-gantt/dist/frappe-gantt.css'

// 导入并配置 HTTP 客户端
import '@/utils/axios';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount('#app');