<template>
  <div class="h-full overflow-y-auto bg-surface-dim px-container-margin pb-12 pt-8">
    <!-- Breadcrumb / Header -->
    <div class="mb-8">
      <div class="flex items-center gap-2 text-primary font-label-pixel text-sm mb-2">
        <span>SYSTEM</span>
        <span class="material-symbols-outlined text-xs">chevron_right</span>
        <span>DATA_VAULT</span>
        <span class="material-symbols-outlined text-xs">chevron_right</span>
        <span class="text-secondary-fixed-dim">STORAGE_MANAGEMENT</span>
      </div>
      <h2 class="font-display-lg text-display-lg text-on-surface">数据存储中心 <span class="text-primary font-label-pixel text-lg ml-4">[STATUS: ONLINE]</span></h2>
    </div>
    <!-- Bento Grid Layout -->
    <div class="grid grid-cols-12 gap-6">
      <!-- Storage Management Stats -->
      <div class="col-span-12 md:col-span-8 grid grid-cols-4 gap-4">
        <div class="pixel-card pixel-header-strip-blue p-card-padding">
          <p class="text-on-surface-variant font-label-pixel text-xs mb-2">已保存数据总量</p>
          <div class="flex items-baseline gap-2">
            <span class="font-display-lg text-4xl text-primary">{{ overview.stats?.total_saved || 0 }}</span>
            <span class="font-label-pixel text-lg text-on-surface-variant">条</span>
          </div>
          <div class="w-full bg-surface-variant h-1 mt-4">
            <div class="bg-primary h-full" :style="{ width: Math.min((overview.stats?.total_saved || 0) / 100 * 100, 100) + '%' }"></div>
          </div>
          <p class="text-[10px] text-on-surface-variant mt-2 font-label-pixel">TOTAL SAVED RECORDS</p>
        </div>
        <div class="pixel-card pixel-header-strip-purple p-card-padding">
          <p class="text-on-surface-variant font-label-pixel text-xs mb-2">今日入库增量</p>
          <div class="flex items-baseline gap-2">
            <span class="font-display-lg text-4xl text-tertiary">{{ overview.stats?.today_saved || 0 }}</span>
            <span class="font-label-pixel text-lg text-on-surface-variant">条</span>
          </div>
          <p class="text-secondary-fixed-dim text-xs mt-4 font-label-pixel flex items-center gap-1">
            <span class="material-symbols-outlined text-xs">trending_up</span> TODAY INCREMENT
          </p>
        </div>
        <div class="pixel-card pixel-header-strip-green p-card-padding">
          <p class="text-on-surface-variant font-label-pixel text-xs mb-2">数据源配置数</p>
          <div class="flex items-baseline gap-2">
            <span class="font-display-lg text-4xl text-secondary-fixed-dim">{{ overview.stats?.total_sources || 0 }}</span>
            <span class="font-label-pixel text-lg text-on-surface-variant">SRC</span>
          </div>
          <p class="text-on-surface-variant text-xs mt-4 font-label-pixel flex items-center gap-1">
            <span class="material-symbols-outlined text-xs">sync</span> ACTIVE SOURCES
          </p>
        </div>
        <div class="pixel-card pixel-header-strip-orange p-card-padding">
          <p class="text-on-surface-variant font-label-pixel text-xs mb-2">运行中任务</p>
          <div class="flex items-baseline gap-2">
            <span class="font-display-lg text-4xl text-error">{{ overview.stats?.running_tasks || 0 }}</span>
            <span class="font-label-pixel text-lg text-on-surface-variant">TASKS</span>
          </div>
          <p class="text-on-surface-variant text-xs mt-4 font-label-pixel flex items-center gap-1">
            <span class="material-symbols-outlined text-xs">play_circle</span> RUNNING NOW
          </p>
        </div>
      </div>
      <!-- Table Structure Preview (Side Card) -->
      <div class="col-span-12 md:col-span-4 row-span-2">
        <div class="pixel-card h-full flex flex-col">
          <div class="p-4 border-b border-outline-variant bg-surface-variant/30 flex justify-between items-center">
            <h3 class="font-title-md text-title-md flex items-center gap-2">
              <span class="material-symbols-outlined text-primary">schema</span> 数据仓库结构
            </h3>
            <span class="text-[10px] font-label-pixel text-on-surface-variant">{{ schemaTime }}</span>
          </div>
          <div class="p-4 flex-1 overflow-y-auto space-y-6">
            <div v-for="s in overview.schema" :key="s.layer">
              <p class="font-label-pixel text-xs mb-2" :class="layerColor(s.layer)"># {{ s.layer }} ({{ s.name }})</p>
              <ul class="space-y-1 text-sm font-body-sm text-on-surface-variant border-l-2 border-outline-variant/30 pl-3">
                <li v-for="f in s.fields" :key="f.name" class="flex justify-between">
                  <span>{{ f.name }}</span>
                  <span class="font-label-pixel text-[10px]">{{ f.type }}</span>
                </li>
              </ul>
            </div>
          </div>
          <div class="p-4 bg-surface-variant/10">
            <button class="w-full py-2 bg-surface-variant hover:bg-outline-variant text-on-surface font-label-pixel text-xs transition-colors">查看完整字典 DATA_DICT.PDF</button>
          </div>
        </div>
      </div>
      <!-- Saved Crawler Data -->
      <div class="col-span-12 md:col-span-8">
        <div class="pixel-card">
          <div class="p-4 border-b border-outline-variant bg-surface-variant/30 flex justify-between items-center">
            <h3 class="font-title-md text-title-md flex items-center gap-2">
              <span class="material-symbols-outlined text-secondary-fixed-dim">saved_search</span> 已保存的爬取数据
            </h3>
            <div class="flex gap-2">
              <button @click="loadAll" class="p-1 hover:bg-surface-variant transition-colors"><span class="material-symbols-outlined text-sm">refresh</span></button>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-surface-container-high border-b border-outline-variant">
                  <th class="p-4 font-label-pixel text-xs text-on-surface-variant uppercase tracking-wider">ID</th>
                  <th class="p-4 font-label-pixel text-xs text-on-surface-variant uppercase tracking-wider">标题</th>
                  <th class="p-4 font-label-pixel text-xs text-on-surface-variant uppercase tracking-wider">内容摘要</th>
                  <th class="p-4 font-label-pixel text-xs text-on-surface-variant uppercase tracking-wider">来源</th>
                  <th class="p-4 font-label-pixel text-xs text-on-surface-variant uppercase tracking-wider text-right">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/30">
                <tr v-for="d in savedData" :key="d.id" class="hover:bg-primary/5 transition-colors group">
                  <td class="p-4 text-sm text-on-surface-variant">{{ d.id }}</td>
                  <td class="p-4">
                    <div class="flex flex-col">
                      <span class="font-bold text-on-surface text-sm">{{ d.title || '无标题' }}</span>
                      <a :href="d.url" target="_blank" class="text-[10px] text-primary hover:underline font-mono truncate max-w-[200px]">{{ d.url || '-' }}</a>
                    </div>
                  </td>
                  <td class="p-4 text-sm text-on-surface-variant max-w-[300px]">
                    <div class="truncate">{{ d.summary ? d.summary.slice(0, 80) + '...' : (d.content ? d.content.slice(0, 80) + '...' : '-') }}</div>
                  </td>
                  <td class="p-4 text-sm text-on-surface-variant">{{ d.source_name || '-' }}</td>
                  <td class="p-4 text-right">
                    <button @click="viewDetail(d)" class="text-primary hover:underline text-xs font-label-pixel mr-3">详情</button>
                    <button @click="deleteItem(d.id)" class="text-error hover:underline text-xs font-label-pixel">删除</button>
                  </td>
                </tr>
                <tr v-if="savedData.length === 0">
                  <td colspan="5" class="p-8 text-center text-on-surface-variant">暂无已保存的爬取数据，请在数据采集页面进行采集并保存</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!-- Source Distribution & Keywords -->
      <div class="col-span-12 md:col-span-4">
        <div class="pixel-card h-full flex flex-col">
          <div class="p-4 border-b border-outline-variant bg-surface-variant/30">
            <h3 class="font-title-md text-title-md flex items-center gap-2">
              <span class="material-symbols-outlined text-tertiary">donut_large</span> 来源分布
            </h3>
          </div>
          <div class="p-4 flex-1 space-y-3">
            <div v-for="src in overview.source_distribution" :key="src.name" class="flex items-center gap-3">
              <span class="text-xs font-label-pixel text-on-surface-variant w-20 truncate">{{ src.name }}</span>
              <div class="flex-1 bg-surface-variant h-2 rounded-full overflow-hidden">
                <div class="bg-primary h-full rounded-full" :style="{ width: sourcePercent(src.count) + '%' }"></div>
              </div>
              <span class="text-xs font-label-pixel text-on-surface">{{ src.count }}</span>
            </div>
            <div v-if="!overview.source_distribution?.length" class="text-center text-on-surface-variant text-sm py-4">暂无数据</div>
          </div>
          <div class="p-4 border-t border-outline-variant bg-surface-variant/30">
            <h4 class="font-label-pixel text-xs text-on-surface-variant mb-2">热门关键词 TOP10</h4>
            <div class="flex flex-wrap gap-2">
              <span v-for="kw in overview.top_keywords" :key="kw.name" class="px-2 py-1 bg-surface-container text-on-surface text-[10px] font-label-pixel border border-outline-variant">
                {{ kw.name }} ({{ kw.count }})
              </span>
            </div>
          </div>
        </div>
      </div>
      <!-- Database Nodes Visualizer -->
      <div class="col-span-12">
        <div class="pixel-card p-6 flex flex-col gap-6 overflow-hidden">
          <div class="flex justify-between items-center">
            <h3 class="font-title-md text-title-md flex items-center gap-2">
              <span class="material-symbols-outlined text-tertiary">hub</span> 存储集群节点状态
            </h3>
            <div class="flex gap-4">
              <div class="flex items-center gap-2"><span class="w-2 h-2 bg-secondary-fixed"></span> <span class="text-xs font-label-pixel">HEALTHY</span></div>
              <div class="flex items-center gap-2"><span class="w-2 h-2 bg-error"></span> <span class="text-xs font-label-pixel">ERROR</span></div>
              <div class="flex items-center gap-2"><span class="w-2 h-2 bg-outline-variant"></span> <span class="text-xs font-label-pixel">OFFLINE</span></div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
            <div v-for="node in overview.nodes" :key="node.id"
              class="bg-surface-container-high border-2 p-3 flex flex-col items-center gap-2 relative"
              :class="nodeBorderClass(node.status)">
              <span class="material-symbols-outlined text-3xl" :class="nodeIconClass(node.status)">{{ nodeIcon(node.status) }}</span>
              <span class="font-label-pixel text-[10px]" :class="node.status === 'error' ? 'text-error' : (node.status === 'offline' ? 'text-on-surface-variant/40' : '')">{{ node.id }}</span>
              <div v-if="node.status === 'healthy'" class="text-[8px] font-label-pixel text-on-surface-variant">
                CPU:{{ node.cpu }}% MEM:{{ node.memory }}%
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <div v-if="detailModal.show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" @click.self="detailModal.show = false">
      <div class="pixel-card w-full max-w-2xl max-h-[80vh] overflow-y-auto m-4">
        <div class="p-4 border-b border-outline-variant bg-surface-variant/30 flex justify-between items-center sticky top-0">
          <h3 class="font-title-md text-title-md">数据详情</h3>
          <button @click="detailModal.show = false" class="p-1 hover:bg-surface-variant transition-colors"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="p-6 space-y-4" v-if="detailModal.item">
          <div>
            <p class="font-label-pixel text-xs text-on-surface-variant mb-1">标题</p>
            <p class="text-on-surface font-bold">{{ detailModal.item.title || '无标题' }}</p>
          </div>
          <div>
            <p class="font-label-pixel text-xs text-on-surface-variant mb-1">URL</p>
            <a :href="detailModal.item.url" target="_blank" class="text-primary text-sm hover:underline break-all">{{ detailModal.item.url || '-' }}</a>
          </div>
          <div>
            <p class="font-label-pixel text-xs text-on-surface-variant mb-1">来源</p>
            <p class="text-on-surface text-sm">{{ detailModal.item.source_name || '-' }}</p>
          </div>
          <div>
            <p class="font-label-pixel text-xs text-on-surface-variant mb-1">摘要</p>
            <p class="text-on-surface text-sm leading-relaxed">{{ detailModal.item.summary || detailModal.item.content || '-' }}</p>
          </div>
          <div v-if="detailModal.item.keywords?.length">
            <p class="font-label-pixel text-xs text-on-surface-variant mb-1">关键词</p>
            <div class="flex flex-wrap gap-2">
              <span v-for="k in detailModal.item.keywords" :key="k" class="px-2 py-1 bg-primary/10 text-primary text-xs font-label-pixel">{{ k }}</span>
            </div>
          </div>
          <div v-if="detailModal.item.entities && Object.keys(detailModal.item.entities).length">
            <p class="font-label-pixel text-xs text-on-surface-variant mb-1">实体信息</p>
            <div class="space-y-1">
              <div v-for="(vals, key) in detailModal.item.entities" :key="key" class="flex gap-2 text-sm">
                <span class="font-label-pixel text-on-surface-variant">{{ key }}:</span>
                <span class="text-on-surface">{{ Array.isArray(vals) ? vals.join('、') : vals }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getSavedData, deleteData, getDataOverview } from '@/api/crawler.js'

