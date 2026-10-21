<template>
  <div class="muscle-page-container">
    <!-- 顶部选项卡 -->
    <div class="top-tabs">
      <el-button 
        v-for="tab in tabs" 
        :key="tab.key"
        :class="{ active: activeTab === tab.key }"
        @click="switchTab(tab.key)"
      >
        {{ tab.name }}
      </el-button>
    </div>

    <div class="main-layout">
      <!-- 左侧：肌肉图谱 / 器械展示 -->
      <div class="map-section">
        <!-- 男性/女性：肌肉图谱 -->
        <div v-if="activeTab !== 'equipment'" class="img-wrap">
          <img 
            v-if="viewType === 'front'"
            src="@/assets/muscle-front.png" 
            alt="正面肌肉图"
            class="muscle-img"
          />
          <img 
            v-else
            src="@/assets/muscle-back.png" 
            alt="背面肌肉图"
            class="muscle-img"
          />
          <div class="hotzone chest-zone" :class="{ active: currentMuscle === 'chest' }" @click="selectMuscle('chest')" title="胸肌"></div>
          <div class="hotzone abs-zone" :class="{ active: currentMuscle === 'abs' }" @click="selectMuscle('abs')" title="腹肌"></div>
          <div class="hotzone shoulder-zone" :class="{ active: currentMuscle === 'shoulder' }" @click="selectMuscle('shoulder')" title="肩部"></div>
        </div>

        <!-- 器械：三张器材图 -->
        <div v-else class="equipment-grid">
          <div 
            class="equipment-card" 
            :class="{ active: currentEquipment === 'treadmill' }"
            @click="selectEquipment('treadmill')"
          >
            <img src="@/assets/equipment-treadmill.webp" alt="跑步机" class="equipment-img" />
            <span class="equipment-name">跑步机</span>
          </div>
          <div 
            class="equipment-card" 
            :class="{ active: currentEquipment === 'bike' }"
            @click="selectEquipment('bike')"
          >
            <img src="@/assets/equipment-bike.webp" alt="动感单车" class="equipment-img" />
            <span class="equipment-name">动感单车</span>
          </div>
          <div 
            class="equipment-card" 
            :class="{ active: currentEquipment === 'dumbbell' }"
            @click="selectEquipment('dumbbell')"
          >
            <img src="@/assets/equipment-dumbbell.webp" alt="哑铃" class="equipment-img" />
            <span class="equipment-name">哑铃</span>
          </div>
        </div>
      </div>

      <!-- 右侧：教程 / 器械详情 -->
      <div class="tutorial-section">
        <!-- 器械详情 -->
        <div v-if="activeTab === 'equipment'">
          <div v-if="!currentEquipment" class="empty-state">
            <div class="empty-icon">🏋️</div>
            <p>点击左侧器材图片查看详情</p>
          </div>
          <div v-else class="tutorial-container">
            <h2 class="muscle-title">{{ equipmentData[currentEquipment].name }}</h2>
            <div class="equipment-detail-img">
              <img :src="equipmentData[currentEquipment].image" :alt="equipmentData[currentEquipment].name" />
            </div>
            <div class="equipment-info-section">
              <h3>📋 主要功能</h3>
              <ul class="info-list">
                <li v-for="(fn, i) in equipmentData[currentEquipment].functions" :key="'fn'+i">{{ fn }}</li>
              </ul>
            </div>
            <div class="equipment-info-section caution">
              <h3>⚠️ 注意事项</h3>
              <ul class="info-list">
                <li v-for="(ca, i) in equipmentData[currentEquipment].cautions" :key="'ca'+i">{{ ca }}</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- 肌肉教程 -->
        <template v-else>
          <div v-if="!currentMuscle" class="empty-state">
            <div class="empty-icon">🏋️</div>
            <p>点击图片上的肌肉部位查看对应教程</p>
          </div>
          <div v-else class="tutorial-container">
            <h2 class="muscle-title">{{ muscleData[currentMuscle].name }} 训练教程</h2>
            <div class="exercise-card" v-for="(item, idx) in muscleData[currentMuscle].exercises" :key="idx">
              <h3 class="exercise-name">{{ item.name }}</h3>
              
              <!-- 视频播放器 -->
              <div class="video-wrapper" v-if="item.videoUrl">
                <video 
                  class="exercise-video"
                  :src="item.videoUrl"
                  controls
                  preload="metadata"
                  playsinline
                >
                  您的浏览器不支持视频播放
                </video>
              </div>
              <div class="video-placeholder" v-else>
                <img src="@/assets/video-cover.png" alt="动作示范图" class="demo-img">
                <div class="placeholder-text">
                  <span>🎬 视频待添加</span>
                  <span class="placeholder-hint">可在 exercise 数据中配置 videoUrl</span>
                </div>
              </div>

              <div class="exercise-details">
                <h4>动作步骤：</h4>
                <ol class="steps-list">
                  <li v-for="(step, sIdx) in item.steps" :key="sIdx">{{ step }}</li>
                </ol>
                <div class="tags">
                  <el-tag size="small" type="info">{{ item.level }}</el-tag>
                  <el-tag size="small" type="success">{{ item.equipment }}</el-tag>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const tabs = [
  { key: 'male', name: '男性' },
  { key: 'female', name: '女性' },
  { key: 'equipment', name: '器械' }
]
const activeTab = ref('male')
const viewType = ref('front')
const currentMuscle = ref('')
const currentEquipment = ref('')

