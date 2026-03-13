<template>
  <el-container class="layout">
    <!-- 移动端：侧边栏改为抽屉 -->
    <el-drawer v-model="drawerVisible" direction="ltr" size="210px" :show-close="false" class="mobile-drawer">
      <div class="drawer-logo">
        <el-icon :size="24" color="#409eff">
          <Connection />
        </el-icon>
        <span class="logo-text">丽姐·锦绣谱</span>
      </div>
      <el-menu :default-active="activeMenu" class="layout-menu" background-color="#1d2939" text-color="#8b949e"
        active-text-color="#fff" :router="true" @select="handleMenuSelect">
        <template v-for="menu in dynamicMenus" :key="menu.id">
          <el-menu-item :index="menu.path">
            <el-icon>
              <component :is="menu.icon || 'Menu'" />
            </el-icon>
            <template #title>{{ menu.name }}</template>
          </el-menu-item>
        </template>
      </el-menu>
    </el-drawer>

    <!-- 左侧 aside（桌面端） -->
    <el-aside class="layout-aside desktop-only">
      <div class="aside-box" :style="{ width: isCollapse ? '65px' : '210px' }">
        <!-- Logo 部分 -->
        <div class="logo flx-center">
          <el-icon :size="24" color="#409eff">
            <Connection />
          </el-icon>
          <span v-show="!isCollapse" class="logo-text">丽姐·锦绣谱</span>
        </div>

        <!-- 导航菜单 -->
        <el-scrollbar>
          <el-menu :default-active="activeMenu" class="layout-menu" background-color="#1d2939" text-color="#8b949e"
            active-text-color="#fff" :router="true" :collapse="isCollapse" :collapse-transition="false">
            <!-- 动态菜单 -->
            <template v-for="menu in dynamicMenus" :key="menu.id">
              <el-menu-item :index="menu.path">
                <el-icon>
                  <component :is="menu.icon || 'Menu'" />
                </el-icon>
                <template #title>{{ menu.name }}</template>
              </el-menu-item>
            </template>
          </el-menu>
        </el-scrollbar>
      </div>
    </el-aside>

    <!-- 右侧 section -->
    <el-container class="layout-section">
      <!-- 右侧顶部导航 -->
      <el-header class="section-header">
        <div class="header-left">
          <!-- 移动端：汉堡菜单 -->
          <el-icon class="collapse-icon mobile-only" @click="drawerVisible = true">
            <Menu />
          </el-icon>
          <!-- 桌面端：收缩按钮 -->
          <el-icon class="collapse-icon desktop-only" @click="handleCollapse">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
          <el-breadcrumb separator="/" class="breadcrumb">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <div class="user-info">
            <el-dropdown @command="handleCommand">
              <div class="user-dropdown">
                <div class="avatar">
                  <img src="../assets/images/avatar.gif" alt="avatar" />
                </div>
                <span class="username">{{ username }}</span>
                <el-icon class="arrow-icon">
                  <ArrowDown />
                </el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">
                    <el-icon>
                      <SwitchButton />
                    </el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>

      <!-- 右侧主内容 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { Connection, User, UserFilled, ArrowDown, SwitchButton, DataAnalysis, Fold, Expand, Menu } from '@element-plus/icons-vue'

  const router = useRouter()
  const route = useRoute()

  // 侧边栏收缩状态
  const isCollapse = ref(false)
  const drawerVisible = ref(false) // 移动端抽屉
  const username = ref('Admin')
  const dynamicMenus = ref([])

  const activeMenu = computed(() => route.path)

  const currentPageTitle = computed(() => {
    // 先从动态菜单中查找
    const menu = dynamicMenus.value.find(m => m.path === route.path)
    if (menu) return menu.name
    
    // 备用静态映射
    const titles = {
      '/stats': '数据统计',
      '/members': '人员信息',
      '/users': '用户管理',
      '/menus': '菜单管理',
      '/roles': '角色管理'
    }
    return titles[route.path] || '首页'
  })

  // 收缩/展开侧边栏
  const handleCollapse = () => {
    isCollapse.value = !isCollapse.value
  }

  // 移动端：菜单选中后关闭抽屉
  const handleMenuSelect = () => {
    drawerVisible.value = false
  }

  // 获取用户名和菜单
  onMounted(() => {
    const savedUsername = localStorage.getItem('username')
    if (savedUsername) {
      username.value = savedUsername
    }
    
    // 从localStorage加载动态菜单
    const savedMenus = localStorage.getItem('menus')
    if (savedMenus) {
      try {
        dynamicMenus.value = JSON.parse(savedMenus)
      } catch (e) {
        console.error('解析菜单失败:', e)
      }
    } else {
      // 如果没有菜单，使用默认菜单
      dynamicMenus.value = [
        { id: 1, name: '数据统计', path: '/stats', icon: 'DataAnalysis' },
        { id: 2, name: '人员记录', path: '/members', icon: 'User' },
        { id: 3, name: '用户管理', path: '/users', icon: 'UserFilled' },
        { id: 4, name: '菜单管理', path: '/menus', icon: 'Menu' },
        { id: 5, name: '角色管理', path: '/roles', icon: 'UserFilled' }
      ]
    }
  })

  // 处理下拉菜单
  const handleCommand = async (command) => {
    if (command === 'logout') {
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        localStorage.removeItem('isLoggedIn')
        localStorage.removeItem('username')
        localStorage.removeItem('menus')
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch {
        // 取消
      }
    }
  }
