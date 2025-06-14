<template>
  <div class="performance-view" style="margin-top: 20px;">
    <div class="performance-header">
      <h1>绩效看板</h1>
      <button @click="calculatePerformance" class="btn btn-primary" :disabled="calculating">
        {{ calculating ? '计算中...' : '重新计算绩效' }}
      </button>
    </div>    <div class="performance-stats">
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
        <h2>绩效排行榜</h2>
        <div class="performance-table">
          <div class="table-header">
            <div class="rank-header">排名</div>
            <div class="name-header">姓名</div>
            <div class="email-header">邮箱</div>
            <div class="profile-header">简介</div>
            <div class="score-header">绩效分数</div>
            <div class="status-header">状态</div>
          </div>
          <div v-for="(user, index) in sortedUsers" :key="user.id" class="table-row">
            <div class="rank-cell">
              <span class="rank-badge">{{ index + 1 }}</span>
            </div>
            <div class="name-cell">{{ user.username }}</div>
            <div class="email-cell">{{ user.email }}</div>
            <div class="profile-cell">{{ user.profile || '暂无简介' }}</div>
            <div class="score-cell">
              <span class="score-badge">{{ user.performance?.toFixed(1) || '0.0' }}</span>
            </div>
            <div class="status-cell">
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
  setup() {    const userStore = useUserStore();

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
    };    onMounted(async () => {
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
  font-size: 32px;
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
  display: block;
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

.performance-table {
  display: grid;
  grid-template-columns: 100px 140px 200px 2fr 120px 120px;
  gap: 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e1e5e9;
}

.table-header {
  display: contents;
  font-weight: 500;
  color: #2c3e50;
  background: #f8f9fa;
}

.table-header > div {
  padding: 15px 12px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  border-right: 1px solid #e9ecef;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.table-header > div:last-child {
  border-right: none;
}

.rank-header,
.score-header,
.status-header {
  justify-content: center;
}

.name-header,
.email-header,
.profile-header {
  justify-content: flex-start;
}

.table-row {
  display: contents;
}

.table-row:nth-child(even) > div {
  background: #fafbfc;
}

.table-row:nth-child(odd) > div {
  background: #ffffff;
}

.table-row:hover > div {
  background: #f0f4f7 !important;
  transition: background-color 0.2s ease;
}

.table-row > div {
  padding: 14px 12px;
  border-bottom: 1px solid #f1f3f5;
  border-right: 1px solid #f1f3f5;
  display: flex;
  align-items: center;
  font-size: 14px;
  min-height: 55px;
}

.table-row > div:last-child {
  border-right: none;
}

.rank-cell {
  justify-content: center;
}

.rank-badge {
  width: 32px;
  height: 32px;
  color: white;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

/* 前三名特殊样式 */
.table-row:nth-child(2) .rank-badge { /* 第一名 */
  background: #FFD700;
  color: #B8860B;
  box-shadow: 0 3px 8px rgba(255, 215, 0, 0.5);
  font-size: 15px;
}

.table-row:nth-child(3) .rank-badge { /* 第二名 */
  background: #C0C0C0;
  color: #696969;
  box-shadow: 0 3px 8px rgba(192, 192, 192, 0.5);
  font-size: 15px;
}

.table-row:nth-child(4) .rank-badge { /* 第三名 */
  background: #CD7F32;
  color: #8B4513;
  box-shadow: 0 3px 8px rgba(205, 127, 50, 0.5);
  font-size: 15px;
}

.table-row:nth-child(n+5) .rank-badge { /* 第四名及以后 */
  background: #95a5a6;
}

.name-cell {
  font-weight: 500;
  color: #2c3e50;
  justify-content: center;
}

.email-cell {
  color: #6c757d;
  font-size: 13px;
  justify-content: flex-start;
  word-break: break-all;
}

.profile-cell {
  color: #6c757d;
  font-size: 13px;
  justify-content: flex-start;
  line-height: 1.4;
  max-width: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.score-cell {
  justify-content: center;
}

.score-badge {
  color: #3498db;
  font-weight: 600;
  font-size: 14px;
}

.status-cell {
  justify-content: center;
}

.outstanding-badge {
  background: linear-gradient(135deg, #f39c12, #e67e22);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  box-shadow: 0 4px 12px rgba(243, 156, 18, 0.5);
  position: relative;
  overflow: hidden;
}

.outstanding-badge::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shine 2s infinite;
}

@keyframes shine {
  0% { left: -100%; }
  100% { left: 100%; }
}

.normal-badge {
  background: #ecf0f1;
  color: #7f8c8d;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid #bdc3c7;
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
  .performance-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .performance-table {
    grid-template-columns: 60px 1fr 100px;
    font-size: 12px;
  }
  
  .table-header > div {
    font-size: 12px;
  }
  
  .table-header > div:nth-child(3),
  .table-header > div:nth-child(4),
  .table-row > div:nth-child(3),
  .table-row > div:nth-child(4) {
    display: none;
  }

  .table-row > div {
    min-height: 50px;
    padding: 12px 10px;
  }

  .rank-badge {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }

  .table-row:nth-child(2) .rank-badge,
  .table-row:nth-child(3) .rank-badge,
  .table-row:nth-child(4) .rank-badge {
    font-size: 13px;
  }

  .outstanding-badge,
  .normal-badge {
    padding: 6px 12px;
    font-size: 11px;
  }

  .score-badge {
    padding: 3px 8px;
    font-size: 11px;
  }
}
</style>