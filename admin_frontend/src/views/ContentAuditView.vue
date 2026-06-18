<template>
  <div class="h-full overflow-y-auto bg-surface-dim">
    <div class="p-container-margin space-y-8 max-w-[1400px] mx-auto">
      <div class="flex justify-between items-end">
        <div>
          <h2 class="font-display-lg text-display-lg text-on-surface mb-2">内容审核</h2>
          <p class="text-on-surface-variant font-body-lg">AI 驱动的聊天消息（messages）安全与合规性审查中心。</p>
        </div>
        <button
          @click="handleScan"
          :disabled="scanning"
          class="px-4 py-2 bg-primary text-on-primary font-label-pixel text-xs hover:bg-primary/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <span v-if="scanning" class="inline-block w-4 h-4 border-2 border-on-primary border-t-transparent rounded-full animate-spin"></span>
          {{ scanning ? '扫描中...' : 'AI 扫描消息' }}
        </button>
      </div>

      <div v-if="scanResult" class="p-3 bg-secondary-fixed/20 border border-secondary-fixed text-on-surface font-body-sm">
        {{ scanResult }}
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-gutter">
        <div class="lg:col-span-2 bg-surface-container border-2 border-outline-variant p-card-padding">
          <div class="flex items-center gap-3 mb-4">
            <span class="material-symbols-outlined text-error text-[24px]">warning</span>
            <h3 class="font-title-md text-title-md">违规消息列表</h3>
            <span class="ml-auto text-[11px] font-label-pixel text-on-surface-variant">共 {{ total }} 条</span>
          </div>
          <div class="space-y-4">
            <div v-if="loading" class="text-center py-8 text-on-surface-variant font-body-sm">加载中...</div>
            <div v-else-if="items.length === 0" class="text-center py-8 text-on-surface-variant font-body-sm">暂无违规消息，点击右上角「AI 扫描消息」开始审核。</div>
            <div v-for="item in items" :key="item.id" class="p-3 bg-error/10 border border-error/30">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <span class="font-label-pixel text-[10px] text-error">{{ item.type_label }}</span>
                  <span class="ml-2 text-[10px] text-on-surface-variant font-label-pixel">{{ item.sender_type === 'staff' ? '数字员工' : '用户' }}: {{ item.sender_name }}</span>
                </div>
                <span class="text-[10px] text-on-surface-variant font-label-pixel">{{ formatDate(item.created_at) }}</span>
              </div>
              <p class="text-sm text-on-surface mb-2 whitespace-pre-wrap">{{ item.content }}</p>
              <div class="flex justify-between items-center">
                <p class="text-xs text-on-surface-variant">判定理由：{{ item.reason }}（置信度 {{ (Math.abs(item.confidence) * 100).toFixed(1) }}%）</p>
                <div class="flex gap-2">
                  <button class="px-3 py-1 bg-error text-on-error text-xs font-label-pixel">拦截</button>
                  <button class="px-3 py-1 bg-surface-variant text-on-surface text-xs font-label-pixel border border-outline-variant">通过</button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="totalPages > 1" class="mt-4 flex justify-end gap-1">
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

        <div class="bg-surface-container border-2 border-outline-variant p-card-padding">
          <div class="flex items-center gap-3 mb-4">
            <span class="material-symbols-outlined text-secondary-fixed text-[24px]">check_circle</span>
            <h3 class="font-title-md text-title-md">违规类型分布</h3>
          </div>
          <div class="space-y-3">
            <div v-for="(count, type) in typeStats" :key="type" class="flex justify-between items-center p-2 border-b border-outline-variant/30">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full" :class="typeColorClass(type)"></span>
                <span class="text-sm text-on-surface">{{ typeLabel(type) }}</span>
              </div>
              <span class="px-2 py-0.5 bg-error/20 text-error text-[10px] font-label-pixel border border-error">{{ count }}</span>
            </div>
            <div v-if="Object.keys(typeStats).length === 0" class="text-center py-4 text-on-surface-variant text-sm">暂无数据</div>
          </div>
        </div>
      </div>

      <!-- 违规用户列表 -->
      <div class="bg-surface-container border-2 border-outline-variant p-card-padding">
        <div class="flex items-center gap-3 mb-4">
          <span class="material-symbols-outlined text-error text-[24px]">person_off</span>
          <h3 class="font-title-md text-title-md">违规用户管理</h3>
          <span class="ml-auto text-[11px] font-label-pixel text-on-surface-variant">共 {{ violators.length }} 人</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-surface-container-highest border-b-2 border-outline-variant">
                <th class="px-4 py-3 font-label-pixel text-xs text-on-surface-variant uppercase">用户</th>
                <th class="px-4 py-3 font-label-pixel text-xs text-on-surface-variant uppercase">违规次数</th>
                <th class="px-4 py-3 font-label-pixel text-xs text-on-surface-variant uppercase">最近违规类型</th>
                <th class="px-4 py-3 font-label-pixel text-xs text-on-surface-variant uppercase">最近违规时间</th>
                <th class="px-4 py-3 font-label-pixel text-xs text-on-surface-variant uppercase">状态</th>
                <th class="px-4 py-3 font-label-pixel text-xs text-on-surface-variant uppercase text-right">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-outline-variant/30">
              <tr v-if="loadingViolators" class="hover:bg-primary/5 transition-colors">
                <td colspan="6" class="px-4 py-6 text-center text-on-surface-variant font-body-sm">加载中...</td>
              </tr>
              <tr v-else-if="violators.length === 0" class="hover:bg-primary/5 transition-colors">
                <td colspan="6" class="px-4 py-6 text-center text-on-surface-variant font-body-sm">暂无违规用户</td>
              </tr>
              <tr v-for="user in violators" :key="user.user_id" class="hover:bg-primary/5 transition-colors">
                <td class="px-4 py-3 text-sm text-on-surface">
                  <div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-xs text-on-surface-variant">
                      {{ (user.nickname || user.username || '?').charAt(0) }}
                    </div>
                    <div>
                      <div class="font-semibold">{{ user.nickname || user.username }}</div>
                      <div class="text-[10px] text-on-surface-variant font-label-pixel">@{{ user.username }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-4 py-3 text-sm text-on-surface">{{ user.violation_count }}</td>
                <td class="px-4 py-3">
                  <span class="px-2 py-0.5 bg-error/20 text-error text-[10px] font-label-pixel border border-error">{{ user.latest_type_label }}</span>
                </td>
                <td class="px-4 py-3 text-sm text-on-surface-variant">{{ formatDate(user.latest_at) }}</td>
                <td class="px-4 py-3">
                  <span v-if="user.is_active" class="px-2 py-0.5 bg-secondary-fixed/20 text-secondary-fixed text-[10px] font-label-pixel border border-secondary-fixed">正常</span>
                  <span v-else class="px-2 py-0.5 bg-error/20 text-error text-[10px] font-label-pixel border border-error">已封禁</span>
                </td>
                <td class="px-4 py-3 text-right">
                  <button
                    v-if="user.is_active"
                    @click="banUser(user)"
                    :disabled="banLoading[user.user_id]"
                    class="px-3 py-1 bg-error text-on-error text-xs font-label-pixel hover:bg-error/90 disabled:opacity-50"
                  >
                    {{ banLoading[user.user_id] ? '处理中...' : '永久封禁' }}
                  </button>
                  <span v-else class="text-xs text-on-surface-variant font-label-pixel">已处理</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { scanMessages, getMessageViolations, getViolatorUsers } from '@/api/audit.js'
import { updateUser } from '@/api/user.js'

const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const scanning = ref(false)
const scanResult = ref('')

const violators = ref([])
const loadingViolators = ref(false)
const banLoading = ref({})

const totalPages = computed(() => Math.ceil(total.value / pageSize.value) || 1)
const visiblePages = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i++) {
    pages.push(i)
  }
  return pages
})

