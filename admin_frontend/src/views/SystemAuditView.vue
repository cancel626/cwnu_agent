<template>
  <div class="h-full overflow-y-auto bg-background p-container-margin pt-8">
    <div class="flex justify-between items-start mb-6">
      <div>
        <h2 class="font-display-lg text-display-lg text-on-surface mb-2">审计追踪</h2>
        <p class="text-on-surface-variant font-body-lg">基于大模型对采集数据（crawled_data）进行合规性审计，识别色情、暴力、政治敏感等违规内容。</p>
      </div>
      <button
        @click="handleScan"
        :disabled="scanning"
        class="px-4 py-2 bg-primary text-on-primary font-label-pixel text-xs hover:bg-primary/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
      >
        <span v-if="scanning" class="inline-block w-4 h-4 border-2 border-on-primary border-t-transparent rounded-full animate-spin"></span>
        {{ scanning ? '扫描中...' : 'AI 扫描' }}
      </button>
    </div>

    <div v-if="scanResult" class="mb-4 p-3 bg-secondary-fixed/20 border border-secondary-fixed text-on-surface font-body-sm">
      {{ scanResult }}
    </div>

    <div class="bg-surface-container border-2 border-outline-variant">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-surface-container-highest border-b-2 border-outline-variant">
              <th class="px-6 py-4 font-label-pixel text-xs text-on-surface-variant uppercase">ID</th>
              <th class="px-6 py-4 font-label-pixel text-xs text-on-surface-variant uppercase">来源 URL</th>
              <th class="px-6 py-4 font-label-pixel text-xs text-on-surface-variant uppercase">标题 / 摘要</th>
              <th class="px-6 py-4 font-label-pixel text-xs text-on-surface-variant uppercase">违规类型</th>
              <th class="px-6 py-4 font-label-pixel text-xs text-on-surface-variant uppercase">判定理由</th>
              <th class="px-6 py-4 font-label-pixel text-xs text-on-surface-variant uppercase">置信度</th>
              <th class="px-6 py-4 font-label-pixel text-xs text-on-surface-variant uppercase text-right">审核时间</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-outline-variant/30">
            <tr v-if="loading" class="hover:bg-primary/5 transition-colors">
              <td colspan="7" class="px-6 py-8 text-center text-on-surface-variant font-body-sm">加载中...</td>
            </tr>
            <tr v-else-if="items.length === 0" class="hover:bg-primary/5 transition-colors">
              <td colspan="7" class="px-6 py-8 text-center text-on-surface-variant font-body-sm">暂无违规内容，点击右上角「AI 扫描」开始审计。</td>
            </tr>
            <tr v-for="item in items" :key="item.id" class="hover:bg-primary/5 transition-colors">
              <td class="px-6 py-4 font-label-pixel text-[10px] text-on-surface-variant">#{{ item.id }}</td>
              <td class="px-6 py-4 text-sm text-on-surface-variant max-w-[200px] truncate" :title="item.url">
                <a v-if="item.url" :href="item.url" target="_blank" class="text-primary hover:underline">{{ item.url }}</a>
                <span v-else>无</span>
              </td>
              <td class="px-6 py-4 text-sm text-on-surface max-w-[300px]">
                <div class="font-semibold mb-1">{{ item.title || '无标题' }}</div>
                <div class="text-on-surface-variant text-xs line-clamp-2">{{ item.content }}</div>
              </td>
              <td class="px-6 py-4">
                <span class="px-2 py-0.5 bg-error/20 text-error text-[10px] font-label-pixel border border-error">{{ item.type_label }}</span>
              </td>
              <td class="px-6 py-4 text-sm text-on-surface-variant max-w-[200px]">{{ item.reason }}</td>
              <td class="px-6 py-4 text-sm text-on-surface">{{ (Math.abs(item.confidence) * 100).toFixed(1) }}%</td>
              <td class="px-6 py-4 text-right font-label-pixel text-[10px] text-on-surface-variant">{{ formatDate(item.audited_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="p-4 border-t border-outline-variant flex justify-between items-center bg-surface-container-low">
        <span class="text-[11px] font-label-pixel text-on-surface-variant">显示 {{ paginationText }} / 共 {{ total }} 条记录</span>
        <div class="flex gap-1">
          <button
            @click="prevPage"
            :disabled="page <= 1"
            class="w-8 h-8 flex items-center justify-center border border-outline-variant hover:bg-surface-variant disabled:opacity-40"
          >
            <span class="material-symbols-outlined text-sm">chevron_left</span>
          </button>
          <button
            v-for="p in visiblePages"
            :key="p"
            @click="goPage(p)"
            class="w-8 h-8 flex items-center justify-center font-label-pixel text-xs"
            :class="p === page ? 'bg-primary text-on-primary' : 'border border-outline-variant hover:bg-surface-variant'"
          >
            {{ p }}
          </button>
          <button
            @click="nextPage"
            :disabled="page >= totalPages"
            class="w-8 h-8 flex items-center justify-center border border-outline-variant hover:bg-surface-variant disabled:opacity-40"
          >
            <span class="material-symbols-outlined text-sm">chevron_right</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { scanCrawlData, getCrawlViolations } from '@/api/audit.js'

const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const scanning = ref(false)
const scanResult = ref('')

const totalPages = computed(() => Math.ceil(total.value / pageSize.value) || 1)
const visiblePages = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i++) {
    pages.push(i)
  }
  return pages
})
const paginationText = computed(() => {
  if (total.value === 0) return '0'
  const start = (page.value - 1) * pageSize.value + 1
  const end = Math.min(page.value * pageSize.value, total.value)
  return `${start}-${end}`
})

function formatDate(iso) {
  if (!iso) return '-'
  const d = new Date(iso)
  if (isNaN(d.getTime())) return iso
  return d.toLocaleString('zh-CN', { hour12: false })
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getCrawlViolations(page.value, pageSize.value)
    items.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (err) {
    console.error('获取爬取数据违规列表失败', err)
  } finally {
    loading.value = false
  }
}

async function handleScan() {
  scanning.value = true
  scanResult.value = ''
  try {
    const res = await scanCrawlData(50)
    scanResult.value = res.message || '扫描完成'
    page.value = 1
    await fetchData()
  } catch (err) {
    scanResult.value = err.message || '扫描失败'
  } finally {
    scanning.value = false
  }
}

function goPage(p) {
  page.value = p
  fetchData()
}

function prevPage() {
  if (page.value > 1) {
    page.value--
    fetchData()
  }
}

function nextPage() {
  if (page.value < totalPages.value) {
    page.value++
    fetchData()
  }
}

onMounted(fetchData)
</script>
