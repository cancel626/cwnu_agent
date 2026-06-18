<template>
  <div class="h-full overflow-y-auto p-container-margin">
    <div class="flex justify-between items-end mb-8">
      <div>
        <h2 class="font-display-lg text-display-lg text-on-surface mb-2">技能管理</h2>
        <div class="flex space-x-4">
          <div class="flex items-center space-x-2 bg-surface-container px-3 py-1 border-l-4 border-secondary-fixed">
            <span class="material-symbols-outlined text-secondary-fixed text-[18px]">psychology</span>
            <span class="font-label-pixel text-label-pixel">技能总数: {{ total }}</span>
          </div>
        </div>
      </div>
      <div class="flex gap-3">
        <button @click="openAI" class="bg-tertiary-container hover:bg-tertiary-fixed text-on-tertiary-container font-headline-lg text-headline-lg px-6 py-3 pixel-btn-shadow flex items-center group transition-all">
          <span class="material-symbols-outlined mr-2 group-hover:rotate-12 transition-transform">auto_fix</span>
          AI创建技能
        </button>
        <button @click="openCreate" class="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-headline-lg text-headline-lg px-6 py-3 pixel-btn-shadow flex items-center group transition-all">
          <span class="material-symbols-outlined mr-2 group-hover:rotate-90 transition-transform">add_box</span>
          添加技能
        </button>
      </div>
    </div>

    <div class="flex gap-4 mb-6">
      <div class="flex-1 flex gap-2">
        <input v-model="search" @keyup.enter="fetchList" class="flex-1 bg-surface-dim border-2 border-outline-variant px-4 py-2 focus:border-primary outline-none font-body-sm" placeholder="搜索技能名称或描述..." />
        <button @click="fetchList" class="bg-primary text-on-primary px-4 py-2 font-label-pixel">搜索</button>
      </div>
      <select v-model="filterType" @change="fetchList" class="bg-surface-dim border-2 border-outline-variant px-4 py-2 font-body-sm">
        <option value="">全部类型</option>
        <option value="functioncall">Function Call</option>
        <option value="mcp">MCP</option>
        <option value="skill">Skill</option>
      </select>
      <label class="flex items-center gap-2 bg-surface-dim border-2 border-outline-variant px-4 py-2 cursor-pointer select-none">
        <input type="checkbox" v-model="showAll" @change="toggleShowAll" />
        <span class="font-body-sm text-on-surface">显示全部</span>
      </label>
    </div>

    <div class="overflow-x-auto bg-surface-container border-2 border-outline-variant">
      <table class="w-full text-left">
        <thead>
          <tr class="bg-surface-dim border-b-2 border-outline-variant">
            <th class="px-6 py-3 font-label-pixel text-label-pixel">名称</th>
            <th class="px-6 py-3 font-label-pixel text-label-pixel">类型</th>
            <th class="px-6 py-3 font-label-pixel text-label-pixel">描述</th>
            <th class="px-6 py-3 font-label-pixel text-label-pixel">状态</th>
            <th class="px-6 py-3 font-label-pixel text-label-pixel text-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in list" :key="item.id" class="border-b border-outline-variant hover:bg-surface-container-high transition-colors">
            <td class="px-6 py-4 font-body text-body text-on-surface">{{ item.name }}</td>
            <td class="px-6 py-4">
              <span class="font-label-pixel text-label-pixel border px-2 py-0.5"
                :class="item.type === 'functioncall' ? 'bg-primary-container text-on-primary-container' : item.type === 'mcp' ? 'bg-tertiary-container text-on-tertiary-container' : 'bg-secondary-container text-on-secondary-container'">
                {{ typeLabel(item.type) }}
              </span>
            </td>
            <td class="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant max-w-xs truncate">{{ item.description || '-' }}</td>
            <td class="px-6 py-4">
              <span class="font-label-pixel text-label-pixel" :class="item.is_active ? 'text-secondary-fixed' : 'text-outline'">
                {{ item.is_active ? '启用' : '禁用' }}
              </span>
            </td>
            <td class="px-6 py-4 text-right">
              <button @click="openEdit(item)" class="text-primary hover:text-primary-fixed font-label-pixel mr-3">编辑</button>
              <button @click="handleDelete(item)" class="text-error hover:text-error-container font-label-pixel">删除</button>
            </td>
          </tr>
          <tr v-if="!list.length">
            <td colspan="5" class="px-6 py-8 text-center text-on-surface-variant font-body">暂无技能数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-center gap-2 mt-6" v-if="!showAll && totalPages > 1">
      <button v-for="p in totalPages" :key="p" @click="page = p; fetchList()" :class="page === p ? 'bg-primary text-on-primary' : 'bg-surface-container text-on-surface'" class="px-3 py-1 font-label-pixel border border-outline-variant">{{ p }}</button>
    </div>

    <!-- Create/Edit Modal -->
    <Teleport to="body">
      <div v-if="visible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-surface-container-low border-2 border-outline-variant w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 relative">
          <button @click="visible = false" class="absolute top-4 right-4 text-on-surface-variant hover:text-error"><span class="material-symbols-outlined">close</span></button>
          <h3 class="font-headline-lg text-headline-lg text-on-surface mb-6">{{ isEdit ? '编辑技能' : '添加技能' }}</h3>

          <div class="space-y-4">
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">技能名称</label>
              <input v-model="form.name" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" />
            </div>

            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">技能类型</label>
              <select v-model="form.type" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 font-body-sm" :disabled="isEdit">
                <option value="functioncall">Function Call (Python沙箱)</option>
                <option value="mcp">MCP 服务调用</option>
                <option value="skill">Skill (skill.md)</option>
              </select>
            </div>

            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">描述</label>
              <textarea v-model="form.description" rows="2" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm"></textarea>
            </div>

            <!-- Dynamic fields based on type -->
            <template v-if="form.type === 'functioncall'">
              <div>
                <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">函数名</label>
                <input v-model="config.function_name" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="例如: calculate" />
              </div>
              <div>
                <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">参数定义 (JSON)</label>
                <textarea v-model="paramsJson" rows="3" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm font-mono text-xs" placeholder='[{"name":"a","type":"int","desc":"第一个数"}]'></textarea>
              </div>
              <div>
                <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">超时时间 (秒)</label>
                <input v-model.number="config.timeout" type="number" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" />
              </div>
              <div>
                <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">Python 代码</label>
                <textarea v-model="form.content" rows="8" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm font-mono text-xs" placeholder="def calculate(a, b):\n    return a + b"></textarea>
              </div>
            </template>

            <template v-if="form.type === 'mcp'">
              <div>
                <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">MCP 服务地址</label>
                <input v-model="config.server_url" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="例如: http://localhost:8000/sse" />
              </div>
              <div>
                <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">工具名</label>
                <input v-model="config.tool_name" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="例如: search" />
              </div>
            </template>

            <template v-if="form.type === 'skill'">
              <div>
                <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">分类</label>
                <input v-model="config.category" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="例如: 数据处理" />
              </div>
              <div>
                <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">skill.md 内容</label>
                <textarea v-model="form.content" rows="10" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm font-mono text-xs" placeholder="# 技能名称\n\n## 描述\n...\n\n## 用法\n..."></textarea>
              </div>
            </template>

            <div class="flex items-center gap-2">
              <input type="checkbox" v-model="form.is_active" id="is_active" />
              <label for="is_active" class="font-body-sm text-on-surface-variant">启用</label>
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button @click="visible = false" class="bg-surface-container hover:bg-surface-container-high text-on-surface px-4 py-2 font-label-pixel">取消</button>
            <button @click="submit" class="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container px-4 py-2 font-label-pixel">{{ isEdit ? '保存' : '创建' }}</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- AI Generate Modal -->
    <Teleport to="body">
      <div v-if="aiVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-surface-container-low border-2 border-outline-variant w-full max-w-lg p-6 relative">
          <button @click="aiVisible = false" class="absolute top-4 right-4 text-on-surface-variant hover:text-error"><span class="material-symbols-outlined">close</span></button>
          <h3 class="font-headline-lg text-headline-lg text-on-surface mb-6">AI 创建技能</h3>
          <div class="space-y-4">
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">技能类型</label>
              <select v-model="aiForm.skill_type" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 font-body-sm">
                <option value="functioncall">Function Call</option>
                <option value="mcp">MCP</option>
                <option value="skill">Skill</option>
              </select>
            </div>
            <div>
              <label class="block font-label-pixel text-label-pixel text-on-surface-variant mb-1">用自然语言描述你想要的功能</label>
              <textarea v-model="aiForm.description" rows="5" class="w-full bg-surface-dim border-2 border-outline-variant px-3 py-2 focus:border-primary outline-none font-body-sm" placeholder="例如: 我需要写一个Python函数，可以计算两个数的和"></textarea>
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="aiVisible = false" class="bg-surface-container hover:bg-surface-container-high text-on-surface px-4 py-2 font-label-pixel">取消</button>
            <button @click="aiGenerate" :disabled="aiLoading" class="bg-tertiary-container hover:bg-tertiary-fixed text-on-tertiary-container px-4 py-2 font-label-pixel flex items-center gap-2">
              <span v-if="aiLoading" class="material-symbols-outlined animate-spin">refresh</span>
              <span v-else class="material-symbols-outlined">auto_fix</span>
              {{ aiLoading ? '生成中...' : '生成' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { getSkillList, createSkill, updateSkill, deleteSkill, aiGenerateSkill } from '../api/skill'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const search = ref('')
const filterType = ref('')
const showAll = ref(false)
const visible = ref(false)
const isEdit = ref(false)
const aiVisible = ref(false)
const aiLoading = ref(false)

const form = reactive({
  id: null,
  name: '',
  type: 'functioncall',
  description: '',
  config: {},
  content: '',
  is_active: true
})

const config = reactive({
  function_name: '',
  timeout: 30,
  server_url: '',
  tool_name: '',
  category: ''
})

const paramsJson = ref('')

const aiForm = reactive({
  skill_type: 'functioncall',
  description: ''
})

const totalPages = computed(() => Math.ceil(total.value / pageSize))

function typeLabel(type) {
  const map = { functioncall: 'Function Call', mcp: 'MCP', skill: 'Skill' }
  return map[type] || type
}

function resetForm() {
  form.id = null
  form.name = ''
  form.type = 'functioncall'
  form.description = ''
  form.config = {}
  form.content = ''
  form.is_active = true
  config.function_name = ''
  config.timeout = 30
  config.server_url = ''
  config.tool_name = ''
  config.category = ''
  paramsJson.value = ''
}

function openCreate() {
  resetForm()
  isEdit.value = false
  visible.value = true
}

function openEdit(item) {
  isEdit.value = true
  Object.assign(form, item)
  const cfg = item.config || {}
  Object.assign(config, cfg)
  if (item.type === 'functioncall' && cfg.params) {
    paramsJson.value = JSON.stringify(cfg.params, null, 2)
  } else {
    paramsJson.value = ''
  }
  visible.value = true
}

function openAI() {
  aiForm.skill_type = 'functioncall'
  aiForm.description = ''
  aiVisible.value = true
}

async function aiGenerate() {
  if (!aiForm.description.trim()) return alert('请输入描述')
  aiLoading.value = true
  try {
    const res = await aiGenerateSkill(aiForm)
    if (res.code === 200 && res.data) {
      aiVisible.value = false
      resetForm()
      form.type = aiForm.skill_type
      form.name = res.data.name || ''
      form.description = res.data.description || ''
      form.content = res.data.content || ''
      if (res.data.config) {
        Object.assign(config, res.data.config)
        if (aiForm.skill_type === 'functioncall' && res.data.config.params) {
          paramsJson.value = JSON.stringify(res.data.config.params, null, 2)
        }
      }
      isEdit.value = false
      visible.value = true
    } else {
      alert(res.message || '生成失败')
    }
  } catch (e) {
    let msg = e.message || '未知错误'
    if (typeof msg === 'object') {
      try { msg = JSON.stringify(msg) } catch (_) { msg = String(msg) }
    }
    alert('生成失败: ' + msg)
  } finally {
    aiLoading.value = false
  }
}

function buildConfig() {
  const cfg = {}
  if (form.type === 'functioncall') {
    cfg.function_name = config.function_name
    cfg.timeout = config.timeout
    try {
      cfg.params = paramsJson.value ? JSON.parse(paramsJson.value) : []
    } catch {
      cfg.params = []
    }
  } else if (form.type === 'mcp') {
    cfg.server_url = config.server_url
    cfg.tool_name = config.tool_name
  } else if (form.type === 'skill') {
    cfg.category = config.category
  }
  return cfg
}

async function submit() {
  if (!form.name.trim()) return alert('请输入技能名称')
  const payload = {
    name: form.name,
    type: form.type,
    description: form.description,
    config: buildConfig(),
    content: form.content,
    is_active: form.is_active
  }
  try {
    if (isEdit.value) {
      await updateSkill(form.id, payload)
    } else {
      await createSkill(payload)
    }
    visible.value = false
    fetchList()
  } catch (e) {
    alert('保存失败: ' + (e.message || '未知错误'))
  }
}

async function handleDelete(item) {
  if (!confirm(`确定删除技能「${item.name}」吗？`)) return
  try {
    await deleteSkill(item.id)
    fetchList()
  } catch (e) {
    alert('删除失败')
  }
}

function toggleShowAll() {
  page.value = 1
  fetchList()
}

async function fetchList() {
  try {
    const res = await getSkillList({
      skip: showAll.value ? 0 : (page.value - 1) * pageSize,
      limit: showAll.value ? 10000 : pageSize,
      keyword: search.value,
      skill_type: filterType.value
    })
    if (res.code === 200 && res.data) {
      list.value = res.data.items || []
      total.value = res.data.total || 0
    }
  } catch (e) {
    console.error(e)
    if (e.code === 401) {
      alert('请先登录管理员账号')
    }
  }
}

fetchList()
</script>
