<template>
  <div class="min-h-full">
    <!-- Top Toolbar -->
    <header class="h-20 flex items-center justify-between px-margin-desktop border-b border-outline-variant/20 bg-surface/30 backdrop-blur-md z-10">
      <div class="flex items-center gap-6 flex-1 max-w-4xl">
        <router-link to="/dashboard" class="flex items-center gap-2 text-on-surface-variant hover:text-primary transition-colors font-label-tech text-label-tech">
          <span class="material-symbols-outlined text-[20px]">arrow_back</span>
          <span class="hidden sm:inline">返回首页</span>
        </router-link>
        <div class="h-6 w-[1px] bg-outline-variant/30"></div>
        <div class="relative flex-1">
          <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant/60">search</span>
          <input v-model="searchQuery" class="w-full bg-surface-container border border-outline-variant/30 rounded-lg py-2 pl-10 pr-4 focus:outline-none focus:border-primary-fixed-dim text-body-md placeholder:text-on-surface-variant/40 transition-all" placeholder="搜索数智员工、编号或职能..." type="text" />
        </div>
        <div class="flex items-center gap-2">
          <button class="flex items-center gap-2 px-4 py-2 bg-surface-container border border-outline-variant/30 rounded-lg hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined text-[20px]">filter_list</span>
            <span class="text-body-md hidden sm:inline">所有类别</span>
          </button>
          <button class="flex items-center gap-2 px-4 py-2 bg-surface-container border border-outline-variant/30 rounded-lg hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined text-[20px]">sort</span>
            <span class="text-body-md hidden sm:inline">排序: 活跃度</span>
          </button>
        </div>
      </div>
      <div class="flex items-center gap-4 ml-6">
        <div class="flex items-center gap-2 px-3 py-1.5 bg-secondary-fixed/10 border border-secondary-fixed/20 rounded-full">
          <div class="w-2 h-2 bg-secondary-fixed rounded-full animate-pulse shadow-[0_0_8px_#2ae500]"></div>
          <span class="text-[12px] font-label-code text-secondary-fixed">系统同步中</span>
        </div>
        <button class="material-symbols-outlined p-2 text-on-surface-variant hover:text-primary transition-colors">notifications</button>
      </div>
    </header>

    <!-- Content -->
    <div class="p-margin-desktop z-10 relative">
      <div class="max-w-[1600px] mx-auto">
        <!-- Page Title -->
        <div class="mb-10">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-1.5 h-6 bg-primary-fixed-dim rounded-full shadow-[0_0_10px_#00dbe7]"></div>
            <h1 class="font-headline-lg text-primary tracking-tight">数智资源中心</h1>
          </div>
          <p class="font-body-lg text-on-surface-variant opacity-80">当前共有 {{ overview.totalNodes || 0 }} 个活跃数智节点，支持校园全场景业务处理。</p>
        </div>

        <!-- Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div v-for="(node, idx) in filteredNodes" :key="idx" class="glass-card rounded-xl p-5 flex flex-col transition-all duration-300 neon-glow-hover cursor-pointer group">
            <div class="scanline-effect"></div>
            <div class="flex items-start justify-between mb-4">
              <div class="w-14 h-14 bg-surface-container rounded-lg border border-primary/20 flex items-center justify-center overflow-hidden relative">
                <span class="material-symbols-outlined text-primary text-2xl">smart_toy</span>
                <div class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full border-2 border-surface" :class="node.statusColor || 'bg-secondary-fixed'"></div>
              </div>
              <span class="material-symbols-outlined text-primary/30 group-hover:text-primary transition-colors text-[20px]">open_in_new</span>
            </div>
            <span class="font-label-code text-[10px] text-primary-fixed-dim/60 uppercase tracking-widest mb-1">{{ node.id }}</span>
            <h2 class="font-headline-sm text-primary mb-2">{{ node.name }}</h2>
            <p class="font-body-md text-on-surface-variant leading-relaxed text-sm line-clamp-2">{{ node.desc }}</p>
            <div class="mt-4 pt-4 border-t border-outline-variant/10 flex items-center justify-between">
              <span class="text-[10px] px-2 py-0.5 bg-primary/5 text-primary/60 rounded">{{ node.tag }}</span>
              <span class="text-[10px] font-label-code text-on-surface-variant/50">{{ node.metric }}</span>
            </div>
          </div>

        </div>

        <!-- System Overview -->
        <section class="mt-16 glass-card rounded-xl p-8 border-dashed border-primary/20">
          <div class="flex items-center justify-between mb-8">
            <h3 class="font-label-tech text-primary uppercase tracking-[0.2em]">HUB 系统实时状态</h3>
            <div class="flex items-center gap-4">
              <span class="flex items-center gap-1.5 text-[12px] font-label-code text-secondary-fixed">
                <span class="w-1.5 h-1.5 bg-secondary-fixed rounded-full"></span>
                全局在线
              </span>
              <span class="text-[12px] font-label-code text-on-surface-variant/40">最后更新: {{ now }}</span>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="space-y-1">
              <div class="font-headline-lg text-primary">{{ overview.totalNodes || 0 }}</div>
              <div class="font-label-code text-sm text-on-surface-variant uppercase tracking-wider">总部署节点</div>
            </div>
            <div class="space-y-1 border-l border-outline-variant/20 pl-8">
              <div class="font-headline-lg text-primary">{{ overview.avgResponse || '0.00s' }}</div>
              <div class="font-label-code text-sm text-on-surface-variant uppercase tracking-wider">平均响应时间</div>
            </div>
            <div class="space-y-1 border-l border-outline-variant/20 pl-8">
              <div class="font-headline-lg text-primary">{{ overview.syncRate || '0%' }}</div>
              <div class="font-label-code text-sm text-on-surface-variant uppercase tracking-wider">神经同步率</div>
            </div>
            <div class="space-y-1 border-l border-outline-variant/20 pl-8">
              <div class="font-headline-lg text-secondary-fixed">{{ overview.todayThroughput || '0 TB' }}</div>
              <div class="font-label-code text-sm text-on-surface-variant uppercase tracking-wider">今日处理通量</div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getStaffList } from '../api/user.js'

const searchQuery = ref('')
const nodes = ref([])
const overview = ref({})
const now = ref(new Date().toLocaleString())

const filteredNodes = computed(() => {
  if (!searchQuery.value) return nodes.value
  const q = searchQuery.value.toLowerCase()
  return nodes.value.filter(n =>
    (n.name && n.name.toLowerCase().includes(q)) ||
    (n.id && n.id.toLowerCase().includes(q)) ||
    (n.desc && n.desc.toLowerCase().includes(q))
  )
})

async function loadStaff() {
  try {
    const res = await getStaffList()
    if (res.code === 200 && res.data) {
      nodes.value = res.data.items || []
      overview.value = res.data.overview || {}
      now.value = new Date().toLocaleString()
    }
  } catch (e) {
    console.error('加载数智员工失败:', e)
  }
}

onMounted(loadStaff)
</script>
