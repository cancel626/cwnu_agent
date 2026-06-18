<template>
  <main class="flex-1 p-3 grid grid-cols-12 grid-rows-[auto_1fr] gap-3 relative z-10 overflow-hidden bg-surface-dim">
    <!-- Header / Top Stats -->
    <section class="col-span-12 grid grid-cols-4 gap-3">
      <div class="bg-surface-container-low/80 backdrop-blur-md border-l-4 border-primary p-4 pixel-corners flex justify-between items-center glow-border">
        <div>
          <p class="text-on-surface-variant font-label-pixel text-xs">数据仓库总量</p>
          <h3 class="text-3xl font-display-lg text-primary mt-1">{{ stats.total_saved.toLocaleString() }}</h3>
        </div>
        <div class="text-primary flex flex-col items-end">
          <span class="material-symbols-outlined text-4xl" style="font-variation-settings: 'FILL' 1;">database</span>
          <span class="text-[10px] font-label-pixel">已保存</span>
        </div>
      </div>
      <div class="bg-surface-container-low/80 backdrop-blur-md border-l-4 border-secondary-fixed-dim p-4 pixel-corners flex justify-between items-center glow-border">
        <div>
          <p class="text-on-surface-variant font-label-pixel text-xs">今日新增</p>
          <h3 class="text-3xl font-display-lg text-secondary-fixed-dim mt-1">{{ stats.today_saved.toLocaleString() }}</h3>
        </div>
        <div class="text-secondary-fixed-dim flex flex-col items-end">
          <span class="material-symbols-outlined text-4xl" style="font-variation-settings: 'FILL' 1;">today</span>
          <span class="text-[10px] font-label-pixel">实时入库</span>
        </div>
      </div>
      <div class="bg-surface-container-low/80 backdrop-blur-md border-l-4 border-tertiary p-4 pixel-corners flex justify-between items-center glow-border">
        <div>
          <p class="text-on-surface-variant font-label-pixel text-xs">数据源</p>
          <h3 class="text-3xl font-display-lg text-tertiary mt-1">{{ stats.total_sources.toLocaleString() }}</h3>
        </div>
        <div class="text-tertiary flex flex-col items-end">
          <span class="material-symbols-outlined text-4xl" style="font-variation-settings: 'FILL' 1;">hub</span>
          <span class="text-[10px] font-label-pixel">接入中</span>
        </div>
      </div>
      <div class="bg-surface-container-low/80 backdrop-blur-md border-l-4 border-error p-4 pixel-corners flex justify-between items-center glow-border">
        <div>
          <p class="text-on-surface-variant font-label-pixel text-xs">运行任务</p>
          <h3 class="text-3xl font-display-lg text-error mt-1">{{ stats.running_tasks.toLocaleString() }}</h3>
        </div>
        <div class="text-error flex flex-col items-end">
          <span class="material-symbols-outlined text-4xl" style="font-variation-settings: 'FILL' 1;">sync</span>
          <span class="text-[10px] font-label-pixel">采集中</span>
        </div>
      </div>
    </section>

    <!-- Left Column -->
    <section class="col-span-3 row-span-1 flex flex-col gap-3">
      <!-- Source Distribution -->
      <div class="bg-surface-container-low/60 backdrop-blur-lg border border-outline-variant p-3 flex-1 pixel-corners flex flex-col min-h-0">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-1 h-4 bg-primary"></div>
          <h4 class="font-title-md text-sm text-primary uppercase tracking-wider">数据源分布</h4>
        </div>
        <div ref="sourceChartRef" class="flex-1 min-h-[180px]"></div>
      </div>
      <!-- Trend -->
      <div class="bg-surface-container-low/60 backdrop-blur-lg border border-outline-variant p-3 flex-1 pixel-corners flex flex-col min-h-0">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-1 h-4 bg-secondary-fixed-dim"></div>
          <h4 class="font-title-md text-sm text-secondary-fixed-dim uppercase tracking-wider">近 7 天保存趋势</h4>
        </div>
        <div ref="trendChartRef" class="flex-1 min-h-[180px]"></div>
      </div>
    </section>

    <!-- Center: 3D Globe -->
    <section class="col-span-6 row-span-1 bg-surface-container-low/60 backdrop-blur-lg border border-outline-variant p-3 pixel-corners flex flex-col min-h-0">
      <div class="flex items-center gap-2 mb-2">
        <div class="w-1 h-4 bg-tertiary"></div>
        <h4 class="font-title-md text-sm text-tertiary uppercase tracking-wider">全球数据分布</h4>
      </div>
      <div ref="globeChartRef" class="flex-1 min-h-[360px]"></div>
    </section>

    <!-- Right Column -->
    <section class="col-span-3 row-span-1 flex flex-col gap-3">
      <!-- Word Cloud -->
      <div class="bg-surface-container-low/60 backdrop-blur-lg border border-outline-variant p-3 flex-1 pixel-corners flex flex-col min-h-0">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-1 h-4 bg-error"></div>
          <h4 class="font-title-md text-sm text-error uppercase tracking-wider">关键词词云</h4>
        </div>
        <div ref="wordcloudChartRef" class="flex-1 min-h-[200px]"></div>
      </div>
      <!-- Recent Logs -->
      <div class="bg-surface-container-low/60 backdrop-blur-lg border border-outline-variant p-3 flex-1 pixel-corners flex flex-col overflow-hidden min-h-0">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-2">
            <div class="w-1 h-4 bg-secondary-fixed-dim"></div>
            <h4 class="font-title-md text-sm text-secondary-fixed-dim uppercase tracking-wider">最新入库</h4>
          </div>
          <span class="text-[10px] font-label-pixel text-on-surface-variant px-2 py-0.5 bg-surface-container-highest">实时</span>
        </div>
        <div class="flex-1 overflow-y-auto space-y-2 pr-1">
          <div v-for="log in recentLogs" :key="log.id" class="p-2 border-b border-outline-variant/20 hover:bg-surface-container-high transition-colors group">
            <div class="flex justify-between items-start mb-1">
              <span class="text-[10px] font-label-pixel text-primary">[{{ log.source }}]</span>
              <span class="text-[10px] font-label-pixel text-on-surface-variant">{{ formatTime(log.created_at) }}</span>
            </div>
            <p class="text-xs text-on-surface font-body-sm truncate group-hover:text-primary transition-colors" :title="log.title">{{ log.title }}</p>
          </div>
          <div v-if="recentLogs.length === 0" class="text-center text-xs text-on-surface-variant py-4">暂无数据</div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import 'echarts-gl'
