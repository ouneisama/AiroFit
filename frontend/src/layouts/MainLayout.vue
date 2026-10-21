<template>
  <div class="app-container">
    <el-container style="height: 100vh;">
      <!-- 优化后的侧边栏 -->
      <el-aside width="200px" class="custom-aside">
        <!-- 新增logo区域，更有层次感 -->
        <div class="sidebar-logo">
          <span>AI健身系统</span>
        </div>
        <el-menu
          default-active="1"
          class="el-menu-vertical-demo custom-menu"
          background-color="#254d41"
          text-color="#e8f5e9"
          active-text-color="#ffffff"
          unique-opened
          :active-text-color="activeTextColor"
        >
          <el-menu-item index="1">
            <router-link to="/home" class="menu-link">
              <template #icon><el-icon><House /></el-icon></template>
              <span>首页</span>
            </router-link>
          </el-menu-item>
          <el-menu-item index="2">
            <router-link to="/food" class="menu-link">
              <template #icon><el-icon><Food /></el-icon></template>
              <span>食物热量识别</span>
            </router-link>
          </el-menu-item>
          <el-menu-item index="3">
            <router-link to="/action" class="menu-link">
              <template #icon><el-icon><UserFilled /></el-icon></template>
              <span>AI动作计数</span>
            </router-link>
          </el-menu-item>
          <el-menu-item index="4">
            <router-link to="/muscle" class="menu-link">
              <template #icon><el-icon><Document /></el-icon></template>
              <span>肌肉图谱</span>
            </router-link>
          </el-menu-item>
          <el-menu-item index="5">
            <router-link to="/community" class="menu-link">
              <template #icon><el-icon><ChatDotRound /></el-icon></template>
              <span>社区功能</span>
            </router-link>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区域 -->
      <el-container>
        <el-header class="top-header">
          <div class="header-left">
            <span class="page-title">{{ currentPageTitle }}</span>
          </div>
          <div class="header-right">
            <span class="username-text">您好，{{ username }}</span>
            <el-button
              type="danger"
              size="small"
              @click="handleLogout"
              :icon="SwitchButton"
            >
              退出登录
            </el-button>
          </div>
        </el-header>
        <el-main style="background-color: #f0f9f4; padding: 20px;">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { House, Food, UserFilled, Document, ChatDotRound, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const username = ref('')
const activeTextColor = ref('#a8e6cf')

const currentPageTitle = computed(() => {
  return route.meta?.title || 'AI智能健身系统'
})

onMounted(() => {
  username.value = localStorage.getItem('username') || '游客'
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  ElMessage.success('退出登录成功！')
  router.push('/login')
}
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
}

.top-header {
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid #e6e6e6;
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username-text {
  font-size: 13px;
  color: #666;
}

/* 侧边栏整体样式优化 */
.custom-aside {
  color: #333;
  background-color: #254d41 !important;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

/* Logo区域样式 */
.sidebar-logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background-color: #1f3f37;
  border-bottom: 1px solid #386858;
}

/* 菜单样式优化 */
.custom-menu {
  border-right: none !important;
  padding-top: 10px;
}

/* 菜单项hover效果 */
:deep(.el-menu-item) {
  margin: 0 8px !important;
  border-radius: 6px !important;
  height: 48px !important;
  line-height: 48px !important;
  margin-bottom: 4px !important;
}

:deep(.el-menu-item:hover) {
  background-color: #386858 !important;
}

:deep(.el-menu-item.is-active) {
  background-color: #4a7c6e !important;
  color: #ffffff !important;
}

/* 链接样式重置 */
.menu-link {
  color: inherit;
  text-decoration: none;
  display: block;
  width: 100%;
  height: 100%;
}
</style>