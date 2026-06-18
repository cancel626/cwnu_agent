import { createRouter, createWebHistory } from 'vue-router'
import AdminLoginView from '@/views/AdminLoginView.vue'

const routes = [
  {
    path: '/',
    name: 'AdminLogin',
    component: AdminLoginView
  }
]

const router = createRouter({
  history: createWebHistory('/admin-login/'),
  routes
})

export default router