import 'echarts-wordcloud'
import { getBigscreenData } from '@/api/bigscreen.js'

const stats = ref({ total_saved: 0, today_saved: 0, total_sources: 0, running_tasks: 0 })
const recentLogs = ref([])
const sourceChartRef = ref(null)
const trendChartRef = ref(null)
const globeChartRef = ref(null)
const wordcloudChartRef = ref(null)

let sourceChart = null
let trendChart = null
let globeChart = null
let wordcloudChart = null

function formatTime(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', { hour12: false, month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function initCharts() {
  if (sourceChartRef.value) sourceChart = echarts.init(sourceChartRef.value)
  if (trendChartRef.value) trendChart = echarts.init(trendChartRef.value)
  if (globeChartRef.value) globeChart = echarts.init(globeChartRef.value)
  if (wordcloudChartRef.value) wordcloudChart = echarts.init(wordcloudChartRef.value)
}

function setSourceChart(data) {
  if (!sourceChart) return
  sourceChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { show: false },
    color: ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'],
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '55%'],
      itemStyle: { borderRadius: 4, borderColor: 'rgba(0,0,0,0.3)', borderWidth: 1 },
      label: { color: '#cbd5e1', fontSize: 10 },
      data: data.length ? data : [{ name: '暂无', value: 0 }]
    }]
  })
}

