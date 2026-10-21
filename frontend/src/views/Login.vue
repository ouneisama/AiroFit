<template>
  <div class="login-container">
    <!-- 左侧品牌区 -->
    <div class="login-left">
      <div class="brand-content">
        <div class="logo-box">
          <div class="default-logo">
            <!-- 用Aim图标替代Fitness -->
            <el-icon size="60" color="#fff"><Aim /></el-icon>
          </div>
        </div>
        <h1 class="brand-title">AI智能健身系统</h1>
        <p class="brand-desc">专业的智能健身管理平台，让健身更科学、更高效</p>
      </div>
    </div>

    <!-- 右侧登录区 -->
    <div class="login-right">
      <div class="login-box">
        <div class="login-header">
          <h2 class="login-title">欢迎登录</h2>
          <p class="login-subtitle">请输入账号密码登录系统</p>
        </div>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          autocomplete="off"
        >
          <el-form-item prop="username" class="form-item">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              class="input-item"
              prefix-icon="User"
            />
          </el-form-item>

          <el-form-item prop="password" class="form-item">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              class="input-item"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item class="form-item verify-item">
            <el-row :gutter="10">
              <el-col :span="16">
                <el-input
                  v-model="loginForm.verifyCode"
                  placeholder="请输入验证码"
                  size="large"
                  class="input-item"
                  prefix-icon="Tickets"
                />
              </el-col>
              <el-col :span="8">
                <div class="verify-code-img" @click="refreshVerifyCode">
                  <img :src="verifyCodeUrl" alt="验证码" />
                </div>
              </el-col>
            </el-row>
          </el-form-item>

          <el-form-item class="form-item remember-item">
            <el-checkbox v-model="loginForm.remember" size="large">
              记住密码
            </el-checkbox>
            <el-link type="primary" class="forget-link" @click="showForgetPwd">
              忘记密码？
            </el-link>
          </el-form-item>

          <el-form-item class="form-item">
            <el-button
              type="primary"
              size="large"
              class="login-btn"
              @click="handleLogin"
              :loading="isLoading"
            >
              登录
            </el-button>
          </el-form-item>

          <div class="other-login">
            <span class="divider">其他登录方式</span>
            <div class="login-icons">
              <!-- 用Message图标替代Wechat，用Suitcase图标替代Github -->
              <el-icon class="icon-item" @click="otherLogin('wechat')"><Message /></el-icon>
              <el-icon class="icon-item" @click="otherLogin('weibo')"><Promotion /></el-icon>
              <el-icon class="icon-item" @click="otherLogin('github')"><Suitcase /></el-icon>
            </div>
          </div>
        </el-form>
      </div>
    </div>

    <!-- 忘记密码弹窗 -->
    <el-dialog
      v-model="forgetPwdDialog"
      title="找回密码"
      width="400px"
      center
      destroy-on-close
    >
      <el-form :model="forgetForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="forgetForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="绑定邮箱">
          <el-input v-model="forgetForm.email" placeholder="请输入注册邮箱" />
        </el-form-item>
        <el-form-item label="验证码">
          <el-input v-model="forgetForm.code" placeholder="请输入验证码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="forgetPwdDialog = false">取消</el-button>
        <el-button type="primary" @click="resetPwd">确认重置</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
// 导入所有真实存在的图标
import { 
  Aim, User, Lock, Tickets, 
  Message, Promotion, Suitcase 
} from '@element-plus/icons-vue'

const router = useRouter()
const isLoading = ref(false)
const forgetPwdDialog = ref(false)
const verifyCodeUrl = ref(`https://picsum.photos/120/40?random=${Math.random()}`)
const loginFormRef = ref(null)

const loginForm = reactive({
  username: '',
  password: '',
  verifyCode: '',
  remember: false
})

const forgetForm = reactive({
  username: '',
  email: '',
  code: ''
})

const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不少于6个字符', trigger: 'blur' }
  ],
  verifyCode: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 4, message: '验证码长度为4位', trigger: 'blur' }
  ]
})

