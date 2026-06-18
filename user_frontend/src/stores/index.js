import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getUserMe } from '../api/user.js'

export const useAppStore = defineStore('app', () => {
  const stored = localStorage.getItem('user_info')
  const parsed = stored ? JSON.parse(stored) : null

  const user = ref({
    name: parsed?.nickname || parsed?.username || '用户',
    id: parsed?.id ? String(parsed.id) : '1946-XNU',
    role: '高级研究员',
    avatar: parsed?.avatar || ''
  })

  async function fetchUserInfo() {
    try {
      const res = await getUserMe()
      if (res.code === 200 && res.data) {
        const d = res.data
        user.value = {
          name: d.nickname || d.username || '用户',
          id: String(d.id),
          role: '高级研究员',
          avatar: d.avatar || ''
        }
        localStorage.setItem('user_info', JSON.stringify(user.value))
      }
    } catch (e) {
      console.error('获取用户信息失败:', e)
    }
  }

  function logout() {
    localStorage.removeItem('user_token')
    localStorage.removeItem('user_info')
    user.value = {
      name: '用户',
      id: '1946-XNU',
      role: '高级研究员',
      avatar: ''
    }
    window.location.href = '/user-login/'
  }

  return { user, fetchUserInfo, logout }
})
