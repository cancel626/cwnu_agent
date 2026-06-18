<template>
  <div class="h-full overflow-y-auto bg-surface-dim">
    <div class="p-container-margin">
      <div class="mb-8">
        <h2 class="font-headline-lg text-primary mb-2">数据采集 <span class="text-on-surface-variant font-light">/ DATA COLLECTION</span></h2>
        <p class="text-body-sm text-on-surface-variant">选择数据源并输入关键词进行爬取，支持选择性保存到数据仓库</p>
      </div>

      <div class="grid grid-cols-12 gap-gutter">
        <!-- 采集控制台 -->
        <div class="col-span-12 lg:col-span-4 space-y-gutter">
          <div class="bg-surface-container border-2 border-outline-variant p-6">
            <h3 class="font-title-lg text-on-surface mb-4 flex items-center gap-2">
              <span class="material-symbols-outlined text-primary">play_circle</span>
              采集控制台
            </h3>
            <div class="space-y-4">
              <div>
                <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">选择数据源</label>
                <select v-model="taskForm.source_id" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none">
                  <option value="">请选择数据源</option>
                  <option v-for="s in activeSources" :key="s.id" :value="s.id">{{ s.name }} — {{ s.base_url }}</option>
                </select>
              </div>
              <div>
                <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">关键词</label>
                <input v-model="taskForm.keyword" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none" placeholder="输入要采集的关键词" @keyup.enter="startTask" />
              </div>
              <div v-if="selectedSource">
                <p class="text-[11px] text-outline font-mono mb-1">URL 预览:</p>
                <p class="text-[11px] text-primary font-mono break-all">{{ previewUrl }}</p>
              </div>
              <button @click="startTask" :disabled="loading" class="w-full bg-secondary-fixed text-on-secondary-fixed font-label-pixel py-3 border-b-4 border-on-secondary-container active:border-b-0 active:translate-y-[4px] transition-all disabled:opacity-50 flex justify-center items-center gap-2">
                <span v-if="loading" class="material-symbols-outlined text-[18px] animate-spin">refresh</span>
                <span v-else class="material-symbols-outlined text-[18px]">send</span>
                {{ loading ? '采集中...' : '开始采集' }}
              </button>
            </div>
          </div>

          <!-- 任务列表 -->
          <div class="bg-surface-container border-2 border-outline-variant overflow-hidden">
            <div class="p-4 border-b border-outline-variant flex justify-between items-center">
              <h3 class="font-title-lg text-on-surface flex items-center gap-2">
                <span class="material-symbols-outlined text-primary">task</span>
                采集任务
              </h3>
              <button @click="loadTasks" class="text-primary text-[12px] font-label-pixel hover:underline">刷新</button>
            </div>
            <div class="max-h-[400px] overflow-y-auto divide-y divide-outline-variant">
              <div v-for="t in tasks" :key="t.id" class="p-3 hover:bg-primary/5 cursor-pointer transition-colors" :class="selectedTask?.id === t.id ? 'bg-primary/10' : ''" @click="selectTask(t)">
                <div class="flex justify-between items-start mb-1">
                  <span class="text-sm font-bold text-on-surface">#{{ t.id }} {{ t.keyword }}</span>
                  <span class="px-2 py-0.5 text-[10px] font-label-pixel border" :class="statusClass(t.status)">{{ statusText(t.status) }}</span>
                </div>
                <p class="text-[11px] text-outline mb-1">{{ t.source_name }}</p>
                <div class="flex justify-between text-[10px] text-outline">
                  <span>{{ t.result_count }} 条结果</span>
                  <span>{{ formatTime(t.created_at) }}</span>
                </div>
                <p v-if="t.error_msg" class="text-[10px] text-error mt-1">{{ t.error_msg }}</p>
              </div>
              <div v-if="tasks.length === 0" class="p-8 text-center text-on-surface-variant text-sm">暂无任务</div>
            </div>
          </div>
        </div>

        <!-- 结果展示 -->
        <div class="col-span-12 lg:col-span-8 space-y-gutter">
          <div v-if="selectedTask" class="bg-surface-container border-2 border-outline-variant overflow-hidden">
            <div class="p-4 border-b border-outline-variant flex justify-between items-center">
              <div>
                <h3 class="font-title-lg text-on-surface flex items-center gap-2">
                  <span class="material-symbols-outlined text-primary">database</span>
                  采集结果 — 任务 #{{ selectedTask.id }}
                </h3>
                <p class="text-[12px] text-outline mt-1">关键词: {{ selectedTask.keyword }} | 状态: {{ statusText(selectedTask.status) }}</p>
              </div>
              <div class="flex gap-2">
                <button @click="loadTaskResult(selectedTask.id)" class="px-3 py-2 border border-outline-variant text-on-surface-variant font-label-pixel text-[12px] hover:bg-surface-variant flex items-center gap-1">
                  <span class="material-symbols-outlined text-[16px]">refresh</span>刷新
                </button>
                <button @click="saveSelected" :disabled="selectedDataIds.length === 0 || saving" class="px-4 py-2 bg-primary text-on-primary font-label-pixel text-[12px] hover:bg-primary/90 disabled:opacity-50 flex items-center gap-1">
                  <span class="material-symbols-outlined text-[16px]">save</span>保存选中 ({{ selectedDataIds.length }})
                </button>
              </div>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-surface-container-highest border-b border-outline-variant">
                    <th class="p-3 w-10">
                      <input type="checkbox" :checked="allSelected" @change="toggleAll" class="w-4 h-4 accent-primary" />
                    </th>
                    <th class="p-3 font-label-pixel text-outline text-[12px] uppercase">标题</th>
                    <th class="p-3 font-label-pixel text-outline text-[12px] uppercase">内容摘要</th>
                    <th class="p-3 font-label-pixel text-outline text-[12px] uppercase">URL</th>
                    <th class="p-3 font-label-pixel text-outline text-[12px] uppercase">时间</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-outline-variant">
                  <tr v-for="d in taskResults" :key="d.id" class="hover:bg-primary/5 transition-colors">
                    <td class="p-3">
                      <input type="checkbox" :value="d.id" v-model="selectedDataIds" class="w-4 h-4 accent-primary" />
                    </td>
                    <td class="p-3 text-sm text-on-surface font-bold max-w-[200px]">
                      <div class="truncate">{{ d.title || '无标题' }}</div>
                    </td>
                    <td class="p-3 text-sm text-on-surface-variant max-w-[300px]">
                      <div class="truncate">{{ d.content ? d.content.slice(0, 100) + '...' : '' }}</div>
                    </td>
                    <td class="p-3 text-sm text-primary max-w-[200px]">
                      <a :href="d.url" target="_blank" class="truncate hover:underline font-mono text-[11px]">{{ d.url || '-' }}</a>
                    </td>
                    <td class="p-3 text-[11px] text-outline">{{ formatTime(d.created_at) }}</td>
                  </tr>
                  <tr v-if="taskResults.length === 0">
                    <td colspan="5" class="p-8 text-center text-on-surface-variant">暂无结果</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-else class="bg-surface-container border-2 border-outline-variant p-12 flex flex-col items-center justify-center text-center">
            <span class="material-symbols-outlined text-[64px] text-outline-variant mb-4">travel_explore</span>
            <h3 class="font-title-lg text-on-surface-variant mb-2">选择一个任务查看结果</h3>
            <p class="text-body-sm text-outline">在左侧创建任务并点击任务卡片即可查看爬取结果</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { getSourceList, getTaskList, createTask, getTaskResult, saveData } from '@/api/crawler.js'

