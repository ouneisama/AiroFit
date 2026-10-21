// 1. 导入Vue核心方法
import { createApp } from 'vue'

// 2. 导入根组件
import App from './App.vue'

// 3. 导入路由实例
import router from './router'

// 4. 导入Element Plus及样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 5. 导入Element Plus所有图标（解决图标不显示问题）
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 6. 可选：导入Element Plus中文语言包（解决组件默认英文问题）
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

// 7. 创建Vue应用实例
const app = createApp(App)

// 8. 全局注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 9. 挂载路由、Element Plus（配置中文）
app.use(router)
app.use(ElementPlus, {
  locale: zhCn, // 设置Element Plus为中文
})

// 10. 挂载应用到#app节点（必须最后执行）
app.mount('#app')

// 可选：全局错误捕获（防止代码报错导致页面空白）
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue全局错误：', err, info)
  // 可在这里添加用户友好的错误提示
}

// 可选：关闭生产环境提示（上线时开启）
// app.config.productionTip = false