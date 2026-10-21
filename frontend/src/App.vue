<template>
  <!-- 路由出口：登录页/主界面切换 -->
  <router-view />
</template>

<script setup>
// 无业务逻辑，仅作为路由容器
</script>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
}
</style>