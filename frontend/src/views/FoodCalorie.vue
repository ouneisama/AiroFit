<template>
  <div class="food-calorie-page">
    <el-row :gutter="20">
      <!-- 左侧：上传识别区 -->
      <el-col :span="14">
        <el-card class="upload-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span><el-icon><Upload /></el-icon> 上传食物图片</span>
              <el-tag v-if="uploading" type="warning" size="small">识别中...</el-tag>
            </div>
          </template>

          <!-- 上传区域 -->
          <div class="upload-area-wrapper">
            <input
              ref="fileInputRef"
              type="file"
              accept="image/jpeg,image/png,image/gif,image/webp"
              style="display: none"
              @change="onFileSelected"
            />
            <div
              v-if="!previewUrl"
              class="upload-dropzone"
              @click="openFilePicker"
              @dragover.prevent
              @drop.prevent="onFileDrop"
            >
              <el-icon class="upload-icon"><Camera /></el-icon>
              <div class="upload-text">
                <p class="primary-text">点击或拖拽食物图片到此处</p>
                <p class="secondary-text">支持 JPG / PNG / GIF / WebP 格式</p>
              </div>
            </div>
            <div v-else class="preview-container">
              <img :src="previewUrl" class="preview-image" />
            </div>
          </div>

          <!-- 快捷操作 -->
          <div class="quick-actions">
            <el-button type="primary" @click="startRecognize" :loading="uploading" :disabled="!selectedFile">
              <el-icon><Camera /></el-icon> 开始识别
            </el-button>
            <el-button @click="clearAll" :disabled="!previewUrl">
              <el-icon><Delete /></el-icon> 清除
            </el-button>
            <el-select v-model="selectedMealType" placeholder="选择餐次" style="width: 140px; margin-left: 10px;">
              <el-option label="🥐 早餐" value="breakfast" />
              <el-option label="🍚 午餐" value="lunch" />
              <el-option label="🍜 晚餐" value="dinner" />
              <el-option label="🍎 加餐" value="snack" />
            </el-select>
          </div>
        </el-card>

        <!-- 识别结果 -->
        <el-card v-if="recognitionResult" class="result-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span><el-icon><DataAnalysis /></el-icon> 识别结果</span>
              <el-tag :type="confidenceType" size="small">
                置信度 {{ (recognitionResult.confidence * 100).toFixed(0) }}%
              </el-tag>
            </div>
          </template>

          <div class="result-content">
            <!-- 食物信息 -->
            <div class="food-info">
              <div class="food-name">
                <el-icon class="food-icon"><DishDot /></el-icon>
                <span>{{ recognitionResult.food_name_cn }}</span>
              </div>
              <div class="food-weight">
                预估重量：<strong>{{ recognitionResult.weight_g }}g</strong>
              </div>
            </div>

            <!-- 热量大数字 -->
            <div class="calorie-big">
              <span class="calorie-number">{{ recognitionResult.calorie }}</span>
              <span class="calorie-unit">kcal</span>
            </div>

            <!-- 营养进度条 -->
            <div class="nutrition-bars">
              <div class="nutrition-item">
                <div class="nutrition-label">
                  <span>蛋白质</span>
                  <span class="nutrition-value">{{ recognitionResult.protein }}g</span>
                </div>
                <el-progress :percentage="getMacroPercent(recognitionResult.protein, 60)" :color="'#409EFF'" :stroke-width="8" />
              </div>
              <div class="nutrition-item">
                <div class="nutrition-label">
                  <span>碳水化合物</span>
                  <span class="nutrition-value">{{ recognitionResult.carb }}g</span>
                </div>
                <el-progress :percentage="getMacroPercent(recognitionResult.carb, 250)" :color="'#E6A23C'" :stroke-width="8" />
              </div>
              <div class="nutrition-item">
                <div class="nutrition-label">
                  <span>脂肪</span>
                  <span class="nutrition-value">{{ recognitionResult.fat }}g</span>
                </div>
                <el-progress :percentage="getMacroPercent(recognitionResult.fat, 65)" :color="'#F56C6C'" :stroke-width="8" />
              </div>
              <div class="nutrition-item" v-if="recognitionResult.fiber > 0">
                <div class="nutrition-label">
                  <span>膳食纤维</span>
                  <span class="nutrition-value">{{ recognitionResult.fiber }}g</span>
                </div>
                <el-progress :percentage="getMacroPercent(recognitionResult.fiber, 25)" :color="'#67C23A'" :stroke-width="8" />
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="result-actions">
              <el-button type="success" @click="saveRecord">
                <el-icon><Check /></el-icon> 记录到饮食日志
              </el-button>
              <el-button @click="adjustWeightDialog = true">
                <el-icon><Edit /></el-icon> 调整重量
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：今日饮食汇总 + 历史记录 -->
      <el-col :span="10">
        <!-- 今日汇总 -->
        <el-card class="summary-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span><el-icon><TrendCharts /></el-icon> 今日饮食汇总</span>
              <span class="date-label">{{ todayStr }}</span>
            </div>
          </template>

          <div class="summary-content">
            <div class="calorie-ring">
              <el-progress type="dashboard" :percentage="caloriePercent" :color="calorieColor" :stroke-width="12" :width="140">
                <template #default>
                  <span class="ring-value">{{ dailySummary.total_calorie }}</span>
                  <span class="ring-label">/ 2000 kcal</span>
                </template>
              </el-progress>
            </div>

            <div class="macro-summary">
              <div class="macro-item protein">
                <div class="macro-dot"></div>
                <div class="macro-info">
                  <span class="macro-name">蛋白质</span>
                  <span class="macro-amount">{{ dailySummary.total_protein }}g</span>
                </div>
              </div>
              <div class="macro-item carb">
                <div class="macro-dot"></div>
                <div class="macro-info">
                  <span class="macro-name">碳水</span>
                  <span class="macro-amount">{{ dailySummary.total_carb }}g</span>
                </div>
              </div>
              <div class="macro-item fat">
                <div class="macro-dot"></div>
                <div class="macro-info">
                  <span class="macro-name">脂肪</span>
                  <span class="macro-amount">{{ dailySummary.total_fat }}g</span>
                </div>
              </div>
            </div>

            <el-divider />
            <div class="meal-count">今日已记录 <strong>{{ dailySummary.meal_count }}</strong> 餐</div>
          </div>
        </el-card>

        <!-- 近7天趋势 -->
        <el-card class="trend-card" shadow="hover">
          <template #header>
            <span><el-icon><Histogram /></el-icon> 近7天热量趋势</span>
          </template>
          <div ref="chartRef" style="height: 200px;"></div>
        </el-card>

        <!-- 今日食物记录 -->
        <el-card class="records-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span><el-icon><List /></el-icon> 今日食物记录</span>
              <el-button text size="small" @click="loadTodayRecords">刷新</el-button>
            </div>
          </template>

          <div v-if="todayRecords.length === 0" class="empty-records">
            <el-empty description="今天还没有记录食物" :image-size="80" />
          </div>

          <div v-else class="records-list">
            <div v-for="record in todayRecords" :key="record.id" class="record-item">
              <div class="record-left">
                <el-tag :type="mealTypeTag(record.meal_type)" size="small" effect="plain">
                  {{ mealTypeLabel(record.meal_type) }}
                </el-tag>
                <span class="record-name">{{ record.food_name_cn || record.food_name }}</span>
              </div>
              <div class="record-right">
                <span class="record-cal">{{ record.calorie }} kcal</span>
                <el-button text type="danger" size="small" @click="deleteRecord(record.id)" :icon="Delete" />
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 调整重量弹窗 -->
    <el-dialog v-model="adjustWeightDialog" title="调整食物重量" width="400px">
      <div class="weight-adjust">
        <p>当前食物：<strong>{{ recognitionResult?.food_name_cn }}</strong></p>
        <el-input-number v-model="adjustedWeight" :min="10" :max="5000" :step="10" size="large" style="width: 100%; margin-top: 16px;" />
        <div class="weight-preview" v-if="adjustedNutrition">
          <el-divider />
          <p>调整后热量：<strong>{{ adjustedNutrition.calorie }} kcal</strong></p>
          <p>蛋白质 {{ adjustedNutrition.protein }}g | 碳水 {{ adjustedNutrition.carb }}g | 脂肪 {{ adjustedNutrition.fat }}g</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="adjustWeightDialog = false">取消</el-button>
        <el-button type="primary" @click="applyWeightAdjust">确认调整</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Camera, Upload, DataAnalysis, DishDot, Check, Edit, Delete,
  TrendCharts, Histogram, List
} from '@element-plus/icons-vue'
import axios from 'axios'
import * as echarts from 'echarts'

