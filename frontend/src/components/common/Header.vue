<template>
  <header class="app-header">
    <div class="header-brand">
      <h1>项目协作管理平台</h1>
    </div>
    <div class="header-actions">
      <div class="user-menu">
        <div class="user-info" @click="toggleProfileDropdown">
          <div class="user-avatar">
            <span>{{ userInitial }}</span>
            <div class="status-dot"></div>
          </div>
          <div class="user-details">
            <span class="username">{{ authStore.user?.username }}</span>
            <span class="user-role">{{ getRoleTextDisplay(authStore.user?.role) }}</span>
          </div>
          <div class="dropdown-arrow" :class="{ 'open': showProfileDropdown }">▼</div>
        </div>
        
        <!-- Profile Dropdown -->
        <div v-if="showProfileDropdown" class="profile-dropdown" @click.stop>
          <div class="profile-header">
            <div class="profile-avatar">{{ userInitial }}</div>
            <div class="profile-info">
              <h4>{{ authStore.user?.username }}</h4>
              <p>{{ authStore.user?.email }}</p>
            </div>
          </div>
          
          <div class="profile-form">
            <div class="form-group">
              <label>用户名</label>
              <input
                v-model="editForm.username"
                type="text"
                class="form-input"
                :disabled="!isEditing"
              />
            </div>
            
            <div class="form-group">
              <label>邮箱</label>
              <input
                v-model="editForm.email"
                type="email"
                class="form-input"
                :disabled="!isEditing"
              />
            </div>
            
            <template v-if="isChangingPassword">
              <div class="form-group">
                <label>当前密码</label>
                <input
                  v-model="passwordForm.currentPassword"
                  type="password"
                  class="form-input"
                  placeholder="请输入当前密码"
                />
              </div>
              
              <div class="form-group">
                <label>新密码</label>
                <input
                  v-model="passwordForm.newPassword"
                  type="password"
                  class="form-input"
                  placeholder="请输入新密码"
                />
              </div>
              
              <div class="form-group">
                <label>确认新密码</label>
                <input
                  v-model="passwordForm.confirmPassword"
                  type="password"
                  class="form-input"
                  placeholder="请再次输入新密码"
                />
              </div>
            </template>
            
            <div v-if="updateError" class="error-message">{{ updateError }}</div>
            <div v-if="updateSuccess" class="success-message">{{ updateSuccess }}</div>
            
            <div class="form-actions">
              <template v-if="!isEditing && !isChangingPassword">
                <button @click="startEdit" class="btn btn-primary">
                  编辑信息
                </button>
                <button @click="startChangePassword" class="btn btn-warning">
                  修改密码
                </button>
              </template>
              
              <template v-else-if="isEditing">
                <button
                  @click="saveChanges"
                  class="btn btn-success"
                  :disabled="saving"
                >
                  {{ saving ? '保存中...' : '保存' }}
                </button>
                <button @click="cancelEdit" class="btn btn-secondary">
                  取消
                </button>
              </template>
              
              <template v-else-if="isChangingPassword">
                <button
                  @click="savePassword"
                  class="btn btn-success"
                  :disabled="saving"
                >
                  {{ saving ? '修改中...' : '确认修改' }}
                </button>
                <button @click="cancelChangePassword" class="btn btn-secondary">
                  取消
                </button>
              </template>
            </div>
          </div>
        </div>
        
        <button @click="logout" class="logout-btn">
          <i class="icon">🚪</i>
          <span>退出</span>
        </button>
      </div>
    </div>
    
    <!-- Overlay -->
    <div v-if="showProfileDropdown" class="dropdown-overlay" @click="closeProfileDropdown"></div>
  </header>
</template>

