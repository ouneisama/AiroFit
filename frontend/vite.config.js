import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  // 核心：打包后的静态资源路径，必须设为根路径
  base: '/', 
  plugins: [vue()],
  resolve: {
    // 配置路径别名（可选，但避免组件导入报错）
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    // 开发环境代理（本地运行 npm run dev 时用）
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      }
    }
  },
  build: {
    // 打包输出目录（默认就是 dist，和你现在的一致）
    outDir: 'dist',
    // 静态资源目录
    assetsDir: 'assets'
  }
})