const API_BASE = import.meta.env.DEV ? '' : 'http://localhost:5000'

// 上传相关
const fileInputRef = ref(null)
const selectedFile = ref(null)
const uploading = ref(false)
const previewUrl = ref(null)
const selectedMealType = ref('lunch')

// 识别结果
const recognitionResult = ref(null)

// 今日汇总
const dailySummary = reactive({
  total_calorie: 0, total_protein: 0, total_carb: 0, total_fat: 0, meal_count: 0,
})

const todayRecords = ref([])

// 调整重量
const adjustWeightDialog = ref(false)
const adjustedWeight = ref(200)
const adjustedNutrition = ref(null)

// 趋势图
const chartRef = ref(null)
let chartInstance = null

const todayStr = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
})

const caloriePercent = computed(() => Math.min(Math.round((dailySummary.total_calorie / 2000) * 100), 100))
const calorieColor = computed(() => {
  if (caloriePercent.value < 50) return '#67C23A'
  if (caloriePercent.value < 80) return '#E6A23C'
  return '#F56C6C'
})
const confidenceType = computed(() => {
  if (!recognitionResult.value) return 'info'
  const conf = recognitionResult.value.confidence
  if (conf >= 0.9) return 'success'
  if (conf >= 0.75) return 'warning'
  return 'danger'
})

