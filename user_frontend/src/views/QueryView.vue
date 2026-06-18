<template>
  <div class="h-full flex flex-col">
    <!-- Top Header -->
    <header class="w-full z-50 bg-surface-container-high/80 backdrop-blur-xl border-b border-primary/20 flex items-center justify-between px-6 h-16 shrink-0 shadow-lg">
      <div class="flex items-center gap-6">
        <router-link to="/dashboard" class="flex items-center gap-2 text-on-surface-variant hover:text-primary transition-colors">
          <span class="material-symbols-outlined text-[20px]">arrow_back</span>
          <span class="hidden sm:inline font-label-tech text-label-tech">返回首页</span>
        </router-link>
        <div class="h-8 w-[1px] bg-outline-variant/30 hidden sm:block"></div>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-primary-fixed-dim/20 rounded flex items-center justify-center border border-primary/30">
            <span class="material-symbols-outlined text-primary text-xl">database</span>
          </div>
          <h1 class="font-headline-sm text-headline-sm font-bold tracking-tighter text-primary">XNU 数据智能终端</h1>
        </div>
      </div>
      <div class="flex items-center gap-6">
        <div class="flex flex-col items-end">
          <span class="font-label-tech text-[10px] text-primary/60">服务器节点: HUB-DESKTOP-01</span>
          <span class="font-label-code text-[10px] text-secondary">系统状态: 运行良好</span>
        </div>
        <div class="h-8 w-[1px] bg-outline-variant/30 hidden sm:block"></div>
        <div class="flex items-center gap-3">
          <div class="text-right hidden sm:block">
            <p class="font-label-tech text-label-tech text-on-surface">{{ store.user.name }}</p>
            <p class="font-label-code text-[10px] text-on-surface-variant">{{ store.user.role }}</p>
          </div>
          <div class="w-10 h-10 rounded-full border-2 border-primary/30 p-0.5 bg-surface-container flex items-center justify-center">
            <span v-if="!store.user.avatar" class="material-symbols-outlined text-primary text-lg">person</span>
            <img v-else alt="用户头像" class="w-full h-full rounded-full object-cover" :src="store.user.avatar" />
          </div>
        </div>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- History Sidebar -->
      <aside class="w-80 bg-surface-container-low/50 border-r border-outline-variant/20 flex flex-col shrink-0 hidden md:flex">
        <div class="p-4 border-b border-outline-variant/20">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-headline-sm text-headline-sm text-primary flex items-center gap-2">
              <span class="material-symbols-outlined text-lg">history</span>
              历史会话
            </h2>
            <button @click="newChat" class="p-1 hover:bg-primary/10 text-primary transition-colors rounded" title="新对话">
              <span class="material-symbols-outlined">add_box</span>
            </button>
          </div>
          <div class="relative">
            <span class="material-symbols-outlined absolute left-3 top-2.5 text-sm opacity-40">search</span>
            <input v-model="historySearch" class="w-full bg-surface-variant/20 border border-outline-variant/30 rounded-lg pl-9 py-2 text-xs font-label-tech focus:ring-1 focus:ring-primary focus:border-primary outline-none" placeholder="搜索历史记录..." type="text" />
          </div>
        </div>
        <nav class="flex-1 overflow-y-auto custom-scrollbar p-2 space-y-1">
          <div v-for="(chat, idx) in filteredHistory" :key="chat.id" @click="loadChat(chat)" class="p-3 flex flex-col gap-1 cursor-pointer transition-colors" :class="activeChatIndex === idx ? 'bg-primary/10 border-l-2 border-primary rounded-r' : 'hover:bg-surface-variant/20 rounded'">
            <div class="flex justify-between items-start">
              <span class="font-label-code text-[10px]" :class="activeChatIndex === idx ? 'text-primary' : 'opacity-40'">{{ formatDate(chat.updated_at) }}</span>
              <button v-if="activeChatIndex === idx" @click.stop="deleteChat(chat)" class="text-on-surface-variant hover:text-error opacity-60 hover:opacity-100" title="删除会话">
                <span class="material-symbols-outlined text-xs">delete</span>
              </button>
            </div>
            <p class="font-body-md truncate" :class="activeChatIndex === idx ? 'text-on-surface' : 'text-on-surface-variant'">{{ chat.title }}</p>
          </div>
          <div v-if="filteredHistory.length === 0" class="p-4 text-center text-on-surface-variant/40 text-sm">
            暂无历史会话
          </div>
        </nav>
      </aside>

      <!-- Main Workspace -->
      <main class="flex-1 flex flex-col relative bg-background overflow-hidden">
        <!-- Canvas Background -->
        <canvas ref="canvasRef" class="fixed inset-0 -z-20 pointer-events-none opacity-20"></canvas>
        <div class="scanline-effect absolute inset-0 pointer-events-none z-0"></div>

        <!-- Staff Selector -->
        <div class="shrink-0 z-20 px-6 py-3 border-b border-outline-variant/20 bg-surface-container/50 backdrop-blur flex items-center gap-4">
          <span class="font-label-tech text-sm text-on-surface-variant">当前智能体</span>
          <div class="relative staff-selector">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-primary text-lg pointer-events-none z-10">smart_toy</span>
            <select :value="selectedStaffId" @change="onSelectStaffChange" class="appearance-none bg-surface-container border border-primary/30 rounded-lg pl-10 pr-10 py-2 text-on-surface font-label-tech min-w-[180px] cursor-pointer hover:bg-surface-container-high transition-colors focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary">
              <option value="" disabled>选择智能体</option>
              <option v-for="staff in staffList" :key="staff.staff_id" :value="staff.staff_id">{{ staff.name }}</option>
            </select>
            <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px] pointer-events-none">expand_more</span>
          </div>
          <div v-if="selectedStaff" class="flex-1 hidden sm:block text-[12px] text-on-surface-variant font-label-tech truncate">
            {{ selectedStaff.desc }}
          </div>
        </div>

        <!-- Chat Content -->
        <div ref="chatContainer" class="flex-1 overflow-y-auto custom-scrollbar p-4 md:p-8 z-10">
          <div class="max-w-6xl mx-auto space-y-8 pb-32">
            <!-- Empty State -->
            <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-on-surface-variant/60 pt-20">
              <span class="material-symbols-outlined text-6xl mb-4 text-primary/30">smart_toy</span>
              <p class="font-headline-sm text-headline-sm text-primary mb-2">选择一个智能体开始提问</p>
              <p class="text-body-md text-center max-w-md">在上方选择数字员工，输入自然语言问题，即可获得数据查询、分析或领域专业解答。</p>
            </div>

            <template v-for="(msg, idx) in messages" :key="idx">
              <!-- User Question -->
              <div v-if="msg.role === 'user'" class="flex flex-col gap-3">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full border border-primary/20 bg-secondary-container/10 flex items-center justify-center">
                    <span class="material-symbols-outlined text-sm text-secondary-fixed">person</span>
                  </div>
                  <span class="font-label-tech text-label-tech text-on-surface-variant">提问者: {{ store.user.name }}</span>
                  <span class="font-label-code text-[10px] opacity-40 px-2 border-l border-outline-variant/30">{{ msg.time }}</span>
                </div>
                <div class="glass-panel p-6 rounded-xl border-l-4 border-l-primary shadow-lg">
                  <p class="font-body-lg text-body-lg text-on-surface leading-relaxed whitespace-pre-wrap">{{ msg.content }}</p>
                </div>
              </div>

              <!-- AI Response -->
              <div v-else class="flex flex-col gap-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-primary-container flex items-center justify-center">
                    <span class="material-symbols-outlined text-sm text-on-primary-container">smart_toy</span>
                  </div>
                  <span class="font-label-tech text-label-tech text-primary">{{ msg.staff_name || 'XNU 智能核心' }}</span>
                  <div v-if="loading && idx === messages.length - 1" class="flex items-center gap-2 px-2 border-l border-outline-variant/30">
                    <span class="w-1.5 h-1.5 rounded-full bg-secondary-fixed animate-pulse"></span>
                    <span class="font-label-code text-[10px] opacity-40">思考中...</span>
                  </div>
                </div>
                <div class="glass-panel p-6 rounded-xl border border-primary/20 shadow-lg">
                  <p class="font-body-md text-on-surface-variant leading-relaxed whitespace-pre-wrap">{{ msg.content }}</p>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- Floating Chat Input -->
        <div class="absolute bottom-0 left-0 w-full p-4 md:p-8 bg-gradient-to-t from-background via-background/90 to-transparent z-20">
          <div class="max-w-4xl mx-auto">
            <div class="glass-panel p-2 rounded-2xl flex items-center gap-3 border-primary/40 shadow-[0_10px_50px_rgba(0,219,231,0.2)] focus-within:border-primary/80 transition-all group">
              <div class="flex items-center pl-4 gap-2">
                <button class="p-2 text-on-surface-variant hover:text-primary transition-colors" title="上传文件">
                  <span class="material-symbols-outlined">attach_file</span>
                </button>
              </div>
              <div class="h-6 w-[1px] bg-outline-variant/30"></div>
              <input v-model="inputQuestion" @keyup.enter="sendQuestion" class="flex-1 bg-transparent border-none focus:ring-0 text-body-lg placeholder:text-on-surface-variant/30 font-label-tech py-4" placeholder="请输入您的自然语言查询指令，例如：'对比各学院经费预算'..." type="text" />
              <button @click="sendQuestion" :disabled="!inputQuestion.trim() || !selectedStaff || loading" class="bg-primary text-on-primary-fixed px-6 md:px-8 py-3 rounded-xl font-label-tech font-bold hover:shadow-[0_0_20px_#00dbe7] transition-all flex items-center gap-3 group/btn active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed">
                <span v-if="loading" class="material-symbols-outlined text-sm animate-spin">sync</span>
                <span v-else class="material-symbols-outlined text-sm group-hover/btn:translate-x-1 transition-transform">terminal</span>
                {{ loading ? '执行中' : '执行查询' }}
              </button>
            </div>
            <div class="flex justify-center mt-3 gap-6">
              <span class="flex items-center gap-1.5 font-label-code text-[10px] text-on-surface-variant/40">
                <span class="w-1.5 h-1.5 rounded-full bg-primary/40"></span>
                当前智能体: {{ selectedStaff ? selectedStaff.name : '未选择' }}
              </span>
              <span class="flex items-center gap-1.5 font-label-code text-[10px] text-on-surface-variant/40">
                <span class="w-1.5 h-1.5 rounded-full bg-primary/40"></span>
                数据安全等级: L3
              </span>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useAppStore } from '../stores/index.js'