const refreshVerifyCode = () => {
  verifyCodeUrl.value = `https://picsum.photos/120/40?random=${Math.random()}`
}

const showForgetPwd = () => {
  forgetPwdDialog.value = true
}

const resetPwd = () => {
  if (!forgetForm.username || !forgetForm.email || !forgetForm.code) {
    ElMessage.error('请完善所有信息')
    return
  }
  ElMessage.success('密码重置成功，请使用新密码登录')
  forgetPwdDialog.value = false
  forgetForm.username = ''
  forgetForm.email = ''
  forgetForm.code = ''
}

const otherLogin = (type) => {
  ElMessage.info(`暂未开放${type === 'wechat' ? '微信' : type === 'weibo' ? '微博' : 'Github'}登录`)
}

const handleLogin = async () => {
  try {
    await loginFormRef.value.validate()
    isLoading.value = true

    setTimeout(() => {
      if (loginForm.username === 'test_user' && loginForm.password === '123456' && loginForm.verifyCode.length === 4) {
        localStorage.setItem('token', 'fitness_' + Date.now())
        localStorage.setItem('username', loginForm.username)
        ElMessage.success('登录成功！即将进入系统')
        router.push('/home')
      } else {
        ElMessage.error('用户名/密码/验证码错误，请检查')
        refreshVerifyCode()
      }
      isLoading.value = false
    }, 1000)
  } catch (error) {
    ElMessage.error('请完善所有必填信息')
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  overflow: hidden;
}

.login-left {
  width: 55%;
  height: 100%;
  background: linear-gradient(135deg, #2c5364 0%, #203a43 50%, #0f2027 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 60px;
  box-sizing: border-box;
}

.brand-content {
  color: #fff;
  text-align: center;
}

.logo-box {
  margin-bottom: 40px;
}

.default-logo {
  width: 120px;
  height: 120px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.brand-title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 20px;
  letter-spacing: 2px;
}

.brand-desc {
  font-size: 18px;
  line-height: 1.6;
  opacity: 0.9;
}

.login-right {
  width: 45%;
  height: 100%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-box {
  width: 100%;
  max-width: 400px;
  padding: 0 40px;
  box-sizing: border-box;
}

.login-header {
  margin-bottom: 40px;
  text-align: center;
}

.login-title {
  font-size: 28px;
  color: #333;
  font-weight: 600;
  margin-bottom: 8px;
}

.login-subtitle {
  font-size: 14px;
  color: #666;
}

.login-form {
  width: 100%;
}

.form-item {
  margin-bottom: 20px !important;
}

.input-item {
  width: 100%;
  height: 50px;
  border-radius: 8px !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
}

.verify-item {
  margin-bottom: 15px !important;
}

.verify-code-img {
  width: 100%;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
}

.verify-code-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remember-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px !important;
}

.forget-link {
  font-size: 14px;
}

.login-btn {
  width: 100%;
  height: 50px;
  background: #2c5364 !important;
  border: none !important;
  border-radius: 8px !important;
  font-size: 16px !important;
  font-weight: 500 !important;
}

.login-btn:hover {
  background: #203a43 !important;
}

.other-login {
  margin-top: 30px;
  text-align: center;
}

.divider {
  display: block;
  font-size: 14px;
  color: #999;
  margin-bottom: 20px;
  position: relative;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30%;
  height: 1px;
  background: #e5e5e5;
}

.divider::before { left: 0; }
.divider::after { right: 0; }

.login-icons {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.icon-item {
  font-size: 24px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.icon-item:hover {
  color: #2c5364;
  transform: scale(1.1);
}

@media (max-width: 992px) {
  .login-left { width: 50%; padding: 0 30px; }
  .login-right { width: 50%; }
  .brand-title { font-size: 28px; }
  .brand-desc { font-size: 16px; }
}

@media (max-width: 768px) {
  .login-left { display: none; }
  .login-right { width: 100%; }
  .login-box { max-width: 350px; }
}
</style>