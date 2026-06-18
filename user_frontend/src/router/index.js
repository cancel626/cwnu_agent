import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue'),
        meta: { title: '控制台首页' }
      },
      {
        path: 'staff',
        name: 'Staff',
        component: () => import('@/views/StaffView.vue'),
        meta: { title: '数智员工库' }
      },
      {
        path: 'query',
        name: 'Query',
        component: () => import('@/views/QueryView.vue'),
        meta: { title: '智能问数' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/ProfileView.vue'),
        meta: { title: '个人中心' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory('/user/'),
  routes
})

export default router
