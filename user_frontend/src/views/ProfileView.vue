<template>
  <div class="h-full flex flex-col">
    <!-- Top App Bar -->
    <header class="fixed top-0 w-full z-50 bg-surface/70 backdrop-blur-xl border-b border-primary/20 shadow-[0px_4px_20px_rgba(0,219,231,0.15)] flex items-center justify-between px-margin-mobile h-16">
      <div class="flex items-center gap-4">
        <router-link to="/dashboard" class="flex items-center gap-1 text-on-surface-variant hover:text-primary transition-colors">
          <span class="material-symbols-outlined">arrow_back</span>
          <span class="hidden sm:inline font-label-tech text-[12px]">返回首页</span>
        </router-link>
        <div class="h-6 w-[1px] bg-outline-variant/30 hidden sm:block"></div>
        <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">grid_view</span>
        <h1 class="font-headline-sm text-headline-sm font-bold tracking-tighter text-primary">XNU DIGITAL HUB</h1>
      </div>
      <div class="flex items-center gap-gutter">
        <span class="material-symbols-outlined text-primary hover:bg-primary/10 p-2 rounded-full cursor-pointer transition-colors active:scale-95">sensors</span>
        <div class="flex items-center gap-xs bg-surface-container px-3 py-1 rounded-full border border-primary/20">
          <div class="w-2 h-2 rounded-full bg-secondary-container animate-pulse shadow-[0_0_8px_#2ff801]"></div>
          <span class="text-label-code font-label-code text-on-surface">SYSTEM ONLINE</span>
        </div>
      </div>
    </header>

    <main class="flex-1 flex pt-16 h-full">
      <!-- Chat List Sidebar -->
      <div class="w-80 glass-panel rounded-xl flex flex-col shrink-0 border border-primary/10 m-gutter mr-0 overflow-hidden">
        <!-- Tabs -->
        <div class="flex border-b border-primary/10">
          <button class="flex-1 py-3 text-center text-body-md font-label-tech transition-colors" :class="listTab === 'friends' ? 'text-primary border-b-2 border-primary bg-primary/5' : 'text-on-surface-variant hover:text-primary'" @click="listTab = 'friends'">
            好友
          </button>
          <button class="flex-1 py-3 text-center text-body-md font-label-tech transition-colors" :class="listTab === 'groups' ? 'text-primary border-b-2 border-primary bg-primary/5' : 'text-on-surface-variant hover:text-primary'" @click="listTab = 'groups'">
            群聊
          </button>
        </div>

        <!-- Search & Actions -->
        <div class="p-gutter border-b border-primary/10 space-y-2">
          <div class="relative">
            <input v-model="searchQuery" class="w-full bg-surface-container-lowest border border-primary/20 rounded-lg py-2 pl-10 pr-4 text-body-md focus:outline-none focus:border-primary transition-all" placeholder="搜索..." type="text" />
            <span class="material-symbols-outlined absolute left-3 top-2.5 text-on-surface-variant text-[20px]">search</span>
          </div>
          <div class="flex gap-2">
            <button @click="showAddFriend = true" class="flex-1 py-1.5 bg-primary/10 text-primary text-[12px] font-label-tech rounded hover:bg-primary/20 transition-colors">
              + 添加好友
            </button>
            <button @click="showCreateGroup = true" class="flex-1 py-1.5 bg-secondary-fixed/10 text-secondary-fixed text-[12px] font-label-tech rounded hover:bg-secondary-fixed/20 transition-colors">
              + 创建群聊
            </button>
          </div>
        </div>

        <!-- List -->
        <div class="flex-1 overflow-y-auto custom-scrollbar">
          <!-- Friends -->
          <template v-if="listTab === 'friends'">
            <div v-if="filteredFriends.length === 0" class="flex flex-col items-center justify-center h-40 text-on-surface-variant/60">
              <span class="material-symbols-outlined text-4xl mb-2">person_off</span>
              <p class="text-body-sm">暂无好友</p>
              <p class="text-[12px]">点击上方按钮添加好友</p>
            </div>
            <div v-for="friend in filteredFriends" :key="friend.friend_id" @click="selectChat('private', friend)" class="p-gutter flex gap-sm cursor-pointer transition-all border-l-4" :class="activeChat?.friend_id === friend.friend_id ? 'bg-primary/10 border-primary' : 'hover:bg-surface-variant/30 border-transparent'">
              <div class="w-12 h-12 rounded-lg bg-surface-container-highest flex items-center justify-center border border-primary/30">
                <span class="material-symbols-outlined text-primary">person</span>
              </div>
              <div class="flex-1 overflow-hidden">
                <div class="flex justify-between items-center">
                  <span class="font-body-lg truncate" :class="activeChat?.friend_id === friend.friend_id ? 'text-primary' : 'text-on-surface'">{{ friend.friend_name }}</span>
                </div>
                <p class="text-body-md text-on-surface-variant truncate">点击开始聊天</p>
              </div>
            </div>
          </template>

          <!-- Groups -->
          <template v-else>
            <div v-if="filteredGroups.length === 0" class="flex flex-col items-center justify-center h-40 text-on-surface-variant/60">
              <span class="material-symbols-outlined text-4xl mb-2">chat_bubble_outline</span>
              <p class="text-body-sm">暂无群聊</p>
              <p class="text-[12px]">点击上方按钮创建群聊</p>
            </div>
            <div v-for="group in filteredGroups" :key="group.id" @click="selectChat('group', group)" class="p-gutter flex gap-sm cursor-pointer transition-all border-l-4" :class="activeChat?.id === group.id ? 'bg-primary/10 border-primary' : 'hover:bg-surface-variant/30 border-transparent'">
              <div class="w-12 h-12 rounded-lg bg-surface-container-highest flex items-center justify-center border border-primary/30">
                <span class="material-symbols-outlined text-primary">diversity_3</span>
              </div>
              <div class="flex-1 overflow-hidden">
                <div class="flex justify-between items-center">
                  <span class="font-body-lg truncate" :class="activeChat?.id === group.id ? 'text-primary' : 'text-on-surface'">{{ group.name }}</span>
                </div>
                <p class="text-body-md text-on-surface-variant truncate">{{ group.desc || '群聊' }}</p>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Chat Window -->
      <div class="flex-1 glass-panel rounded-xl flex flex-col border border-primary/20 relative overflow-hidden m-gutter mx-gutter">
        <!-- Empty State -->
        <div v-if="!activeChat" class="flex-1 flex items-center justify-center">
          <div class="text-center space-y-4">
            <span class="material-symbols-outlined text-6xl text-primary/30">chat</span>
            <p class="text-on-surface-variant">选择一个好友或群聊开始对话</p>
          </div>
        </div>

        <template v-else>
          <!-- Chat Header -->
          <div class="p-gutter flex items-center justify-between border-b border-primary/10">
            <div class="flex items-center gap-base">
              <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center border border-primary/30">
                <span class="material-symbols-outlined text-primary">{{ chatType === 'group' ? 'diversity_3' : 'person' }}</span>
              </div>
              <div>
                <h3 class="font-headline-sm text-headline-sm text-primary">{{ activeChat.name }}</h3>
                <div class="flex items-center gap-xs">
                  <span class="w-2 h-2 rounded-full bg-secondary-container"></span>
                  <span class="text-label-code text-on-surface-variant">{{ chatType === 'group' ? `${groupMembers.length} 位成员` : '在线' }}</span>
                </div>
              </div>
            </div>
            <div class="flex gap-gutter">
              <button v-if="chatType === 'group'" @click="showInvite = true" class="text-[12px] font-label-tech text-primary bg-primary/10 px-3 py-1 rounded hover:bg-primary/20 transition-colors">
                + 邀请成员
              </button>
              <span class="material-symbols-outlined text-on-surface-variant hover:text-primary cursor-pointer transition-colors">more_vert</span>
            </div>
          </div>

          <!-- Messages -->
          <div ref="msgContainer" class="flex-1 overflow-y-auto p-gutter custom-scrollbar flex flex-col gap-lg bg-[radial-gradient(circle_at_center,rgba(0,219,231,0.05)_0%,transparent_100%)]">
            <div v-for="msg in messages" :key="msg.id" class="flex items-start gap-base max-w-[80%]" :class="msg.sender_id === currentUserId ? 'self-end flex-row-reverse' : ''">
              <div class="w-10 h-10 rounded-lg bg-surface-variant flex items-center justify-center overflow-hidden shrink-0">
                <img v-if="msg.sender_avatar" :src="msg.sender_avatar" class="w-full h-full object-cover" />
                <span v-else class="material-symbols-outlined text-on-surface-variant">{{ msg.sender_type === 'staff' ? 'smart_toy' : 'person' }}</span>
              </div>
              <div class="flex flex-col" :class="msg.sender_id === currentUserId ? 'items-end' : ''">
                <div class="flex items-center gap-base mb-1" :class="msg.sender_id === currentUserId ? 'flex-row-reverse' : ''">
                  <span class="text-label-tech font-label-tech text-secondary">{{ msg.sender_name }}</span>
                  <span v-if="msg.tag" class="text-[10px] px-1.5 py-0.5 bg-primary/10 text-primary rounded">{{ msg.tag }}</span>
                  <span class="text-label-code text-on-surface-variant/50">{{ formatTime(msg.created_at) }}</span>
                </div>
                <div class="message-bubble p-3 border" :class="msg.sender_id === currentUserId ? 'bg-primary/20 border-primary/30 text-right' : 'glass-panel border-primary/40'">
                  <!-- 文件消息 -->
                  <template v-if="msg.msg_type === 'file'">
                    <template v-if="isImageFile(msg.content)">
                      <a :href="getFileUrl(msg.content)" target="_blank" rel="noopener noreferrer">
                        <img :src="getFileUrl(msg.content)" class="max-w-[240px] max-h-[200px] rounded-lg object-contain border border-primary/20 hover:opacity-90 transition-opacity" />
                      </a>
                    </template>
                    <template v-else>
                      <div class="flex items-start gap-3 p-3 rounded-lg bg-surface-container-lowest border border-primary/10 min-w-[180px]">
                        <span class="material-symbols-outlined text-4xl text-primary">description</span>
                        <div class="flex-1 min-w-0 text-left">
                          <p class="text-body-sm text-on-surface truncate" :title="parseFileData(msg.content)?.name">{{ parseFileData(msg.content)?.name }}</p>
                          <p class="text-[10px] text-on-surface-variant mt-1">{{ formatFileSize(parseFileData(msg.content)?.size || 0) }}</p>
                        </div>
                        <a :href="getFileUrl(msg.content)" :download="parseFileData(msg.content)?.name" target="_blank" rel="noopener noreferrer" class="shrink-0 p-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition-colors">
                          <span class="material-symbols-outlined text-[18px]">download</span>
                        </a>
                      </div>
                    </template>
                  </template>
                  <!-- 文本/emoji 消息 -->
                  <p v-else class="text-body-md leading-relaxed whitespace-pre-wrap">{{ msg.content }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Bar -->
          <div class="p-gutter border-t border-primary/10 glass-panel relative">
            <!-- @ Suggestions -->
            <div v-if="showAtSuggestions" class="absolute bottom-full left-4 right-4 mb-2 bg-surface-container-high border border-primary/20 rounded-xl shadow-lg max-h-48 overflow-y-auto z-20">
              <div v-for="staff in atableStaffs" :key="staff.staff_id" @click="insertAtStaff(staff)" class="flex items-center gap-3 p-3 hover:bg-primary/10 cursor-pointer transition-colors">
                <div class="w-8 h-8 rounded bg-surface-variant flex items-center justify-center">
                  <span class="material-symbols-outlined text-[18px] text-primary">smart_toy</span>
                </div>
                <div>
                  <p class="text-body-sm text-on-surface">{{ staff.name }}</p>
                  <p class="text-[10px] text-on-surface-variant">{{ staff.tag || '数字员工' }}</p>
                </div>
              </div>
            </div>

            <!-- 工具栏 -->
            <div class="flex items-center gap-2 mb-2">
              <!-- Emoji -->
              <div class="relative">
                <button @click="toggleEmojiPicker" class="p-2 rounded-lg hover:bg-primary/10 text-on-surface-variant hover:text-primary transition-colors">
                  <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">mood</span>
                </button>
                <div v-if="showEmojiPicker" class="absolute bottom-full left-0 mb-2 w-64 bg-surface-container-high border border-primary/20 rounded-xl shadow-lg p-3 z-30">
                  <div class="grid grid-cols-8 gap-1 max-h-48 overflow-y-auto custom-scrollbar">
                    <button v-for="emoji in emojis" :key="emoji" @click="insertEmoji(emoji)" class="text-xl hover:bg-primary/20 rounded p-1 transition-colors">
                      {{ emoji }}
                    </button>
                  </div>
                </div>
              </div>
              <!-- File -->
              <input ref="fileInputRef" type="file" class="hidden" @change="handleFileChange" />
              <button @click="fileInputRef?.click()" :disabled="uploadingFile" class="p-2 rounded-lg hover:bg-primary/10 text-on-surface-variant hover:text-primary transition-colors disabled:opacity-40">
                <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">attach_file</span>
              </button>
              <span v-if="uploadingFile" class="text-[12px] text-on-surface-variant">上传中...</span>
            </div>

            <div class="flex items-center gap-sm">
              <textarea ref="inputRef" v-model="messageText" @keydown.enter.prevent="sendMsg" @input="handleInput" class="flex-1 bg-surface-container-lowest border border-primary/20 rounded-xl py-3 px-4 text-body-md focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/40 resize-none transition-all custom-scrollbar" placeholder="发送消息... 输入 @ 可呼叫数字员工" rows="2"></textarea>
              <button @click="sendMsg" :disabled="!messageText.trim()" class="w-12 h-12 bg-primary-container text-on-primary-container rounded-xl flex items-center justify-center shadow-[0_0_20px_rgba(0,242,255,0.3)] hover:scale-105 active:scale-95 transition-all disabled:opacity-40 disabled:cursor-not-allowed">
                <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">send</span>
              </button>
            </div>
          </div>
        </template>
      </div>

      <!-- Right Sidebar -->
      <div v-if="chatType === 'group' && activeChat" class="w-64 flex flex-col gap-gutter shrink-0 m-gutter ml-0 hidden xl:flex">
        <div class="flex-1 glass-panel rounded-xl p-gutter border border-primary/10 flex flex-col overflow-hidden">
          <h4 class="font-label-tech text-label-tech text-secondary mb-gutter uppercase tracking-widest">群成员 ({{ groupMembers.length }})</h4>
          <div class="flex-1 overflow-y-auto custom-scrollbar flex flex-col gap-sm">
            <div v-for="member in groupMembers" :key="member.id" class="flex items-center gap-sm p-2 hover:bg-surface-variant/30 rounded-lg transition-all">
              <div class="w-8 h-8 rounded-md bg-surface-variant flex items-center justify-center">
                <span class="material-symbols-outlined text-[18px] text-primary">{{ member.type === 'staff' ? 'smart_toy' : 'person' }}</span>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-body-md text-on-surface truncate">{{ member.name }}</p>
                <p v-if="member.tag" class="text-[10px] text-primary">{{ member.tag }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Add Friend Modal -->
    <div v-if="showAddFriend" class="fixed inset-0 z-[60] bg-black/50 flex items-center justify-center" @click.self="showAddFriend = false">
      <div class="glass-panel rounded-xl p-8 border border-primary/20 w-96">
        <h3 class="font-headline-sm text-primary mb-4">添加好友</h3>
        <input v-model="friendUsername" class="w-full bg-surface-container-lowest border border-primary/20 rounded-lg py-2 px-4 text-body-md focus:outline-none focus:border-primary mb-4" placeholder="输入用户名" type="text" />
        <div class="flex gap-2">
          <button @click="showAddFriend = false" class="flex-1 py-2 bg-surface-variant text-on-surface rounded hover:bg-surface-variant/80 transition-colors">取消</button>
          <button @click="doAddFriend" class="flex-1 py-2 bg-primary-container text-on-primary-container rounded hover:bg-primary-container/80 transition-colors">添加</button>
        </div>
      </div>
    </div>

    <!-- Create Group Modal -->
    <div v-if="showCreateGroup" class="fixed inset-0 z-[60] bg-black/50 flex items-center justify-center" @click.self="showCreateGroup = false">
      <div class="glass-panel rounded-xl p-8 border border-primary/20 w-96">
        <h3 class="font-headline-sm text-primary mb-4">创建群聊</h3>
        <input v-model="newGroupName" class="w-full bg-surface-container-lowest border border-primary/20 rounded-lg py-2 px-4 text-body-md focus:outline-none focus:border-primary mb-4" placeholder="群名称" type="text" />
        <textarea v-model="newGroupDesc" class="w-full bg-surface-container-lowest border border-primary/20 rounded-lg py-2 px-4 text-body-md focus:outline-none focus:border-primary mb-4 resize-none" placeholder="群描述（可选）" rows="2"></textarea>
        <div class="flex gap-2">
          <button @click="showCreateGroup = false" class="flex-1 py-2 bg-surface-variant text-on-surface rounded hover:bg-surface-variant/80 transition-colors">取消</button>
          <button @click="doCreateGroup" class="flex-1 py-2 bg-primary-container text-on-primary-container rounded hover:bg-primary-container/80 transition-colors">创建</button>
        </div>
      </div>
    </div>

    <!-- Invite Member Modal -->
    <div v-if="showInvite" class="fixed inset-0 z-[60] bg-black/50 flex items-center justify-center" @click.self="showInvite = false">
      <div class="glass-panel rounded-xl p-8 border border-primary/20 w-[480px] max-h-[80vh] flex flex-col">
        <h3 class="font-headline-sm text-primary mb-4">邀请成员</h3>
        <!-- Tabs -->
        <div class="flex border-b border-primary/10 mb-4">
          <button class="flex-1 py-2 text-center text-body-sm font-label-tech transition-colors" :class="inviteTab === 'user' ? 'text-primary border-b-2 border-primary' : 'text-on-surface-variant'" @click="inviteTab = 'user'">用户</button>
          <button class="flex-1 py-2 text-center text-body-sm font-label-tech transition-colors" :class="inviteTab === 'staff' ? 'text-primary border-b-2 border-primary' : 'text-on-surface-variant'" @click="inviteTab = 'staff'">数字员工</button>
        </div>
        <!-- User List -->
        <div v-if="inviteTab === 'user'" class="flex-1 overflow-y-auto custom-scrollbar space-y-2">
          <div v-for="friend in friends.filter(f => !groupMembers.some(m => m.type === 'user' && m.user_id === f.friend_id))" :key="friend.friend_id" @click="doInvite('user', friend.friend_id)" class="flex items-center gap-3 p-3 hover:bg-primary/10 cursor-pointer rounded-lg transition-colors">
            <div class="w-10 h-10 rounded bg-surface-variant flex items-center justify-center"><span class="material-symbols-outlined text-primary">person</span></div>
            <span class="text-body-md text-on-surface">{{ friend.friend_name }}</span>
          </div>
        </div>
        <!-- Staff List -->
        <div v-else class="flex-1 overflow-y-auto custom-scrollbar space-y-2">
          <div v-for="staff in staffList" :key="staff.staff_id" @click="doInvite('staff', staff.staff_id)" class="flex items-center gap-3 p-3 hover:bg-primary/10 cursor-pointer rounded-lg transition-colors">
            <div class="w-10 h-10 rounded bg-surface-variant flex items-center justify-center"><span class="material-symbols-outlined text-primary">smart_toy</span></div>
            <div>
              <p class="text-body-md text-on-surface">{{ staff.name }}</p>
              <p class="text-[10px] text-on-surface-variant">{{ staff.tag || '数字员工' }}</p>
            </div>
          </div>
        </div>
        <button @click="showInvite = false" class="mt-4 w-full py-2 bg-surface-variant text-on-surface rounded hover:bg-surface-variant/80 transition-colors">关闭</button>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toast.visible" class="fixed top-20 left-1/2 -translate-x-1/2 z-[70] px-6 py-3 rounded-lg shadow-lg font-label-tech text-sm transition-all" :class="toast.type === 'success' ? 'bg-secondary-container text-on-secondary-container' : 'bg-error-container text-on-error-container'">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useAppStore } from '../stores/index.js'
import {
  addFriend, getFriendList, deleteFriend,
  createGroup, getGroupList, getGroupMembers, inviteMember,
  getPrivateHistory, getGroupHistory, sendMessage, uploadChatFile, getStaffList
} from '../api/chat.js'

// 常用 emoji 列表
const emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇',
  '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚',
  '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🥸',
  '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️',
  '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡',
  '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓',
  '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄',
  '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵',
  '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠',
  '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽',
  '👍', '👎', '👏', '🙌', '🤝', '🙏', '💪', '🤞', '🤟', '🤘',
  '✌️', '🤙', '👌', '🤌', '🤏', '☝️', '👆', '👇', '👈', '👉',
  '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💖',
  '🔥', '✨', '🎉', '🎊', '🎁', '💯', '💢', '💬', '💭', '🗯️']

const store = useAppStore()
const currentUserId = computed(() => Number(store.user?.id) || 0)

// Tabs & Lists
const listTab = ref('friends')
const friends = ref([])
const groups = ref([])
const searchQuery = ref('')

// Active Chat
const chatType = ref('')
const activeChat = ref(null)
const messages = ref([])
const groupMembers = ref([])

// Input
const messageText = ref('')
const inputRef = ref(null)
const showAtSuggestions = ref(false)
const atableStaffs = ref([])
const atStaffIds = ref('')
const showEmojiPicker = ref(false)
const fileInputRef = ref(null)
const uploadingFile = ref(false)

// Modals
const showAddFriend = ref(false)
const friendUsername = ref('')
const showCreateGroup = ref(false)
const newGroupName = ref('')
const newGroupDesc = ref('')
const showInvite = ref(false)
const inviteTab = ref('user')
const staffList = ref([])

// Toast
const toast = ref({ visible: false, message: '', type: 'success' })

// WebSocket
let ws = null

function showToast(message, type = 'success') {
  toast.value = { visible: true, message, type }
  setTimeout(() => { toast.value.visible = false }, 3000)
}

const filteredFriends = computed(() => {
  if (!searchQuery.value) return friends.value
  const q = searchQuery.value.toLowerCase()
  return friends.value.filter(f => f.friend_name.toLowerCase().includes(q))
})

const filteredGroups = computed(() => {
  if (!searchQuery.value) return groups.value
  const q = searchQuery.value.toLowerCase()
  return groups.value.filter(g => g.name.toLowerCase().includes(q))
})

function formatTime(t) {
  if (!t) return ''
  const d = new Date(t)
  return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

async function loadFriends() {
  const res = await getFriendList()
  console.log('[loadFriends] res:', res)
  if (res.code === 200) {
    friends.value = res.data || []
    console.log('[loadFriends] friends set:', friends.value)
  } else {
    console.warn('[loadFriends] failed:', res)
  }
}

async function loadGroups() {
  const res = await getGroupList()
  console.log('[loadGroups] res:', res)
  if (res.code === 200) {
    groups.value = res.data || []
    console.log('[loadGroups] groups set:', groups.value)
  } else {
    console.warn('[loadGroups] failed:', res)
  }
}

async function loadStaffs() {
  const res = await getStaffList()
  if (res.code === 200) staffList.value = res.data?.items || []
}

async function doAddFriend() {
  if (!friendUsername.value.trim()) return
  const res = await addFriend(friendUsername.value.trim())
  if (res.code === 200) {
    showToast('添加好友成功', 'success')
    showAddFriend.value = false
    friendUsername.value = ''
    await loadFriends()
    listTab.value = 'friends'
  } else {
    showToast(res.message || '添加失败', 'error')
  }
}

async function doCreateGroup() {
  if (!newGroupName.value.trim()) return
  const res = await createGroup({ name: newGroupName.value.trim(), desc: newGroupDesc.value.trim() })
  if (res.code === 200) {
    showToast('创建群聊成功', 'success')
    showCreateGroup.value = false
    newGroupName.value = ''
    newGroupDesc.value = ''
    await loadGroups()
    listTab.value = 'groups'
  } else {
    showToast(res.message || '创建失败', 'error')
  }
}

async function doInvite(memberType, memberId) {
  if (!activeChat.value) return
  const res = await inviteMember(activeChat.value.id, { member_type: memberType, member_id: memberId })
  if (res.code === 200) {
    showToast('邀请成功', 'success')
    await loadGroupMembers(activeChat.value.id)
  } else {
    showToast(res.message || '邀请失败', 'error')
  }
}

async function loadGroupMembers(groupId) {
  const res = await getGroupMembers(groupId)
  if (res.code === 200) groupMembers.value = res.data || []
}

async function selectChat(type, item) {
  chatType.value = type
  activeChat.value = item
  messages.value = []
  if (type === 'group') {
    await loadGroupMembers(item.id)
    const res = await getGroupHistory(item.id)
    if (res.code === 200) messages.value = res.data || []
  } else {
    const res = await getPrivateHistory(item.friend_id)
    if (res.code === 200) messages.value = res.data || []
  }
  scrollToBottom()
}

async function sendMsg() {
  const content = messageText.value.trim()
  if (!content || !activeChat.value) return

  // Extract @staff ids
  let atIds = ''
  if (chatType.value === 'group') {
    atIds = atStaffIds.value
  }

  const payload = {
    content,
    msg_type: 'text',
    at_staff_ids: atIds
  }
  if (chatType.value === 'private') {
    payload.receiver_id = activeChat.value.friend_id
  } else {
    payload.group_id = activeChat.value.id
  }

  // 优先使用 WebSocket 发送（避免重复消息）
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      action: chatType.value === 'private' ? 'send_private' : 'send_group',
      [chatType.value === 'private' ? 'receiver_id' : 'group_id']: chatType.value === 'private' ? activeChat.value.friend_id : activeChat.value.id,
      content,
      msg_type: 'text',
      at_staff_ids: atIds
    }))
    messageText.value = ''
    atStaffIds.value = ''
    showAtSuggestions.value = false
    scrollToBottom()
    return
  }

  // WebSocket 不可用，fallback 到 HTTP
  const res = await sendMessage(payload)
  if (res.code === 200) {
    messageText.value = ''
    atStaffIds.value = ''
    showAtSuggestions.value = false
    // Refresh messages
    if (chatType.value === 'group') {
      const r = await getGroupHistory(activeChat.value.id)
      if (r.code === 200) messages.value = r.data || []
    } else {
      const r = await getPrivateHistory(activeChat.value.friend_id)
      if (r.code === 200) messages.value = r.data || []
    }
    scrollToBottom()
  }
}

