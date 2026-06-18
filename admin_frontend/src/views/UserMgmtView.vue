<template>
  <div class="h-full overflow-y-auto bg-surface">
    <div class="p-6">
      <!-- Header Section -->
      <div class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h2 class="font-headline-lg text-display-lg text-primary">用户管理</h2>
          <p class="font-body-lg text-on-surface-variant mt-2 border-l-4 border-primary pl-4">配置全系统角色并监控 WCNU 网络中的实时用户活动。</p>
        </div>
        <div class="flex gap-4">
          <button class="flex items-center gap-2 bg-surface-container border-2 border-outline-variant px-4 py-2 hover:border-primary hover:text-primary transition-all font-label-pixel active:translate-y-px">
            <span class="material-symbols-outlined text-[18px]">filter_list</span>
            <span>筛选</span>
          </button>
          <button @click="openAddModal" class="flex items-center gap-2 bg-primary text-on-primary px-6 py-2 btn-3d border-b-primary-container font-label-pixel">
            <span class="material-symbols-outlined text-[18px]">person_add</span>
            <span>添加用户</span>
          </button>
        </div>
      </div>
      <!-- Dashboard Stats Summary (Mini Bento) -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-surface-container border-2 border-outline-variant p-4 hover:border-primary transition-all group">
          <p class="font-label-pixel text-outline text-xs uppercase mb-1">当前活跃</p>
          <div class="flex items-end justify-between">
            <span class="font-display-lg text-[28px] text-primary">{{ formatNumber(stats.active) }}</span>
            <span class="material-symbols-outlined text-secondary-fixed-dim">trending_up</span>
          </div>
          <div class="w-full h-1 bg-outline-variant mt-3 overflow-hidden">
            <div class="h-full bg-primary transition-all duration-1000 group-hover:w-full" :style="{ width: activePercent + '%' }"></div>
          </div>
        </div>
        <div class="bg-surface-container border-2 border-outline-variant p-4 hover:border-secondary-fixed-dim transition-all group">
          <p class="font-label-pixel text-outline text-xs uppercase mb-1">普通用户</p>
          <div class="flex items-end justify-between">
            <span class="font-display-lg text-[28px] text-secondary-fixed-dim">{{ formatNumber(stats.normal) }}</span>
            <span class="material-symbols-outlined text-secondary-fixed-dim">person</span>
          </div>
          <div class="w-full h-1 bg-outline-variant mt-3">
            <div class="h-full bg-secondary-fixed-dim transition-all" :style="{ width: normalPercent + '%' }"></div>
          </div>
        </div>
        <div class="bg-surface-container border-2 border-outline-variant p-4 hover:border-tertiary transition-all group">
          <p class="font-label-pixel text-outline text-xs uppercase mb-1">管理员</p>
          <div class="flex items-end justify-between">
            <span class="font-display-lg text-[28px] text-tertiary">{{ formatNumber(stats.super) }}</span>
            <span class="material-symbols-outlined text-tertiary">verified_user</span>
          </div>
          <div class="w-full h-1 bg-outline-variant mt-3">
            <div class="h-full bg-tertiary transition-all" :style="{ width: superPercent + '%' }"></div>
          </div>
        </div>
        <div class="bg-surface-container border-2 border-outline-variant p-4 hover:border-error transition-all group">
          <p class="font-label-pixel text-outline text-xs uppercase mb-1">已禁用</p>
          <div class="flex items-end justify-between">
            <span class="font-display-lg text-[28px] text-error">{{ formatNumber(stats.inactive) }}</span>
            <span class="material-symbols-outlined text-error">cloud_off</span>
          </div>
          <div class="w-full h-1 bg-outline-variant mt-3">
            <div class="h-full bg-error transition-all" :style="{ width: inactivePercent + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="flex gap-2 mb-4">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="switchTab(tab.key)"
          class="px-4 py-2 font-label-pixel text-xs uppercase border-2 transition-all"
          :class="userType === tab.key
            ? 'border-primary bg-primary text-on-primary'
            : 'border-outline-variant text-outline hover:border-primary hover:text-primary'"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Table Section -->
      <div class="bg-surface-container-low border-2 border-outline-variant relative overflow-hidden">
        <div class="h-1 w-full bg-primary mb-0.5"></div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse font-body-sm">
            <thead class="bg-surface-container-high border-b-2 border-outline-variant">
              <tr>
                <th class="px-6 py-4 font-label-pixel text-primary uppercase tracking-tighter">头像</th>
                <th class="px-6 py-4 font-label-pixel text-primary uppercase tracking-tighter">用户名</th>
                <th class="px-6 py-4 font-label-pixel text-primary uppercase tracking-tighter">角色</th>
                <th class="px-6 py-4 font-label-pixel text-primary uppercase tracking-tighter">状态</th>
                <th class="px-6 py-4 font-label-pixel text-primary uppercase tracking-tighter text-right">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-outline-variant/30">
              <tr v-for="user in userList" :key="user.id + '-' + user.user_type" class="hover:bg-primary/5 transition-colors group" :class="{ 'bg-surface-container/30': user.id % 2 === 0 }">
                <td class="px-6 py-4">
                  <div class="w-10 h-10 border-2 overflow-hidden bg-surface-variant flex items-center justify-center p-0.5" :class="user.is_superuser ? 'border-primary' : 'border-outline-variant'">
                    <img v-if="user.avatar" alt="头像" class="w-full h-full object-cover" :src="user.avatar" />
                    <span v-else class="material-symbols-outlined text-on-surface-variant text-[20px]">person</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div class="flex flex-col">
                    <span class="font-title-md text-on-surface group-hover:text-primary transition-colors">{{ user.nickname || user.username }}</span>
                    <span class="text-xs text-outline font-label-pixel">{{ user.email || '暂无邮箱' }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span
                    class="font-label-pixel px-2 py-1 border"
                    :class="getRoleClass(user)"
                  >
                    {{ getRoleLabel(user) }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <span class="pixel-status" :class="user.is_online ? 'bg-secondary-fixed-dim animate-pulse' : 'bg-outline'"></span>
                    <span class="font-label-pixel uppercase text-[10px]" :class="user.is_online ? 'text-secondary-fixed-dim' : 'text-outline'">
                      {{ user.is_online ? '在线' : '离线' }}
                    </span>
                    <span
                      v-if="!user.is_active"
                      class="font-label-pixel uppercase text-[10px] px-2 py-0.5 border border-error bg-error/10 text-error"
                    >已封禁</span>
                    <span
                      v-else
                      class="font-label-pixel uppercase text-[10px] px-2 py-0.5 border border-secondary-fixed-dim bg-secondary-fixed-dim/10 text-secondary-fixed-dim"
                    >正常</span>
                  </div>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex justify-end gap-2">
                    <button
                      v-if="!user.is_active"
                      @click="confirmUnban(user)"
                      class="px-2 py-1 bg-secondary-fixed-dim text-on-primary text-[10px] font-label-pixel hover:bg-secondary-fixed-dim/90 transition-all flex items-center gap-1"
                    >
                      <span class="material-symbols-outlined text-[14px]">lock_open</span>
                      解封
                    </button>
                    <button @click="openEditModal(user)" class="p-1.5 hover:bg-surface-variant border border-transparent hover:border-outline-variant text-outline hover:text-on-surface transition-all"><span class="material-symbols-outlined text-sm">edit</span></button>
                    <button class="p-1.5 hover:bg-surface-variant border border-transparent hover:border-outline-variant text-outline hover:text-on-surface transition-all"><span class="material-symbols-outlined text-sm">visibility</span></button>
                    <button @click="confirmDelete(user)" class="p-1.5 hover:bg-error/20 border border-transparent hover:border-error text-error transition-all"><span class="material-symbols-outlined text-sm">delete</span></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Pagination -->
        <div class="bg-surface-container-high px-6 py-4 flex flex-col sm:flex-row items-center justify-between border-t-2 border-outline-variant gap-4">
          <p class="font-label-pixel text-outline text-xs uppercase">显示第 {{ pagination.start }} 至 {{ pagination.end }} 条，共 {{ formatNumber(pagination.total) }} 条记录</p>
          <div class="flex items-center gap-1">
            <button @click="prevPage" :disabled="query.page <= 1" class="w-10 h-10 flex items-center justify-center border-2 border-outline-variant hover:border-primary text-outline hover:text-primary transition-all active:translate-y-px disabled:opacity-30"><span class="material-symbols-outlined">chevron_left</span></button>
            <button v-for="p in visiblePages" :key="p" @click="goPage(p)" class="w-10 h-10 flex items-center justify-center border-2 font-label-pixel transition-all active:translate-y-px" :class="p === query.page ? 'border-primary bg-primary text-on-primary' : 'border-outline-variant hover:border-primary text-outline hover:text-primary'">
              {{ p }}
            </button>
            <button @click="nextPage" :disabled="query.page >= totalPages" class="w-10 h-10 flex items-center justify-center border-2 border-outline-variant hover:border-primary text-outline hover:text-primary transition-all active:translate-y-px disabled:opacity-30"><span class="material-symbols-outlined">chevron_right</span></button>
          </div>
        </div>
      </div>
      <!-- Footer Meta Info -->
      <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8 opacity-60">
        <div class="flex items-start gap-4">
          <div class="bg-primary/10 p-3 border-2 border-primary/20">
            <span class="material-symbols-outlined text-primary">security</span>
          </div>
          <div>
            <h4 class="font-label-pixel text-primary uppercase text-sm">安全策略</h4>
            <p class="text-xs font-body-sm text-on-surface-variant mt-1">所有用户修改均记录在全局审计日志中。未经授权的访问尝试将立即触发校园安保系统的警报。</p>
          </div>
        </div>
        <div class="flex items-start gap-4">
          <div class="bg-secondary-fixed-dim/10 p-3 border-2 border-secondary-fixed-dim/20">
            <span class="material-symbols-outlined text-secondary-fixed-dim">sync</span>
          </div>
          <div>
            <h4 class="font-label-pixel text-secondary-fixed-dim uppercase text-sm">数据同步</h4>
            <p class="text-xs font-body-sm text-on-surface-variant mt-1">已启用与 WCNU 统一身份认证系统的目录同步。上次同步时间为 4 分钟前。系统每 15 分钟自动更新一次。</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="modalVisible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-surface-container border-2 border-outline-variant w-full max-w-lg mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between px-6 py-4 border-b-2 border-outline-variant bg-surface-container-high">
          <h3 class="font-headline-md text-primary">{{ isEditing ? '编辑用户' : '添加用户' }}</h3>
          <button @click="closeModal" class="text-outline hover:text-on-surface transition-colors"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="p-6 space-y-4">
          <!-- 用户类型选择 -->
          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">用户类型</label>
            <div class="flex gap-2">
              <button
                type="button"
                @click="form.user_type = 'user'"
                class="flex-1 py-2 border-2 font-label-pixel text-xs uppercase transition-all"
                :class="form.user_type === 'user' ? 'border-primary bg-primary text-on-primary' : 'border-outline-variant text-outline hover:border-primary'"
              >普通用户</button>
              <button
                type="button"
                @click="form.user_type = 'admin'"
                class="flex-1 py-2 border-2 font-label-pixel text-xs uppercase transition-all"
                :class="form.user_type === 'admin' ? 'border-primary bg-primary text-on-primary' : 'border-outline-variant text-outline hover:border-primary'"
              >管理员</button>
            </div>
          </div>

          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">用户名 *</label>
            <input v-model="form.username" type="text" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="请输入用户名" />
          </div>

          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">昵称</label>
            <input v-model="form.nickname" type="text" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="请输入昵称" />
          </div>

          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">邮箱 *</label>
            <input v-model="form.email" type="email" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="请输入邮箱" />
          </div>

          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">手机号</label>
            <input v-model="form.phone" type="text" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="请输入手机号" />
          </div>

          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">头像 URL</label>
            <input v-model="form.avatar" type="text" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="请输入头像 URL" />
          </div>

          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">密码 {{ isEditing ? '(留空则不修改)' : '*' }}</label>
            <input v-model="form.password" type="password" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="请输入密码" />
          </div>

          <div class="flex items-center gap-3">
            <input id="is_active" v-model="form.is_active" type="checkbox" class="w-4 h-4 accent-primary" />
            <label for="is_active" class="font-label-pixel text-xs uppercase text-outline">启用账号</label>
          </div>
        </div>
        <div class="flex justify-end gap-3 px-6 py-4 border-t-2 border-outline-variant bg-surface-container-high">
          <button @click="closeModal" class="px-4 py-2 border-2 border-outline-variant text-outline hover:border-primary hover:text-primary font-label-pixel transition-all">取消</button>
          <button @click="submitForm" class="px-6 py-2 bg-primary text-on-primary font-label-pixel btn-3d border-b-primary-container">{{ isEditing ? '保存' : '创建' }}</button>
        </div>
      </div>
    </div>

    <!-- Delete Confirm Modal -->
    <div v-if="deleteVisible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" @click.self="deleteVisible = false">
      <div class="bg-surface-container border-2 border-error w-full max-w-sm mx-4">
        <div class="flex items-center gap-3 px-6 py-4 border-b-2 border-error/30 bg-error/10">
          <span class="material-symbols-outlined text-error">warning</span>
          <h3 class="font-headline-md text-error">确认删除</h3>
        </div>
        <div class="p-6">
          <p class="font-body-sm text-on-surface">确定要删除用户 <strong class="text-primary">{{ deleteTarget?.nickname || deleteTarget?.username }}</strong> 吗？此操作不可撤销。</p>
        </div>
        <div class="flex justify-end gap-3 px-6 py-4 border-t-2 border-error/30 bg-error/5">
          <button @click="deleteVisible = false" class="px-4 py-2 border-2 border-outline-variant text-outline hover:border-primary hover:text-primary font-label-pixel transition-all">取消</button>
          <button @click="doDelete" class="px-6 py-2 bg-error text-on-primary font-label-pixel btn-3d border-b-error-container">删除</button>
        </div>
      </div>
    </div>

    <!-- Unban Confirm Modal -->
    <div v-if="unbanVisible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" @click.self="unbanVisible = false">
      <div class="bg-surface-container border-2 border-secondary-fixed-dim w-full max-w-sm mx-4">
        <div class="flex items-center gap-3 px-6 py-4 border-b-2 border-secondary-fixed-dim/30 bg-secondary-fixed-dim/10">
          <span class="material-symbols-outlined text-secondary-fixed-dim">lock_open</span>
          <h3 class="font-headline-md text-secondary-fixed-dim">确认解封</h3>
        </div>
        <div class="p-6">
          <p class="font-body-sm text-on-surface">确定要解封用户 <strong class="text-primary">{{ unbanTarget?.nickname || unbanTarget?.username }}</strong> 吗？解封后该用户可以正常登录。</p>
        </div>
        <div class="flex justify-end gap-3 px-6 py-4 border-t-2 border-secondary-fixed-dim/30 bg-secondary-fixed-dim/5">
          <button @click="unbanVisible = false" class="px-4 py-2 border-2 border-outline-variant text-outline hover:border-primary hover:text-primary font-label-pixel transition-all">取消</button>
          <button @click="doUnban" class="px-6 py-2 bg-secondary-fixed-dim text-on-primary font-label-pixel btn-3d border-b-secondary-fixed-dim">解封</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getAdminList, createAdmin, updateAdmin, deleteAdmin } from '../api/admin.js'
import { getUserList, createUser, updateUser, deleteUser } from '../api/user.js'

const userType = ref('all')
const tabs = [
  { key: 'all', label: '全部用户' },
  { key: 'admin', label: '管理员' },
  { key: 'user', label: '普通用户' }
]

const userList = ref([])
const allItems = ref([])
const pagination = ref({ total: 0, start: 0, end: 0 })
const query = ref({ page: 1, limit: 10, keyword: '' })
const stats = ref({ active: 0, normal: 0, super: 0, inactive: 0 })

const totalPages = computed(() => Math.ceil(pagination.value.total / query.value.limit) || 1)

const visiblePages = computed(() => {
  const total = totalPages.value
  const current = query.value.page
  const pages = []
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 4)
  if (end - start < 4) start = Math.max(1, end - 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const activePercent = computed(() => {
  const t = pagination.value.total || 1
  return Math.round((stats.value.active / t) * 100)
})
const normalPercent = computed(() => {
  const t = pagination.value.total || 1
  return Math.round((stats.value.normal / t) * 100)
})
const superPercent = computed(() => {
  const t = pagination.value.total || 1
  return Math.round((stats.value.super / t) * 100)
})
const inactivePercent = computed(() => {
  const t = pagination.value.total || 1
  return Math.round((stats.value.inactive / t) * 100)
})

function formatNumber(n) {
  if (!n && n !== 0) return '0'
  return n.toLocaleString()
}

function getRoleLabel(user) {
  if (user.user_type === 'user') return '普通用户'
  if (user.is_superuser) return '超级管理员'
  return '管理员'
}

function getRoleClass(user) {
  if (user.user_type === 'user') return 'text-secondary-fixed-dim bg-secondary-fixed-dim/10 border-secondary-fixed-dim'
  if (user.is_superuser) return 'text-tertiary bg-tertiary/10 border-tertiary'
  return 'text-primary bg-primary/10 border-primary'
}

function computeStats(items) {
  stats.value.active = items.filter(u => u.is_online).length
  stats.value.inactive = items.filter(u => !u.is_active).length
  stats.value.super = items.filter(u => u.user_type === 'admin' && u.is_superuser).length
  stats.value.normal = items.filter(u => u.user_type === 'user').length
}

async function loadData() {
  try {
    if (userType.value === 'all') {
      const [adminRes, userRes] = await Promise.all([
        getAdminList({ skip: 0, limit: 200, keyword: query.value.keyword }),
        getUserList({ skip: 0, limit: 200, keyword: query.value.keyword })
      ])

      let merged = []
      if (adminRes.code === 200 && adminRes.data) {
        merged = merged.concat((adminRes.data.items || []).map(u => ({ ...u, user_type: 'admin' })))
      }
      if (userRes.code === 200 && userRes.data) {
        merged = merged.concat((userRes.data.items || []).map(u => ({ ...u, user_type: 'user' })))
      }

      merged.sort((a, b) => b.id - a.id)
      allItems.value = merged

      const total = merged.length
      const start = (query.value.page - 1) * query.value.limit
      const end = start + query.value.limit
      userList.value = merged.slice(start, end)
      pagination.value.total = total
      pagination.value.start = total > 0 ? start + 1 : 0
      pagination.value.end = Math.min(end, total)

      computeStats(merged)
    } else if (userType.value === 'admin') {
      const res = await getAdminList({
        skip: (query.value.page - 1) * query.value.limit,
        limit: query.value.limit,
        keyword: query.value.keyword
      })
      if (res.code === 200 && res.data) {
        const items = (res.data.items || []).map(u => ({ ...u, user_type: 'admin' }))
        userList.value = items
        pagination.value.total = res.data.total || 0
        pagination.value.start = (query.value.page - 1) * query.value.limit + 1
        pagination.value.end = Math.min(query.value.page * query.value.limit, pagination.value.total)
        computeStats(items)
      }
    } else if (userType.value === 'user') {
      const res = await getUserList({
        skip: (query.value.page - 1) * query.value.limit,
        limit: query.value.limit,
        keyword: query.value.keyword
      })
      if (res.code === 200 && res.data) {
        const items = (res.data.items || []).map(u => ({ ...u, user_type: 'user' }))
        userList.value = items
        pagination.value.total = res.data.total || 0
        pagination.value.start = (query.value.page - 1) * query.value.limit + 1
        pagination.value.end = Math.min(query.value.page * query.value.limit, pagination.value.total)
        computeStats(items)
      }
    }
  } catch (e) {
    console.error('加载用户列表失败:', e)
  }
}

function switchTab(type) {
  userType.value = type
  query.value.page = 1
  loadData()
}

function prevPage() {
  if (query.value.page > 1) {
    query.value.page--
  }
}
function nextPage() {
  if (query.value.page < totalPages.value) {
    query.value.page++
  }
}
function goPage(p) {
  query.value.page = p
}

watch(() => query.value.page, () => {
  if (userType.value === 'all') {
    const total = allItems.value.length
    const start = (query.value.page - 1) * query.value.limit
    const end = start + query.value.limit
    userList.value = allItems.value.slice(start, end)
    pagination.value.start = total > 0 ? start + 1 : 0
    pagination.value.end = Math.min(end, total)
  } else {
    loadData()
  }
})

onMounted(loadData)

/* Modal */
const modalVisible = ref(false)
const isEditing = ref(false)
const editingUser = ref(null)
const form = ref({
  user_type: 'user',
  username: '',
  nickname: '',
  email: '',
  phone: '',
  avatar: '',
  password: '',
  is_active: true
})

function openAddModal() {
  isEditing.value = false
  editingUser.value = null
  form.value = {
    user_type: userType.value === 'admin' ? 'admin' : 'user',
    username: '',
    nickname: '',
    email: '',
    phone: '',
    avatar: '',
    password: '',
    is_active: true
  }
  modalVisible.value = true
}

function openEditModal(user) {
  isEditing.value = true
  editingUser.value = user
  form.value = {
    user_type: user.user_type,
    username: user.username,
    nickname: user.nickname || '',
    email: user.email || '',
    phone: user.phone || '',
    avatar: user.avatar || '',
    password: '',
    is_active: user.is_active !== false
  }
  modalVisible.value = true
}

function closeModal() {
  modalVisible.value = false
}

async function submitForm() {
  try {
    if (!form.value.username || !form.value.email) {
      alert('请填写必填项')
      return
    }
    if (!isEditing.value && !form.value.password) {
      alert('新建用户时必须设置密码')
      return
    }

    const payload = {
      username: form.value.username,
      nickname: form.value.nickname || undefined,
      email: form.value.email,
      phone: form.value.phone || undefined
    }

    if (!isEditing.value || form.value.password) {
      payload.password = form.value.password
    }

    let res
    if (isEditing.value) {
      payload.is_active = form.value.is_active
      if (form.value.avatar) payload.avatar = form.value.avatar
      if (form.value.user_type === 'admin') {
        res = await updateAdmin(editingUser.value.id, payload)
      } else {
        res = await updateUser(editingUser.value.id, payload)
      }
    } else {
      if (form.value.user_type === 'admin') {
        res = await createAdmin(payload)
      } else {
        res = await createUser(payload)
      }
    }

    if (res.code === 200) {
      closeModal()
      await loadData()
    } else {
      alert(res.message || '操作失败')
    }
  } catch (e) {
    console.error('提交失败:', e)
    alert(e.response?.data?.detail || '请求失败')
  }
}

/* Delete */
const deleteVisible = ref(false)
const deleteTarget = ref(null)

function confirmDelete(user) {
  deleteTarget.value = user
  deleteVisible.value = true
}

async function doDelete() {
  if (!deleteTarget.value) return
  try {
    let res
    if (deleteTarget.value.user_type === 'admin') {
      res = await deleteAdmin(deleteTarget.value.id)
    } else {
      res = await deleteUser(deleteTarget.value.id)
    }
    if (res.code === 200) {
      deleteVisible.value = false
      deleteTarget.value = null
      await loadData()
    } else {
      alert(res.message || '删除失败')
    }
  } catch (e) {
    console.error('删除失败:', e)
    alert(e.response?.data?.detail || '删除失败')
  }
}

/* Unban */
const unbanVisible = ref(false)
const unbanTarget = ref(null)

function confirmUnban(user) {
  unbanTarget.value = user
  unbanVisible.value = true
}

async function doUnban() {
  if (!unbanTarget.value) return
  try {
    let res
    const payload = { is_active: true }
    if (unbanTarget.value.user_type === 'admin') {
      res = await updateAdmin(unbanTarget.value.id, payload)
    } else {
      res = await updateUser(unbanTarget.value.id, payload)
    }
    if (res.code === 200) {
      unbanVisible.value = false
      unbanTarget.value = null
      await loadData()
    } else {
      alert(res.message || '解封失败')
    }
  } catch (e) {
    console.error('解封失败:', e)
    alert(e.response?.data?.detail || '解封失败')
  }
}
</script>