import {
  getStaffList,
  askStaffQuestion,
  createConversation,
  getConversationList,
  getConversation,
  updateConversation,
  deleteConversation
} from '../api/user.js'

const store = useAppStore()

const canvasRef = ref(null)
let particles = []
let animationId = null

const staffList = ref([])
const selectedStaffId = ref('')
const selectedStaff = computed(() => staffList.value.find(s => s.staff_id === selectedStaffId.value) || null)
const inputQuestion = ref('')
const messages = ref([])
const loading = ref(false)
const currentConversationId = ref(null)
const activeChatIndex = ref(-1)
const historySearch = ref('')
const history = ref([])

const filteredHistory = computed(() => {
  if (!historySearch.value) return history.value
  const q = historySearch.value.toLowerCase()
  return history.value.filter(h => h.title.toLowerCase().includes(q))
})

function formatTime() {
  const d = new Date()
  return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function makeTitle(question) {
  return question.length > 30 ? question.slice(0, 30) + '...' : question
}

async function loadStaffs() {
  try {
    const res = await getStaffList()
    if (res.code === 200 && res.data) {
      staffList.value = res.data.items || []
      if (staffList.value.length && !selectedStaffId.value) {
        selectedStaffId.value = staffList.value[0].staff_id
      }
    }
  } catch (e) {
    console.error('加载数字员工失败:', e)
  }
}

async function loadHistory() {
  try {
    const res = await getConversationList()
    if (res.code === 200 && res.data) {
      history.value = res.data.items || []
    }
  } catch (e) {
    console.error('加载历史会话失败:', e)
  }
}

function onSelectStaffChange(e) {
  selectedStaffId.value = Number(e.target.value)
}

function resetCurrentSession() {
  messages.value = []
  currentConversationId.value = null
  activeChatIndex.value = -1
  inputQuestion.value = ''
  if (staffList.value.length) {
    selectedStaffId.value = staffList.value[0].staff_id
  }
}

async function newChat() {
  // 当前会话已有消息且未保存过 conversation_id 时，创建会话并保存
  if (messages.value.length && !currentConversationId.value) {
    await saveCurrentSession()
  }
  resetCurrentSession()
  await loadHistory()
}

async function saveCurrentSession() {
  if (!messages.value.length) return
  const userMsg = messages.value.find(m => m.role === 'user')
  const title = userMsg ? makeTitle(userMsg.content) : '新会话'
  try {
    const res = await createConversation({
      staff_id: selectedStaffId.value,
      title
    })
    if (res.code === 200 && res.data) {
      currentConversationId.value = res.data.id
      await updateConversation(res.data.id, { messages: messages.value })
    }
  } catch (e) {
    console.error('保存当前会话失败:', e)
  }
}

async function loadChat(chat) {
  activeChatIndex.value = history.value.findIndex(h => h.id === chat.id)
  if (currentConversationId.value !== chat.id && messages.value.length && !currentConversationId.value) {
    // 切换前先把当前未保存会话落地
    await saveCurrentSession()
  }
  try {
    const res = await getConversation(chat.id)
    if (res.code === 200 && res.data) {
      currentConversationId.value = res.data.id
      selectedStaffId.value = res.data.staff_id || staffList.value[0]?.staff_id
      messages.value = Array.isArray(res.data.messages) ? res.data.messages : []
    }
  } catch (e) {
    console.error('加载会话详情失败:', e)
  }
}

async function deleteChat(chat) {
  if (!confirm('确定删除该会话吗？')) return
  try {
    const res = await deleteConversation(chat.id)
    if (res.code === 200) {
      if (currentConversationId.value === chat.id) {
        resetCurrentSession()
      }
      await loadHistory()
    }
  } catch (e) {
    console.error('删除会话失败:', e)
  }
}

async function sendQuestion() {
  const question = inputQuestion.value.trim()
  if (!question || !selectedStaff.value || loading.value) return

  messages.value.push({ role: 'user', content: question, time: formatTime() })
  inputQuestion.value = ''
  loading.value = true
  scrollToBottom()

  // 首次发送时创建会话
  let convId = currentConversationId.value
  if (!convId) {
    try {
      const createRes = await createConversation({
        staff_id: selectedStaff.value.staff_id,
        title: makeTitle(question)
      })
      if (createRes.code === 200 && createRes.data) {
        convId = createRes.data.id
        currentConversationId.value = convId
        await loadHistory()
        activeChatIndex.value = history.value.findIndex(h => h.id === convId)
      }
    } catch (e) {
      console.error('创建会话失败:', e)
    }
  }

  try {
    const res = await askStaffQuestion({
      staff_id: selectedStaff.value.staff_id,
      question
    })
    if (res.code === 200 && res.data) {
      messages.value.push({
        role: 'assistant',
        content: res.data.reply,
        staff_name: res.data.staff_name,
        time: formatTime()
      })
    } else {
      messages.value.push({
        role: 'assistant',
        content: res.message || '请求失败，请稍后重试',
        staff_name: selectedStaff.value.name,
        time: formatTime()
      })
    }
  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: '网络异常，请稍后重试',
      staff_name: selectedStaff.value.name,
      time: formatTime()
    })
  } finally {
    loading.value = false
    scrollToBottom()
    // 保存消息到当前会话
    if (convId) {
      try {
        await updateConversation(convId, { messages: messages.value })
        await loadHistory()
        activeChatIndex.value = history.value.findIndex(h => h.id === convId)
      } catch (e) {
        console.error('保存消息失败:', e)
      }
    }
  }
}

function scrollToBottom() {
  nextTick(() => {
    const container = document.querySelector('.custom-scrollbar.overflow-y-auto')
    if (container) container.scrollTop = container.scrollHeight
  })
}

watch(messages, scrollToBottom)

function initParticles() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  function resize() {
    canvas.width = canvas.offsetWidth
    canvas.height = canvas.offsetHeight
    particles = []
    for (let i = 0; i < 80; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2 + 0.5,
        speedY: Math.random() * 0.3 + 0.05,
        opacity: Math.random() * 0.5
      })
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    particles.forEach(p => {
      p.y -= p.speedY
      if (p.y < 0) p.y = canvas.height
      ctx.fillStyle = `rgba(0, 219, 231, ${p.opacity})`
      ctx.fillRect(p.x, p.y, p.size, p.size)
    })
    animationId = requestAnimationFrame(animate)
  }

  resize()
  animate()
  window.addEventListener('resize', resize)
}

onMounted(() => {
  initParticles()
  loadStaffs()
  loadHistory()
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
})
</script>

<style scoped>
canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
</style>