const switchTab = (key) => {
  activeTab.value = key
  currentMuscle.value = ''
  currentEquipment.value = ''
}

const selectMuscle = (type) => {
  currentMuscle.value = type
}

const selectEquipment = (type) => {
  currentEquipment.value = type
}

// 器械数据
import bikeImg from '@/assets/equipment-bike.webp'
import treadmillImg from '@/assets/equipment-treadmill.webp'
import dumbbellImg from '@/assets/equipment-dumbbell.webp'

const equipmentData = {
  bike: {
    name: '动感单车',
    image: bikeImg,
    functions: [
      '高效燃脂：45分钟可消耗400-600大卡热量',
      '增强心肺功能：持续骑行提升心肺耐力',
      '塑形腿部肌肉：重点锻炼股四头肌、小腿和臀部',
      '低冲击运动：对膝盖关节压力小，适合各年龄段',
      '可调节阻力：通过旋钮自由调节骑行强度'
    ],
    cautions: [
      '骑行前调整座椅高度，膝盖微弯为最佳位置',
      '保持上半身稳定，不要左右摇晃',
      '初学者建议从低阻力开始，逐步增加强度',
      '骑行过程中保持均匀呼吸，不要憋气',
      '运动后做腿部拉伸，防止肌肉酸痛',
      '有膝关节损伤者请咨询医生后再使用'
    ]
  },
  treadmill: {
    name: '跑步机',
    image: treadmillImg,
    functions: [
      '全身有氧运动：跑步可同时锻炼腿部、核心和心肺',
      '速度/坡度可调：模拟平地、上坡等不同跑步场景',
      '心率监测：实时显示心率数据，科学控制运动强度',
      '减震系统：降低跑步对膝盖和踝关节的冲击',
      '多种训练模式：燃脂模式、间歇模式、心率模式等',
      '折叠收纳：节省家庭空间'
    ],
    cautions: [
      '跑步前先以慢走热身3-5分钟',
      '保持身体直立，目视前方，不要低头看脚',
      '步幅适中，脚掌中部先着地，避免脚跟着地',
      '速度不宜过快，以能正常交谈的强度为宜',
      '结束后逐步减速，不要突然停止',
      '定期检查跑带松紧度，确保安全使用'
    ]
  },
  dumbbell: {
    name: '哑铃',
    image: dumbbellImg,
    functions: [
      '全身力量训练：可锻炼胸、背、肩、臂、腿等肌群',
      '自由重量训练：动作轨迹自然，激活更多稳定肌群',
      '重量可调节：通过增减配重片适应不同训练阶段',
      '改善肌肉不平衡：单侧训练可纠正左右力量差异',
      '提高基础代谢：增加肌肉量，日常消耗更多热量',
      '占地小：适合家庭健身，无需大型器械'
    ],
    cautions: [
      '选择合适重量，能完成8-12次标准动作为宜',
      '动作过程中保持核心收紧，背部挺直',
      '控制动作速度，举起2秒、放下3秒',
      '不要锁死关节，保持微弯保护肘部和膝盖',
      '训练前充分热身，训练后拉伸放松',
      '初学者建议从复合动作开始（卧推、划船、深蹲）',
      '哑铃使用后归位，避免绊倒'
    ]
  }
}

