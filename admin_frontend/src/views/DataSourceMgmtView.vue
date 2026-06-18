<template>
  <div class="h-full overflow-y-auto bg-surface-dim">
    <div class="p-container-margin">
      <div class="flex justify-between items-end mb-8">
        <div>
          <h2 class="font-headline-lg text-primary mb-2">数据源管理 <span class="text-on-surface-variant font-light">/ CRAWL SOURCE MANAGEMENT</span></h2>
          <p class="text-body-sm text-on-surface-variant">配置和管理爬虫数据源，支持自定义爬取规则</p>
        </div>
        <button @click="openModal()" class="bg-secondary-fixed text-on-secondary-fixed font-label-pixel px-6 py-3 border-b-4 border-on-secondary-container active:border-b-0 active:translate-y-[4px] transition-all flex items-center gap-2">
          <span class="material-symbols-outlined text-[18px]">add_box</span>
          新增数据源
        </button>
      </div>

      <!-- Source List -->
      <div class="bg-surface-container border-2 border-outline-variant overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-surface-container-highest border-b-2 border-outline-variant">
                <th class="p-4 font-label-pixel text-outline text-[12px] uppercase">ID</th>
                <th class="p-4 font-label-pixel text-outline text-[12px] uppercase">名称</th>
                <th class="p-4 font-label-pixel text-outline text-[12px] uppercase">类型</th>
                <th class="p-4 font-label-pixel text-outline text-[12px] uppercase">基础 URL</th>
                <th class="p-4 font-label-pixel text-outline text-[12px] uppercase">占位符</th>
                <th class="p-4 font-label-pixel text-outline text-[12px] uppercase">深度</th>
                <th class="p-4 font-label-pixel text-outline text-[12px] uppercase">状态</th>
                <th class="p-4 font-label-pixel text-outline text-[12px] uppercase text-right">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-outline-variant">
              <tr v-for="s in sources" :key="s.id" class="hover:bg-primary/5 transition-colors">
                <td class="p-4 text-on-surface-variant text-sm">{{ s.id }}</td>
                <td class="p-4">
                  <p class="font-bold text-on-surface">{{ s.name }}</p>
                  <p class="text-[11px] text-outline">{{ s.description }}</p>
                </td>
                <td class="p-4">
                  <span class="px-2 py-1 text-[10px] font-label-pixel border" :class="s.source_type === 'preset' ? 'bg-primary/10 text-primary border-primary/30' : 'bg-tertiary/10 text-tertiary border-tertiary/30'">
                    {{ s.source_type === 'preset' ? '预设' : '自定义' }}
                  </span>
                </td>
                <td class="p-4 text-sm text-on-surface font-mono max-w-[300px] truncate">{{ s.base_url }}</td>
                <td class="p-4 text-sm text-on-surface font-mono">{{ s.keyword_placeholder }}</td>
                <td class="p-4 text-sm text-on-surface">{{ s.max_depth }}</td>
                <td class="p-4">
                  <span class="px-2 py-1 text-[10px] font-label-pixel border" :class="s.is_active ? 'bg-secondary-container/20 text-secondary-fixed border-secondary-fixed/30' : 'bg-error/10 text-error border-error/30'">
                    {{ s.is_active ? '启用' : '禁用' }}
                  </span>
                </td>
                <td class="p-4 text-right">
                  <div class="flex justify-end gap-2">
                    <button @click="openModal(s)" class="p-2 hover:bg-surface-variant text-on-surface-variant hover:text-primary"><span class="material-symbols-outlined text-[20px]">edit</span></button>
                    <button @click="deleteSource(s.id)" class="p-2 hover:bg-surface-variant text-on-surface-variant hover:text-error"><span class="material-symbols-outlined text-[20px]">delete</span></button>
                  </div>
                </td>
              </tr>
              <tr v-if="sources.length === 0">
                <td colspan="8" class="p-8 text-center text-on-surface-variant">暂无数据源，请点击右上角添加</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50" @click.self="showModal = false">
      <div class="bg-surface-container-low w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 border-2 border-outline-variant shadow-2xl">
        <div class="flex justify-between items-center mb-6 pb-4 border-b border-outline-variant">
          <h3 class="font-headline-lg text-primary">{{ editingId ? '编辑数据源' : '新增数据源' }}</h3>
          <button @click="showModal = false" class="p-2 hover:bg-surface-variant text-on-surface-variant"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">名称</label>
              <input v-model="form.name" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none" placeholder="新浪新闻" />
            </div>
            <div>
              <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">类型</label>
              <select v-model="form.source_type" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none">
                <option value="custom">自定义</option>
                <option value="preset">预设</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">基础 URL（使用 {keyword} 作为占位符）</label>
            <input v-model="form.base_url" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none font-mono text-sm" placeholder="https://search.sina.com.cn/?q={keyword}&c=news" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">关键词占位符</label>
              <input v-model="form.keyword_placeholder" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none font-mono" placeholder="{keyword}" />
            </div>
            <div>
              <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">爬取深度</label>
              <input v-model.number="form.max_depth" type="number" min="1" max="5" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none" />
            </div>
          </div>
          <div>
            <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">描述</label>
            <input v-model="form.description" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none" placeholder="数据源描述..." />
          </div>
          <div>
            <label class="block text-[12px] font-label-pixel text-on-surface-variant mb-1">自定义参数（JSON）</label>
            <textarea v-model="form.params" rows="3" class="w-full px-3 py-2 bg-surface-container border border-outline-variant text-on-surface focus:border-primary focus:outline-none font-mono text-sm" placeholder='{"headers": {"User-Agent": "..."}}'></textarea>
          </div>
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-[12px] font-label-pixel text-on-surface-variant">爬取规则</label>
              <button @click="addRule" class="text-primary text-[12px] font-label-pixel hover:underline">+ 添加规则</button>
            </div>
            <div v-for="(rule, idx) in form.rules" :key="idx" class="grid grid-cols-12 gap-2 mb-2 items-center">
              <select v-model="rule.type" class="col-span-2 px-2 py-2 bg-surface-container border border-outline-variant text-on-surface text-sm focus:border-primary focus:outline-none">
                <option value="css">CSS</option>
                <option value="xpath">XPath</option>
              </select>
              <input v-model="rule.selector" class="col-span-5 px-2 py-2 bg-surface-container border border-outline-variant text-on-surface text-sm focus:border-primary focus:outline-none font-mono" placeholder="h2.title 或 //div[@class='title']" />
              <input v-model="rule.field" class="col-span-3 px-2 py-2 bg-surface-container border border-outline-variant text-on-surface text-sm focus:border-primary focus:outline-none" placeholder="title / content / url" />
              <button @click="removeRule(idx)" class="col-span-2 p-2 hover:bg-error/10 text-error text-[12px]">删除</button>
            </div>
            <p v-if="form.rules.length === 0" class="text-[11px] text-outline">无自定义规则时将使用 crawl4ai 自动提取</p>
          </div>
          <div class="flex items-center gap-2">
            <input v-model="form.is_active" type="checkbox" id="is_active" class="w-4 h-4 accent-primary" />
            <label for="is_active" class="text-sm text-on-surface">启用该数据源</label>
          </div>
        </div>
        <div class="mt-6 pt-4 border-t border-outline-variant flex justify-end gap-3">
          <button @click="showModal = false" class="px-4 py-2 border border-outline-variant text-on-surface-variant font-label-pixel hover:bg-surface-variant">取消</button>
          <button @click="saveSource" class="px-6 py-2 bg-primary text-on-primary font-label-pixel hover:bg-primary/90">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getSourceList, createSource, updateSource, deleteSource as apiDeleteSource } from '@/api/crawler.js'

