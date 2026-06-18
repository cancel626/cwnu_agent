<template>
  <div class="h-full overflow-y-auto bg-surface">
    <div class="p-6">
      <!-- Header -->
      <div class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h2 class="font-headline-lg text-display-lg text-primary">模型管理</h2>
          <p class="font-body-lg text-on-surface-variant mt-2 border-l-4 border-primary pl-4">管理数字员工所使用的底层 AI 模型，支持 OpenAI 协议。</p>
        </div>
        <button @click="openAddModal" class="flex items-center gap-2 bg-primary text-on-primary px-6 py-2 btn-3d border-b-primary-container font-label-pixel">
          <span class="material-symbols-outlined text-[18px]">add</span>
          <span>添加模型</span>
        </button>
      </div>

      <!-- Model List -->
      <div class="space-y-4">
        <div
          v-for="model in modelList"
          :key="model.id"
          class="bg-surface-container border-2 border-outline-variant p-5 hover:border-primary transition-all"
          :class="{ 'border-secondary-fixed': model.is_default }"
        >
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-surface-variant flex items-center justify-center border-2" :class="model.is_default ? 'border-secondary-fixed' : 'border-outline-variant'">
                <span class="material-symbols-outlined text-primary text-[28px]">neurology</span>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h3 class="font-title-md text-title-md text-on-surface">{{ model.name }}</h3>
                  <span v-if="model.is_default" class="px-2 py-0.5 bg-secondary-fixed/20 text-secondary-fixed text-[10px] font-label-pixel border border-secondary-fixed">默认</span>
                  <span v-if="!model.is_active" class="px-2 py-0.5 bg-error/20 text-error text-[10px] font-label-pixel border border-error">已停用</span>
                </div>
                <p class="text-body-sm text-on-surface-variant mt-0.5">{{ model.provider }} | {{ model.model_name }} | {{ model.api_base }}</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button
                v-if="!model.is_default"
                @click="handleSetDefault(model)"
                class="px-3 py-1.5 border-2 border-secondary-fixed text-secondary-fixed hover:bg-secondary-fixed/10 font-label-pixel text-xs transition-all"
              >设为默认</button>
              <button @click="handleTest(model)" class="px-3 py-1.5 border-2 border-outline-variant text-outline hover:border-primary hover:text-primary font-label-pixel text-xs transition-all">测试</button>
              <button @click="openEditModal(model)" class="px-3 py-1.5 border-2 border-outline-variant text-outline hover:border-primary hover:text-primary font-label-pixel text-xs transition-all">编辑</button>
              <button @click="confirmDelete(model)" class="px-3 py-1.5 border-2 border-error text-error hover:bg-error/10 font-label-pixel text-xs transition-all">删除</button>
            </div>
          </div>
          <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="bg-surface-dim p-3 border border-outline-variant">
              <p class="text-[10px] text-on-surface-variant font-label-pixel mb-1">温度</p>
              <p class="text-lg font-display-lg text-primary">{{ model.temperature }}</p>
            </div>
            <div class="bg-surface-dim p-3 border border-outline-variant">
              <p class="text-[10px] text-on-surface-variant font-label-pixel mb-1">最大 Token</p>
              <p class="text-lg font-display-lg text-tertiary">{{ model.max_tokens }}</p>
            </div>
            <div class="bg-surface-dim p-3 border border-outline-variant">
              <p class="text-[10px] text-on-surface-variant font-label-pixel mb-1">超时</p>
              <p class="text-lg font-display-lg text-secondary-fixed">{{ model.timeout }}s</p>
            </div>
            <div class="bg-surface-dim p-3 border border-outline-variant">
              <p class="text-[10px] text-on-surface-variant font-label-pixel mb-1">API Key</p>
              <p class="text-sm font-label-pixel text-on-surface truncate">{{ model.api_key_masked || '****' }}</p>
            </div>
          </div>
          <p v-if="model.remark" class="mt-3 text-xs text-on-surface-variant font-body-sm">{{ model.remark }}</p>
        </div>

        <div v-if="modelList.length === 0" class="text-center py-16 text-on-surface-variant font-body-lg">
          暂无模型配置，点击右上角添加模型
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total > 0" class="bg-surface-container-high px-6 py-4 flex flex-col sm:flex-row items-center justify-between border-t-2 border-outline-variant gap-4 mt-6">
        <p class="font-label-pixel text-outline text-xs uppercase">显示第 {{ pagination.start }} 至 {{ pagination.end }} 条，共 {{ pagination.total }} 条记录</p>
        <div class="flex items-center gap-1">
          <button @click="prevPage" :disabled="query.page <= 1" class="w-10 h-10 flex items-center justify-center border-2 border-outline-variant hover:border-primary text-outline hover:text-primary transition-all disabled:opacity-30"><span class="material-symbols-outlined">chevron_left</span></button>
          <button v-for="p in visiblePages" :key="p" @click="goPage(p)" class="w-10 h-10 flex items-center justify-center border-2 font-label-pixel transition-all" :class="p === query.page ? 'border-primary bg-primary text-on-primary' : 'border-outline-variant hover:border-primary text-outline hover:text-primary'">{{ p }}</button>
          <button @click="nextPage" :disabled="query.page >= totalPages" class="w-10 h-10 flex items-center justify-center border-2 border-outline-variant hover:border-primary text-outline hover:text-primary transition-all disabled:opacity-30"><span class="material-symbols-outlined">chevron_right</span></button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="modalVisible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-surface-container border-2 border-outline-variant w-full max-w-xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between px-6 py-4 border-b-2 border-outline-variant bg-surface-container-high">
          <h3 class="font-headline-md text-primary">{{ isEditing ? '编辑模型' : '添加模型' }}</h3>
          <button @click="closeModal" class="text-outline hover:text-on-surface transition-colors"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">模型显示名称 *</label>
            <input v-model="form.name" type="text" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="如 GPT-4o" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-label-pixel text-xs uppercase text-outline mb-1">提供商</label>
              <select v-model="form.provider" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm">
                <option value="openai">OpenAI</option>
                <option value="azure">Azure OpenAI</option>
                <option value="local">本地 / 兼容</option>
              </select>
            </div>
            <div>
              <label class="block font-label-pixel text-xs uppercase text-outline mb-1">模型名称 *</label>
              <input v-model="form.model_name" type="text" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="如 gpt-4o" />
            </div>
          </div>
          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">API 基础地址 *</label>
            <input v-model="form.api_base" type="text" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="如 https://api.openai.com/v1" />
          </div>
          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">API 密钥 *</label>
            <input v-model="form.api_key" type="password" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="sk-..." />
            <p v-if="isEditing" class="text-[10px] text-outline mt-1">留空则保持原密钥不变</p>
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block font-label-pixel text-xs uppercase text-outline mb-1">温度</label>
              <input v-model.number="form.temperature" type="number" step="0.1" min="0" max="2" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" />
            </div>
            <div>
              <label class="block font-label-pixel text-xs uppercase text-outline mb-1">最大 Token</label>
              <input v-model.number="form.max_tokens" type="number" min="1" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" />
            </div>
            <div>
              <label class="block font-label-pixel text-xs uppercase text-outline mb-1">超时(秒)</label>
              <input v-model.number="form.timeout" type="number" min="1" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" />
            </div>
          </div>
          <div>
            <label class="block font-label-pixel text-xs uppercase text-outline mb-1">备注</label>
            <textarea v-model="form.remark" rows="2" class="w-full bg-surface border-2 border-outline-variant px-3 py-2 text-on-surface focus:border-primary focus:outline-none font-body-sm" placeholder="可选备注"></textarea>
          </div>
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <input id="m_active" v-model="form.is_active" type="checkbox" class="w-4 h-4 accent-primary" />
              <label for="m_active" class="font-label-pixel text-xs uppercase text-outline">启用</label>
            </div>
            <div class="flex items-center gap-2">
              <input id="m_default" v-model="form.is_default" type="checkbox" class="w-4 h-4 accent-primary" />
              <label for="m_default" class="font-label-pixel text-xs uppercase text-outline">设为默认</label>
            </div>
          </div>
        </div>
        <div class="flex justify-end gap-3 px-6 py-4 border-t-2 border-outline-variant bg-surface-container-high">
          <button @click="closeModal" class="px-4 py-2 border-2 border-outline-variant text-outline hover:border-primary hover:text-primary font-label-pixel transition-all">取消</button>
          <button @click="submitForm" class="px-6 py-2 bg-primary text-on-primary font-label-pixel btn-3d border-b-primary-container">{{ isEditing ? '保存' : '创建' }}</button>
        </div>
      </div>
    </div>

    <!-- Delete Confirm -->
    <div v-if="deleteVisible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" @click.self="deleteVisible = false">
      <div class="bg-surface-container border-2 border-error w-full max-w-sm mx-4">
        <div class="flex items-center gap-3 px-6 py-4 border-b-2 border-error/30 bg-error/10">
          <span class="material-symbols-outlined text-error">warning</span>
          <h3 class="font-headline-md text-error">确认删除</h3>
        </div>
        <div class="p-6">
          <p class="font-body-sm text-on-surface">确定要删除模型 <strong class="text-primary">{{ deleteTarget?.name }}</strong> 吗？</p>
        </div>
        <div class="flex justify-end gap-3 px-6 py-4 border-t-2 border-error/30 bg-error/5">
          <button @click="deleteVisible = false" class="px-4 py-2 border-2 border-outline-variant text-outline hover:border-primary hover:text-primary font-label-pixel transition-all">取消</button>
          <button @click="doDelete" class="px-6 py-2 bg-error text-on-primary font-label-pixel btn-3d border-b-error-container">删除</button>
        </div>
      </div>
    </div>

    <!-- Test Result Modal -->
    <div v-if="testVisible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" @click.self="testVisible = false">
      <div class="bg-surface-container border-2 border-outline-variant w-full max-w-lg mx-4 max-h-[80vh] overflow-y-auto">
        <div class="flex items-center justify-between px-6 py-4 border-b-2 border-outline-variant bg-surface-container-high">
          <h3 class="font-headline-md" :class="testResult?.status === 'ok' ? 'text-secondary-fixed' : 'text-error'">测试结果</h3>
          <button @click="testVisible = false" class="text-outline hover:text-on-surface transition-colors"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="p-6">
          <p class="font-label-pixel text-xs uppercase text-outline mb-2">模型</p>
          <p class="font-body-sm text-on-surface mb-4">{{ testTarget?.name }} ({{ testTarget?.model_name }})</p>
          <p class="font-label-pixel text-xs uppercase text-outline mb-2">状态</p>
          <p class="font-body-sm mb-4" :class="testResult?.status === 'ok' ? 'text-secondary-fixed' : 'text-error'">
            {{ testResult?.status === 'ok' ? '连通正常' : (testResult?.status === 'timeout' ? '连接超时' : '连接失败') }}
          </p>
          <div v-if="testResult?.http_code" class="mb-4">
            <p class="font-label-pixel text-xs uppercase text-outline mb-1">HTTP 状态码</p>
            <p class="font-body-sm text-error">{{ testResult.http_code }}</p>
          </div>
          <div v-if="testResult?.request_url" class="mb-4">
            <p class="font-label-pixel text-xs uppercase text-outline mb-1">请求地址</p>
            <p class="font-body-sm text-on-surface break-all">{{ testResult.request_url }}</p>
          </div>
          <div v-if="testResult?.request_model" class="mb-4">
            <p class="font-label-pixel text-xs uppercase text-outline mb-1">请求模型</p>
            <p class="font-body-sm text-on-surface">{{ testResult.request_model }}</p>
          </div>
          <div v-if="testResult?.response">
            <p class="font-label-pixel text-xs uppercase text-outline mb-2">回复内容</p>
            <div class="bg-surface-dim p-3 border border-outline-variant font-body-sm text-on-surface whitespace-pre-wrap">{{ testResult.response }}</div>
          </div>
          <div v-if="testResult?.detail && testResult.status !== 'ok'">
            <p class="font-label-pixel text-xs uppercase text-outline mb-2">错误详情</p>
            <div class="bg-error/10 p-3 border border-error/30 font-body-sm text-error whitespace-pre-wrap">{{ testResult.detail }}</div>
          </div>
        </div>
        <div class="flex justify-end gap-3 px-6 py-4 border-t-2 border-outline-variant bg-surface-container-high">
          <button @click="testVisible = false" class="px-4 py-2 border-2 border-outline-variant text-outline hover:border-primary hover:text-primary font-label-pixel transition-all">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getModelList, createModel, updateModel, deleteModel, setDefaultModel, testModel } from '../api/model.js'

