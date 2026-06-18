<template>
  <div class="h-full flex overflow-hidden">
    <!-- Left Sidebar -->
    <aside class="w-[280px] bg-surface-container border-r-2 border-outline-variant flex flex-col">
      <div class="p-4 border-b border-outline-variant">
        <button
          @click="startNewChat"
          class="w-full bg-primary text-on-primary py-2 font-label-pixel flex items-center justify-center gap-2 hover:bg-primary/90 transition-all"
        >
          <span class="material-symbols-outlined text-sm">add</span>
          新对话
        </button>
      </div>
      <div class="flex-1 overflow-y-auto p-2 space-y-1">
        <div
          v-for="(session, idx) in sessions"
          :key="idx"
          @click="switchSession(idx)"
          class="p-3 cursor-pointer transition-colors"
          :class="currentSessionIndex === idx ? 'bg-primary/10 border-l-4 border-primary' : 'hover:bg-surface-variant border-l-4 border-transparent'"
        >
          <p class="text-sm text-on-surface font-bold truncate">{{ session.title || '新对话' }}</p>
          <p class="text-[10px] text-on-surface-variant font-label-pixel mt-1">{{ session.messages.length }} 条消息</p>
        </div>
        <div v-if="sessions.length === 0" class="p-3 text-center text-on-surface-variant text-xs">
          暂无历史对话
        </div>
      </div>
    </aside>

    <!-- Right Main Area -->
    <main class="flex-1 flex flex-col bg-surface-dim">
      <div class="flex-1 overflow-y-auto p-6 space-y-6" ref="messageContainer">
        <!-- Welcome Message -->
        <div v-if="currentSession.messages.length === 0" class="flex gap-4">
          <div class="w-8 h-8 bg-primary text-on-primary shrink-0 flex items-center justify-center font-label-pixel">AI</div>
          <div class="bg-surface-container border-2 border-outline-variant p-4 max-w-[80%]">
            <p class="text-sm text-on-surface leading-relaxed">你好！我是西华师范大学数智校园系统的 AI 问讯助手。我可以基于数据仓库中的已保存数据为你解答问题。</p>
            <p class="text-[10px] text-on-surface-variant font-label-pixel mt-2">数据仓库检索 + 大模型生成</p>
          </div>
        </div>

        <!-- Messages -->
        <template v-for="(msg, idx) in currentSession.messages" :key="idx">
          <!-- AI Message -->
          <div v-if="msg.role === 'ai'" class="flex gap-4">
            <div class="w-8 h-8 bg-primary text-on-primary shrink-0 flex items-center justify-center font-label-pixel">AI</div>
            <div class="bg-surface-container border-2 border-outline-variant p-4 max-w-[80%]">
              <p class="text-sm text-on-surface leading-relaxed whitespace-pre-wrap">{{ msg.content }}</p>
              <div v-if="msg.sources && msg.sources.length" class="mt-3 pt-3 border-t border-outline-variant/30">
                <p class="text-[10px] text-on-surface-variant font-label-pixel mb-1">参考来源：</p>
                <div class="flex flex-wrap gap-2">
                  <a
                    v-for="source in msg.sources"
                    :key="source.id"
                    :href="source.url"
                    target="_blank"
                    class="text-[10px] px-2 py-0.5 bg-primary/10 text-primary border border-primary/30 hover:bg-primary/20"
                  >
                    {{ source.title || `资料 ${source.id}` }}
                  </a>
                </div>
              </div>
              <p class="text-[10px] text-on-surface-variant font-label-pixel mt-2">{{ formatTime(msg.time) }}</p>
            </div>
          </div>

          <!-- User Message -->
          <div v-else class="flex gap-4 flex-row-reverse">
            <div class="w-8 h-8 bg-secondary-fixed text-on-secondary-fixed shrink-0 flex items-center justify-center font-label-pixel">ME</div>
            <div class="bg-primary-container border-2 border-primary p-4 max-w-[80%]">
              <p class="text-sm text-on-primary-container leading-relaxed">{{ msg.content }}</p>
              <p class="text-[10px] text-on-primary-container/60 font-label-pixel mt-2 text-right">{{ formatTime(msg.time) }}</p>
            </div>
          </div>
        </template>

        <!-- Loading -->
        <div v-if="loading" class="flex gap-4">
          <div class="w-8 h-8 bg-primary text-on-primary shrink-0 flex items-center justify-center font-label-pixel">AI</div>
          <div class="bg-surface-container border-2 border-outline-variant p-4 max-w-[80%]">
            <div class="flex items-center gap-2">
              <span class="inline-block w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></span>
              <span class="text-sm text-on-surface">正在检索数据仓库并生成回答...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="p-4 border-t-2 border-outline-variant bg-surface-container">
        <div class="flex gap-2">
          <input
            v-model="inputText"
            @keydown.enter="sendMessage"
            class="flex-1 bg-surface-dim border-2 border-outline-variant px-4 py-3 focus:border-primary outline-none transition-colors"
            placeholder="输入您的问题，例如：西华师范大学的天文学科情况如何？"
            type="text"
            :disabled="loading"
          />
          <button
            @click="sendMessage"
            :disabled="loading || !inputText.trim()"
            class="bg-primary text-on-primary px-6 py-3 font-label-pixel flex items-center gap-2 hover:bg-primary/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="material-symbols-outlined text-sm">send</span>
            发送
          </button>
        </div>
        <p class="text-[10px] text-on-surface-variant font-label-pixel mt-2 text-center">AI 生成内容基于数据仓库中已保存的数据，仅供参考，重要决策请人工复核。</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { aiInquiry } from '@/api/aiInquiry.js'

const sessions = ref([
  {
    title: '当前对话',
    messages: []
  }
])
const currentSessionIndex = ref(0)
const currentSession = computed(() => sessions.value[currentSessionIndex.value] || { messages: [] })

const inputText = ref('')
const loading = ref(false)
const messageContainer = ref(null)

function formatTime(date) {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleString('zh-CN', { hour12: false, month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function scrollToBottom() {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

function startNewChat() {
  sessions.value.unshift({
    title: '新对话',
    messages: []
  })
  currentSessionIndex.value = 0
  inputText.value = ''
}

function switchSession(idx) {
  currentSessionIndex.value = idx
}

async function sendMessage() {
  const question = inputText.value.trim()
  if (!question || loading.value) return

  // 更新对话标题
  if (!currentSession.value.title || currentSession.value.title === '新对话') {
    currentSession.value.title = question.slice(0, 20) + (question.length > 20 ? '...' : '')
  }

  // 添加用户消息
  currentSession.value.messages.push({
    role: 'user',
    content: question,
    time: new Date()
  })
  inputText.value = ''
  loading.value = true
  await scrollToBottom()

  try {
    const res = await aiInquiry(question)
    const data = res.data || {}
    currentSession.value.messages.push({
      role: 'ai',
      content: data.answer || '抱歉，暂时没有获得有效回答。',
      sources: data.sources || [],
      time: new Date()
    })
  } catch (err) {
    currentSession.value.messages.push({
      role: 'ai',
      content: err.message || '请求失败，请稍后再试。',
      time: new Date()
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}
</script>
