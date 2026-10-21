import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'

import Login from '../views/Login.vue'
import MainLayout from '../layouts/MainLayout.vue'
import Home from '../views/Home.vue'
import FoodCalorie from '../views/FoodCalorie.vue'
import ActionJudge from '../views/ActionJudge.vue'
import MuscleMap from '../views/MuscleMap.vue' // 必须存在！
import Community from '../views/Community.vue'
import VideoZone from '../views/VideoZone.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/home' },
      { path: 'home', name: 'Home', component: Home, meta: { title: '首页' } },
      { path: 'food', name: 'FoodCalorie', component: FoodCalorie, meta: { title: '食物热量识别' } },
      { path: 'action', name: 'ActionJudge', component: ActionJudge, meta: { title: 'AI动作计数' } },
      { path: 'muscle', name: 'MuscleMap', component: MuscleMap, meta: { title: '肌肉图谱' } },
      { path: 'video', name: 'VideoZone', component: VideoZone, meta: { title: '健身视频专区' } },
      { path: 'community', name: 'Community', component: Community, meta: { title: '社区功能' } }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() { return { top: 0 } }
})

router.beforeEach((to, from, next) => {
  if (to.meta.title) document.title = `${to.meta.title} - AI智能健身系统`
  const hasToken = !!localStorage.getItem('token')
  try {
    if (to.meta.requiresAuth && !hasToken) {
      ElMessage.warning('请先登录系统后再操作！')
      return next('/login')
    }
    if (to.path === '/login' && hasToken) return next('/home')
    next()
  } catch (e) {
    console.error('路由守卫异常：', e)
    next()
  }
})

export default router