<script lang="ts">
import { defineComponent, computed, ref, reactive, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { getRoleText } from '@/utils/helpers';

export default defineComponent({
  name: 'Header',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const showProfileDropdown = ref(false);
    const isEditing = ref(false);
    const isChangingPassword = ref(false);
    const saving = ref(false);
    const updateError = ref('');
    const updateSuccess = ref('');
    
    const editForm = reactive({
      username: '',
      email: ''
    });

    const passwordForm = reactive({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });

    const userInitial = computed(() => {
      return authStore.user?.username?.charAt(0).toUpperCase() || 'U';
    });

    const getRoleTextDisplay = (role: string | undefined) => {
      return getRoleText(role);
    };

    const logout = () => {
      authStore.logout();
      router.push('/login');
    };

    const toggleProfileDropdown = () => {
      showProfileDropdown.value = !showProfileDropdown.value;
      if (showProfileDropdown.value) {
        resetForm();
      }
    };

    const closeProfileDropdown = () => {
      showProfileDropdown.value = false;
      if (isEditing.value) {
        cancelEdit();
      }
      if (isChangingPassword.value) {
        cancelChangePassword();
      }
    };

    const resetForm = () => {
      editForm.username = authStore.user?.username || '';
      editForm.email = authStore.user?.email || '';
    };

    const resetPasswordForm = () => {
      passwordForm.currentPassword = '';
      passwordForm.newPassword = '';
      passwordForm.confirmPassword = '';
    };

    const startEdit = () => {
      isEditing.value = true;
      updateError.value = '';
      updateSuccess.value = '';
    };

    const cancelEdit = () => {
      isEditing.value = false;
      resetForm();
      updateError.value = '';
      updateSuccess.value = '';
    };

    const startChangePassword = () => {
      isChangingPassword.value = true;
      resetPasswordForm();
      updateError.value = '';
      updateSuccess.value = '';
    };

    const cancelChangePassword = () => {
      isChangingPassword.value = false;
      resetPasswordForm();
      updateError.value = '';
      updateSuccess.value = '';
    };

    const savePassword = async () => {
      if (!passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
        updateError.value = '请填写所有密码字段';
        return;
      }

      if (passwordForm.newPassword !== passwordForm.confirmPassword) {
        updateError.value = '新密码两次输入不一致';
        return;
      }

      if (passwordForm.newPassword.length < 6) {
        updateError.value = '新密码长度至少6位';
        return;
      }

      saving.value = true;
      updateError.value = '';
      updateSuccess.value = '';

      try {
        await authStore.changePassword({
          currentPassword: passwordForm.currentPassword,
          newPassword: passwordForm.newPassword
        });
        
        updateSuccess.value = '密码修改成功';
        isChangingPassword.value = false;
        resetPasswordForm();
        
        setTimeout(() => {
          updateSuccess.value = '';
        }, 3000);
      } catch (error: any) {
        updateError.value = error.message || '密码修改失败，请稍后重试';
      } finally {
        saving.value = false;
      }
    };

    const saveChanges = async () => {
      if (!editForm.username.trim() || !editForm.email.trim()) {
        updateError.value = '用户名和邮箱不能为空';
        return;
      }

      saving.value = true;
      updateError.value = '';
      updateSuccess.value = '';

      try {
        // 调用用户更新API
        await authStore.updateUserInfo({
          username: editForm.username.trim(),
          email: editForm.email.trim()
        });
        
        updateSuccess.value = '信息更新成功';
        isEditing.value = false;
        
        setTimeout(() => {
          updateSuccess.value = '';
        }, 3000);
      } catch (error: any) {
        updateError.value = error.message || '更新失败，请稍后重试';
      } finally {
        saving.value = false;
      }
    };

    // Close dropdown when clicking outside
    const handleClickOutside = (event: Event) => {
      const target = event.target as HTMLElement;
      const userMenu = document.querySelector('.user-menu');
      if (userMenu && !userMenu.contains(target)) {
        closeProfileDropdown();
      }
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
      resetForm();
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      authStore,
      userInitial,
      getRoleTextDisplay,
      logout,
      showProfileDropdown,
      isEditing,
      isChangingPassword,
      saving,
      updateError,
      updateSuccess,
      editForm,
      passwordForm,
      toggleProfileDropdown,
      closeProfileDropdown,
      startEdit,
      cancelEdit,
      startChangePassword,
      cancelChangePassword,
      saveChanges,
      savePassword
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
  position: relative;
  z-index: 100;
}

.header-brand h1 {
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  border-radius: 8px;
  transition: background-color 0.2s;
  cursor: pointer;
}

.user-info:hover {
  background: #f8f9fa;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
  position: relative;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
}

.status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  background: #28a745;
  border: 2px solid white;
  border-radius: 50%;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.username {
  color: #2c3e50;
  font-weight: 600;
  font-size: 14px;
  line-height: 1.2;
}

.user-role {
  color: #6c757d;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.2;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(231, 76, 60, 0.3);
}

.logout-btn:hover {
  background: linear-gradient(135deg, #c0392b, #a93226);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.4);
}

.logout-btn .icon {
  font-size: 14px;
}

.dropdown-arrow {
  color: #6c757d;
  font-size: 10px;
  transition: transform 0.2s;
  margin-left: 4px;
}

.dropdown-arrow.open {
  transform: rotate(180deg);
}

.profile-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  width: 320px;
  z-index: 1001;
  animation: fadeInDown 0.2s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.profile-header {
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  display: flex;
  align-items: center;
  gap: 12px;
}

.profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
}

.profile-info h4 {
  margin: 0 0 4px 0;
  color: #2c3e50;
  font-size: 16px;
}

.profile-info p {
  margin: 0;
  color: #6c757d;
  font-size: 13px;
}

.profile-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: #495057;
  font-size: 13px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-input:disabled {
  background: #f8f9fa;
  color: #6c757d;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 12px;
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 12px;
}

.form-actions {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #218838;
}

.btn-success:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background: #e0a800;
}

.dropdown-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  background: transparent;
}
</style>