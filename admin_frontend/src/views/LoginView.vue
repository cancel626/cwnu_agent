<template>
  <div class="flex h-screen w-full items-center justify-center bg-surface-dim">
    <div class="w-full max-w-md p-8">
      <div class="text-center mb-10">
        <h1 class="font-headline-lg text-primary text-3xl font-bold mb-2">西华师范数智瞭望系统</h1>
        <p class="font-body-sm text-on-surface/60">管理控制台 V2.0.4</p>
      </div>

      <div class="pixel-card p-8">
        <h2 class="font-title-md text-white text-xl mb-6 text-center">管理员登录</h2>

        <form class="space-y-5" @submit.prevent="handleLogin">
          <div>
            <label class="font-label-pixel text-primary text-xs block mb-2">账号</label>
            <input
              v-model="username"
              type="text"
              required
              placeholder="请输入管理员账号"
              class="w-full bg-surface-container-high border border-outline-variant rounded px-4 py-3 text-white placeholder:text-on-surface-variant/40 focus:border-primary focus:outline-none transition-colors"
            />
          </div>

          <div>
            <label class="font-label-pixel text-primary text-xs block mb-2">密码</label>
            <input
              v-model="password"
              type="password"
              required
              placeholder="请输入密码"
              class="w-full bg-surface-container-high border border-outline-variant rounded px-4 py-3 text-white placeholder:text-on-surface-variant/40 focus:border-primary focus:outline-none transition-colors"
            />
          </div>

          <div v-if="errorMsg" class="text-error text-sm text-center py-2 border border-error/40 bg-error-container/20 rounded">
            {{ errorMsg }}
          </div>

          <button
            :disabled="isLoading"
            type="submit"
            class="w-full bg-primary text-on-primary font-title-md py-3 rounded pixel-btn-shadow block-3d transition-all disabled:opacity-50"
          >
            <span v-if="!isLoading">执行登录</span>
            <span v-else class="inline-block w-5 h-5 border-2 border-on-primary/30 border-t-on-primary rounded-full animate-spin"></span>
          </button>
        </form>
      </div>

      <p class="text-center text-on-surface/40 text-xs mt-8 font-label-pixel">
        &copy; 2026 西华师范大学 / 数据加密 256-BIT
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/index.js'
import { adminLogin } from '@/api/admin.js'

const router = useRouter()
const store = useAppStore()

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  errorMsg.value = ''
  isLoading.value = true

  try {
    const result = await adminLogin({
      username: username.value,
      password: password.value
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
      router.push('/')
    } else {
      errorMsg.value = result.message || '登录失败'
    }
  } catch (err) {
    errorMsg.value = err.message || '网络请求失败'
  } finally {
    isLoading.value = false
  }
}
</script>