const savedData = ref([])
const detailModal = ref({ show: false, item: null })
const overview = ref({
  stats: {},
  source_distribution: [],
  top_keywords: [],
  top_locations: [],
  schema: [],
  nodes: []
})

const schemaTime = computed(() => {
  const now = new Date()
  return now.toTimeString().slice(0, 5)
})

function layerColor(layer) {
  if (layer.includes('ODS')) return 'text-secondary-fixed-dim'
  if (layer.includes('DWD')) return 'text-tertiary'
  return 'text-primary'
}

function sourcePercent(count) {
  const max = overview.value.source_distribution?.[0]?.count || 1
  if (!max) return 0
  return Math.round((count / max) * 100)
}

function nodeBorderClass(status) {
  if (status === 'healthy') return 'border-secondary-fixed'
  if (status === 'error') return 'border-error'
  return 'border-outline-variant opacity-50'
}

function nodeIconClass(status) {
  if (status === 'healthy') return 'text-secondary-fixed'
  if (status === 'error') return 'text-error animate-pulse'
  return 'text-on-surface-variant/40'
}

function nodeIcon(status) {
  if (status === 'error') return 'report'
  if (status === 'offline') return 'add_circle'
  return 'storage'
}

async function loadOverview() {
  const res = await getDataOverview()
  if (res.code === 200) {
    overview.value = res.data || {}
  }
}

async function loadSavedData() {
  const res = await getSavedData()
  if (res.code === 200) {
    savedData.value = res.data?.items || []
  }
}

async function loadAll() {
  await Promise.all([loadOverview(), loadSavedData()])
}

function viewDetail(item) {
  detailModal.value = { show: true, item }
}

async function deleteItem(id) {
  if (!confirm('确定删除该数据吗？')) return
  const res = await deleteData(id)
  if (res.code === 200) {
    await loadAll()
  } else {
    alert(res.message || '删除失败')
  }
}

onMounted(loadAll)
</script>
