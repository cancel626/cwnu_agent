<template>
  <aside class="fixed left-0 top-0 h-full w-[260px] bg-surface-container-lowest border-r-2 border-outline-variant flex flex-col py-gutter px-2 z-50">
    <div class="flex items-center gap-3 px-4 mb-8">
      <div class="w-10 h-10 bg-primary flex items-center justify-center rounded-sm">
        <span class="material-symbols-outlined text-on-primary" style="font-variation-settings: 'FILL' 1;">dataset</span>
      </div>
      <div>
        <h1 class="font-headline-lg text-[18px] text-primary tracking-tight leading-none">数智瞭望系统</h1>
        <p class="text-[10px] text-on-surface-variant uppercase tracking-widest mt-1">管理控制台</p>
      </div>
    </div>

    <nav class="flex-1 space-y-1 custom-scrollbar overflow-y-auto">
      <template v-for="item in navItems" :key="item.path || item.label">
        <!-- 有子菜单的项 -->
        <div v-if="item.children" class="space-y-1">
          <button
            @click="toggleExpand(item.label)"
            :class="[
              'w-full flex items-center justify-between gap-3 px-4 py-3 rounded-sm transition-all duration-200',
              isGroupActive(item)
                ? 'bg-primary-container text-on-primary-container border-r-4 border-secondary-fixed shadow-[0_0_8px_rgba(58,134,255,0.4)]'
                : 'text-on-surface-variant hover:bg-surface-variant hover:text-on-surface'
            ]"
          >
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined">{{ item.icon }}</span>
              <span class="font-title-md text-[14px]">{{ item.label }}</span>
            </div>
            <span class="material-symbols-outlined text-[18px] transition-transform" :class="expanded[item.label] ? 'rotate-180' : ''">expand_more</span>
          </button>
          <div v-show="expanded[item.label]" class="pl-8 space-y-1">
            <router-link
              v-for="child in item.children"
              :key="child.path"
              :to="child.path"
              :class="[
                'block px-4 py-2 rounded-sm transition-all duration-200 text-[13px]',
                isActive(child.path)
                  ? 'bg-secondary-container text-on-secondary-container font-medium'
                  : 'text-on-surface-variant hover:bg-surface-variant hover:text-on-surface'
              ]"
            >
              {{ child.label }}
            </router-link>
          </div>
        </div>
        <!-- 普通项 -->
        <router-link
          v-else
          :to="item.path"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-sm transition-all duration-200',
            isActive(item.path)
              ? 'bg-primary-container text-on-primary-container border-r-4 border-secondary-fixed shadow-[0_0_8px_rgba(58,134,255,0.4)]'
              : 'text-on-surface-variant hover:bg-surface-variant hover:text-on-surface'
          ]"
        >
          <span class="material-symbols-outlined">{{ item.icon }}</span>
          <span class="font-title-md text-[14px]">{{ item.label }}</span>
        </router-link>
      </template>
    </nav>

    <div class="mt-auto px-4 pt-4 border-t border-outline-variant">
      <div class="flex items-center gap-3">
        <img alt="校徽" class="w-8 h-8 object-contain" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBlkmNb0YQFVa2omXPkmTCxMvSXRHhbsGpZNeo8bgZvDzOV4Bb5swJVDElsAkJrJa1M_tu6XL5irmmX_zam19XGfSnMeV2-3ZwA1trFEMRskc5UsgmsyAu8n2bMmVOFHukR4gZJru4dT1z5q7oQQtVDLD7MQKzmnyjp8LLZht1FpGHT8m5ZMKt24TgkZVLyvcE0uXHP6IChWOdgeKzCdK6TJKtEi8HYKGfn7xM28fFFE3HgfhR59ABqgzeJmCAWzsjCni37gJHyMuS5" />
        <span class="text-[10px] text-on-surface-variant font-label-pixel">WCNU 管理系统 v2.4</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const expanded = reactive({})

function toggleExpand(label) {
  expanded[label] = !expanded[label]
}

const navItems = [
  { path: '/dashboard', icon: 'dashboard', label: '仪表盘' },
  { path: '/users', icon: 'person', label: '用户管理' },
  {
    label: '数据采集',
    icon: 'input',
    children: [
      { path: '/collection', label: '数据采集' },
      { path: '/source-mgmt', label: '数据源管理' }
    ]
  },
  { path: '/cleaning', icon: 'cleaning_services', label: '数据清洗' },
  { path: '/storage', icon: 'database', label: '存储管理' },
  { path: '/ai-inquiry', icon: 'psychology', label: 'AI 问询' },
  { path: '/digital-staff', icon: 'smart_toy', label: '数字员工' },
  { path: '/skills', icon: 'bolt', label: '技能中心' },
  { path: '/models', icon: 'deployed_code', label: '模型管理' },
  { path: '/big-screen', icon: 'monitoring', label: '大屏监控' },
  { path: '/audit', icon: 'fact_check', label: '审计追踪' },
  { path: '/content-audit', icon: 'policy', label: '内容审核' }
]

function isActive(path) {
  const current = route.path.replace(/\/$/, '')
  const target = path.replace(/\/$/, '')
  return current === target || current.endsWith(target)
}

function isGroupActive(item) {
  if (!item.children) return false
  return item.children.some(child => isActive(child.path))
}
</script>
