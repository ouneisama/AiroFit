<template>
  <div class="action-container">
    <!-- 标题区 -->
    <div class="page-header">
      <div class="header-icon">
        <el-icon :size="28"><VideoCamera /></el-icon>
      </div>
      <div class="header-text">
        <h2>AI 动作计数</h2>
        <p>实时识别健身动作，智能语音播报</p>
      </div>
    </div>

    <!-- 视频预览区 -->
    <div class="video-wrapper">
      <div class="video-frame" :class="{ active: isStart }">
        <img v-if="isStart" :src="videoUrl" class="video-feed" />
        <div v-else class="video-idle">
          <div class="idle-icon">
            <el-icon :size="64"><VideoCamera /></el-icon>
          </div>
          <p class="idle-title">摄像头预览</p>
          <p class="idle-desc">选择动作类型后点击开始</p>
        </div>
        <!-- 状态角标 -->
        <div v-if="isStart" class="status-badge" :class="{ paused: isPaused }">
          <span class="status-dot"></span>
          {{ isPaused ? '已暂停' : '检测中' }}
        </div>
      </div>
    </div>

    <!-- 控制栏 -->
    <div class="control-bar">
      <div class="control-left">
        <el-select v-model="actionType" :disabled="isStart" placeholder="选择动作" size="large" class="action-select">
          <el-option label="🦵 深蹲" value="squat" />
          <el-option label="🖐️ 臂展" value="arm" />
        </el-select>
      </div>
      <div class="control-right">
        <el-button
          v-if="!isStart"
          type="success"
          size="large"
          :icon="VideoPlay"
          @click="start"
          class="btn-start"
        >
          开始计数
        </el-button>
        <el-button
          v-else
          :type="isPaused ? 'success' : 'warning'"
          size="large"
          :icon="isPaused ? VideoPlay : VideoPause"
          @click="pause"
        >
          {{ isPaused ? '继续' : '暂停' }}
        </el-button>
        <el-button size="large" :icon="RefreshLeft" @click="reset" class="btn-reset">
          重置
        </el-button>
        <el-button size="large" :icon="Close" type="danger" @click="stop" plain>
          结束
        </el-button>
      </div>
    </div>

    <!-- 计数展示 -->
    <transition name="count-fade">
      <div v-if="isStart" class="count-section">
        <div class="count-card">
          <span class="count-label">当前计数</span>
          <div class="count-display">
            <span class="count-number">{{ count }}</span>
            <span class="count-unit">次</span>
          </div>
          <div class="count-bar">
            <div class="count-bar-fill" :style="{ width: countProgress + '%' }"></div>
          </div>
          <span class="count-target">目标 20 次</span>
        </div>
      </div>
    </transition>

    <!-- 动作提示 -->
    <transition name="tip-fade">
      <div v-if="isStart" class="tip-card">
        <div class="tip-icon">
          <el-icon :size="20"><InfoFilled /></el-icon>
        </div>
        <div class="tip-content">
          <template v-if="actionType === 'squat'">
            <p class="tip-title">深蹲动作要领</p>
            <p>双脚与肩同宽，背部挺直 → 缓慢下蹲至大腿与地面平行 → 站起还原</p>
          </template>
          <template v-else>
            <p class="tip-title">臂展动作要领</p>
            <p>双臂平举至与肩同高 → 缓慢放下至身体两侧 → 重复动作</p>
          </template>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, watch } from 'vue'
import { VideoCamera, VideoPlay, VideoPause, RefreshLeft, Close, InfoFilled } from '@element-plus/icons-vue'

const videoUrl = ref('http://127.0.0.1:5000/video_feed')
const actionType = ref('squat')
const isStart = ref(false)
const isPaused = ref(false)
const count = ref(0)
const lastCount = ref(0)
let timer = null
let bestVoice = null

const countProgress = computed(() => Math.min((count.value / 20) * 100, 100))

const loadVoice = () => {
  const synth = window.speechSynthesis
  synth.onvoiceschanged = () => {
    const voices = synth.getVoices()
    bestVoice = voices.find(v => v.name.includes('Xiaoxiao')) || voices.find(v => v.lang.startsWith('zh'))
  }
}
loadVoice()

const speak = (text) => {
  if (!window.speechSynthesis) return
  window.speechSynthesis.cancel()
  const u = new SpeechSynthesisUtterance(text)
  u.lang = 'zh-CN'
  u.rate = 0.95
  u.pitch = 1.05
  if (bestVoice) u.voice = bestVoice
  window.speechSynthesis.speak(u)
}

const start = () => {
  isStart.value = true
  isPaused.value = false
  speak('开始')
  fetchLoop()
}

const pause = () => {
  isPaused.value = !isPaused.value
  isPaused.value ? speak('暂停') : speak('继续')
}

const reset = () => {
  fetch('http://127.0.0.1:5000/api/reset', { method: 'POST' })
    .then(() => {
      count.value = 0
      speak('已重置')
    })
}

const stop = () => {
  fetch('http://127.0.0.1:5000/api/reset', { method: 'POST' }).then(() => {
    isStart.value = false
    isPaused.value = false
    clearInterval(timer)
    count.value = 0
    speak('结束')
  })
}