// 肌肉教程数据
const muscleData = reactive({
  chest: {
    name: '胸肌',
    exercises: [
      {
        name: '杠铃卧推',
        level: '中级',
        equipment: '杠铃',
        videoUrl: '/videos/barbell-bench-press.mp4',
        steps: [
          '躺在卧推凳上，双脚平放地面，背部贴紧凳面',
          '双手握杠铃，握距略宽于肩，手腕保持直立',
          '吸气，缓慢下放杠铃至胸前（乳头线位置）',
          '发力推起至手臂伸直但不锁死，呼气',
          '每组 8-12 次，做 3-4 组'
        ]
      },
      {
        name: '哑铃飞鸟',
        level: '中级',
        equipment: '哑铃',
        videoUrl: '/videos/dumbbell-fly.mp4',
        steps: [
          '仰卧在平凳上，双手各持哑铃举至胸部上方',
          '手臂微弯保持固定角度，向两侧缓慢打开',
          '感受胸肌拉伸，下放到与肩同高',
          '用胸肌力量将哑铃夹回起始位置',
          '每组 10-15 次，做 3 组'
        ]
      },
      {
        name: '俯卧撑',
        level: '初级',
        equipment: '无',
        videoUrl: '/videos/push-up.mp4',
        steps: [
          '双手撑地略宽于肩，身体呈一条直线',
          '收紧核心和臀部，不要塌腰或撅臀',
          '缓慢下降至胸部接近地面',
          '发力推起回到起始位置',
          '每组做到力竭，做 3-4 组'
        ]
      }
    ]
  },
  abs: {
    name: '腹肌',
    exercises: [
      {
        name: '平板支撑',
        level: '初级',
        equipment: '无',
        videoUrl: '/videos/plank-new.mp4',
        steps: [
          '双肘撑地与肩同宽，脚尖着地',
          '身体保持一条直线，收紧腹部和臀部',
          '眼睛看向地面，保持颈部自然',
          '均匀呼吸不要憋气',
          '每组坚持 30-60 秒，做 3-4 组'
        ]
      },
      {
        name: '卷腹',
        level: '初级',
        equipment: '无',
        videoUrl: '/videos/crunch.mp4',
        steps: [
          '仰卧屈膝，双脚平放地面，双手交叉放胸前',
          '用腹部力量将上半身卷起，下背部贴地',
          '在最高点停顿 1 秒，感受腹肌收缩',
          '缓慢下放回到起始位置',
          '每组 15-20 次，做 3-4 组'
        ]
      },
      {
        name: '仰卧举腿',
        level: '中级',
        equipment: '无',
        videoUrl: '/videos/leg-raise-new.mp4',
        steps: [
          '仰卧在垫子上，双手放身体两侧',
          '双腿并拢伸直，缓慢抬起至与地面垂直',
          '下背部始终贴地，用下腹发力',
          '控制速度缓慢下放，脚不触地',
          '每组 12-15 次，做 3 组'
        ]
      }
    ]
  },
  shoulder: {
    name: '肩部',
    exercises: [
      {
        name: '哑铃侧平举',
        level: '初级',
        equipment: '哑铃',
        videoUrl: '/videos/lateral-raise-new.mp4',
        steps: [
          '双手握哑铃垂于身体两侧，掌心相对',
          '手臂微弯保持固定角度，肘关节略高于手腕',
          '向两侧平举至肩高，不要耸肩',
          '在最高点稍作停顿，缓慢回落',
          '每组 12-15 次，做 3-4 组'
        ]
      },
      {
        name: '哑铃推举',
        level: '中级',
        equipment: '哑铃',
        videoUrl: '/videos/shoulder-press.mp4',
        steps: [
          '坐姿或站姿，双手持哑铃举至肩部两侧',
          '核心收紧，背部挺直，不要后仰',
          '向上推举至手臂伸直，哑铃在头顶正上方',
          '缓慢下放回到起始位置',
          '每组 8-12 次，做 3-4 组'
        ]
      },
      {
        name: '前平举',
        level: '初级',
        equipment: '哑铃',
        videoUrl: '/videos/front-raise.mp4',
        steps: [
          '站立，双手握哑铃垂于大腿前方',
          '手臂微弯，将哑铃向前平举至肩高',
          '控制速度，不要借力摆动身体',
          '缓慢下放回到起始位置',
          '每组 12-15 次，做 3 组'
        ]
      }
    ]
  }
})
</script>