function getMacroPercent(value, dailyTarget) {
  return Math.min(Math.round((value / dailyTarget) * 100), 100)
}

function mealTypeLabel(type) {
  const map = { breakfast: '早餐', lunch: '午餐', dinner: '晚餐', snack: '加餐' }
  return map[type] || type
}

function mealTypeTag(type) {
  const map = { breakfast: 'warning', lunch: 'success', dinner: '', snack: 'info' }
  return map[type] || 'info'
}

// ============ 文件选择 ============

function openFilePicker() {
  fileInputRef.value?.click()
}

function onFileSelected(e) {
  const file = e.target.files[0]
  if (file) processFile(file)
  // 重置 input，允许重复选择同一文件
  e.target.value = ''
}

function onFileDrop(e) {
  const file = e.dataTransfer.files[0]
  if (file) processFile(file)
}

function processFile(file) {
  // 验证类型
  const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!validTypes.includes(file.type)) {
    ElMessage.error('仅支持 JPG / PNG / GIF / WebP 格式')
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 10MB')
    return
  }
  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
  recognitionResult.value = null
}

function clearAll() {
  selectedFile.value = null
  previewUrl.value = null
  recognitionResult.value = null
}

// ============ 识别 ============

async function startRecognize() {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择一张食物图片')
    return
  }

  uploading.value = true
  const formData = new FormData()
  formData.append('image', selectedFile.value)

  try {
    const res = await axios.post(`${API_BASE}/api/food/recognize`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 15000,
    })

    if (res.data && res.data.success) {
      recognitionResult.value = res.data.data
      ElMessage.success(`识别成功：${res.data.data.food_name_cn}，${res.data.data.calorie} kcal`)
    } else {
      ElMessage.error(res.data?.error || '识别失败，请重试')
    }
  } catch (err) {
    console.error('识别请求失败:', err)
    if (err.code === 'ECONNREFUSED' || err.message.includes('Network Error')) {
      ElMessage.error('无法连接后端服务，请确保后端已启动 (localhost:5000)')
    } else if (err.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请检查网络后重试')
    } else {
      ElMessage.error('上传失败：' + (err.response?.data?.error || err.message))
    }
  } finally {
    uploading.value = false
  }
}

// ============ 保存记录 ============

