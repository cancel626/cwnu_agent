<template>
  <header class="fixed top-0 right-0 w-[calc(100%-260px)] h-16 z-40 bg-surface/80 backdrop-blur-md border-b-2 border-outline-variant shadow-sm flex justify-between items-center px-container-margin">
    <div class="flex items-center gap-4">
      <div class="relative group">
        <span class="absolute inset-y-0 left-3 flex items-center text-on-surface-variant">
          <span class="material-symbols-outlined text-[20px]">search</span>
        </span>
        <input
          v-model="searchQuery"
          class="bg-surface-container-high border-none text-on-surface text-body-sm pl-10 pr-4 py-2 w-64 focus:ring-2 focus:ring-primary-container transition-all"
          placeholder="搜索资源或任务..."
          type="text"
        />
      </div>
    </div>
    <div class="flex items-center gap-6">
      <div class="flex items-center gap-4">
        <button class="text-on-surface-variant hover:text-primary transition-colors relative">
          <span class="material-symbols-outlined">notifications</span>
          <span class="absolute top-0 right-0 w-2 h-2 bg-secondary-fixed rounded-full"></span>
        </button>
        <button class="text-on-surface-variant hover:text-primary transition-colors">
          <span class="material-symbols-outlined">settings</span>
        </button>
      </div>
      <div class="h-8 w-[1px] bg-outline-variant mx-2"></div>
      <div class="flex items-center gap-3">
        <div class="text-right">
          <p class="text-body-sm font-bold text-on-surface">{{ store.user.name }}</p>
          <p class="text-[10px] text-secondary-fixed-dim uppercase tracking-tighter">{{ store.user.role }}</p>
        </div>
        <div class="w-10 h-10 rounded-sm border-2 border-outline-variant overflow-hidden bg-surface-variant flex items-center justify-center">
          <img v-if="store.user.avatar" :src="store.user.avatar" alt="Admin Avatar" class="w-full h-full object-cover" />
          <span v-else class="material-symbols-outlined text-on-surface-variant">person</span>
        </div>
        <button @click="store.logout" class="text-error hover:bg-error/10 px-3 py-1 text-label-pixel uppercase border border-error/20 transition-colors">退出登录</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAppStore } from '../stores/index.js'

const searchQuery = ref('')
const store = useAppStore()

onMounted(() => {
  store.fetchUserInfo()
})
</script>