const sources = ref([])
const tasks = ref([])
const taskForm = reactive({ source_id: '', keyword: '' })
const loading = ref(false)
const saving = ref(false)
const selectedTask = ref(null)
const taskResults = ref([])
const selectedDataIds = ref([])

const activeSources = computed(() => sources.value.filter(s => s.is_active))
const selectedSource = computed(() => sources.value.find(s => s.id === taskForm.source_id))
const previewUrl = computed(() => {
  if (!selectedSource.value || !taskForm.keyword) return ''
  return selectedSource.value.base_url.replace(selectedSource.value.keyword_placeholder || '{keyword}', encodeURIComponent(taskForm.keyword))
})
const allSelected = computed(() => taskResults.value.length > 0 && selectedDataIds.value.length === taskResults.value.length)

function statusClass(status) {
  const map = {
    pending: 'bg-tertiary/10 text-tertiary border-tertiary/30',
    running: 'bg-primary/10 text-primary border-primary/30',
    completed: 'bg-secondary-container/20 text-secondary-fixed border-secondary-fixed/30',
    failed: 'bg-error/10 text-error border-error/30'
  }
  return map[status] || 'bg-outline-variant/10 text-outline border-outline-variant/30'
}

function statusText(status) {
  const map = { pending: '等待中', running: '采集中', completed: '已完成', failed: '失败' }
  return map[status] || status
}

