<template>
  <aside class="w-20 lg:w-64 flex flex-col border-r border-outline-variant/30 bg-surface-container/50 backdrop-blur-xl z-50 shrink-0">
    <!-- Logo -->
    <div class="h-16 flex items-center px-6 border-b border-outline-variant/20">
      <div class="w-8 h-8 bg-primary-fixed-dim shadow-[0_0_15px_#00dbe7] rounded flex items-center justify-center mr-3 hidden lg:flex">
        <span class="material-symbols-outlined text-background font-bold">hub</span>
      </div>
      <span class="font-headline-sm text-primary-fixed-dim font-bold tracking-tight hidden lg:block">XNU 数智枢纽</span>
      <span class="material-symbols-outlined text-primary-fixed-dim lg:hidden mx-auto">hub</span>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 py-6 px-3 flex flex-col gap-2">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        :class="[
          'flex items-center gap-3 px-3 py-3 rounded-lg transition-all group',
          isActive(item.path)
            ? 'bg-primary/10 text-primary-fixed-dim border border-primary/20'
            : 'text-on-surface-variant hover:bg-primary/5 hover:text-primary'
        ]"
      >
        <span class="material-symbols-outlined" :style="isActive(item.path) ? 'font-variation-settings: &quot;FILL&quot; 1;' : ''">{{ item.icon }}</span>
        <span class="font-body-md hidden lg:block">{{ item.name }}</span>
      </router-link>

      <div class="mt-auto">
        <router-link
          to="/profile"
          :class="[
            'flex items-center gap-3 px-3 py-3 rounded-lg transition-all group',
            isActive('/profile')
              ? 'bg-primary/10 text-primary-fixed-dim border border-primary/20'
              : 'text-on-surface-variant hover:bg-primary/5 hover:text-primary'
          ]"
        >
          <span class="material-symbols-outlined">person</span>
          <span class="font-body-md hidden lg:block">个人中心</span>
        </router-link>
      </div>
    </nav>

    <!-- User Profile Mini -->
    <div class="p-4 border-t border-outline-variant/20 relative">
      <div class="flex items-center justify-between gap-2">
        <router-link to="/profile" class="flex items-center gap-3 p-3 rounded-xl bg-surface-variant/20 flex-1 min-w-0">
          <div class="w-10 h-10 rounded-lg border border-primary/20 bg-surface-container flex items-center justify-center shrink-0">
            <span v-if="!user.avatar" class="material-symbols-outlined text-primary text-lg">person</span>
            <img v-else :src="user.avatar" alt="用户头像" class="w-full h-full rounded-lg object-cover" />
          </div>
          <div class="overflow-hidden hidden lg:block">
            <p class="font-label-tech text-primary truncate">{{ user.name }}</p>
            <p class="font-label-code text-on-surface-variant text-[10px]">{{ user.id }}</p>
          </div>
        </router-link>
        <button @click="logout" title="退出登录" class="w-10 h-10 rounded-xl bg-surface-variant/20 hover:bg-error/10 text-on-surface-variant hover:text-error flex items-center justify-center transition-colors shrink-0">
          <span class="material-symbols-outlined text-lg">logout</span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores'

const route = useRoute()
const store = useAppStore()
const { user, logout } = store

const navItems = [
  { name: '控制台首页', path: '/dashboard', icon: 'home' },
  { name: '数智员工库', path: '/staff', icon: 'smart_toy' },
  { name: '智能问数', path: '/query', icon: 'database' }
]

function isActive(path) {
  const current = route.path.replace(/\/$/, '')
  const target = path.replace(/\/$/, '')
  return current === target || current.endsWith(target)
}
</script>
