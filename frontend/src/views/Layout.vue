<template>
  <el-container style="height: 100vh;">
    <!-- 左侧侧边栏 -->
    <el-aside width="200px" style="background-color: #001529;">
      <div class="logo">
        <el-icon size="28" color="#409eff"><Aim /></el-icon>
        <span style="color: white; font-size: 16px; margin-left: 8px;">AI智能健身系统</span>
      </div>
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        background-color="#001529"
        text-color="#fff"
        active-text-color="#409eff"
        @open="handleOpen"
        @close="handleClose"
        @select="handleSelect"
      >
        <el-menu-item index="1">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><VideoCamera /></el-icon>
          <span>智能健身</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><Food /></el-icon>
          <span>食物分析</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 右侧内容区 -->
    <el-container>
      <el-header style="background: #fff; display: flex; justify-content: space-between; align-items: center; padding: 0 20px;">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item>首页</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <el-avatar size="30" src="https://cube.elemecdn.com/0/88/03de5774d4ad2f440eb330b39a636dpng.png"></el-avatar>
              <span style="margin-left: 8px;">test</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}
const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}
const handleSelect = (key, keyPath) => {
  // 后续可以在这里加路由跳转逻辑
  console.log(key, keyPath)
}
const handleLogout = () => {
  localStorage.removeItem('token')
  ElMessage.success('退出成功')
  router.push('/login')
}
</script>

<style scoped>
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}
</style>