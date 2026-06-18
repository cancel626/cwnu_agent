<template>
  <div class="h-screen w-screen bg-surface-dim overflow-hidden flex flex-col">
    <header class="relative z-10 w-full h-20 flex items-center justify-between px-container-margin header-bg">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-primary-container flex items-center justify-center pixel-corners">
          <span class="material-symbols-outlined text-on-primary-container text-2xl">monitoring</span>
        </div>
        <div>
          <h2 class="font-label-pixel text-primary text-xs uppercase tracking-widest">数字智能</h2>
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 bg-secondary-fixed-dim animate-pulse"></span>
            <span class="text-on-surface-variant text-sm font-label-pixel">系统状态: 运行中</span>
          </div>
        </div>
      </div>
      <div class="absolute left-1/2 -translate-x-1/2 text-center">
        <h1 class="font-headline-lg text-headline-lg text-primary tracking-tighter">西华师范数智瞭望实时大屏</h1>
        <div class="flex justify-center gap-8 mt-1">
          <div class="h-[2px] w-24 bg-gradient-to-r from-transparent via-primary to-transparent"></div>
        </div>
      </div>
      <div class="flex items-center gap-6">
        <button
          @click="$router.push('/dashboard')"
          class="flex items-center gap-2 px-4 py-2 bg-primary-container text-on-primary-container border border-primary hover:bg-primary hover:text-on-primary transition-all font-label-pixel"
        >
          <span class="material-symbols-outlined text-sm">arrow_back</span>
          返回控制台
        </button>
        <div class="text-right">
          <div class="font-label-pixel text-secondary-fixed-dim text-lg">{{ currentTime }}</div>
          <div class="text-xs text-on-surface-variant font-label-pixel">{{ currentDate }}</div>
        </div>
      </div>
    </header>
    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentTime = ref('12:00:00')
const currentDate = ref('2024.10.24 星期四')
let timer = null

function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false })
  const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  currentDate.value = `${now.getFullYear()}.${String(now.getMonth() + 1).padStart(2, '0')}.${String(now.getDate()).padStart(2, '0')} ${days[now.getDay()]}`
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>
