<template>
  <div class="h-full overflow-y-auto p-container-margin">
    <!-- Dashboard Header -->
    <div class="flex justify-between items-end mb-8">
      <div>
        <h2 class="font-display-lg text-display-lg text-on-surface mb-2">数智员工管理</h2>
        <div class="flex space-x-4">
          <div class="flex items-center space-x-2 bg-surface-container px-3 py-1 border-l-4 border-secondary-fixed">
            <span class="material-symbols-outlined text-secondary-fixed text-[18px]">group</span>
            <span class="font-label-pixel text-label-pixel">活跃员工: {{ staffStats.active || 0 }}</span>
          </div>
          <div class="flex items-center space-x-2 bg-surface-container px-3 py-1 border-l-4 border-tertiary">
            <span class="material-symbols-outlined text-tertiary text-[18px]">memory</span>
            <span class="font-label-pixel text-label-pixel">总算力消耗: 84%</span>
          </div>
        </div>
      </div>
      <button @click="openCreateModal" class="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-headline-lg text-headline-lg px-8 py-3 pixel-btn-shadow flex items-center group transition-all" style="--tw-shadow-color: #006a5a">
        <span class="material-symbols-outlined mr-2 group-hover:rotate-90 transition-transform">add_box</span>
        雇佣新员工
      </button>
    </div>

    <!-- Search & Filter -->
    <div class="flex gap-4 mb-6">
      <div class="flex-1 flex gap-2">
        <input
          v-model="searchKeyword"
          @keyup.enter="handleSearch"
          class="flex-1 bg-surface-dim border-2 border-outline-variant px-4 py-2 focus:border-primary outline-none transition-colors font-body-sm"
          placeholder="搜索员工名称、角色或标签..."
        />
        <button
          @click="handleSearch"
          class="bg-primary text-on-primary px-4 py-2 font-label-pixel flex items-center gap-2"
        >
          <span class="material-symbols-outlined text-sm">search</span>
          搜索
        </button>
      </div>
      <select
        v-model="filterStatus"
        @change="handleStatusChange"
        class="bg-surface-dim border-2 border-outline-variant px-4 py-2 focus:border-primary outline-none font-body-sm"
      >
        <option value="">全部状态</option>
        <option value="活跃">活跃</option>
        <option value="处理中">处理中</option>
        <option value="待命中">待命中</option>
      </select>
    </div>

    <!-- Bento Grid for AI Agents -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-gutter">
      <div
        v-for="staff in staffList"
        :key="staff.id"
        class="bg-surface-container-low border-2 border-outline-variant hover:border-primary transition-all p-card-padding relative group overflow-hidden"
      >
        <div :class="`absolute top-0 left-0 w-full h-1 ${getTagColorClass(staff.tag)}`"></div>
        <div class="flex justify-between items-start mb-6">
          <div class="w-16 h-16 bg-surface-container-high border-2 p-1" :class="`border-${getTagColorName(staff.tag)}`">
            <img
              v-if="staff.avatar"
              :src="staff.avatar"
              :alt="staff.name"
              class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all"
            />
            <div v-else class="w-full h-full flex items-center justify-center bg-surface-container">
              <span class="material-symbols-outlined text-3xl text-on-surface-variant">smart_toy</span>
            </div>
          </div>
          <div class="text-right">
            <span :class="`font-label-pixel text-label-pixel border px-2 py-0.5 ${getModelBadgeClass(staff.tag)}`">
              {{ staff.model_type || '未知模型' }}
            </span>
            <div class="flex items-center justify-end mt-2 text-on-surface-variant">
              <span
                :class="`w-2 h-2 rounded-full mr-2 ${staff.status === '处理中' || staff.status === '活跃' ? 'bg-secondary-fixed animate-pulse' : 'bg-on-surface-variant'}`"
              ></span>
              <span class="font-label-pixel text-[10px]">{{ staff.status }}</span>
            </div>
          </div>
        </div>
        <h3 class="font-title-md text-title-md text-on-surface mb-1">{{ staff.name }}</h3>
        <p class="text-on-surface-variant font-body-sm text-body-sm mb-4">{{ staff.desc }}</p>
        <div class="mb-6">
          <p class="font-label-pixel text-[10px] text-on-surface-variant mb-2 uppercase tracking-widest">核心技能</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="skill in parseSkills(staff.skills)"
              :key="skill"
              class="bg-surface-container px-2 py-1 font-label-pixel text-[10px] border border-outline-variant"
            >
              {{ skill }}
            </span>
          </div>
        </div>
        <div class="bg-surface-container-lowest border-2 border-outline-variant p-3 relative pixel-tail">
          <p class="font-label-pixel text-[10px] text-primary mb-1">当前任务：</p>
          <p class="font-body-sm text-body-sm italic">"{{ staff.current_task || '暂无任务' }}"</p>
        </div>
        <div class="mt-6 flex justify-between items-center opacity-0 group-hover:opacity-100 transition-opacity">
          <div class="flex gap-3">
            <button @click="openEditModal(staff)" class="text-primary font-label-pixel text-label-pixel hover:underline decoration-2 underline-offset-4">编辑</button>
            <button class="text-primary font-label-pixel text-label-pixel hover:underline decoration-2 underline-offset-4">查看日志</button>
          </div>
          <button class="bg-surface-variant text-on-surface font-label-pixel text-[10px] px-3 py-1 border border-outline hover:bg-error/20 hover:text-error transition-colors">终止任务</button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="pagination.total > 0" class="mt-8 flex justify-center items-center gap-2">
      <button
        @click="changePage(pagination.page - 1)"
        :disabled="pagination.page <= 1"
        class="px-3 py-1 border-2 border-outline-variant font-label-pixel text-xs hover:border-primary disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        上一页
      </button>
      <span class="font-label-pixel text-xs text-on-surface-variant">
        第 {{ pagination.page }} / {{ pagination.total_pages }} 页 (共 {{ pagination.total }} 条)
      </span>
      <button
        @click="changePage(pagination.page + 1)"
        :disabled="pagination.page >= pagination.total_pages"
        class="px-3 py-1 border-2 border-outline-variant font-label-pixel text-xs hover:border-primary disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        下一页
      </button>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && staffList.length === 0" class="flex flex-col items-center justify-center py-20 text-on-surface-variant">
      <span class="material-symbols-outlined text-6xl mb-4">smart_toy</span>
      <p class="font-label-pixel text-label-pixel">暂无数字员工数据</p>
    </div>

    <!-- Create Staff Modal -->
    <Teleport to="body">
      <div v-if="createVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-surface-container-low border-2 border-outline-variant w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 relative">
          <button @click="createVisible = false" class="absolute top-4 right-4 text-on-surface-variant hover:text-error"><span class="material-symbols-outlined">close</span></button>
          <h3 class="font-headline-lg text-headline-lg text-on-surface mb-6">雇佣新员工</h3>
          <div class="space-y-4">
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">员工名称</label>
              <input v-model="createForm.name" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" />
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">选择模型</label>
              <select v-model="createForm.model_config_id" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 font-body-sm">
                <option :value="null">-- 请选择模型 --</option>
                <option v-for="m in modelList" :key="m.id" :value="m.id">{{ m.name }} ({{ m.model_name }})</option>
              </select>
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">角色 / 职责</label>
              <input v-model="createForm.role" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" />
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">标签</label>
              <input v-model="createForm.tag" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="例如: 核心智脑" />
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">描述</label>
              <textarea v-model="createForm.desc" rows="2" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm"></textarea>
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">选择技能</label>
              <div class="flex flex-wrap gap-2 bg-surface-dim border-2 border-outline-variant p-3 min-h-[48px]">
                <label v-for="s in skillList" :key="s.id" class="flex items-center gap-1 cursor-pointer select-none">
                  <input type="checkbox" :value="s.name" v-model="selectedSkillNames" />
                  <span class="font-body-sm text-on-surface">{{ s.name }}</span>
                </label>
                <span v-if="!skillList.length" class="text-on-surface-variant font-body-sm">暂无可用技能</span>
              </div>
            </div>
            <div>
              <div class="flex justify-between items-center mb-1">
                <label class="font-label-pixel text-label-pixel text-on-surface-variant">系统提示词</label>
                <button @click="aiGenPrompt" :disabled="genPromptLoading" class="text-tertiary font-label-pixel text-[10px] flex items-center gap-1 hover:underline">
                  <span v-if="genPromptLoading" class="material-symbols-outlined animate-spin text-[14px]">refresh</span>
                  <span v-else class="material-symbols-outlined text-[14px]">auto_fix</span>
                  {{ genPromptLoading ? '生成中...' : 'AI生成' }}
                </button>
              </div>
              <textarea v-model="createForm.system_prompt" rows="5" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="根据所选技能自动生成，或手动填写..."></textarea>
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">头像 URL</label>
              <input v-model="createForm.avatar" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="可选" />
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="createVisible = false" class="bg-surface-container hover:bg-surface-container-high text-on-surface px-4 py-2 font-label-pixel">取消</button>
            <button @click="submitCreate" class="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container px-4 py-2 font-label-pixel">创建</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Edit Staff Modal -->
    <Teleport to="body">
      <div v-if="editVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-surface-container-low border-2 border-outline-variant w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 relative">
          <button @click="editVisible = false" class="absolute top-4 right-4 text-on-surface-variant hover:text-error"><span class="material-symbols-outlined">close</span></button>
          <h3 class="font-headline-lg text-headline-lg text-on-surface mb-6">编辑员工</h3>
          <div class="space-y-4">
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">员工名称</label>
              <input v-model="editForm.name" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" />
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">选择模型</label>
              <select v-model="editForm.model_config_id" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 font-body-sm">
                <option :value="null">-- 请选择模型 --</option>
                <option v-for="m in modelList" :key="m.id" :value="m.id">{{ m.name }} ({{ m.model_name }})</option>
              </select>
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">角色 / 职责</label>
              <input v-model="editForm.role" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" />
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">标签</label>
              <input v-model="editForm.tag" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="例如: 核心智脑" />
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">描述</label>
              <textarea v-model="editForm.desc" rows="2" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm"></textarea>
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">选择技能</label>
              <div class="flex flex-wrap gap-2 bg-surface-dim border-2 border-outline-variant p-3 min-h-[48px]">
                <label v-for="s in skillList" :key="s.id" class="flex items-center gap-1 cursor-pointer select-none">
                  <input type="checkbox" :value="s.name" v-model="editSelectedSkillNames" />
                  <span class="font-body-sm text-on-surface">{{ s.name }}</span>
                </label>
                <span v-if="!skillList.length" class="text-on-surface-variant font-body-sm">暂无可用技能</span>
              </div>
            </div>
            <div>
              <div class="flex justify-between items-center mb-1">
                <label class="font-label-pixel text-label-pixel text-on-surface-variant">系统提示词</label>
                <button @click="aiGenPromptEdit" :disabled="genPromptLoading" class="text-tertiary font-label-pixel text-[10px] flex items-center gap-1 hover:underline">
                  <span v-if="genPromptLoading" class="material-symbols-outlined animate-spin text-[14px]">refresh</span>
                  <span v-else class="material-symbols-outlined text-[14px]">auto_fix</span>
                  {{ genPromptLoading ? '生成中...' : 'AI生成' }}
                </button>
              </div>
              <textarea v-model="editForm.system_prompt" rows="5" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="根据所选技能自动生成，或手动填写..."></textarea>
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">头像 URL</label>
              <input v-model="editForm.avatar" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="可选" />
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="editVisible = false" class="bg-surface-container hover:bg-surface-container-high text-on-surface px-4 py-2 font-label-pixel">取消</button>
            <button @click="submitEdit" class="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container px-4 py-2 font-label-pixel">保存</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getStaffList, getStaffStats, createStaff, updateStaff } from '../api/staff.js'
