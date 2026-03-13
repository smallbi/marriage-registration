import { createRouter, createWebHashHistory } from 'vue-router'
import { ElMessage } from 'element-plus'

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/stats',
    children: [
      {
        path: 'stats',
        name: 'Stats',
        component: () => import('../views/Stats.vue'),
        meta: { title: '数据统计' }
      },
      {
        path: 'members',
        name: 'Members',
        component: () => import('../views/Members.vue'),
        meta: { title: '会员管理' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/Users.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'menus',
        name: 'Menus',
        component: () => import('../views/Menus.vue'),
        meta: { title: '菜单管理' }
      },
      {
        path: 'roles',
        name: 'Roles',
        component: () => import('../views/Roles.vue'),
        meta: { title: '角色管理' }
      }
    ],
    meta: { requiresAuth: true }
  }
]

// 创建路由
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 权限检查函数
const checkPermission = (path) => {
  // 从localStorage获取用户菜单权限
  const savedMenus = localStorage.getItem('menus')
  if (!savedMenus) {
    return false
  }

  try {
    const menus = JSON.parse(savedMenus)
    // 检查是否有权限访问目标路径
    return menus.some(menu => menu.path === path)
  } catch (e) {
    console.error('解析菜单失败:', e)
    return false
  }
}

// 路由守卫 - 检查登录状态和权限
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn')

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && isLoggedIn) {
    next('/')
  } else if (to.meta.requiresAuth) {
    // 检查权限
    const targetPath = '/' + to.path.split('/')[1]
    if (!checkPermission(targetPath)) {
      ElMessage.warning('您没有权限访问')
      next(from.fullPath)
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router