const modelList = ref([])
const pagination = ref({ total: 0, start: 0, end: 0 })
const query = ref({ page: 1, limit: 10, keyword: '' })

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

async function loadData() {
  try {
    const res = await getModelList({
      skip: (query.value.page - 1) * query.value.limit,
      limit: query.value.limit,
      keyword: query.value.keyword
    })
    if (res.code === 200 && res.data) {
      modelList.value = res.data.items || []
      pagination.value.total = res.data.total || 0
      pagination.value.start = (query.value.page - 1) * query.value.limit + 1
      pagination.value.end = Math.min(query.value.page * query.value.limit, pagination.value.total)
    }
  } catch (e) {
    console.error('加载模型列表失败:', e)
  }
}

function prevPage() { if (query.value.page > 1) query.value.page-- }
function nextPage() { if (query.value.page < totalPages.value) query.value.page++ }
function goPage(p) { query.value.page = p }

onMounted(loadData)

/* Modal */
const modalVisible = ref(false)
const isEditing = ref(false)
const editingModel = ref(null)
const form = ref({
  name: '',
  provider: 'openai',
  api_base: '',
  api_key: '',
  model_name: '',
  is_default: false,
  is_active: true,
  temperature: 0.7,
  max_tokens: 2048,
  timeout: 30,
  remark: ''
})