import { getModelList } from '../api/model.js'
import { getSkillList, generateSystemPrompt } from '../api/skill.js'

const staffList = ref([])
const staffStats = ref({ total: 0, active: 0, busy: 0 })
const loading = ref(false)
const searchKeyword = ref('')
const filterStatus = ref('')

const pagination = ref({
  page: 1,
  page_size: 6,
  total: 0,
  total_pages: 0
})

// Create modal
const createVisible = ref(false)
const createForm = reactive({
  name: '',
  model_config_id: null,
  role: '',
  tag: '',
  desc: '',
  system_prompt: '',
  avatar: ''
})
const modelList = ref([])
const skillList = ref([])
const selectedSkillNames = ref([])
const genPromptLoading = ref(false)

// Edit modal
const editVisible = ref(false)
const editForm = reactive({
  id: null,
  name: '',
  model_config_id: null,
  role: '',
  tag: '',
  desc: '',
  system_prompt: '',
  avatar: ''
})
const editSelectedSkillNames = ref([])

function resetCreateForm() {
  createForm.name = ''
  createForm.model_config_id = null
  createForm.role = ''
  createForm.tag = ''
  createForm.desc = ''
  createForm.system_prompt = ''
  createForm.avatar = ''
  selectedSkillNames.value = []
}

