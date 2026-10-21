<template>
  <div class="home-container">
    <section class="welcome-section">
      <h2 class="welcome-title">欢迎使用 AI 智能健身系统</h2>
      <p class="welcome-desc">一站式解决你的健身、饮食管理需求</p>
    </section>

    <section class="feature-grid">
      <div class="feature-card" @click="navigateTo('/food')">
        <div class="card-icon food-icon">
          <el-icon><Dish /></el-icon>
        </div>
        <h3 class="card-title">食物热量识别</h3>
        <p class="card-desc">上传图片识别食物，自动计算热量</p>
      </div>

      <div class="feature-card" @click="navigateTo('/action')">
        <div class="card-icon ai-icon">
          <el-icon><VideoCamera /></el-icon>
        </div>
        <h3 class="card-title">AI 动作纠正</h3>
        <p class="card-desc">实时识别健身动作，纠正不规范姿势</p>
      </div>

      <!-- 核心修改：点击跳转到 视频专区 /video -->
      <div class="feature-card" @click="navigateTo('/video')">
        <div class="card-icon muscle-icon">
          <el-icon><Document /></el-icon>
        </div>
        <h3 class="card-title">肌肉图谱&健身视频</h3>
        <p class="card-desc">查看肌肉图解，观看配套训练视频</p>
      </div>

      <div class="feature-card" @click="navigateTo('/community')">
        <div class="card-icon community-icon">
          <el-icon><ChatDotRound /></el-icon>
        </div>
        <h3 class="card-title">社区功能</h3>
        <p class="card-desc">分享健身心得，交流训练经验</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Dish, VideoCamera, Document, ChatDotRound } from '@element-plus/icons-vue'

const router = useRouter()
const navigateTo = (path) => router.push(path)
</script>

<style scoped>
.home-container {
  padding: 20px;
  background-color: #f0f9f4;
  min-height: 100%;
}

.welcome-section {
  text-align: center;
  margin-bottom: 30px;
}

.welcome-title {
  font-size: 24px;
  color: #254d41;
}

.welcome-desc {
  color: #557c6e;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.feature-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #e0f7e8;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 6px 16px rgba(100, 180, 130, 0.1);
}

.card-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
}

.food-icon { background: linear-gradient(135deg, #81e9c5, #3ac298); }
.ai-icon { background: linear-gradient(135deg, #73e6b7, #2fb98b); }
.muscle-icon { background: linear-gradient(135deg, #91e7c1, #42b983); }
.community-icon { background: linear-gradient(135deg, #7ed8b0, #38a169); }

.card-title {
  font-size: 16px;
  color: #254d41;
  margin-bottom: 8px;
}

.card-desc {
  font-size: 13px;
  color: #666;
}

@media (max-width: 1200px) {
  .feature-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>