function setTrendChart(data) {
  if (!trendChart) return
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { top: 20, right: 15, bottom: 25, left: 35 },
    xAxis: {
      type: 'category',
      data: data.map(d => d.date),
      axisLine: { lineStyle: { color: '#475569' } },
      axisLabel: { color: '#94a3b8', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#334155', type: 'dashed' } },
      axisLabel: { color: '#94a3b8', fontSize: 10 }
    },
    series: [{
      type: 'line',
      data: data.map(d => d.count),
      smooth: true,
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(59,130,246,0.5)' }, { offset: 1, color: 'rgba(59,130,246,0.05)' }]) },
      lineStyle: { color: '#3b82f6', width: 2 },
      itemStyle: { color: '#3b82f6' }
    }]
  })
}

function setGlobeChart(data) {
  if (!globeChart) return
  const hasData = data && data.length > 0
  const option = {
    backgroundColor: 'transparent',
    globe: {
      baseTexture: 'https://raw.githubusercontent.com/apache/echarts-examples/gh-pages/public/data-gl/asset/earth.jpg',
      heightTexture: 'https://raw.githubusercontent.com/apache/echarts-examples/gh-pages/public/data-gl/asset/bathymetry_bw_composite_4k.jpg',
      displacementScale: 0.05,
      shading: 'lambert',
      environment: 'https://raw.githubusercontent.com/apache/echarts-examples/gh-pages/public/data-gl/asset/starfield.jpg',
      light: { ambient: { intensity: 0.6 }, main: { intensity: 1.2 } },
      viewControl: { autoRotate: true, autoRotateSpeed: 2, distance: 220 },
      postEffect: { enable: true, bloom: { enable: true } }
    },
    series: []
  }
  if (hasData) {
    // 发光柱状标记
    option.series.push({
      type: 'bar3D',
      coordinateSystem: 'globe',
      data: data.map(d => ({
        name: d.name,
        value: d.value
      })),
      barSize: 0.8,
      minHeight: 3,
      silent: true,
      itemStyle: {
        color: '#f59e0b',
        opacity: 0.9
      },
      emphasis: {
        itemStyle: { color: '#fbbf24' }
      }
    })
    // 城市光点标记
    option.series.push({
      type: 'scatter3D',
      coordinateSystem: 'globe',
      data: data.map(d => ({
        name: d.name,
        value: [d.value[0], d.value[1], d.value[2] + 2]
      })),
      symbolSize: 12,
      itemStyle: {
        color: '#ef4444',
        opacity: 1,
        borderWidth: 2,
        borderColor: '#fff'
      },
      emphasis: {
        itemStyle: { color: '#f87171', borderColor: '#fee2e2' },
        label: { show: true, formatter: '{b}', color: '#fff', fontSize: 12 }
      },
      label: { show: false }
    })
  }
  globeChart.setOption(option)
}

function setWordcloudChart(data) {
  if (!wordcloudChart) return
  wordcloudChart.setOption({
    tooltip: { show: true },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '95%',
      height: '95%',
      sizeRange: [12, 36],
      rotationRange: [-45, 45],
      rotationStep: 15,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function () {
          const colors = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899']
          return colors[Math.floor(Math.random() * colors.length)]
        }
      },
      emphasis: { focus: 'self', textStyle: { textShadowBlur: 5, textShadowColor: '#fff' } },
      data: data.length ? data : [{ name: '暂无', value: 1 }]
    }]
  })
}

async function loadData() {
  try {
    const res = await getBigscreenData()
    const data = res.data || {}
    stats.value = data.stats || stats.value
    recentLogs.value = data.recent_logs || []
    setSourceChart(data.source_distribution || [])
    setTrendChart(data.trend || [])
    setGlobeChart(data.globe || [])
    setWordcloudChart(data.wordcloud || [])
  } catch (err) {
    console.error('大屏数据加载失败', err)
  }
}

function onResize() {
  sourceChart && sourceChart.resize()
  trendChart && trendChart.resize()
  globeChart && globeChart.resize()
  wordcloudChart && wordcloudChart.resize()
}

onMounted(async () => {
  await nextTick()
  initCharts()
  await loadData()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', onResize)
  sourceChart && sourceChart.dispose()
  trendChart && trendChart.dispose()
  globeChart && globeChart.dispose()
  wordcloudChart && wordcloudChart.dispose()
})
</script>