const fetchLoop = () => {
  clearInterval(timer)
  timer = setInterval(() => {
    if (isPaused.value) return
    fetch('http://127.0.0.1:5000/api/get-count?type=' + actionType.value)
      .then(r => r.json()).then(d => { count.value = d.score })
  }, 200)
}

watch(count, (n) => {
  if (isStart.value && !isPaused.value && n > lastCount.value)
    speak(n + '个')
  lastCount.value = n
})

onUnmounted(() => { clearInterval(timer) })
</script>

<style scoped>
.action-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

/* ===== 标题区 ===== */
.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding: 20px 24px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e8f4fd 100%);
  border-radius: 16px;
  border: 1px solid #d4e7f7;
}
.header-icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #409EFF, #66b1ff);
  border-radius: 14px;
  color: #fff;
  flex-shrink: 0;
}
.header-text h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #1d2b3a;
}
.header-text p {
  margin: 4px 0 0;
  font-size: 13px;
  color: #6b7c8e;
}

/* ===== 视频区 ===== */
.video-wrapper {
  margin-bottom: 20px;
}
.video-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  max-height: 480px;
  background: #0f1419;
  border-radius: 16px;
  overflow: hidden;
  border: 3px solid #e5e7eb;
  transition: border-color 0.4s, box-shadow 0.4s;
}
.video-frame.active {
  border-color: #409EFF;
  box-shadow: 0 0 0 4px rgba(64, 158, 255, 0.15);
}
.video-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.video-idle {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #8899aa;
}
.idle-icon {
  opacity: 0.5;
  margin-bottom: 12px;
}
.idle-title {
  font-size: 18px;
  font-weight: 600;
  color: #a0b0c0;
  margin: 0 0 6px;
}
.idle-desc {
  font-size: 13px;
  color: #6b7c8e;
  margin: 0;
}

/* 状态角标 */
.status-badge {
  position: absolute;
  top: 14px;
  right: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(0, 180, 42, 0.9);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  border-radius: 20px;
  backdrop-filter: blur(8px);
}
.status-badge.paused {
  background: rgba(255, 125, 0, 0.9);
}
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #fff;
  animation: pulse-dot 1.5s ease-in-out infinite;
}
.status-badge.paused .status-dot {
  animation: none;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.7); }
}

/* ===== 控制栏 ===== */
.control-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  padding: 16px 20px;
  background: #fff;
  border-radius: 14px;
  border: 1px solid #ebeef5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  margin-bottom: 20px;
}
.control-right {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.action-select {
  width: 160px;
}
.btn-start {
  font-weight: 600;
  letter-spacing: 0.5px;
}
.btn-reset {
  color: #409EFF;
  border-color: #409EFF;
}

/* ===== 计数展示 ===== */
.count-section {
  margin-bottom: 20px;
}
.count-card {
  text-align: center;
  padding: 28px 20px;
  background: linear-gradient(145deg, #ffffff, #f8fbff);
  border-radius: 16px;
  border: 1px solid #e8edf4;
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.08);
}
.count-label {
  display: block;
  font-size: 13px;
  color: #909399;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 8px;
}
.count-display {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 6px;
  margin-bottom: 16px;
}
.count-number {
  font-size: 72px;
  font-weight: 800;
  color: #409EFF;
  line-height: 1;
  font-variant-numeric: tabular-nums;
  transition: color 0.3s;
}
.count-unit {
  font-size: 20px;
  color: #909399;
  font-weight: 500;
}
.count-bar {
  height: 6px;
  background: #e8edf4;
  border-radius: 3px;
  overflow: hidden;
  max-width: 240px;
  margin: 0 auto 10px;
}
.count-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #409EFF, #66b1ff);
  border-radius: 3px;
  transition: width 0.4s ease;
}
.count-target {
  font-size: 12px;
  color: #b0b8c4;
}

/* ===== 动作提示 ===== */
.tip-card {
  display: flex;
  gap: 14px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #fff9f0, #fff7e8);
  border-radius: 12px;
  border-left: 4px solid #e6a23c;
}
.tip-icon {
  color: #e6a23c;
  flex-shrink: 0;
  margin-top: 2px;
}
.tip-content p {
  margin: 0;
  font-size: 14px;
  color: #6b5e3e;
  line-height: 1.7;
}
.tip-title {
  font-weight: 700 !important;
  color: #5a4a2a !important;
  margin-bottom: 4px !important;
}

/* ===== 过渡动画 ===== */
.count-fade-enter-active,
.tip-fade-enter-active {
  transition: all 0.4s ease;
}
.count-fade-leave-active,
.tip-fade-leave-active {
  transition: all 0.25s ease;
}
.count-fade-enter-from,
.tip-fade-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.count-fade-leave-to,
.tip-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ===== 响应式 ===== */
@media (max-width: 640px) {
  .action-container {
    padding: 12px;
  }
  .control-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .control-right {
    justify-content: center;
  }
  .action-select {
    width: 100%;
  }
  .count-number {
    font-size: 56px;
  }
}
</style>
