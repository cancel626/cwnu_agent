import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getAdminMe } from '../api/admin.js'

export const useAppStore = defineStore('app', () => {
  // 从 localStorage 初始化，避免闪烁
  const stored = localStorage.getItem('admin_info')
  const parsed = stored ? JSON.parse(stored) : null

  const user = ref({
    id: parsed?.id || 0,
    username: parsed?.username || '',
    name: parsed?.nickname || parsed?.username || '管理员',
    role: parsed?.is_superuser ? '超级管理员' : '系统管理员',
    avatar: parsed?.avatar || '',
    is_superuser: parsed?.is_superuser || false,
  })

  const isLoggedIn = computed(() => !!user.value.id)

  async function fetchUserInfo() {
    try {
      const res = await getAdminMe()
      if (res.code === 200 && res.data) {
        const d = res.data
        user.value = {
          id: d.id,
          username: d.username,
          name: d.nickname || d.username,
          role: d.is_superuser ? '超级管理员' : '系统管理员',
          avatar: d.avatar || '',
          is_superuser: d.is_superuser,
        }
        localStorage.setItem('admin_info', JSON.stringify(user.value))
      }
    } catch (e) {
      console.error('获取用户信息失败:', e)
    }
  }

  function logout() {
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_info')
    user.value = { id: 0, username: '', name: '', role: '', avatar: '', is_superuser: false }
    window.location.href = '/'
  }

  return { user, isLoggedIn, fetchUserInfo, logout }
})