</script>

<style scoped>
  .layout {
    width: 100%;
    height: 100vh;
  }

  /* 左侧 aside */
  .layout-aside {
    background: #1d2939;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    transition: width 0.3s ease;
  }

  .aside-box {
    display: flex;
    flex-direction: column;
    height: 100%;
    transition: width 0.3s ease;
  }

  /* Logo 部分 */
  .logo {
    box-sizing: border-box;
    height: 55px;
    display: flex;
    align-items: center;
    gap: 10px;
    color: white;
    padding: 0 20px;
  }

  .logo-text {
    font-size: 21.5px;
    font-weight: bold;
    white-space: nowrap;
  }

  /* 导航菜单 */
  .layout-menu {
    flex: 1;
    width: 100%;
    border-right: none;
  }

  .el-aside {
    width: auto;
    min-width: 65px;
  }

  .el-scrollbar {
    height: calc(100% - 55px);
  }

  .layout-menu .el-menu-item {
    height: 48px;
    line-height: 48px;
    margin: 0;
    border-radius: 0;
    transition: all 0.3s ease;
  }

  .layout-menu .el-menu-item:hover {
    color: rgba(255, 255, 255, 0.8);
    background: rgba(64, 158, 255, 0.1) !important;
  }

  .layout-menu .el-menu-item.is-active {
    color: #ffffff !important;
    background: rgba(64, 158, 255, 0.2) !important;
    position: relative;
  }

  .layout-menu .el-menu-item.is-active::before {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 4px;
    content: "";
    background-color: var(--el-color-primary, #409eff);
  }

  /* 收起时的菜单样式 */
  .el-aside .el-menu--collapse .el-menu-item {
    padding: 0 calc(50% - 14px);
  }

  .el-aside .el-menu--collapse .el-menu-item span {
    display: none;
  }

  .el-aside .el-menu--collapse .el-menu-item.is-active {
    background: rgba(64, 158, 255, 0.3) !important;
  }

  /* 右侧 section */
  .layout-section {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  /* 右侧顶部导航 */
  .section-header {
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 55px;
    padding: 0 15px;
    background: white;
    border-bottom: 1px solid #eaeef1;
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .collapse-icon {
    font-size: 20px;
    color: #606266;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.2s;
  }

  .collapse-icon:hover {
    background: #f5f7fa;
    color: #409eff;
  }

  .breadcrumb {
    font-size: 14px;
  }

  .header-right {
    display: flex;
    align-items: center;
  }

  .user-info {
    display: flex;
    align-items: center;
  }

  .user-dropdown {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 8px 12px;
    border-radius: 8px;
    transition: background 0.2s;
  }

  .user-dropdown:hover {
    background: #f5f7fa;
  }

  .avatar {
    width: 40px;
    height: 40px;
    overflow: hidden;
    cursor: pointer;
    border-radius: 50%;

    img {
      width: 100%;
      height: 100%;
    }
  }

  .username {
    font-size: 14px;
    color: #303133;
    white-space: nowrap;
  }

  .arrow-icon {
    font-size: 12px;
    color: #909399;
  }

  /* 右侧主内容 */
  .main-content {
    flex: 1;
    background: #f0f2f5;
    padding: 20px;
    overflow: auto;
  }

  /* 辅助类 */
  .flx-center {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* ====== 响应式样式 ====== */
  /* 显示/隐藏控制 */
  .mobile-only {
    display: none;
  }
  .desktop-only {
    display: block;
  }

  /* 移动端抽屉 */
  .mobile-drawer .el-drawer__body {
    padding: 0;
    background: #1d2939;
  }
  .drawer-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    height: 55px;
    padding: 0 20px;
    color: white;
    background: #1d2939;
  }
  .drawer-logo .logo-text {
    font-size: 18px;
    font-weight: bold;
  }
  .mobile-drawer .layout-menu {
    border-right: none;
  }

  /* 响应式断点：768px 以下 */
  @media (max-width: 768px) {
    .mobile-only {
      display: block;
    }
    .desktop-only {
      display: none;
    }
    .main-content {
      padding: 12px;
    }
  }
</style>