const typeStats = computed(() => {
  const stats = {}
  items.value.forEach(item => {
    const key = item.type || 'OTHER'
    stats[key] = (stats[key] || 0) + 1
  })
  return stats
})

const typeLabelMap = {
  PORN: '色情低俗',
  VIOLENCE: '暴力血腥',
  POLITICAL: '政治敏感',
  ILLEGAL: '违法违规',
  HATE: '仇恨言论',
  SPAM: '垃圾广告',
  SENSITIVE_INFO: '敏感信息泄露',
  OTHER: '其他违规'
}

function typeLabel(type) {
  return typeLabelMap[type] || type
}

function typeColorClass(type) {
  const map = {
    PORN: 'bg-pink-500',
    VIOLENCE: 'bg-red-600',
    POLITICAL: 'bg-amber-500',
    ILLEGAL: 'bg-purple-500',
    HATE: 'bg-orange-500',
    SPAM: 'bg-blue-500',
    SENSITIVE_INFO: 'bg-cyan-500',
    OTHER: 'bg-gray-500'
  }
  return map[type] || 'bg-gray-500'
}

function formatDate(iso) {
  if (!iso) return '-'
  const d = new Date(iso)
  if (isNaN(d.getTime())) return iso
  return d.toLocaleString('zh-CN', { hour12: false })
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getMessageViolations(page.value, pageSize.value)
    items.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (err) {
    console.error('获取消息违规列表失败', err)
  } finally {
    loading.value = false
  }
}

async function handleScan() {
  scanning.value = true
  scanResult.value = ''
  try {
    const res = await scanMessages(100)
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

async function fetchViolators() {
  loadingViolators.value = true
  try {
    const res = await getViolatorUsers()
    violators.value = res.data.items || []
  } catch (err) {
    console.error('获取违规用户失败', err)
  } finally {
    loadingViolators.value = false
  }
}

async function banUser(user) {
  if (!confirm(`确定永久封禁用户「${user.nickname || user.username}」吗？封禁后该用户将无法登录。`)) {
    return
  }
  banLoading.value[user.user_id] = true
  try {
    await updateUser(user.user_id, { is_active: false })
    user.is_active = false
    scanResult.value = `已永久封禁用户 ${user.nickname || user.username}`
  } catch (err) {
    scanResult.value = err.message || '封禁失败'
  } finally {
    banLoading.value[user.user_id] = false
  }
}

onMounted(() => {
  fetchData()
  fetchViolators()
})
</script>
