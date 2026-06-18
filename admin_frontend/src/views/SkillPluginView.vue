<template>
  <div class="h-full overflow-y-auto px-container-margin pb-12 pt-8 custom-scrollbar">
    <h2 class="font-display-lg text-display-lg text-on-surface mb-2">技能中心</h2>
    <p class="text-on-surface-variant font-body-lg mb-8">管理和查看数字员工可调用技能模块。</p>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">
      <div class="bg-surface-container border-2 border-outline-variant p-card-padding hover:border-primary transition-all relative">
        <div class="flex justify-between items-start mb-4">
          <span class="material-symbols-outlined text-primary text-[32px]">psychology</span>
          <span class="px-2 py-0.5 bg-secondary-fixed/20 text-secondary-fixed text-[10px] font-label-pixel border border-secondary-fixed">V 2.1</span>
        </div>
        <h3 class="font-title-md text-title-md text-on-surface mb-2">自然语言解析 (NLP)</h3>
        <p class="text-body-sm text-on-surface-variant mb-4">解析校园咨询、工单及师生反馈中的语义意图。</p>
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">TOKENIZER</span>
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">NER</span>
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">SENTIMENT</span>
        </div>
        <div class="flex justify-between items-center pt-4 border-t border-outline-variant">
          <span class="text-[10px] text-on-surface-variant font-label-pixel">调用次数: 12,402</span>
          <button class="text-primary text-sm hover:underline">配置</button>
        </div>
      </div>
      <div class="bg-surface-container border-2 border-outline-variant p-card-padding hover:border-primary transition-all relative">
        <div class="flex justify-between items-start mb-4">
          <span class="material-symbols-outlined text-tertiary text-[32px]">bar_chart</span>
          <span class="px-2 py-0.5 bg-secondary-fixed/20 text-secondary-fixed text-[10px] font-label-pixel border border-secondary-fixed">V 1.8</span>
        </div>
        <h3 class="font-title-md text-title-md text-on-surface mb-2">实时报表生成</h3>
        <p class="text-body-sm text-on-surface-variant mb-4">将清洗后的数据自动转化为可视化图表与PDF报表。</p>
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">ECHARTS</span>
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">PDF</span>
        </div>
        <div class="flex justify-between items-center pt-4 border-t border-outline-variant">
          <span class="text-[10px] text-on-surface-variant font-label-pixel">调用次数: 8,921</span>
          <button class="text-primary text-sm hover:underline">配置</button>
        </div>
      </div>
      <div class="bg-surface-container border-2 border-outline-variant p-card-padding hover:border-primary transition-all relative">
        <div class="flex justify-between items-start mb-4">
          <span class="material-symbols-outlined text-secondary-fixed-dim text-[32px]">shield</span>
          <span class="px-2 py-0.5 bg-error/20 text-error text-[10px] font-label-pixel border border-error">V 3.0</span>
        </div>
        <h3 class="font-title-md text-title-md text-on-surface mb-2">权限校验网关</h3>
        <p class="text-body-sm text-on-surface-variant mb-4">基于RBAC模型的动态权限拦截与审计日志记录。</p>
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">RBAC</span>
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">JWT</span>
        </div>
        <div class="flex justify-between items-center pt-4 border-t border-outline-variant">
          <span class="text-[10px] text-on-surface-variant font-label-pixel">调用次数: 45,102</span>
          <button class="text-primary text-sm hover:underline">配置</button>
        </div>
      </div>
      <div class="bg-surface-container border-2 border-outline-variant p-card-padding hover:border-primary transition-all relative">
        <div class="flex justify-between items-start mb-4">
          <span class="material-symbols-outlined text-error text-[32px]">notifications_active</span>
          <span class="px-2 py-0.5 bg-secondary-fixed/20 text-secondary-fixed text-[10px] font-label-pixel border border-secondary-fixed">V 1.2</span>
        </div>
        <h3 class="font-title-md text-title-md text-on-surface mb-2">异常预警推送</h3>
        <p class="text-body-sm text-on-surface-variant mb-4">监控系统负载与数据流异常，实时触发多渠道告警。</p>
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">WEBHOOK</span>
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">EMAIL</span>
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">SMS</span>
        </div>
        <div class="flex justify-between items-center pt-4 border-t border-outline-variant">
          <span class="text-[10px] text-on-surface-variant font-label-pixel">调用次数: 3,401</span>
          <button class="text-primary text-sm hover:underline">配置</button>
        </div>
      </div>
      <div class="bg-surface-container border-2 border-outline-variant p-card-padding hover:border-primary transition-all relative">
        <div class="flex justify-between items-start mb-4">
          <span class="material-symbols-outlined text-primary text-[32px]">auto_fix_high</span>
          <span class="px-2 py-0.5 bg-secondary-fixed/20 text-secondary-fixed text-[10px] font-label-pixel border border-secondary-fixed">V 2.5</span>
        </div>
        <h3 class="font-title-md text-title-md text-on-surface mb-2">数据自动修复</h3>
        <p class="text-body-sm text-on-surface-variant mb-4">针对缺失值、重复项及格式错误执行智能修复策略。</p>
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">NULL_FILL</span>
          <span class="bg-surface-variant px-2 py-1 text-[10px] font-label-pixel">DEDUP</span>
        </div>
        <div class="flex justify-between items-center pt-4 border-t border-outline-variant">
          <span class="text-[10px] text-on-surface-variant font-label-pixel">调用次数: 9,112</span>
          <button class="text-primary text-sm hover:underline">配置</button>
        </div>
      </div>
      <div class="bg-surface-container border-2 border-outline-variant p-card-padding hover:border-primary transition-all relative opacity-50 flex items-center justify-center flex-col gap-2 cursor-pointer hover:opacity-100 transition-opacity">
        <span class="material-symbols-outlined text-4xl text-outline-variant">add_circle</span>
        <span class="font-label-pixel text-on-surface-variant">安装新技能</span>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
