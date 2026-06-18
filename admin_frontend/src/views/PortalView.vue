<template>
  <div class="portal-page">
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>
    <div class="scanline"></div>

    <div class="container">
      <div class="logo-area">
        <div class="logo-icon">
          <span class="material-symbols-outlined" style="font-size: 32px; color: #00dbe7;">hub</span>
        </div>
        <h1>XNU 数智枢纽</h1>
        <p>统一身份认证网关</p>
      </div>

      <div class="login-box">
        <!-- 身份切换 -->
        <div class="tab-switch">
          <button :class="{ active: activeTab === 'user' }" @click="activeTab = 'user'">
            <span class="material-symbols-outlined" style="font-size: 16px; vertical-align: middle; margin-right: 4px;">person</span>
            用户登录
          </button>
          <button :class="{ active: activeTab === 'admin' }" @click="activeTab = 'admin'">
            <span class="material-symbols-outlined" style="font-size: 16px; vertical-align: middle; margin-right: 4px;">shield_person</span>
            管理员登录
          </button>
        </div>

        <div v-if="activeTab === 'user'">
          <div class="input-group">
            <label>账号</label>
            <input v-model="userForm.username" type="text" placeholder="请输入用户名" @keydown.enter="doUserLogin" />
          </div>
          <div class="input-group">
            <label>密码</label>
            <input v-model="userForm.password" type="password" placeholder="请输入密码" @keydown.enter="doUserLogin" />
          </div>
          <button class="login-btn" :disabled="userLoading" @click="doUserLogin">
            <span class="material-symbols-outlined" style="font-size: 18px;">login</span>
            <span>{{ userLoading ? '登录中...' : '安全登录' }}</span>
          </button>
        </div>

        <div v-else>
          <div class="input-group">
            <label>账号 / ID</label>
            <input v-model="adminForm.username" type="text" placeholder="请输入工号" @keydown.enter="doAdminLogin" />
          </div>
          <div class="input-group">
            <label>访问密钥</label>
            <input v-model="adminForm.password" type="password" placeholder="请输入密码" @keydown.enter="doAdminLogin" />
          </div>
          <button class="login-btn" :disabled="adminLoading" @click="doAdminLogin">
            <span class="material-symbols-outlined" style="font-size: 18px;">admin_panel_settings</span>
            <span>{{ adminLoading ? '登录中...' : '管理员登录' }}</span>
          </button>
        </div>

        <div v-if="toast.msg" class="toast" :class="toast.type">
          {{ toast.msg }}
        </div>

        <div class="divider">快速入口</div>

        <div class="portals">
          <a href="/user-login/" class="portal-btn">
            <span class="material-symbols-outlined">person_add</span>
            <span>用户注册</span>
          </a>
          <a href="/admin-login/" class="portal-btn">
            <span class="material-symbols-outlined">admin_panel_settings</span>
            <span>管理员注册</span>
          </a>
          <a href="/user/" class="portal-btn">
            <span class="material-symbols-outlined">dashboard</span>
            <span>用户工作台</span>
          </a>
          <a href="/admin/" class="portal-btn">
            <span class="material-symbols-outlined">settings</span>
            <span>管理控制台</span>
          </a>
        </div>
      </div>
    </div>

    <div class="status-bar">
      <span class="status-dot"></span>
      <span>SYSTEM ONLINE • GATEWAY v1.1 • 所有子系统正常运行</span>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/index.js'
import { adminLogin } from '@/api/admin.js'

const router = useRouter()
const store = useAppStore()

const activeTab = ref('user')
const userLoading = ref(false)
const adminLoading = ref(false)
const toast = reactive({ msg: '', type: '' })

const userForm = reactive({ username: '', password: '' })
const adminForm = reactive({ username: '', password: '' })

function showToast(msg, type) {
  toast.msg = msg
  toast.type = type
  setTimeout(() => { toast.msg = '' }, 4000)
}

async function doUserLogin() {
  if (!userForm.username || !userForm.password) {
    showToast('请填写账号和密码', 'error')
    return
  }
  userLoading.value = true
  try {
    const res = await fetch('/api/v1/user/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: userForm.username, password: userForm.password })
    })
    const data = await res.json()
    if (data.code === 200 && data.data) {
      localStorage.setItem('user_token', data.data.access_token)
      localStorage.setItem('user_info', JSON.stringify(data.data.user))
      showToast('登录成功，正在跳转...', 'success')
      setTimeout(() => { window.location.href = '/user/'; }, 1500)
    } else {
      showToast(data.message || '登录失败', 'error')
    }
  } catch (e) {
    showToast('网络错误，请检查后端服务', 'error')
  } finally {
    userLoading.value = false
  }
}

