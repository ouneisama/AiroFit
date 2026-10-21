<template>
  <div class="community-page">
    <!-- 发布模块 -->
    <div class="publish-card">
      <h3>分享健身动态</h3>
      <el-input
        v-model="content"
        type="textarea"
        :rows="3"
        placeholder="分享你的训练、饮食、心得..."
        class="text-area"
      />

      <!-- 图片预览区 -->
      <div class="img-preview" v-if="previewList.length">
        <div class="preview-item" v-for="(img, i) in previewList" :key="i">
          <img :src="img" alt="预览" />
          <span class="del" @click="delImg(i)">×</span>
        </div>
      </div>

      <!-- 上传 + 发布 -->
      <div class="btn-group">
        <el-button type="primary" plain @click="chooseImg">
          {{ previewList.length > 0 ? `已选 ${previewList.length} 张` : '添加图片' }}
        </el-button>
        <el-button type="primary" @click="publish" :loading="loading">
          发布动态
        </el-button>
      </div>

      <input
        ref="fileInput"
        type="file"
        multiple
        accept="image/*"
        style="display: none"
        @change="handleImgChange"
      />
    </div>

    <!-- 动态列表 -->
    <div class="post-list">
      <div class="post-item" v-for="item in postList" :key="item.id">
        <div class="content">{{ item.content }}</div>
        <div class="img-list" v-if="item.image_urls.length">
          <img v-for="(img, i) in item.image_urls" :key="i" :src="img" alt="动态图片" />
        </div>
        <div class="time">{{ item.time }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 接口地址（和你后端完全一致）
const api = axios.create({ baseURL: 'http://localhost:5000/api' })

// 数据
const content = ref('')
const fileList = ref([])
const previewList = ref([])
const postList = ref([])
const loading = ref(false)
const fileInput = ref(null)

// 选择图片
const chooseImg = () => fileInput.value.click()

// 图片预览
const handleImgChange = (e) => {
  const files = e.target.files
  if (!files) return
  for (let f of files) {
    fileList.value.push(f)
    const reader = new FileReader()
    reader.onload = (ev) => previewList.value.push(ev.target.result)
    reader.readAsDataURL(f)
  }
}

// 删除预览图
const delImg = (idx) => {
  fileList.value.splice(idx, 1)
  previewList.value.splice(idx, 1)
}

// 发布动态（文字 + 多图）
const publish = async () => {
  if (!content.value.trim()) return ElMessage.warning('请输入内容')
  loading.value = true

  const form = new FormData()
  form.append('content', content.value)
  fileList.value.forEach(f => form.append('images', f))

  try {
    await api.post('/posts', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    ElMessage.success('发布成功')
    content.value = ''
    fileList.value = []
    previewList.value = []
    loadPosts()
  } catch (err) {
    ElMessage.error('发布失败')
    console.error(err)
  } finally {
    loading.value = false
  }
}

// 加载动态列表
const loadPosts = async () => {
  try {
    const res = await api.get('/posts')
    postList.value = res.data
  } catch (err) {
    console.error('加载失败', err)
  }
}

onMounted(() => loadPosts())
</script>

<style scoped>
.community-page {
  padding: 20px;
  background: #f0f9f4;
  min-height: 100vh;
}

.publish-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 1px 5px #00000010;
}

.publish-card h3 {
  margin: 0 0 12px 0;
  color: #254d41;
  font-size: 16px;
}

.text-area {
  margin-bottom: 12px;
}

.img-preview {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.preview-item {
  position: relative;
  width: 80px;
  height: 80px;
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

.del {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #ff4444;
  color: #fff;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  cursor: pointer;
}

.btn-group {
  display: flex;
  gap: 10px;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.post-item {
  background: #fff;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 1px 5px #00000010;
}

.post-item .content {
  margin-bottom: 10px;
  color: #333;
}

.img-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.img-list img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
}

.post-item .time {
  font-size: 12px;
  color: #999;
  text-align: right;
}
</style>