async function openCreateModal() {
  resetCreateForm()
  await Promise.all([loadModels(), loadSkills()])
  createVisible.value = true
}

async function loadModels() {
  try {
    const res = await getModelList({ skip: 0, limit: 100 })
    if (res.code === 200 && res.data) {
      modelList.value = res.data.items || []
    }
  } catch (e) {
    console.error(e)
  }
}

async function loadSkills() {
  try {
    const res = await getSkillList({ skip: 0, limit: 100, keyword: '' })
    if (res.code === 200 && res.data) {
      skillList.value = (res.data.items || []).filter(s => s.is_active)
    }
  } catch (e) {
    console.error(e)
  }
}

async function aiGenPrompt() {
  if (!selectedSkillNames.value.length) {
    alert('请至少选择一个技能')
    return
  }
  genPromptLoading.value = true
  try {
    const skillIds = skillList.value
      .filter(s => selectedSkillNames.value.includes(s.name))
      .map(s => s.id)
    const res = await generateSystemPrompt({
      skill_ids: skillIds,
      extra_desc: createForm.desc
    })
    if (res.code === 200 && res.data) {
      createForm.system_prompt = res.data.system_prompt || ''
    } else {
      alert(res.message || '生成失败')
    }
  } catch (e) {
    alert('生成失败: ' + (e.message || '未知错误'))
  } finally {
    genPromptLoading.value = false
  }
}