function handleInput() {
  const text = messageText.value
  const lastAt = text.lastIndexOf('@')
  if (lastAt !== -1 && chatType.value === 'group') {
    const afterAt = text.slice(lastAt + 1)
    if (!afterAt.includes(' ')) {
      showAtSuggestions.value = true
      // 显示所有数字员工；不在当前群的员工被 @ 时后端会自动邀请入群
      atableStaffs.value = staffList.value
      return
    }
  }
  showAtSuggestions.value = false
}

function insertAtStaff(staff) {
  const text = messageText.value
  const lastAt = text.lastIndexOf('@')
  messageText.value = text.slice(0, lastAt) + `@${staff.name} `
  const sid = String(staff.staff_id)
  if (!atStaffIds.value) {
    atStaffIds.value = sid
  } else if (!atStaffIds.value.split(',').includes(sid)) {
    atStaffIds.value += ',' + sid
  }
  showAtSuggestions.value = false
  inputRef.value?.focus()
}

function toggleEmojiPicker() {
  showEmojiPicker.value = !showEmojiPicker.value
}

function insertEmoji(emoji) {
  const textarea = inputRef.value
  if (!textarea) {
    messageText.value += emoji
    return
  }
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const text = messageText.value
  messageText.value = text.slice(0, start) + emoji + text.slice(end)
  showEmojiPicker.value = false
  nextTick(() => {
    textarea.focus()
    const pos = start + emoji.length
    textarea.setSelectionRange(pos, pos)
  })
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

function parseFileData(content) {
  try {
    if (typeof content === 'object') return content
    return JSON.parse(content)
  } catch (e) {
    return null
  }
}

function isImageFile(content) {
  const file = parseFileData(content)
  if (!file) return false
  return /\.(jpg|jpeg|png|gif|webp)$/i.test(file.ext || file.name || '')
}

function getFileUrl(content) {
  const file = parseFileData(content)
  if (!file || !file.url) return ''
  return file.url.startsWith('http') ? file.url : `http://localhost:8000${file.url}`
}

async function handleFileChange(e) {
  const file = e.target.files?.[0]
  if (!file || !activeChat.value) return

  uploadingFile.value = true
  try {
    const res = await uploadChatFile(file)
    if (res.code === 200) {
      await sendFileMessage(res.data)
    } else {
      showToast(res.message || '文件上传失败', 'error')
    }
  } catch (err) {
    console.error(err)
    showToast('文件上传失败', 'error')
  } finally {
    uploadingFile.value = false
    e.target.value = ''
  }
}

async function sendFileMessage(fileData) {
  const payload = {
    content: JSON.stringify(fileData),
    msg_type: 'file'
  }
  if (chatType.value === 'private') {
    payload.receiver_id = activeChat.value.friend_id
  } else {
    payload.group_id = activeChat.value.id
  }

  // 优先 WebSocket 实时发送
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      action: chatType.value === 'private' ? 'send_private' : 'send_group',
      [chatType.value === 'private' ? 'receiver_id' : 'group_id']: chatType.value === 'private' ? activeChat.value.friend_id : activeChat.value.id,
      content: payload.content,
      msg_type: 'file'
    }))
    scrollToBottom()
    return
  }

  // HTTP fallback
  const res = await sendMessage(payload)
  if (res.code === 200) {
    if (chatType.value === 'group') {
      const r = await getGroupHistory(activeChat.value.id)
      if (r.code === 200) messages.value = r.data || []
    } else {
      const r = await getPrivateHistory(activeChat.value.friend_id)
      if (r.code === 200) messages.value = r.data || []
    }
    scrollToBottom()
  }
}