function formatTime(t) {
  if (!t) return '-'
  const d = new Date(t)
  return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function loadSources() {
  const res = await getSourceList()
  if (res.code === 200) {
    sources.value = res.data?.items || []
  }
}

async function loadTasks() {
  const res = await getTaskList()
  if (res.code === 200) {
    tasks.value = res.data?.items || []
  }
}

async function startTask() {
  if (!taskForm.source_id || !taskForm.keyword) {
    alert('请选择数据源并输入关键词')
    return
  }
  loading.value = true
  try {
    const res = await createTask({ source_id: taskForm.source_id, keyword: taskForm.keyword })
    if (res.code === 200) {
      taskForm.keyword = ''
      await loadTasks()
      // 自动选中新创建的任务并刷新结果
      const newTask = tasks.value.find(t => t.id === res.data?.task_id)
      if (newTask) selectTask(newTask)
    } else {
      alert(res.message || '创建任务失败')
    }
  } finally {
    loading.value = false
  }
}

async function selectTask(task) {
  selectedTask.value = task
  selectedDataIds.value = []
  if (task.status === 'completed' || task.status === 'failed') {
    await loadTaskResult(task.id)
  } else {
    taskResults.value = []
  }
}

async function loadTaskResult(taskId) {
  const res = await getTaskResult(taskId)
  if (res.code === 200) {
    taskResults.value = res.data?.items || []
  }
}

function toggleAll() {
  if (allSelected.value) {
    selectedDataIds.value = []
  } else {
    selectedDataIds.value = taskResults.value.map(d => d.id)
  }
}

async function saveSelected() {
  if (selectedDataIds.value.length === 0) return
  saving.value = true
  try {
    const res = await saveData({ ids: selectedDataIds.value })
    if (res.code === 200) {
      alert(`已保存 ${res.data?.saved_count || 0} 条数据到仓库`)
      selectedDataIds.value = []
      await loadTaskResult(selectedTask.value.id)
    } else {
      alert(res.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

// 轮询运行中的任务
let pollTimer = null
function startPolling() {
  stopPolling()
  pollTimer = setInterval(async () => {
    const hasRunning = tasks.value.some(t => t.status === 'running' || t.status === 'pending')
    if (hasRunning || (selectedTask.value && selectedTask.value.status === 'running')) {
      await loadTasks()
      if (selectedTask.value) {
        const updated = tasks.value.find(t => t.id === selectedTask.value.id)
        if (updated) {
          selectedTask.value = updated
          if (updated.status === 'completed' || updated.status === 'failed') {
            await loadTaskResult(updated.id)
          }
        }
      }
    }
  }, 3000)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

onMounted(async () => {
  await loadSources()
  await loadTasks()
  startPolling()
})

watch(() => selectedTask.value?.id, () => {
  selectedDataIds.value = []
})
</script>
