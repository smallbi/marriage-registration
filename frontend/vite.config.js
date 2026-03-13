import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://mixinkoma-7gt4hjdoc70dd03b-1317071406.ap-shanghai.app.tcloudbase.com',
        changeOrigin: true
      }
    }
  },
  assetsInclude: ['**/*.svg']
})