async function saveRecord() {
  if (!recognitionResult.value) return
  try {
    const res = await axios.post(`${API_BASE}/api/food/records`, {
      meal_type: selectedMealType.value,
      food_name: recognitionResult.value.food_key,
      food_name_cn: recognitionResult.value.food_name_cn,
      weight_g: recognitionResult.value.weight_g,
      calorie: recognitionResult.value.calorie,
      protein: recognitionResult.value.protein,
      carb: recognitionResult.value.carb,
      fat: recognitionResult.value.fat,
      fiber: recognitionResult.value.fiber,
      image_url: recognitionResult.value.image_url,
      confidence: recognitionResult.value.confidence,
    })
    if (res.data.success) {
      ElMessage.success('已记录到饮食日志')
      loadTodayData()
    }
  } catch (err) {
    ElMessage.error('保存失败：' + (err.response?.data?.error || err.message))
  }
}

async function deleteRecord(id) {
  try {
    await ElMessageBox.confirm('确定要删除这条记录吗？', '确认删除', { type: 'warning' })
    await axios.delete(`${API_BASE}/api/food/records/${id}`)
    ElMessage.success('已删除')
    loadTodayData()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('删除失败')
  }
}

// ============ 重量调整 ============

watch(adjustedWeight, async (newWeight) => {
  if (!recognitionResult.value) return
  try {
    const res = await axios.get(`${API_BASE}/api/food/nutrition/${recognitionResult.value.food_key}`, {
      params: { weight: newWeight },
    })
    if (res.data.success) adjustedNutrition.value = res.data.data
  } catch (e) { /* ignore */ }
})

function applyWeightAdjust() {
  if (adjustedNutrition.value) {
    recognitionResult.value = { ...recognitionResult.value, ...adjustedNutrition.value }
  }
  adjustWeightDialog.value = false
  ElMessage.success('重量已调整')
}

// ============ 数据加载 ============

async function loadTodayData() {
  try {
    const summaryRes = await axios.get(`${API_BASE}/api/food/daily_summary`, {
      params: { date: todayStr.value },
    })
    if (summaryRes.data.success) Object.assign(dailySummary, summaryRes.data.data)
    await loadTodayRecords()
  } catch (err) {
    console.error('加载今日数据失败:', err)
  }
}

async function loadTodayRecords() {
  try {
    const res = await axios.get(`${API_BASE}/api/food/records`, {
      params: { date: todayStr.value, per_page: 50 },
    })
    if (res.data.success) todayRecords.value = res.data.data
  } catch (err) {
    console.error('加载记录失败:', err)
  }
}

async function loadWeeklyTrend() {
  try {
    const res = await axios.get(`${API_BASE}/api/food/weekly_summary`)
    if (res.data.success && chartRef.value) renderChart(res.data.data)
  } catch (err) {
    console.error('加载趋势失败:', err)
  }
}

function renderChart(data) {
  if (!chartRef.value) return
  if (chartInstance) chartInstance.dispose()
  chartInstance = echarts.init(chartRef.value)

  const dates = data.map(d => d.record_date.slice(5))
  const option = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['热量(kcal)', '蛋白质(g)', '碳水(g)', '脂肪(g)'], bottom: 0, textStyle: { fontSize: 10 } },
    grid: { left: 10, right: 10, top: 10, bottom: 30 },
    xAxis: { type: 'category', data: dates, axisLabel: { fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { fontSize: 10 }, splitLine: { lineStyle: { type: 'dashed' } } },
    series: [
      { name: '热量(kcal)', type: 'bar', data: data.map(d => d.total_calorie), itemStyle: { color: '#FF6B6B', borderRadius: [4, 4, 0, 0] } },
      { name: '蛋白质(g)', type: 'line', data: data.map(d => d.total_protein), smooth: true, lineStyle: { color: '#409EFF' }, itemStyle: { color: '#409EFF' } },
      { name: '碳水(g)', type: 'line', data: data.map(d => d.total_carb), smooth: true, lineStyle: { color: '#E6A23C' }, itemStyle: { color: '#E6A23C' } },
      { name: '脂肪(g)', type: 'line', data: data.map(d => d.total_fat), smooth: true, lineStyle: { color: '#67C23A' }, itemStyle: { color: '#67C23A' } },
    ],
  }
  chartInstance.setOption(option)
  window.addEventListener('resize', () => chartInstance?.resize())
}