<style scoped>
.muscle-page-container {
  padding: 24px;
  background-color: #f0f9f4;
  min-height: 100vh;
}

.top-tabs {
  margin-bottom: 32px;
  display: flex;
  gap: 12px;
}
.top-tabs .el-button {
  border-radius: 8px;
}
.top-tabs .el-button.active {
  background-color: #254d41;
  color: #fff;
}

.main-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  flex-wrap: wrap;
}

/* 左侧 */
.map-section {
  flex: 1;
  min-width: 320px;
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.img-wrap {
  position: relative;
  display: inline-block;
  width: 100%;
  max-width: 500px;
}
.muscle-img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 8px;
}

/* 热区 */
.hotzone {
  position: absolute;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.3s ease;
}
.hotzone:hover {
  background: rgba(37, 77, 65, 0.12);
}
.hotzone.active {
  background: rgba(37, 77, 65, 0.18);
  box-shadow: 0 0 0 2px rgba(37, 77, 65, 0.3);
}
.chest-zone { top: 22%; left: 30%; width: 30%; height: 14%; }
.abs-zone { top: 40%; left: 32%; width: 26%; height: 16%; }
.shoulder-zone { top: 12%; left: 15%; width: 35%; height: 12%; }

/* 器械网格 */
.equipment-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.equipment-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  border-radius: 12px;
  border: 2px solid #e8edf2;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafbfc;
}
.equipment-card:hover {
  border-color: #254d41;
  background: #f0f7f4;
  transform: translateX(4px);
}
.equipment-card.active {
  border-color: #254d41;
  background: #e8f5ee;
  box-shadow: 0 2px 12px rgba(37, 77, 65, 0.12);
}
.equipment-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}
.equipment-name {
  font-size: 17px;
  font-weight: 600;
  color: #254d41;
}

/* 右侧 */
.tutorial-section {
  flex: 1;
  min-width: 320px;
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  min-height: 450px;
}
.empty-state {
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}
.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
.muscle-title {
  font-size: 20px;
  color: #254d41;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

/* 器械详情 */
.equipment-detail-img {
  width: 100%;
  height: 180px;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
}
.equipment-detail-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.equipment-info-section {
  margin-bottom: 18px;
}
.equipment-info-section h3 {
  font-size: 15px;
  color: #254d41;
  margin-bottom: 10px;
}
.equipment-info-section.caution {
  background: #fff8f0;
  padding: 14px 16px;
  border-radius: 10px;
  border-left: 3px solid #e6a23c;
}
.info-list {
  padding-left: 18px;
  margin: 0;
}
.info-list li {
  font-size: 13px;
  color: #555;
  line-height: 2;
}

/* 训练教程 */
.exercise-card {
  background-color: #f8fffc;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #e0f7e8;
}
.exercise-name {
  font-size: 16px;
  color: #254d41;
  margin-bottom: 16px;
}
.video-wrapper {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background-color: #000;
  margin-bottom: 16px;
}
.exercise-video {
  width: 100%;
  max-height: 360px;
  display: block;
  border-radius: 8px;
}
.video-placeholder {
  width: 100%;
  height: 220px;
  border-radius: 8px;
  overflow: hidden;
  background-color: #eef2f5;
  margin-bottom: 16px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.video-placeholder .demo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.35;
}
.video-placeholder .placeholder-text {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: #8899a6;
  font-size: 15px;
  font-weight: 500;
}
.video-placeholder .placeholder-hint {
  font-size: 12px;
  color: #aab5bc;
  font-weight: 400;
}
.exercise-details h4 {
  font-size: 14px;
  color: #386858;
  margin-bottom: 8px;
}
.steps-list {
  padding-left: 20px;
  color: #666;
  line-height: 1.8;
  margin-bottom: 12px;
}
.tags {
  display: flex;
  gap: 8px;
}

@media (max-width: 900px) {
  .main-layout {
    flex-direction: column;
  }
}
</style>
