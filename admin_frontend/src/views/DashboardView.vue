<template>
  <div class="h-full overflow-y-auto p-container-margin">
    <!-- Stats Row -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-surface-container-low p-card-padding rounded-lg border-t-4 border-primary block-3d relative overflow-hidden">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-on-surface-variant font-label-pixel text-xs mb-1">总采集量</p>
            <h2 class="font-display-lg text-display-lg text-on-surface">{{ stats.totalCollection || '0' }}</h2>
          </div>
          <div class="p-3 bg-primary/20 text-primary rounded flex items-center justify-center">
            <span class="material-symbols-outlined text-3xl">database</span>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2">
          <span class="text-secondary-fixed text-xs font-bold flex items-center"><span class="material-symbols-outlined text-xs">trending_up</span> {{ stats.trend?.collection || '+0%' }}</span>
          <span class="text-on-surface-variant text-xs">较上月</span>
        </div>
      </div>
      <div class="bg-surface-container-low p-card-padding rounded-lg border-t-4 border-tertiary-container block-3d relative overflow-hidden">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-on-surface-variant font-label-pixel text-xs mb-1">总用户数</p>
            <h2 class="font-display-lg text-display-lg text-on-surface">{{ formatNumber(stats.totalUsers) }}</h2>
          </div>
          <div class="p-3 bg-tertiary-container/20 text-tertiary-container rounded flex items-center justify-center">
            <span class="material-symbols-outlined text-3xl">group</span>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2">
          <span class="text-secondary-fixed text-xs font-bold flex items-center"><span class="material-symbols-outlined text-xs">trending_up</span> {{ stats.trend?.users || '+0%' }}</span>
          <span class="text-on-surface-variant text-xs">活跃状态</span>
        </div>
      </div>
      <div class="bg-surface-container-low p-card-padding rounded-lg border-t-4 border-secondary-fixed block-3d relative overflow-hidden">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-on-surface-variant font-label-pixel text-xs mb-1">清洗成功率</p>
            <h2 class="font-display-lg text-display-lg text-on-surface">{{ stats.cleaningRate || '0%' }}</h2>
          </div>
          <div class="p-3 bg-secondary-fixed/20 text-secondary-fixed rounded flex items-center justify-center">
            <span class="material-symbols-outlined text-3xl">auto_transmission</span>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2">
          <span class="text-secondary-fixed text-xs font-bold flex items-center"><span class="material-symbols-outlined text-xs">check_circle</span> {{ stats.trend?.cleaning || '正常' }}</span>
          <span class="text-on-surface-variant text-xs">过去 24 小时</span>
        </div>
      </div>
      <div class="bg-surface-container-low p-card-padding rounded-lg border-t-4 border-error block-3d relative overflow-hidden">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-on-surface-variant font-label-pixel text-xs mb-1">活跃员工</p>
            <h2 class="font-display-lg text-display-lg text-on-surface">{{ stats.activeStaff || 0 }}</h2>
          </div>
          <div class="p-3 bg-error/20 text-error rounded flex items-center justify-center">
            <span class="material-symbols-outlined text-3xl">smart_toy</span>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2">
          <span class="text-primary text-xs font-bold flex items-center"><span class="material-symbols-outlined text-xs">pause</span> {{ stats.trend?.staff || '在线' }}</span>
          <span class="text-on-surface-variant text-xs">数字代理</span>
        </div>
      </div>
    </div>
    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <div class="lg:col-span-2 bg-surface-container-low p-card-padding rounded-lg border-2 border-outline-variant chart-container">
        <div class="flex justify-between items-center mb-6">
          <h3 class="font-title-md text-title-md text-on-surface flex items-center gap-2">
            <span class="w-2 h-2 bg-primary animate-pulse"></span>
            数据流量趋势
          </h3>
          <div class="flex gap-2">
            <button class="px-3 py-1 font-label-pixel text-[10px] bg-primary text-on-primary rounded uppercase">实时</button>
            <button class="px-3 py-1 font-label-pixel text-[10px] bg-surface-container-high text-on-surface-variant rounded uppercase hover:text-on-surface">24时</button>
          </div>
        </div>
        <div class="h-64 flex items-end justify-between gap-1 px-4">
          <div
            v-for="(item, idx) in stats.trafficData"
            :key="idx"
            class="flex-1 bg-primary/40 rounded-t relative group cursor-pointer"
            :style="{ height: trafficHeight(item.value) }"
            :class="{ 'border-t-2 border-secondary-fixed': idx === 4 || idx === 7 }"
          >
            <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-surface-container-highest px-2 py-1 rounded text-[10px] opacity-0 group-hover:opacity-100 transition-opacity">{{ item.value }}k</div>
          </div>
        </div>
        <div class="flex justify-between px-4 mt-2 font-label-pixel text-[10px] text-on-surface-variant">
          <span v-for="(item, idx) in stats.trafficData" :key="idx">{{ item.time }}</span>
        </div>
      </div>
      <div class="bg-surface-container-low p-card-padding rounded-lg border-2 border-outline-variant flex flex-col">
        <h3 class="font-title-md text-title-md text-on-surface mb-6">各部门贡献度</h3>
        <div class="flex-1 flex items-center justify-center relative">
          <svg class="w-40 h-40" viewbox="0 0 36 36">
            <path
              v-for="(dept, idx) in stats.departmentDistribution"
              :key="idx"
              :class="`text-${dept.color}`"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="currentColor"
              :stroke-dasharray="`${dept.value}, 100`"
              :stroke-dashoffset="deptOffset(idx)"
              stroke-width="6"
            ></path>
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span class="font-display-lg text-xl">100%</span>
            <span class="font-label-pixel text-[8px] uppercase">已分配</span>
          </div>
        </div>
        <div class="mt-4 space-y-2">
          <div v-for="(dept, idx) in stats.departmentDistribution" :key="idx" class="flex items-center justify-between">
            <div class="flex items-center gap-2"><div :class="`w-3 h-3 bg-${dept.color} rounded-sm`"></div> <span class="text-sm">{{ dept.name }}</span></div>
            <span class="font-label-pixel text-xs">{{ dept.value }}%</span>
          </div>
        </div>
      </div>
    </div>
    <!-- Table Section -->
    <section class="bg-surface-container-low rounded-lg border-2 border-outline-variant overflow-hidden">
      <div class="px-card-padding py-4 border-b border-outline-variant flex justify-between items-center bg-surface-container-high/30">
        <h3 class="font-title-md text-title-md text-on-surface">最新采集任务</h3>
        <button class="px-4 py-1.5 bg-primary text-on-primary font-label-pixel text-xs block-3d rounded flex items-center gap-2">
          <span class="material-symbols-outlined text-sm">add</span>
          新建任务
        </button>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-surface-container border-b border-outline-variant font-label-pixel text-xs text-on-surface-variant uppercase tracking-wider">
              <th class="px-6 py-4">任务名称</th>
              <th class="px-6 py-4">来源</th>
              <th class="px-6 py-4">频率</th>
              <th class="px-6 py-4">状态</th>
              <th class="px-6 py-4 text-right">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-outline-variant font-body-sm">
            <tr v-for="task in stats.recentTasks" :key="task.id" class="hover:bg-primary/5 transition-colors group">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded bg-surface-container-highest flex items-center justify-center text-primary">
                    <span class="material-symbols-outlined text-sm">link</span>
                  </div>
                  <span class="font-bold text-on-surface">{{ task.name }}</span>
                </div>
              </td>
              <td class="px-6 py-4">{{ task.source }}</td>
              <td class="px-6 py-4">{{ task.frequency }}</td>
              <td class="px-6 py-4">
                <span v-if="task.status === 'success'" class="px-3 py-1 bg-secondary-fixed/10 text-secondary-fixed border border-secondary-fixed/30 font-label-pixel text-[10px] uppercase rounded-sm">{{ task.statusText }}</span>
                <div v-else class="flex items-center gap-2 text-primary font-label-pixel text-[10px] uppercase">
                  <span class="w-2 h-2 rounded-full bg-primary animate-ping"></span>
                  {{ task.statusText }}
                </div>
              </td>
              <td class="px-6 py-4 text-right">
                <button class="p-1 hover:text-primary transition-colors"><span class="material-symbols-outlined">visibility</span></button>
                <button class="p-1 hover:text-primary transition-colors"><span class="material-symbols-outlined">edit</span></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="px-6 py-4 bg-surface-container border-t border-outline-variant flex justify-center">
        <button class="text-on-surface-variant font-label-pixel text-[10px] hover:text-primary transition-colors flex items-center gap-2">
          加载更多任务
          <span class="material-symbols-outlined text-sm">expand_more</span>
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboardStats } from '../api/dashboard.js'

const stats = ref({
  totalCollection: '0',
  totalUsers: 0,
  cleaningRate: '0%',
  activeStaff: 0,
  trend: {},
  trafficData: [],
  departmentDistribution: [],
  recentTasks: []
})

function formatNumber(n) {
  if (!n && n !== 0) return '0'
  return n.toLocaleString()
}

function trafficHeight(value) {
  const max = Math.max(...(stats.value.trafficData || []).map(d => d.value), 1)
  return `${(value / max) * 100}%`
}

function deptOffset(idx) {
  const list = stats.value.departmentDistribution || []
  let offset = 0
  for (let i = 0; i < idx; i++) {
    offset -= list[i]?.value || 0
  }
  return offset
}

onMounted(async () => {
  try {
    const res = await getDashboardStats()
    if (res.code === 200 && res.data) {
      stats.value = { ...stats.value, ...res.data }
    }
  } catch (e) {
    console.error('获取仪表盘数据失败:', e)
  }
})
</script>
