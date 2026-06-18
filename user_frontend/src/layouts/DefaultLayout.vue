<template>
  <div class="flex h-screen overflow-hidden bg-background text-on-background">
    <SideNavBar />
    <div class="flex-1 flex flex-col overflow-hidden">
      <main class="flex-1 overflow-y-auto custom-scrollbar relative">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import SideNavBar from '@/components/SideNavBar.vue'
</script>
