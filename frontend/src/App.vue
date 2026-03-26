<template>
  <router-view />
</template>

<script setup>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'

  const router = useRouter()

  // 检查登录状态
  onMounted(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn')
    if (!isLoggedIn && router.currentRoute.value.path !== '/login') {
      router.push('/login')
    }
  })
</script>

<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: #f5f7fa;
  }

  /* Element Plus 主题色覆盖 - 紫色主题 */
  :root {
    --el-color-primary: #8b5cf6;
    --el-color-primary-light-3: #a78bfa;
    --el-color-primary-light-5: #c4b5fd;
    --el-color-primary-light-7: #ddd6fe;
    --el-color-primary-light-9: #ede9fe;
    --el-color-primary-dark-2: #7c3aed;
    --el-color-primary-dark-3: #6d28d9;
  }
</style>