async function doAdminLogin() {
  if (!adminForm.username || !adminForm.password) {
    showToast('请填写账号和密码', 'error')
    return
  }
  adminLoading.value = true
  try {
    const result = await adminLogin({
      username: adminForm.username,
      password: adminForm.password
    })

    if (result.code === 200 && result.data) {
      localStorage.setItem('admin_token', result.data.access_token)
      localStorage.setItem('admin_info', JSON.stringify(result.data.admin))
      store.user = {
        id: result.data.admin.id,
        username: result.data.admin.username,
        name: result.data.admin.nickname || result.data.admin.username,
        role: result.data.admin.is_superuser ? '超级管理员' : '系统管理员',
        avatar: result.data.admin.avatar || '',
        is_superuser: result.data.admin.is_superuser
      }
      showToast('登录成功，正在跳转...', 'success')
      setTimeout(() => { router.push('/dashboard') }, 1500)
    } else {
      showToast(result.message || '登录失败', 'error')
    }
  } catch (e) {
    showToast(e.message || '网络错误', 'error')
  } finally {
    adminLoading.value = false
  }
}
</script>

<style scoped>
.portal-page {
  min-height: 100vh;
  background: #0a0a0f;
  color: #e3e2e2;
  font-family: 'Space Grotesk', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,219,231,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,219,231,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
}
.bg-glow {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,219,231,0.08) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}
.scanline {
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.03) 2px,
    rgba(0,0,0,0.03) 4px
  );
  pointer-events: none;
  z-index: 5;
}
.container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  padding: 0 20px;
}
.logo-area {
  text-align: center;
  margin-bottom: 40px;
}
.logo-icon {
  width: 64px;
  height: 64px;
  background: rgba(0,219,231,0.1);
  border: 1px solid rgba(0,219,231,0.3);
  border-radius: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-shadow: 0 0 30px rgba(0,219,231,0.15);
}
.logo-area h1 {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #e1fdff;
  margin-bottom: 8px;
}
.logo-area p {
  font-size: 13px;
  color: rgba(227,226,226,0.5);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.login-box {
  background: rgba(18,20,30,0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0,219,231,0.15);
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.tab-switch {
  display: flex;
  margin-bottom: 24px;
  background: rgba(10,10,15,0.5);
  border-radius: 10px;
  padding: 4px;
}
.tab-switch button {
  flex: 1;
  padding: 10px;
  background: transparent;
  border: none;
  color: rgba(227,226,226,0.5);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
  font-family: inherit;
}
.tab-switch button.active {
  background: rgba(0,219,231,0.12);
  color: #e1fdff;
}
.input-group {
  margin-bottom: 16px;
}
.input-group label {
  display: block;
  font-size: 11px;
  font-weight: 500;
  color: rgba(227,226,226,0.6);
  margin-bottom: 8px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.input-group input {
  width: 100%;
  background: rgba(10,10,15,0.6);
  border: 1px solid rgba(0,219,231,0.15);
  border-radius: 10px;
  padding: 12px 16px;
  color: #e3e2e2;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
  font-family: inherit;
}
.input-group input:focus {
  border-color: rgba(0,219,231,0.5);
  box-shadow: 0 0 15px rgba(0,219,231,0.1);
}
.input-group input::placeholder {
  color: rgba(227,226,226,0.25);
}
.login-btn {
  width: 100%;
  padding: 14px;
  background: rgba(0,219,231,0.12);
  border: 1px solid rgba(0,219,231,0.3);
  border-radius: 10px;
  color: #e1fdff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.login-btn:hover {
  background: rgba(0,219,231,0.2);
  box-shadow: 0 0 25px rgba(0,219,231,0.2);
  transform: translateY(-1px);
}
.login-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
.toast {
  margin-top: 16px;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 13px;
}
.toast.success {
  background: rgba(47,248,1,0.1);
  border: 1px solid rgba(47,248,1,0.2);
  color: #2ff801;
}
.toast.error {
  background: rgba(255,50,50,0.1);
  border: 1px solid rgba(255,50,50,0.2);
  color: #ff5555;
}
.divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
  gap: 12px;
  font-size: 11px;
  color: rgba(227,226,226,0.3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.divider::before, .divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(0,219,231,0.1);
}
.portals {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.portal-btn {
  padding: 14px 10px;
  background: rgba(10,10,15,0.5);
  border: 1px solid rgba(0,219,231,0.1);
  border-radius: 12px;
  color: #e3e2e2;
  text-decoration: none;
  text-align: center;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}
.portal-btn:hover {
  border-color: rgba(0,219,231,0.4);
  background: rgba(0,219,231,0.05);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,219,231,0.1);
}
.portal-btn .material-symbols-outlined {
  font-size: 24px;
  color: #00dbe7;
}
.portal-btn span:last-child {
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.05em;
}
.status-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: rgba(227,226,226,0.4);
  font-family: 'Space Mono', monospace;
  border-top: 1px solid rgba(0,219,231,0.05);
  background: rgba(10,10,15,0.8);
}
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #2ff801;
  box-shadow: 0 0 8px #2ff801;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
