<template>
  <div class="layout-container">
    <!-- 左侧侧边栏 -->
    <el-aside width="240px" class="sidebar">
      <h2 class="logo">🏃‍♂️ AI 健身系统</h2>
      <el-menu
        router
        :default-active="$route.path"
        class="menu"
      >
        <el-menu-item index="/home">
          <el-icon><House /></el-icon>
          <span>系统首页</span>
        </el-menu-item>
        <el-menu-item index="/profile">
          <el-icon><User /></el-icon>
          <span>个人信息</span>
        </el-menu-item>
        <el-menu-item index="/exercise">
          <el-icon><Trophy /></el-icon>
          <span>运动记录</span>
        </el-menu-item>
        <el-menu-item index="/setting">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>
        <el-menu-item @click="logout">
          <el-icon><Logout /></el-icon>
          <span>退出登录</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 右侧内容区 -->
    <el-main class="main-content">
      <router-view />
    </el-main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function logout() {
  ElMessageBox.confirm('确定退出登录？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    localStorage.clear()
    router.push('/login')
  }).catch(() => {})
}
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  background: linear-gradient(180deg, #409eff, #337ecc);
  color: #fff;
  padding-top: 20px;
}

.logo {
  text-align: center;
  font-size: 18px;
  margin-bottom: 30px;
}

.menu {
  background: transparent;
  border: none;
}

.menu .el-menu-item {
  color: rgba(255,255,255,0.8);
}

.menu .el-menu-item:hover,
.menu .el-menu-item.is-active {
  background: rgba(255,255,255,0.15);
  color: #fff;
}

.main-content {
  background: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>