onMounted(() => {
  loadTodayData()
  nextTick(() => loadWeeklyTrend())
})
</script>

<style scoped>
.food-calorie-page { max-width: 1400px; margin: 0 auto; }

.card-header {
  display: flex; align-items: center; justify-content: space-between;
  font-weight: 600; font-size: 15px;
}
.card-header span { display: flex; align-items: center; gap: 6px; }

/* 上传区域 */
.upload-card { margin-bottom: 20px; }
.upload-area-wrapper { width: 100%; }

.upload-dropzone {
  border: 2px dashed #dcdfe6; border-radius: 8px;
  padding: 50px 20px; text-align: center; cursor: pointer;
  transition: border-color 0.3s, background 0.3s;
}
.upload-dropzone:hover { border-color: #409EFF; background: #f0f7ff; }
.upload-icon { font-size: 48px; color: #c0c4cc; margin-bottom: 12px; }
.upload-text .primary-text { font-size: 15px; color: #606266; margin: 0 0 4px 0; }
.upload-text .secondary-text { font-size: 12px; color: #c0c4cc; margin: 0; }

.preview-container {
  border-radius: 8px; overflow: hidden; max-height: 300px;
  border: 1px solid #ebeef5;
}
.preview-image { width: 100%; max-height: 300px; object-fit: contain; display: block; }

.quick-actions { margin-top: 16px; display: flex; align-items: center; }

/* 识别结果 */
.result-card { margin-bottom: 20px; }
.result-content { text-align: center; }
.food-info { margin-bottom: 16px; }
.food-name { font-size: 20px; font-weight: 600; color: #303133; display: flex; align-items: center; justify-content: center; gap: 8px; }
.food-icon { color: #E6A23C; }
.food-weight { font-size: 13px; color: #909399; }

.calorie-big { margin: 20px 0; }
.calorie-number { font-size: 56px; font-weight: 700; color: #FF6B6B; line-height: 1; }
.calorie-unit { font-size: 18px; color: #909399; margin-left: 4px; }

.nutrition-bars { max-width: 400px; margin: 0 auto 20px; }
.nutrition-item { margin-bottom: 12px; }
.nutrition-label { display: flex; justify-content: space-between; font-size: 13px; color: #606266; margin-bottom: 4px; }
.nutrition-value { font-weight: 600; }
.result-actions { display: flex; gap: 12px; justify-content: center; }

/* 今日汇总 */
.summary-card { margin-bottom: 20px; }
.date-label { font-size: 13px; color: #909399; font-weight: normal; }
.calorie-ring { text-align: center; margin-bottom: 16px; }
.ring-value { font-size: 28px; font-weight: 700; color: #303133; }
.ring-label { font-size: 12px; color: #909399; }

.macro-summary { display: flex; justify-content: space-around; margin-bottom: 8px; }
.macro-item { display: flex; align-items: center; gap: 6px; }
.macro-dot { width: 10px; height: 10px; border-radius: 50%; }
.macro-item.protein .macro-dot { background: #409EFF; }
.macro-item.carb .macro-dot { background: #E6A23C; }
.macro-item.fat .macro-dot { background: #F56C6C; }
.macro-info { display: flex; flex-direction: column; }
.macro-name { font-size: 11px; color: #909399; }
.macro-amount { font-size: 16px; font-weight: 600; color: #303133; }
.meal-count { text-align: center; font-size: 13px; color: #606266; }

/* 趋势图 */
.trend-card { margin-bottom: 20px; }

/* 记录列表 */
.records-list { max-height: 300px; overflow-y: auto; }
.record-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
.record-item:last-child { border-bottom: none; }
.record-left { display: flex; align-items: center; gap: 8px; }
.record-name { font-size: 14px; color: #303133; }
.record-right { display: flex; align-items: center; gap: 8px; }
.record-cal { font-size: 14px; font-weight: 600; color: #FF6B6B; }
.empty-records { padding: 20px 0; }

.weight-preview p { font-size: 14px; color: #606266; margin: 4px 0; }

@media (max-width: 992px) { .el-row { flex-direction: column; } }
</style>
