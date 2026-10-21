<template>
  <div class="video-container">
    <div class="page-title">
      <h2>健身视频专区</h2>
      <p>结合肌肉图谱，观看专业训练教学视频</p>
    </div>

    <!-- 视频列表区域（后续可扩展分页、筛选、播放功能） -->
    <div class="video-list">
      <el-empty description="视频内容开发中，敬请期待" />
    </div>
  </div>
</template>

<script setup>
// 后续视频加载、播放、分类逻辑写在这里
</script>

<style scoped>
.video-container {
  padding: 20px;
  background-color: #f0f9f4;
  min-height: 100%;
}

.page-title {
  text-align: center;
  margin-bottom: 40px;
}

.page-title h2 {
  color: #254d41;
  font-size: 22px;
  margin-bottom: 10px;
}

.page-title p {
  color: #557c6e;
  font-size: 14px;
}

.video-list {
  background: #fff;
  padding: 40px;
  border-radius: 12px;
  border: 1px solid #e0f7e8;
}
</style>