function scrollToBottom() {
  nextTick(() => {
    const el = document.querySelector('.overflow-y-auto.custom-scrollbar.flex.flex-col.gap-lg')
    if (el) el.scrollTop = el.scrollHeight
  })
}

function connectWebSocket() {
  const token = localStorage.getItem('user_token')
  if (!token) return
  const wsUrl = `ws://localhost:8000/api/v1/chat/ws/chat?token=${token}`
  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('WebSocket connected')
  }

  ws.onmessage = (event) => {
    const payload = JSON.parse(event.data)
    if (payload.type === 'group_message' || payload.type === 'message') {
      const msg = payload.data
      if (chatType.value === 'group' && activeChat.value && msg.group_id === activeChat.value.id) {
        messages.value.push(msg)
        scrollToBottom()
      }
    } else if (payload.type === 'private_message') {
      const msg = payload.data
      if (chatType.value === 'private' && activeChat.value && (msg.sender_id === activeChat.value.friend_id || msg.receiver_id === activeChat.value.friend_id)) {
        messages.value.push(msg)
        scrollToBottom()
      }
    }
  }

  ws.onclose = () => {
    console.log('WebSocket disconnected, retrying...')
    setTimeout(connectWebSocket, 3000)
  }

  ws.onerror = (e) => {
    console.error('WebSocket error', e)
  }
}

onMounted(async () => {
  store.fetchUserInfo()
  await loadFriends()
  await loadGroups()
  await loadStaffs()
  connectWebSocket()
})
</script>
