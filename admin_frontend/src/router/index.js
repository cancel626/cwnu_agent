import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import BigScreenLayout from '@/layouts/BigScreenLayout.vue'
import PortalView from '@/views/PortalView.vue'
import LoginView from '@/views/LoginView.vue'
import { useAppStore } from '@/stores/index.js'

const routes = [
  {
    path: '/',
    name: 'Portal',
    component: PortalView,
    meta: { public: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { public: true }
  },
  {
    path: '/dashboard',
    component: DefaultLayout,
    children: [
      { path: '', name: 'Dashboard', alias: '/dashboard', component: () => import('@/views/DashboardView.vue'), meta: { title: '仪表盘' } },
      { path: 'users', name: 'Users', alias: '/users', component: () => import('@/views/UserMgmtView.vue'), meta: { title: '用户管理' } },
      { path: 'collection', name: 'Collection', alias: '/collection', component: () => import('@/views/DataCollectionView.vue'), meta: { title: '数据采集' } },
      { path: 'source-mgmt', name: 'SourceMgmt', alias: '/source-mgmt', component: () => import('@/views/DataSourceMgmtView.vue'), meta: { title: '数据源管理' } },
      { path: 'cleaning', name: 'Cleaning', alias: '/cleaning', component: () => import('@/views/DataCleaningView.vue'), meta: { title: '数据清洗' } },
      { path: 'storage', name: 'Storage', alias: '/storage', component: () => import('@/views/DataStorageView.vue'), meta: { title: '存储管理' } },
      { path: 'ai-inquiry', name: 'AiInquiry', alias: '/ai-inquiry', component: () => import('@/views/AiInquiryView.vue'), meta: { title: 'AI 问询' } },
      { path: 'digital-staff', name: 'DigitalStaff', alias: '/digital-staff', component: () => import('@/views/DigitalStaffView.vue'), meta: { title: '数字员工' } },
      { path: 'skills', name: 'Skills', alias: '/skills', component: () => import('@/views/SkillMgmtView.vue'), meta: { title: '技能管理' } },
      { path: 'models', name: 'Models', alias: '/models', component: () => import('@/views/ModelDeployView.vue'), meta: { title: '模型管理' } },
      { path: 'audit', name: 'Audit', alias: '/audit', component: () => import('@/views/SystemAuditView.vue'), meta: { title: '审计追踪' } },
      { path: 'content-audit', name: 'ContentAudit', alias: '/content-audit', component: () => import('@/views/ContentAuditView.vue'), meta: { title: '内容审核' } }
    ]
  },
  {
    path: '/big-screen',
    component: BigScreenLayout,
    children: [
      { path: '', name: 'BigScreen', component: () => import('@/views/BigScreenView.vue'), meta: { title: '大屏监控' } }
    ]
  }
]

const router = createRouter({
  history: createWebHistory('/admin/'),
  routes
})

router.beforeEach((to, from, next) => {
  const store = useAppStore()
  const isLoggedIn = store.isLoggedIn

  if (to.path === '/' && isLoggedIn) {
    next('/dashboard')
  } else if (!to.meta.public && !isLoggedIn) {
    next('/')
  } else if (to.meta.public && isLoggedIn && to.path !== '/') {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
