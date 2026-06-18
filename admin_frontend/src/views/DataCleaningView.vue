<template>
  <div class="h-full flex flex-col bg-surface-dim overflow-hidden">
    <!-- Header -->
    <div class="shrink-0 px-6 py-4 border-b-2 border-outline-variant bg-surface-container flex justify-between items-center">
      <div>
        <h2 class="font-headline-lg text-headline-lg text-primary tracking-tight">数据清洗中心 <span class="text-secondary font-label-pixel text-sm ml-2">[DATA_CLEANING]</span></h2>
        <p class="text-on-surface-variant font-body-lg">选择数据仓库中的内容，使用大模型进行智能清洗与精炼。</p>
      </div>
      <div class="flex gap-3">
        <button
          @click="fetchData"
          class="bg-surface-variant text-on-surface font-label-pixel px-4 py-2 border-b-4 border-outline-variant pixel-button-press flex items-center gap-2"
        >
          <span class="material-symbols-outlined">refresh</span>
          刷新数据
        </button>
      </div>
    </div>

    <!-- Three Column Layout -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Left: Data Warehouse List -->
      <div class="w-[36%] border-r-2 border-outline-variant bg-surface-container flex flex-col">
        <div class="px-4 py-3 border-b-2 border-outline-variant bg-surface-container-high flex justify-between items-center">
          <h3 class="font-title-md text-title-md text-on-surface flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">database</span>
            数据仓库
          </h3>
          <div class="flex items-center gap-2">
            <label class="flex items-center gap-1 text-xs text-on-surface-variant cursor-pointer select-none">
              <input
                type="checkbox"
                :checked="isAllSelected"
                @change="toggleSelectAll"
                class="w-4 h-4 accent-primary"
              />
              全选
            </label>
            <span class="text-xs font-label-pixel text-on-surface-variant">{{ selectedIds.length }}/{{ dataList.length }}</span>
          </div>
        </div>
        <div class="flex-1 overflow-y-auto p-3 space-y-2">
          <div v-if="loading" class="text-center py-10 text-on-surface-variant font-label-pixel">加载中...</div>
          <div v-else-if="dataList.length === 0" class="text-center py-10 text-on-surface-variant font-label-pixel">
            暂无已保存数据
          </div>
          <div
            v-for="item in dataList"
            :key="item.id"
            class="group border-2 border-outline-variant bg-surface-variant/20 hover:border-primary hover:bg-primary/5 transition-all cursor-pointer relative"
            :class="{ 'border-primary bg-primary/5': selectedIds.includes(item.id) }"
            @click="toggleSelect(item.id)"
          >
            <div class="p-3">
              <div class="flex items-start gap-2 mb-2">
                <input
                  type="checkbox"
                  :checked="selectedIds.includes(item.id)"
                  @click.stop
                  @change="toggleSelect(item.id)"
                  class="w-4 h-4 accent-primary mt-0.5 shrink-0"
                />
                <div class="flex-1 min-w-0">
                  <p class="font-label-pixel text-on-surface text-sm truncate">{{ item.title || '无标题' }}</p>
                  <p class="text-[10px] text-on-surface-variant mt-0.5">{{ item.source_name }} · {{ formatDate(item.created_at) }}</p>
                </div>
              </div>
              <p class="text-xs text-on-surface-variant leading-relaxed line-clamp-3 mb-2 pl-6">
                {{ item.summary || item.content || '暂无摘要' }}
              </p>
              <div class="pl-6 flex flex-wrap gap-1">
                <span
                  v-for="kw in (item.keywords || []).slice(0, 5)"
                  :key="kw"
                  class="px-1.5 py-0.5 bg-primary/10 text-primary text-[10px] font-label-pixel"
                >
                  {{ kw }}
                </span>
                <span
                  v-for="loc in ((item.entities || {}).地点 || []).slice(0, 3)"
                  :key="loc"
                  class="px-1.5 py-0.5 bg-secondary/10 text-secondary text-[10px] font-label-pixel"
                >
                  {{ loc }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Middle: Model Cleaning Config -->
      <div class="w-[28%] border-r-2 border-outline-variant bg-surface-container flex flex-col">
        <div class="px-4 py-3 border-b-2 border-outline-variant bg-surface-container-high">
          <h3 class="font-title-md text-title-md text-on-surface flex items-center gap-2">
            <span class="material-symbols-outlined text-secondary">psychology</span>
            清洗配置
          </h3>
        </div>
        <div class="flex-1 overflow-y-auto p-4 space-y-4">
          <div class="bg-primary-container border-2 border-primary p-4">
            <div class="flex items-center gap-3 mb-2">
              <span class="material-symbols-outlined text-2xl text-on-primary-container">auto_awesome</span>
              <div>
                <p class="font-label-pixel text-on-primary-container">AI 大模型清洗</p>
                <p class="text-[10px] text-on-primary-container/70">调用默认模型对摘要进行精炼</p>
              </div>
            </div>
            <div class="flex items-center gap-2 mt-3">
              <label class="relative inline-flex items-center cursor-pointer">
                <input v-model="useModel" type="checkbox" class="sr-only peer" />
                <div class="w-11 h-6 bg-surface-variant/40 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-secondary"></div>
              </label>
              <span class="text-xs font-label-pixel" :class="useModel ? 'text-secondary' : 'text-on-surface-variant'">
                {{ useModel ? '已启用' : '未启用' }}
              </span>
            </div>
          </div>

          <div>
            <label class="block text-xs font-label-pixel text-on-surface-variant mb-1">清洗指令 (Prompt)</label>
            <textarea
              v-model="instruction"
              rows="6"
              class="w-full px-3 py-2 bg-surface-container border-2 border-outline-variant text-on-surface text-sm focus:border-primary focus:outline-none resize-none font-mono"
              placeholder="输入对大模型的清洗指令..."
            ></textarea>
            <p class="text-[10px] text-on-surface-variant mt-1">系统会自动将数据摘要拼接在指令后发送给模型。</p>
          </div>

          <button
            @click="startClean"
            :disabled="cleaning || selectedIds.length === 0 || !useModel"
            class="w-full bg-primary text-on-primary font-label-pixel px-4 py-3 border-b-4 border-on-primary-container pixel-button-press flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="cleaning" class="material-symbols-outlined animate-spin">refresh</span>
            <span v-else class="material-symbols-outlined">play_arrow</span>
            {{ cleaning ? '清洗中...' : '开始清洗' }}
          </button>

          <div v-if="selectedIds.length === 0" class="text-center text-xs text-on-surface-variant font-label-pixel py-4">
            请先在左侧选择要清洗的数据
          </div>
        </div>
      </div>

      <!-- Right: Cleaning Results -->
      <div class="flex-1 bg-surface-container flex flex-col">
        <div class="px-4 py-3 border-b-2 border-outline-variant bg-surface-container-high flex justify-between items-center">
          <h3 class="font-title-md text-title-md text-on-surface flex items-center gap-2">
            <span class="material-symbols-outlined text-tertiary">text_snippet</span>
            清洗结果
          </h3>
          <button
            v-if="results.length > 0"
            @click="clearResults"
            class="text-xs text-on-surface-variant hover:text-error font-label-pixel flex items-center gap-1"
          >
            <span class="material-symbols-outlined text-sm">delete_sweep</span>
            清空结果
          </button>
        </div>
        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          <div v-if="results.length === 0" class="h-full flex flex-col items-center justify-center text-on-surface-variant">
            <span class="material-symbols-outlined text-5xl mb-2 opacity-30">text_snippet</span>
            <p class="font-label-pixel text-sm">暂无清洗结果</p>
            <p class="text-[10px] mt-1">选择数据并点击开始清洗后，结果将展示在这里</p>
          </div>
          <div
            v-for="res in results"
            :key="res.id"
            class="border-2 border-outline-variant bg-surface-variant/20"
          >
            <div class="px-3 py-2 border-b border-outline-variant/30 bg-surface-container-high flex justify-between items-center">
              <span class="font-label-pixel text-xs text-on-surface truncate">{{ res.title || '无标题' }}</span>
              <span
                class="px-2 py-0.5 text-[10px] font-label-pixel"
                :class="{
                  'bg-primary/20 text-primary': res.status === 'success',
                  'bg-error/20 text-error': res.status === 'failed',
                  'bg-surface-variant text-on-surface-variant': res.status === 'skipped'
                }"
              >
                {{ statusText(res.status) }}
              </span>
            </div>
            <div class="p-3">
              <div class="mb-2">
                <p class="text-[10px] font-label-pixel text-on-surface-variant mb-0.5">原文摘要</p>
                <p class="text-xs text-on-surface-variant leading-relaxed bg-surface-container p-2 border border-outline-variant/30">{{ res.original || '无' }}</p>
              </div>
              <div class="flex items-center justify-center my-1">
                <span class="material-symbols-outlined text-primary text-lg">arrow_downward</span>
              </div>
              <div>
                <p class="text-[10px] font-label-pixel text-secondary mb-0.5">清洗后</p>
                <p class="text-xs text-on-surface leading-relaxed bg-primary/5 p-2 border border-primary/20">{{ res.cleaned }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSavedData, cleanData } from '../api/crawler.js'

