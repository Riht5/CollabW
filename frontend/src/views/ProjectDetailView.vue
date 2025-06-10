<template>
  <div class="container" style="padding-top: 20px;">
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <div class="error-icon">❌</div>
      <h3>加载失败</h3>
      <p>{{ error }}</p>
      <button @click="fetchProject" class="btn btn-danger btn-sm">重试</button>
    </div>
    
    <div v-else-if="project">
      <div class="page-header">
        <div class="d-flex align-center gap-md">
          <h1>{{ project.name }}</h1>
          <span class="status-badge" :class="project.status">
            {{ getStatusText(project.status) }}
          </span>
        </div>
        <div class="header-actions">
          <button @click="goBackToProjects" class="btn btn-secondary btn-sm">
            <i class="icon">← </i> {{ getBackButtonText() }}
          </button>
        </div>
      </div>

      <div class="grid grid-2 mb-lg">
        <div class="card">
          <div class="card-header">
            <h2>项目信息</h2>
          </div>
          <div class="card-body">
            <div class="form-row cols-2">
              <div class="form-group">
                <label class="form-label">描述</label>
                <p>{{ project.description || '无描述' }}</p>
              </div>
              <div class="form-group">
                <label class="form-label">预计工期</label>
                <p>{{ project.estimated_duration || '未设置' }} 天</p>
              </div>
            </div>
            <div class="form-row cols-2">
              <div class="form-group">
                <label class="form-label">开始时间</label>
                <p>{{ formatDate(project.start_time) || '未设置' }}</p>
              </div>
              <div class="form-group">
                <label class="form-label">结束时间</label>
                <p>{{ formatDate(project.end_time) || '未设置' }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header d-flex justify-between align-center">
            <h2>项目成员 ({{ projectMembers.length }})</h2>
          </div>
          <div class="card-body">
            <div v-if="projectMembers.length" class="d-flex flex-column gap-md">
              <div v-for="user in projectMembers" :key="user.id" class="d-flex align-center gap-md p-md bg-secondary" style="border-radius: var(--radius-sm);">
                <div class="avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
                <div class="flex-1">
                  <h4 class="mb-0">{{ user.username }}</h4>
                  <p class="text-muted mb-0">{{ user.email }}</p>
                  <span class="role-badge" :class="user.role">{{ getRoleText(user.role) }}</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <div class="empty-icon">👥</div>
              <p>暂无分配成员</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="burnDownData?.ideal_progresses?.length !== 0 || null" class="mt-lg">
        <div class="card">
          <div class="card-header d-flex justify-between align-center">
            <h2>燃尽图</h2>
            <span 
              class="wraning-from" :class="burnDownData?.risk_level">
              {{ RiskLevelText(burnDownData?.risk_level ?? RiskLevel.NONE) }}
            </span>
          </div>
          <div class="card-body">
            <BurnoutDiagram 
              :actualProgresses="burnDownData?.actual_progresses ?? []"
              :idealProgresses="burnDownData?.ideal_progresses ?? []"
              :riskLevel="burnDownData?.risk_level ?? RiskLevel.NONE"
            />
          </div>
        </div>
      </div>

      <!-- 项目任务 - 仅非Director角色可见 -->
      <div v-if="!isDirector" class="card mt-lg mb-lg">
        <div class="card-header d-flex justify-between align-center">
          <h2>项目任务 ({{ projectTasks.length }})</h2>
          <!-- 仅 Manager 可见添加任务按钮 -->
          <button 
            v-if="isManager"
            @click="showTaskModal = true" 
            class="btn btn-primary btn-sm"
          >
            <i class="icon">📝</i> 添加任务
          </button>
        </div>
        <div class="card-body">
          <TaskList 
            :tasks="projectTasks" 
            :show-actions="isManager"
            @edit="editTask"
            @delete="deleteTask"
            @toggle-status="toggleTaskStatus"
            @assign-members="assignMembersToTask"
            @update-task="handleTaskUpdate"
          />
        </div>
      </div>

      <!-- Modals - 仅 Manager 可见 -->
      <UserAssignModal
        v-if="showAssignModal && selectedTask && isManager"
        :project-id="project?.id"
        :assigned-users="projectMembers"
        :pre-selected-task="selectedTask"
        @close="showAssignModal = false"
        @assigned="handleUserAssigned"
      />

      <TaskCreateModal
        v-if="showTaskModal && isManager"
        :project-id="project.id"
        @close="showTaskModal = false"
        @created="handleTaskCreated"
      />

      <TaskEditModal
        v-if="showEditTaskModal && editingTask && isManager"
        :task="editingTask"
        @close="showEditTaskModal = false"
        @updated="handleTaskUpdated"
        @deleted="handleTaskDeleted"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import { useTaskStore } from '@/stores/task';
import { useAuthStore } from '@/stores/auth';
import { getStatusText, getRoleText, getRiskLevelText } from '@/utils/helpers';
import TaskList from '@/components/tasks/TaskList.vue';
import BurnoutDiagram from '@/components/tasks/BurnoutDiagram.vue';
import UserAssignModal from '@/components/modals/UserAssignModal.vue';
import TaskCreateModal from '@/components/modals/TaskCreateModal.vue';
import TaskEditModal from '@/components/modals/TaskEditModal.vue';
import { Project, Task, User, BurnDownProject , RiskLevel } from '@/types/index';

export default defineComponent({
  name: 'ProjectDetailView',
  components: {
    TaskList,
    BurnoutDiagram,
    UserAssignModal,
    TaskCreateModal,
    TaskEditModal,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const projectStore = useProjectStore();
    const taskStore = useTaskStore();
    const authStore = useAuthStore();
    
    const project = ref<Project | null>(null);
    const projectTasks = ref<Task[]>([]);
    const projectMembers = ref<User[]>([]);
    const burnDownData = ref<BurnDownProject | null>(null)
    const loading = ref(false);
    const error = ref('');
    const showAssignModal = ref(false);
    const showTaskModal = ref(false);
    const showEditTaskModal = ref(false);    const editingTask = ref<Task | null>(null);
    const selectedTask = ref<Task | null>(null);

    const RiskLevelText = (level: RiskLevel) => {
      return getRiskLevelText(level);
    };

    const formatDate = (dateStr?: string) => {
      if (!dateStr) return '';
      return new Date(dateStr).toLocaleDateString();
    };

    const fetchProject = async () => {
      loading.value = true;
      error.value = '';
      try {
        const projectId = route.params.id as string;
        
        // 并行获取项目基本信息、任务和成员
        const [projectData, tasks, members] = await Promise.all([
          projectStore.fetchProjectById(projectId),
          projectStore.fetchProjectTasks(projectId),
          projectStore.fetchProjectMembers(projectId)
        ]);
        
        project.value = projectData;
        projectTasks.value = tasks;
        projectMembers.value = members;

        // 获取燃尽图板块的数据
        burnDownData.value = await projectStore.fetchBurnDown(projectId);
      } catch (err: any) {
        error.value = err.message || '加载项目失败';
      } finally {
        loading.value = false;
      }
    };

    const removeUser = async (userId: number) => {
      if (!project.value) return;
      if (confirm('确定要移除此成员吗？')) {
        try {
          // 实现移除用户逻辑
          await projectStore.removeUserFromProject(project.value.id, userId);
          await fetchProject();
        } catch (err) {
          console.error('移除用户失败:', err);
        }
      }
    };

    const editTask = (task: Task) => {
      editingTask.value = task;
      showEditTaskModal.value = true;
    };

    const deleteTask = async (taskId: number) => {
      if (confirm('确定要删除此任务吗？')) {
        try {
          await taskStore.deleteTask(taskId);
          await fetchProject();
        } catch (err) {
          console.error('删除任务失败:', err);
        }
      }
    };

    const toggleTaskStatus = async (task: Task) => {
      try {
        await taskStore.updateTask(task.id, { finished: !task.finished });
        await fetchProject();
      } catch (err) {
        console.error('更新任务状态失败:', err);
      }
    };

    const assignMembersToTask = (task: Task) => {
      selectedTask.value = task;
      showAssignModal.value = true;
    };

    const handleUserAssigned = async () => {
      showAssignModal.value = false;
      selectedTask.value = null;
      // 重新获取项目数据以更新任务成员信息
      await fetchProject();
    };

    const handleTaskCreated = () => {
      showTaskModal.value = false;
      fetchProject();
    };

    const handleTaskUpdated = () => {
      showEditTaskModal.value = false;
      editingTask.value = null;
      fetchProject();
    };

    const handleTaskDeleted = () => {
      showEditTaskModal.value = false;
      editingTask.value = null;
      fetchProject();
    };

    const handleTaskUpdate = async (taskId: number, updateData: Partial<Task>) => {
      try {
        await taskStore.updateTask(taskId, updateData);
        // 更新本地数据
        const taskIndex = projectTasks.value.findIndex(t => t.id === taskId);
        if (taskIndex !== -1) {
          projectTasks.value[taskIndex] = { ...projectTasks.value[taskIndex], ...updateData };
        }
        console.log('任务更新成功:', updateData);
      } catch (err) {
        console.error('更新任务失败:', err);
        // 如果更新失败，重新获取数据
        await fetchProject();
      }
    };


    const handleTaskReorder = async (reorderedTasks: Task[]) => {
      try {
        // 更新本地状态
        projectTasks.value = reorderedTasks;
        
        // 可以在这里调用API更新服务器端的任务顺序
        // await taskStore.updateTaskOrder(reorderedTasks.map((task, index) => ({
        //   id: task.id,
        //   order: index
        // })));
        
        console.log('任务顺序已更新:', reorderedTasks.map(t => t.name));
      } catch (err) {
        console.error('更新任务顺序失败:', err);
        // 如果更新失败，重新获取数据
        await fetchProject();
      }
    };

    const getBackButtonText = () => {
      const userRole = authStore.user?.role;
      return userRole === 'user' ? '返回工作台' : '返回项目列表';
    };

    const goBackToProjects = () => {
      const userRole = authStore.user?.role;
      if (userRole === 'user') {
        router.push('/personal'); // User角色返回个人工作台
      } else {
        router.push('/projects'); // Director和Manager返回项目列表
      }
    };

    onMounted(fetchProject);

    // 用户角色判断
    const isManager = computed(() => authStore.user?.role === 'manager');
    const isDirector = computed(() => authStore.user?.role === 'director');

    return {
      project,
      projectTasks,
      projectMembers,
      burnDownData,
      loading,
      error,
      showAssignModal,
      showTaskModal,
      showEditTaskModal,
      editingTask,
      selectedTask,
      RiskLevel,
      isManager,
      isDirector,
      getStatusText,
      getRoleText,
      RiskLevelText,
      formatDate,
      fetchProject,
      removeUser,
      editTask,
      deleteTask,
      toggleTaskStatus,
      assignMembersToTask,
      handleUserAssigned,
      handleTaskCreated,
      handleTaskUpdated,
      handleTaskDeleted,
      handleTaskUpdate,
      handleTaskReorder,
      getBackButtonText,
      goBackToProjects,
    };
  },
});

</script>

<style scoped>
.role-badge.director {
  background: #ff6b6b;
  color: white;
}

.role-badge.manager {
  background: #4ecdc4;
  color: white;
}

.role-badge.user {
  background: var(--secondary-color);
  color: white;
}
</style>