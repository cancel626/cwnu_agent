<template>
  <div class="min-h-full">
    <!-- Top Header -->
    <header class="h-16 flex-none border-b border-primary/10 flex items-center justify-between px-margin-desktop sticky top-0 bg-background/80 backdrop-blur-md z-40">
      <div class="flex items-center gap-4">
        <h2 class="font-headline-sm text-on-surface">控制面板仪表盘</h2>
        <div class="flex items-center gap-2 px-3 py-1 bg-secondary/10 border border-secondary/20 rounded-full">
          <span class="w-2 h-2 bg-secondary rounded-full animate-pulse"></span>
          <span class="font-label-code text-secondary text-[10px] uppercase">系统运行正常</span>
        </div>
      </div>
      <div class="flex items-center gap-6">
        <div class="flex gap-4 border-r border-outline-variant/30 pr-6">
          <div class="text-right">
            <p class="font-label-code text-on-surface-variant text-[10px]">实时负载</p>
            <p class="font-label-tech text-primary">{{ system.load || 0 }}%</p>
          </div>
          <div class="text-right">
            <p class="font-label-code text-on-surface-variant text-[10px]">活跃节点</p>
            <p class="font-label-tech text-secondary">{{ system.activeNodes || 0 }}</p>
          </div>
        </div>
        <span class="material-symbols-outlined text-on-surface-variant cursor-pointer hover:text-primary">notifications</span>
        <span class="material-symbols-outlined text-on-surface-variant cursor-pointer hover:text-primary">sensors</span>
      </div>
    </header>

    <main class="p-margin-desktop space-y-lg max-w-[1600px] mx-auto w-full">
      <!-- Stats Cards -->
      <section class="grid grid-cols-1 md:grid-cols-4 gap-gutter">
        <div class="glass-card p-5 rounded-xl border-l-4 border-primary">
          <div class="flex justify-between items-start mb-2">
            <span class="material-symbols-outlined text-primary">smart_toy</span>
            <span class="font-label-code text-secondary">{{ stats.activeStaffCount || 0 }} 活跃</span>
          </div>
          <p class="font-label-tech text-on-surface-variant">数字员工总数</p>
          <h4 class="font-headline-md text-primary mt-1">{{ stats.staffCount?.toLocaleString() || 0 }}</h4>
        </div>
        <div class="glass-card p-5 rounded-xl border-l-4 border-secondary">
          <div class="flex justify-between items-start mb-2">
            <span class="material-symbols-outlined text-secondary">record_voice_over</span>
            <span class="font-label-code text-on-surface-variant">累计调用</span>
          </div>
          <p class="font-label-tech text-on-surface-variant">调用智能体次数</p>
          <h4 class="font-headline-md text-secondary mt-1">{{ stats.staffCallCount?.toLocaleString() || 0 }}</h4>
        </div>
        <div class="glass-card p-5 rounded-xl border-l-4 border-tertiary-fixed-dim">
          <div class="flex justify-between items-start mb-2">
            <span class="material-symbols-outlined text-tertiary-fixed-dim">analytics</span>
            <span class="font-label-code text-on-surface-variant">+12.5%</span>
          </div>
          <p class="font-label-tech text-on-surface-variant">今日处理请求</p>
          <h4 class="font-headline-md text-tertiary-fixed-dim mt-1">{{ stats.todayRequests?.toLocaleString() || 0 }}</h4>
        </div>
        <div class="glass-card p-5 rounded-xl border-l-4 border-error">
          <div class="flex justify-between items-start mb-2">
            <span class="material-symbols-outlined text-error">shield</span>
            <span class="font-label-code text-error">{{ stats.securityCount || 0 }}次拦截</span>
          </div>
          <p class="font-label-tech text-on-surface-variant">安全哨兵状态</p>
          <h4 class="font-headline-md text-error mt-1">{{ stats.securityStatus || '安全' }}</h4>
        </div>
      </section>

      <!-- Main Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-lg">
        <!-- Left & Middle -->
        <div class="lg:col-span-2 space-y-lg">
          <!-- Staff Recommendations -->
          <section>
            <div class="flex justify-between items-center mb-sm">
              <div>
                <h2 class="font-headline-md text-primary-fixed-dim pixel-text-shadow">数智员工推荐</h2>
                <p class="font-label-tech text-label-tech text-on-surface-variant uppercase">表现最佳的 AI 研究实体</p>
              </div>
              <button class="font-label-tech text-label-tech text-primary border border-primary/30 px-4 py-1.5 rounded-lg hover:bg-primary/10 transition-colors">
                查看全部名录
              </button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter">
              <div v-for="(staff, idx) in staffList" :key="idx" class="glass-card p-5 rounded-xl relative overflow-hidden group hover:border-primary/50 transition-all duration-300">
                <div class="absolute top-2 right-2 opacity-30 group-hover:opacity-100 transition-opacity">
                  <span class="material-symbols-outlined text-primary text-sm">verified</span>
                </div>
                <div class="w-16 h-16 rounded-lg mb-4 bg-surface-container flex items-center justify-center border border-primary/20">
                  <span class="material-symbols-outlined text-primary text-3xl">{{ staff.icon || 'smart_toy' }}</span>
                </div>
                <h3 class="font-headline-sm text-primary mb-1 text-base">{{ staff.name }}</h3>
                <p class="font-label-tech text-label-tech text-on-surface-variant mb-4">{{ staff.role }}</p>
                <div class="flex justify-between items-center pt-3 border-t border-outline-variant/30">
                  <span class="font-label-code text-secondary text-[10px]">状态：{{ staff.status }}</span>
                  <span class="material-symbols-outlined text-primary-fixed-dim text-lg" :class="staff.iconClass">{{ staff.icon }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- Quick Access -->
          <section>
            <h2 class="font-headline-md text-primary mb-sm">快捷管理入口</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-gutter">
              <div v-for="(item, idx) in quickLinks" :key="idx" class="glass-card p-6 rounded-xl flex flex-col items-center justify-center text-center group cursor-pointer hover:bg-primary/10 transition-all active:scale-95 border-b-2 border-transparent hover:border-primary shadow-lg h-40">
                <div class="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-primary/20 group-hover:scale-110 transition-all">
                  <span class="material-symbols-outlined text-primary-fixed-dim text-3xl">{{ item.icon }}</span>
                </div>
                <span class="font-body-md font-bold text-on-surface">{{ item.name }}</span>
                <span class="font-label-code text-on-surface-variant mt-1">{{ item.desc }}</span>
              </div>
            </div>
          </section>
        </div>

        <!-- Right Sidebar -->
        <div class="space-y-lg">
          <!-- System Gauge -->
          <section class="glass-card p-6 rounded-xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-6">
              <h3 class="font-headline-sm text-primary text-base flex items-center gap-2">
                <span class="material-symbols-outlined text-primary">data_usage</span>
                核心计算负荷
              </h3>
              <span class="font-label-code text-primary">{{ system.computeEfficiency || 98 }}% 效率</span>
            </div>
            <div class="flex flex-col items-center py-4">
              <div class="relative w-32 h-32 flex items-center justify-center">
                <svg class="w-full h-full -rotate-90" viewBox="0 0 36 36">
                  <path class="stroke-current text-surface-container" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke-width="3" />
                  <path class="stroke-current text-primary" :stroke-dasharray="`${system.coreLoad || 85}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke-linecap="round" stroke-width="3" />
                </svg>
                <span class="absolute font-headline-md text-primary">{{ system.coreLoad || 0 }}%</span>
              </div>
              <div class="mt-6 w-full space-y-3">
                <div class="flex justify-between text-xs">
                  <span class="text-on-surface-variant">内存占用</span>
                  <span class="text-primary">{{ system.memoryUsage || 0 }} GB</span>
                </div>
                <div class="w-full bg-surface-container h-1.5 rounded-full overflow-hidden">
                  <div class="bg-primary h-full" :style="{ width: (system.memoryUsage || 0) + '%', boxShadow: '0 0 8px #00dbe7' }"></div>
                </div>
                <div class="flex justify-between text-xs pt-1">
                  <span class="text-on-surface-variant">显存计算</span>
                  <span class="text-secondary">{{ system.gpuUsage || 0 }}%</span>
                </div>
                <div class="w-full bg-surface-container h-1.5 rounded-full overflow-hidden">
                  <div class="bg-secondary h-full" :style="{ width: (system.gpuUsage || 0) + '%', boxShadow: '0 0 8px #2ae500' }"></div>
                </div>
              </div>
            </div>
          </section>

          <!-- Recent Communications -->
          <section>
            <div class="flex items-center justify-between mb-sm">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-primary text-lg">message</span>
                <h2 class="font-headline-sm text-primary text-base">最近通讯</h2>
              </div>
            </div>
            <div class="glass-card rounded-xl overflow-hidden divide-y divide-outline-variant/20">
              <div v-for="(msg, idx) in messages" :key="idx" @click="goToChat(msg)" class="p-4 flex items-start gap-4 hover:bg-white/5 transition-colors cursor-pointer group">
                <div class="w-10 h-10 rounded-lg bg-surface-container-highest flex-none flex items-center justify-center font-label-tech text-primary border border-primary/20 overflow-hidden">
                  <img v-if="msg.avatar" :src="msg.avatar" class="w-full h-full object-cover" />
                  <span v-else>{{ msg.from.slice(0, 1) }}</span>
                </div>
                <div class="flex-grow min-w-0">
                  <div class="flex justify-between items-center mb-1">
                    <span class="font-body-md font-bold text-on-surface text-sm truncate">{{ msg.from }}</span>
                    <span class="font-label-code text-[10px] text-on-surface-variant">{{ msg.time }}</span>
                  </div>
                  <p class="font-body-md text-xs text-on-surface-variant line-clamp-1">{{ msg.content }}</p>
                </div>
              </div>
            </div>
            <div v-if="messages.length === 0" class="text-center text-on-surface-variant/40 text-sm py-6">
              暂无最近通讯
            </div>
            <div class="mt-4 text-center">
              <button class="font-label-tech text-[12px] text-primary underline underline-offset-4 decoration-primary/30 hover:decoration-primary transition-all">
                查看全部通讯历史
              </button>
            </div>
          </section>
        </div>
      </div>

      <!-- System Log -->
      <section class="glass-card rounded-xl overflow-hidden">
        <div class="p-4 border-b border-outline-variant/20 flex items-center justify-between">
          <h3 class="font-headline-sm text-base text-primary flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">terminal</span>
            实时系统日志
          </h3>
          <div class="flex gap-2">
            <span class="px-2 py-0.5 bg-surface-variant/40 rounded text-[10px] font-label-code text-on-surface-variant">过滤器: 全部</span>
            <span class="px-2 py-0.5 bg-surface-variant/40 rounded text-[10px] font-label-code text-on-surface-variant">自动滚动: 开</span>
          </div>
        </div>
        <div class="p-4 font-label-code text-xs space-y-2 overflow-x-auto bg-black/40">
          <div v-for="(log, idx) in logs" :key="idx" class="flex gap-4" :class="log.opacity ? 'opacity-70' : ''">
            <span class="text-on-surface-variant">{{ log.time }}</span>
            <span :class="log.levelClass">{{ log.level }}</span>
            <span :class="log.textClass">{{ log.text }}</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/index.js'
import { getUserDashboard } from '../api/user.js'

const store = useAppStore()
const router = useRouter()

const loading = ref(true)
const stats = ref({})
const system = ref({})
const staffList = ref([])
const quickLinks = ref([])
const messages = ref([])
const logs = ref([])

function goToChat(msg) {
  // 统一进入个人中心/聊天页面
  router.push('/profile')
}

async function loadDashboard() {
  try {
    const res = await getUserDashboard()
    if (res.code === 200 && res.data) {
      stats.value = res.data.stats || {}
      system.value = res.data.system || {}
      staffList.value = res.data.staff || []
      quickLinks.value = res.data.quickLinks || []
      messages.value = res.data.messages || []
      logs.value = res.data.logs || []
    }
  } catch (e) {
    console.error('获取仪表盘数据失败:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  store.fetchUserInfo()
  loadDashboard()
})
</script>
