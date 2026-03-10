<template>
  <div class="login-container flx-center" :style="{ backgroundImage: `url(${loginLeftImg})` }">
    <div class="login-box">
      <div class="login-left">
        <img class="login-left-img" src="../assets/images/login_left.png" alt="login" />
      </div>
      <div class="login-form">
        <div class="login-logo">
          <h2 class="logo-text">婚介信息管理</h2>
        </div>
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" size="large">
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名">
              <template #prefix>
                <el-icon class="el-input__icon">
                  <User />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password
              autocomplete="new-password">
              <template #prefix>
                <el-icon class="el-input__icon">
                  <Lock />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>
        </el-form>
        <div class="login-btn">
          <el-button round size="large" @click="resetForm"> 重置 </el-button>
          <el-button round size="large" type="primary" :loading="loading" @click="handleLogin">
            登录
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
  import { useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus'
  import { Connection, User, Lock } from '@element-plus/icons-vue'
  import loginLeftImg from '../assets/images/login_left.png'

  const router = useRouter()
  const loginFormRef = ref(null)
  const loading = ref(false)

  // 登录表单
  const loginForm = reactive({
    username: '',
    password: ''
  })

  // 验证规则
  const loginRules = {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, message: '密码至少6位', trigger: 'blur' }
    ]
  }

  // 登录处理
  const handleLogin = async () => {
    if (!loginFormRef.value) return

    await loginFormRef.value.validate(async (valid) => {
      if (!valid) return

      loading.value = true

      try {
        // 使用登录接口进行验证
        const response = await fetch('http://localhost:8000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(loginForm)
        })
        
        if (!response.ok) throw new Error('登录请求失败')
        
        const result = await response.json()
        
        if (result.success) {
          // 保存登录状态
          localStorage.setItem('isLoggedIn', 'true')
          localStorage.setItem('username', loginForm.username)

          ElMessage.success('登录成功，欢迎回来！')
          router.push('/')
        } else {
          ElMessage.error(result.message)
        }
      } catch (error) {
        console.error('登录验证失败:', error)
        ElMessage.error('登录验证失败，请稍后重试')
      } finally {
        loading.value = false
      }
    })
  }

  // 重置表单
  const resetForm = () => {
    if (loginFormRef.value) {
      loginFormRef.value.resetFields()
    }
  }

  // 监听回车键
  onMounted(() => {
    document.onkeydown = (e) => {
      if (e.code === "Enter" || e.code === "enter" || e.code === "NumpadEnter") {
        if (loading.value) return
        handleLogin()
      }
    }
  })

  onBeforeUnmount(() => {
    document.onkeydown = null
  })
</script>

<style scoped>
  .login-container {
    height: 100vh;
    min-height: 550px;
    background-color: #eeeeee;
    background-size: 100% 100%;
    background-size: cover;
  }

  .login-box {
    position: relative;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: space-around;
    width: 96.5%;
    height: 94%;
    padding: 0 50px;
    background-color: rgb(255 255 255 / 80%);
    border-radius: 10px;
  }

  .login-left {
    width: 800px;
    margin-right: 10px;
  }

  .login-left-img {
    width: 100%;
    height: 100%;
  }

  .login-form {
    width: 420px;
    padding: 50px 40px 45px;
    background-color: var(--el-bg-color);
    border-radius: 10px;
    box-shadow: rgb(0 0 0 / 10%) 0 2px 10px 2px;
  }

  .login-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 45px;
  }

  .login-logo el-icon {
    color: #409eff;
  }

  .logo-text {
    padding: 0 0 0 25px;
    margin: 0;
    font-size: 42px;
    font-weight: bold;
    color: #34495e;
    white-space: nowrap;
  }

  .login-form .el-form-item {
    margin-bottom: 40px;
  }

  .login-btn {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 40px;
    white-space: nowrap;
  }

  .login-btn .el-button {
    width: 185px;
  }

  @media screen and (width <=1250px) {
    .login-left {
      display: none;
    }
  }

  @media screen and (width <=600px) {
    .login-form {
      width: 97% !important;
    }
  }

  /* 辅助类 */
  .flx-center {
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>