function openAddModal() {
  isEditing.value = false
  editingModel.value = null
  form.value = {
    name: '', provider: 'openai', api_base: '', api_key: '', model_name: '',
    is_default: false, is_active: true, temperature: 0.7, max_tokens: 2048, timeout: 30, remark: ''
  }
  modalVisible.value = true
}

function openEditModal(model) {
  isEditing.value = true
  editingModel.value = model
  form.value = {
    name: model.name,
    provider: model.provider || 'openai',
    api_base: model.api_base,
    api_key: '',
    model_name: model.model_name,
    is_default: model.is_default,
    is_active: model.is_active,
    temperature: model.temperature ?? 0.7,
    max_tokens: model.max_tokens ?? 2048,
    timeout: model.timeout ?? 30,
    remark: model.remark || ''
  }
  modalVisible.value = true
}

function closeModal() {
  modalVisible.value = false
}

async function submitForm() {
  try {
    if (!form.value.name || !form.value.api_base || !form.value.model_name) {
      alert('请填写必填项')
      return
    }
    if (!isEditing.value && !form.value.api_key) {
      alert('新建模型时必须填写 API 密钥')
      return
    }

    const payload = {
      name: form.value.name,
      provider: form.value.provider,
      api_base: form.value.api_base,
      model_name: form.value.model_name,
      is_default: form.value.is_default,
      is_active: form.value.is_active,
      temperature: form.value.temperature,
      max_tokens: form.value.max_tokens,
      timeout: form.value.timeout,
      remark: form.value.remark || undefined
    }
    if (!isEditing.value || form.value.api_key) {
      payload.api_key = form.value.api_key
    }

    let res
    if (isEditing.value) {
      res = await updateModel(editingModel.value.id, payload)
    } else {
      res = await createModel(payload)
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

/* Set Default */
async function handleSetDefault(model) {
  try {
    const res = await setDefaultModel(model.id)
    if (res.code === 200) {
      await loadData()
    } else {
      alert(res.message || '设置失败')
    }
  } catch (e) {
    console.error('设置默认失败:', e)
    alert(e.response?.data?.detail || '请求失败')
  }
}

/* Delete */
const deleteVisible = ref(false)
const deleteTarget = ref(null)

function confirmDelete(model) {
  deleteTarget.value = model
  deleteVisible.value = true
}

async function doDelete() {
  if (!deleteTarget.value) return
  try {
    const res = await deleteModel(deleteTarget.value.id)
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

/* Test */
const testVisible = ref(false)
const testTarget = ref(null)
const testResult = ref(null)

async function handleTest(model) {
  testTarget.value = model
  testResult.value = null
  testVisible.value = true
  try {
    const res = await testModel(model.id, { message: 'Hello, are you working?' })
    if (res.code === 200 && res.data) {
      testResult.value = res.data
    } else {
      testResult.value = { status: 'error', detail: res.message }
    }
  } catch (e) {
    console.error('测试失败:', e)
    testResult.value = { status: 'error', detail: e.response?.data?.detail || e.message }
  }
}
</script>
