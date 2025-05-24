<template>
  <div class="performance-view">
    <div class="performance-header">
      <h1>绩效看板</h1>
      <button @click="calculatePerformance" class="btn btn-primary" :disabled="calculating">
        {{ calculating ? '计算中...' : '重新计算绩效' }}
      </button>
    </div>

    <div class="performance-stats">
      <div class="stat-card">
        <h3>总员工数</h3>
        <div class="stat-number">{{ allUsers.length }}</div>
      </div>
      <div class="stat-card">
        <h3>优秀员工</h3>
        <div class="stat-number outstanding">{{ outstandingUsers.length }}</div>
      </div>
      <div class="stat-card">
        <h3>平均绩效</h3>
        <div class="stat-number">{{ averagePerformance.toFixed(1) }}</div>
      </div>
      <div class="stat-card">
        <h3>最高绩效</h3>
        <div class="stat-number">{{ maxPerformance.toFixed(1) }}</div>
      </div>
    </div>

    <div class="performance-content">
      <div class="section">
        <h2>优秀员工榜</h2>
        <div v-if="outstandingUsers.length" class="outstanding-list">
          <div v-for="(user, index) in outstandingUsers" :key="user.id" class="outstanding-item">
            <div class="rank">{{ index + 1 }}</div>
            <div class="user-info">
              <h4>{{ user.username }}</h4>
              <p>{{ user.email }}</p>
              <span class="role-badge" :class="user.role">{{ getRoleText(user.role) }}</span>
            </div>
            <div class="performance-score">
              {{ user.performance?.toFixed(1) || '0.0' }}
            </div>
          </div>
        </div>
        <p v-else class="empty-text">暂无优秀员工数据</p>
      </div>

      <div class="section">
        <h2>全员绩效排行</h2>
        <div class="performance-table">
          <div class="table-header">
            <div>排名</div>
            <div>姓名</div>
            <div>邮箱</div>
            <div>角色</div>
            <div>绩效分数</div>
            <div>状态</div>
          </div>
          <div v-for="(user, index) in sortedUsers" :key="user.id" class="table-row">
            <div class="rank-cell">{{ index + 1 }}</div>
            <div>{{ user.username }}</div>
            <div>{{ user.email }}</div>
            <div>
              <span class="role-badge" :class="user.role">{{ getRoleText(user.role) }}</span>
            </div>
            <div class="score-cell">{{ user.performance?.toFixed(1) || '0.0' }}</div>
            <div>
              <span v-if="user.outstanding" class="outstanding-badge">优秀</span>
              <span v-else class="normal-badge">普通</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';

export default defineComponent({
  name: 'PerformanceView',
  setup() {
    const userStore = useUserStore();

    const allUsers = computed(() => userStore.users);
    const outstandingUsers = computed(() => userStore.outstandingUsers);
    const calculating = computed(() => userStore.loading);
    const error = computed(() => userStore.error);

    const sortedUsers = computed(() => 
      [...allUsers.value].sort((a, b) => (b.performance || 0) - (a.performance || 0))
    );

    const averagePerformance = computed(() => {
      if (allUsers.value.length === 0) return 0;
      const total = allUsers.value.reduce((sum, user) => sum + (user.performance || 0), 0);
      return total / allUsers.value.length;
    });

    const maxPerformance = computed(() => 
      Math.max(...allUsers.value.map(user => user.performance || 0), 0)
    );

    const getRoleText = (role: string) => {
      const roleMap: Record<string, string> = {
        'director': '总监',
        'manager': '经理',
        'user': '员工'
      };
      return roleMap[role] || role;
    };

    const calculatePerformance = async () => {
      try {
        await userStore.calculatePerformance();
      } catch (err) {
        console.error('计算绩效失败:', err);
      }
    };

    onMounted(async () => {
      await Promise.all([
        userStore.fetchUsers(),
        userStore.fetchOutstandingUsers(),
      ]);
    });

    return {
      allUsers,
      outstandingUsers,
      sortedUsers,
      calculating,
      error,
      averagePerformance,
      maxPerformance,
      getRoleText,
      calculatePerformance,
    };
  },
});
</script>

<style scoped>
.performance-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.performance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.performance-header h1 {
  margin: 0;
  color: #2c3e50;
}

.performance-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-card h3 {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #3498db;
}

.stat-number.outstanding {
  color: #f39c12;
}

.performance-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
}

.section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.section h2 {
  margin: 0;
  padding: 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
  color: #2c3e50;
}

.outstanding-list {
  padding: 20px;
}

.outstanding-item {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #f39c12;
}

.rank {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f39c12;
  color: white;
  border-radius: 50%;
  font-weight: bold;
  margin-right: 15px;
}

.user-info {
  flex: 1;
}

.user-info h4 {
  margin: 0 0 5px 0;
  color: #2c3e50;
}

.user-info p {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.performance-score {
  font-size: 24px;
  font-weight: bold;
  color: #f39c12;
}

.performance-table {
  display: grid;
  grid-template-columns: 60px 1fr 1fr 100px 100px 80px;
  gap: 10px;
}

.table-header {
  display: contents;
  font-weight: 500;
  color: #666;
}

.table-header > div {
  padding: 15px 10px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.table-row {
  display: contents;
}

.table-row > div {
  padding: 15px 10px;
  border-bottom: 1px solid #f1f1f1;
  display: flex;
  align-items: center;
}

.rank-cell {
  font-weight: bold;
  color: #f39c12;
}

.score-cell {
  font-weight: bold;
  color: #3498db;
}

.role-badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.role-badge.director {
  background: #e74c3c;
  color: white;
}

.role-badge.manager {
  background: #3498db;
  color: white;
}

.role-badge.user {
  background: #95a5a6;
  color: white;
}

.outstanding-badge {
  background: #f39c12;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.normal-badge {
  background: #95a5a6;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.empty-text {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 40px;
}

.error {
  color: #e74c3c;
  text-align: center;
  margin-top: 20px;
  padding: 15px;
  background: #fdf2f2;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .performance-content {
    grid-template-columns: 1fr;
  }
  
  .performance-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .performance-table {
    grid-template-columns: 40px 1fr 80px;
    font-size: 12px;
  }
  
  .table-header > div:nth-child(3),
  .table-header > div:nth-child(4),
  .table-row > div:nth-child(3),
  .table-row > div:nth-child(4) {
    display: none;
  }
}
</style>