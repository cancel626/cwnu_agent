<template>
  <div class="flex h-screen overflow-hidden">
    <SideNavBar />
    <div class="flex-1 flex flex-col ml-[260px]">
      <TopNavBar />
      <main class="flex-1 pt-16 bg-surface-dim overflow-hidden">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import SideNavBar from '@/components/SideNavBar.vue'
import TopNavBar from '@/components/TopNavBar.vue'
</script>