async function submitCreate() {
  if (!createForm.name.trim()) return alert('请输入员工名称')
  const payload = {
    name: createForm.name,
    model_type: createForm.model_config_id ? (modelList.value.find(m => m.id === createForm.model_config_id)?.model_name || '') : '',
    model_config_id: createForm.model_config_id,
    role: createForm.role,
    tag: createForm.tag,
    desc: createForm.desc,
    skills: selectedSkillNames.value.join(','),
    system_prompt: createForm.system_prompt,
    avatar: createForm.avatar,
    status: '待命中',
    is_active: true
  }
  try {
    await createStaff(payload)
    createVisible.value = false
    loadStaffList()
    loadStaffStats()
  } catch (e) {
    alert('创建失败: ' + (e.message || '未知错误'))
  }
}

async function openEditModal(staff) {
  editForm.id = staff.id
  editForm.name = staff.name || ''
  editForm.model_config_id = staff.model_config_id || null
  editForm.role = staff.role || ''
  editForm.tag = staff.tag || ''
  editForm.desc = staff.desc || ''
  editForm.system_prompt = staff.system_prompt || ''
  editForm.avatar = staff.avatar || ''
  editSelectedSkillNames.value = parseSkills(staff.skills)
  await Promise.all([loadModels(), loadSkills()])
  editVisible.value = true
}