const sources = ref([])
const showModal = ref(false)
const editingId = ref(null)
const form = reactive({
  name: '',
  source_type: 'custom',
  base_url: '',
  keyword_placeholder: '{keyword}',
  description: '',
  params: '{}',
  rules: [],
  max_depth: 1,
  is_active: true
})

async function loadSources() {
  const res = await getSourceList()
  if (res.code === 200) {
    sources.value = res.data?.items || []
  }
}

function openModal(item = null) {
  if (item) {
    editingId.value = item.id
    form.name = item.name
    form.source_type = item.source_type
    form.base_url = item.base_url
    form.keyword_placeholder = item.keyword_placeholder
    form.description = item.description
    form.params = JSON.stringify(item.params || {}, null, 2)
    form.rules = Array.isArray(item.rules) ? [...item.rules] : []
    form.max_depth = item.max_depth
    form.is_active = item.is_active
  } else {
    editingId.value = null
    form.name = ''
    form.source_type = 'custom'
    form.base_url = ''
    form.keyword_placeholder = '{keyword}'
    form.description = ''
    form.params = '{}'
    form.rules = []
    form.max_depth = 1
    form.is_active = true
  }
  showModal.value = true
}

function addRule() {
  form.rules.push({ type: 'css', selector: '', field: 'title' })
}

function removeRule(idx) {
  form.rules.splice(idx, 1)
}

async function saveSource() {
  let params = {}
  try {
    params = JSON.parse(form.params || '{}')
  } catch {
    alert('自定义参数必须是有效的 JSON')
    return
  }
  const payload = {
    name: form.name,
    source_type: form.source_type,
    base_url: form.base_url,
    keyword_placeholder: form.keyword_placeholder,
    description: form.description,
    params,
    rules: form.rules,
    max_depth: form.max_depth,
    is_active: form.is_active
  }
  let res
  if (editingId.value) {
    res = await updateSource(editingId.value, payload)
  } else {
    res = await createSource(payload)
  }
  if (res.code === 200) {
    showModal.value = false
    await loadSources()
  } else {
    alert(res.message || '保存失败')
  }
}

async function deleteSource(id) {
  if (!confirm('确定删除该数据源吗？')) return
  const res = await apiDeleteSource(id)
  if (res.code === 200) {
    await loadSources()
  } else {
    alert(res.message || '删除失败')
  }
}

onMounted(loadSources)
</script>