const dataList = ref([])
const loading = ref(false)
const selectedIds = ref([])
const useModel = ref(true)
const instruction = ref('对以下文本进行清洗、去噪、精炼，保留核心信息并输出一段通顺的中文摘要。')
const cleaning = ref(false)
const results = ref([])

const isAllSelected = computed(() => {
  return dataList.value.length > 0 && selectedIds.value.length === dataList.value.length
})

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function statusText(status) {
  const map = { success: '成功', failed: '失败', skipped: '跳过' }
  return map[status] || status
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getSavedData()
    dataList.value = res.data?.items || []
    selectedIds.value = []
  } catch (e) {
    console.error(e)
    alert('加载数据失败: ' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

function toggleSelect(id) {
  const idx = selectedIds.value.indexOf(id)
  if (idx > -1) {
    selectedIds.value.splice(idx, 1)
  } else {
    selectedIds.value.push(id)
  }
}

function toggleSelectAll() {
  if (isAllSelected.value) {
    selectedIds.value = []
  } else {
    selectedIds.value = dataList.value.map(i => i.id)
  }
}

async function startClean() {
  if (selectedIds.value.length === 0) return
  if (!useModel.value) return
  cleaning.value = true
  try {
    const res = await cleanData({
      ids: selectedIds.value,
      instruction: instruction.value
    })
    const newResults = res.data?.results || []
    results.value = newResults
  } catch (e) {
    console.error(e)
    alert('清洗失败: ' + (e.message || '未知错误'))
  } finally {
    cleaning.value = false
  }
}

function clearResults() {
  results.value = []
}

onMounted(fetchData)
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