async function aiGenPromptEdit() {
  if (!editSelectedSkillNames.value.length) {
    alert('请至少选择一个技能')
    return
  }
  genPromptLoading.value = true
  try {
    const skillIds = skillList.value
      .filter(s => editSelectedSkillNames.value.includes(s.name))
      .map(s => s.id)
    const res = await generateSystemPrompt({
      skill_ids: skillIds,
      extra_desc: editForm.desc
    })
    if (res.code === 200 && res.data) {
      editForm.system_prompt = res.data.system_prompt || ''
    } else {
      alert(res.message || '生成失败')
    }
  } catch (e) {
    alert('生成失败: ' + (e.message || '未知错误'))
  } finally {
    genPromptLoading.value = false
  }
}

async function submitEdit() {
  if (!editForm.name.trim()) return alert('请输入员工名称')
  const payload = {
    name: editForm.name,
    model_type: editForm.model_config_id ? (modelList.value.find(m => m.id === editForm.model_config_id)?.model_name || '') : '',
    model_config_id: editForm.model_config_id,
    role: editForm.role,
    tag: editForm.tag,
    desc: editForm.desc,
    skills: editSelectedSkillNames.value.join(','),
    system_prompt: editForm.system_prompt,
    avatar: editForm.avatar
  }
  try {
    await updateStaff(editForm.id, payload)
    editVisible.value = false
    loadStaffList()
    loadStaffStats()
  } catch (e) {
    alert('保存失败: ' + (e.message || '未知错误'))
  }
}

function parseSkills(skillsStr) {
  if (!skillsStr) return []
  return skillsStr.split(',').map(s => s.trim()).filter(Boolean)
}

function getTagColorClass(tag) {
  const map = {
    '核心智脑': 'bg-secondary-fixed',
    '管理枢纽': 'bg-tertiary',
    '底层架构': 'bg-primary',
    '知识中心': 'bg-tertiary-container',
    '后勤支撑': 'bg-outline',
    '社区互动': 'bg-secondary-container'
  }
  return map[tag] || 'bg-outline'
}

function getTagColorName(tag) {
  const map = {
    '核心智脑': 'secondary-fixed',
    '管理枢纽': 'tertiary',
    '底层架构': 'primary',
    '知识中心': 'tertiary-container',
    '后勤支撑': 'outline-variant',
    '社区互动': 'secondary-container'
  }
  return map[tag] || 'outline-variant'
}

function getModelBadgeClass(tag) {
  const map = {
    '核心智脑': 'text-secondary-fixed border-secondary-fixed',
    '管理枢纽': 'text-tertiary border-tertiary',
    '底层架构': 'text-primary border-primary',
    '知识中心': 'text-tertiary-container border-tertiary-container',
    '后勤支撑': 'text-on-surface-variant border-outline-variant',
    '社区互动': 'text-secondary-container border-secondary-container'
  }
  return map[tag] || 'text-on-surface-variant border-outline-variant'
}

async function loadStaffList() {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size
    }
    if (searchKeyword.value) params.keyword = searchKeyword.value
    if (filterStatus.value) params.status = filterStatus.value

    const res = await getStaffList(params)
    if (res.code === 200 && res.data) {
      staffList.value = res.data.items || []
      pagination.value.total = res.data.total || 0
      pagination.value.total_pages = res.data.total_pages || 0
    }
  } catch (e) {
    console.error('获取员工列表失败:', e)
  } finally {
    loading.value = false
  }
}

async function loadStaffStats() {
  try {
    const res = await getStaffStats()
    if (res.code === 200 && res.data) {
      staffStats.value = res.data
    }
  } catch (e) {
    console.error('获取员工统计失败:', e)
  }
}

function changePage(page) {
  if (page < 1 || page > pagination.value.total_pages) return
  pagination.value.page = page
  loadStaffList()
}

function handleSearch() {
  pagination.value.page = 1
  loadStaffList()
}

function handleStatusChange() {
  pagination.value.page = 1
  loadStaffList()
}

onMounted(() => {
  loadStaffList()
  loadStaffStats()
})
</script>
