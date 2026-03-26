<template>
  <div class="grid min-h-screen lg:grid-cols-2">
    <!-- Left Content Section -->
    <div
      class="relative hidden flex-col justify-between bg-gradient-to-br from-primary/90 via-primary to-primary/80 p-12 text-primary-foreground lg:flex">
      <div class="relative z-20 flex flex-col items-center" style="padding-top: 40px;">
        <div class="flex items-center gap-2 text-lg font-semibold">
          <div class="flex size-8 items-center justify-center rounded-lg bg-primary-foreground/10 backdrop-blur-sm">
            <Sparkles class="size-4" />
          </div>
          <span>丽姐·锦绣谱</span>
        </div>
      </div>

      <div class="relative z-20 flex h-[500px] items-end justify-center">
        <!-- Cartoon Characters -->
        <div class="relative" style="width: 550px; height: 400px">
          <!-- Purple tall rectangle character - Back layer -->
          <div ref="purpleRef" class="absolute bottom-0 transition-all duration-700 ease-in-out" :style="{
              left: '70px',
              width: '180px',
              height: isTyping || (password.length > 0 && !showPassword) ? '440px' : '400px',
              backgroundColor: '#8b5cf6',
              borderRadius: '10px 10px 0 0',
              zIndex: 1,
              transform: password.length > 0 && showPassword
                ? 'skewX(0deg)'
                : isTyping || (password.length > 0 && !showPassword)
                ? `skewX(${purplePos.bodySkew - 12}deg) translateX(40px)`
                : `skewX(${purplePos.bodySkew}deg)`,
              transformOrigin: 'bottom center'
            }">
            <!-- Eyes -->
            <div class="absolute flex gap-8 transition-all duration-700 ease-in-out" :style="{
                left: password.length > 0 && showPassword
                  ? '20px'
                  : isLookingAtEachOther
                  ? '55px'
                  : `${45 + purplePos.faceX}px`,
                top: password.length > 0 && showPassword
                  ? '35px'
                  : isLookingAtEachOther
                  ? '65px'
                  : `${40 + purplePos.faceY}px`
              }">
              <EyeBall :size="18" :pupilSize="7" :maxDistance="5" eyeColor="white" pupilColor="#2D2D2D"
                :isBlinking="isPurpleBlinking"
                :forceLookX="password.length > 0 && showPassword ? (isPurplePeeking ? 4 : -4) : (isLookingAtEachOther ? 3 : undefined)"
                :forceLookY="password.length > 0 && showPassword ? (isPurplePeeking ? 5 : -4) : (isLookingAtEachOther ? 4 : undefined)" />
              <EyeBall :size="18" :pupilSize="7" :maxDistance="5" eyeColor="white" pupilColor="#2D2D2D"
                :isBlinking="isPurpleBlinking"
                :forceLookX="password.length > 0 && showPassword ? (isPurplePeeking ? 4 : -4) : (isLookingAtEachOther ? 3 : undefined)"
                :forceLookY="password.length > 0 && showPassword ? (isPurplePeeking ? 5 : -4) : (isLookingAtEachOther ? 4 : undefined)" />
            </div>
          </div>

          <!-- Black tall rectangle character - Middle layer -->
          <div ref="blackRef" class="absolute bottom-0 transition-all duration-700 ease-in-out" :style="{
              left: '240px',
              width: '120px',
              height: '310px',
              backgroundColor: '#2D2D2D',
              borderRadius: '8px 8px 0 0',
              zIndex: 2,
              transform: password.length > 0 && showPassword
                ? 'skewX(0deg)'
                : isLookingAtEachOther
                ? `skewX(${blackPos.bodySkew * 1.5 + 10}deg) translateX(20px)`
                : isTyping || (password.length > 0 && !showPassword)
                ? `skewX(${blackPos.bodySkew * 1.5}deg)`
                : `skewX(${blackPos.bodySkew}deg)`,
              transformOrigin: 'bottom center'
            }">
            <!-- Eyes -->
            <div class="absolute flex gap-6 transition-all duration-700 ease-in-out" :style="{
                left: password.length > 0 && showPassword
                  ? '10px'
                  : isLookingAtEachOther
                  ? '32px'
                  : `${26 + blackPos.faceX}px`,
                top: password.length > 0 && showPassword
                  ? '28px'
                  : isLookingAtEachOther
                  ? '12px'
                  : `${32 + blackPos.faceY}px`
              }">
              <EyeBall :size="16" :pupilSize="6" :maxDistance="4" eyeColor="white" pupilColor="#2D2D2D"
                :isBlinking="isBlackBlinking"
                :forceLookX="password.length > 0 && showPassword ? -4 : (isLookingAtEachOther ? 0 : undefined)"
                :forceLookY="password.length > 0 && showPassword ? -4 : (isLookingAtEachOther ? -4 : undefined)" />
              <EyeBall :size="16" :pupilSize="6" :maxDistance="4" eyeColor="white" pupilColor="#2D2D2D"
                :isBlinking="isBlackBlinking"
                :forceLookX="password.length > 0 && showPassword ? -4 : (isLookingAtEachOther ? 0 : undefined)"
                :forceLookY="password.length > 0 && showPassword ? -4 : (isLookingAtEachOther ? -4 : undefined)" />
            </div>
          </div>

          <!-- Orange semi-circle character - Front left -->
          <div ref="orangeRef" class="absolute bottom-0 transition-all duration-700 ease-in-out" :style="{
              left: '0px',
              width: '240px',
              height: '200px',
              zIndex: 3,
              backgroundColor: '#FF9B6B',
              borderRadius: '120px 120px 0 0',
              transform: password.length > 0 && showPassword ? 'skewX(0deg)' : `skewX(${orangePos.bodySkew}deg)`,
              transformOrigin: 'bottom center'
            }">
            <!-- Eyes - just pupils, no white -->
            <div class="absolute flex gap-8 transition-all duration-200 ease-out" :style="{
                left: password.length > 0 && showPassword
                  ? '50px'
                  : `${82 + orangePos.faceX}px`,
                top: password.length > 0 && showPassword
                  ? '85px'
                  : `${90 + orangePos.faceY}px`
              }">
              <Pupil :size="12" :maxDistance="5" pupilColor="#2D2D2D"
                :forceLookX="password.length > 0 && showPassword ? -5 : undefined"
                :forceLookY="password.length > 0 && showPassword ? -4 : undefined" />
              <Pupil :size="12" :maxDistance="5" pupilColor="#2D2D2D"
                :forceLookX="password.length > 0 && showPassword ? -5 : undefined"
                :forceLookY="password.length > 0 && showPassword ? -4 : undefined" />
            </div>
          </div>

          <!-- Yellow tall rectangle character - Front right -->
          <div ref="yellowRef" class="absolute bottom-0 transition-all duration-700 ease-in-out" :style="{
              left: '310px',
              width: '140px',
              height: '230px',
              backgroundColor: '#E8D754',
              borderRadius: '70px 70px 0 0',
              zIndex: 4,
              transform: password.length > 0 && showPassword ? 'skewX(0deg)' : `skewX(${yellowPos.bodySkew}deg)`,
              transformOrigin: 'bottom center'
            }">
            <!-- Eyes - just pupils, no white -->
            <div class="absolute flex gap-6 transition-all duration-200 ease-out" :style="{
                left: password.length > 0 && showPassword
                  ? '20px'
                  : `${52 + yellowPos.faceX}px`,
                top: password.length > 0 && showPassword
                  ? '35px'
                  : `${40 + yellowPos.faceY}px`
              }">
              <Pupil :size="12" :maxDistance="5" pupilColor="#2D2D2D"
                :forceLookX="password.length > 0 && showPassword ? -5 : undefined"
                :forceLookY="password.length > 0 && showPassword ? -4 : undefined" />
              <Pupil :size="12" :maxDistance="5" pupilColor="#2D2D2D"
                :forceLookX="password.length > 0 && showPassword ? -5 : undefined"
                :forceLookY="password.length > 0 && showPassword ? -4 : undefined" />
            </div>
            <!-- Horizontal line for mouth -->
            <div class="absolute h-[4px] w-20 rounded-full bg-[#2D2D2D] transition-all duration-200 ease-out" :style="{
                left: password.length > 0 && showPassword
                  ? '10px'
                  : `${40 + yellowPos.faceX}px`,
                top: password.length > 0 && showPassword
                  ? '88px'
                  : `${88 + yellowPos.faceY}px`
              }" />
          </div>
        </div>
      </div>

      <div class="relative z-20 flex items-center gap-8 text-sm text-primary-foreground/60">
        <a href="#" class="transition-colors hover:text-primary-foreground">
          隐私政策
        </a>
        <a href="#" class="transition-colors hover:text-primary-foreground">
          服务条款
        </a>
        <a href="#" class="transition-colors hover:text-primary-foreground">
          联系我们
        </a>
      </div>

      <!-- Decorative elements -->
      <div class="bg-grid-white/[0.05] absolute inset-0 bg-[size:20px_20px]" />
      <div class="absolute top-1/4 right-1/4 size-64 rounded-full bg-primary-foreground/10 blur-3xl" />
      <div class="absolute bottom-1/4 left-1/4 size-96 rounded-full bg-primary-foreground/5 blur-3xl" />
    </div>

    <!-- Right Login Section -->
    <div class="flex items-center justify-center bg-background p-8">
      <div class="w-full max-w-[420px]">
        <!-- Mobile Logo -->
        <div class="mb-12 flex items-center justify-center gap-2 text-lg font-semibold lg:hidden">
          <div class="flex size-8 items-center justify-center rounded-lg bg-primary/10">
            <Sparkles class="size-4 text-primary" />
          </div>
          <span>丽姐·锦绣谱</span>
        </div>

        <!-- Header -->
        <div class="text-center" style="margin-bottom: 40px;">
          <h1 class="text-3xl font-bold tracking-tight">
            Welcome back!
          </h1>
        </div>

        <!-- Login Form -->
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" size="large">
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名" @focus="setIsTyping(true)"
              @blur="setIsTyping(false)">
              <template #prefix>
                <el-icon class="el-input__icon">
                  <User />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="loginForm.password" :type="showPassword ? 'text' : 'password'" placeholder="请输入密码"
              autocomplete="new-password">
              <template #prefix>
                <el-icon class="el-input__icon">
                  <Lock />
                </el-icon>
              </template>
              <template #suffix>
                <el-icon class="el-input__icon cursor-pointer" @click="showPassword = !showPassword">
                  <View v-if="!showPassword" />
                  <Hide v-else />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>
        </el-form>
        <div class="login-btn" style="margin-top: 32px;">
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
  import { ref, reactive, onMounted, onUnmounted, computed, onBeforeUnmount } from 'vue'
  import { useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus'
  import { User, Lock, View, Hide } from '@element-plus/icons-vue'
  import { Sparkles } from 'lucide-vue-next'
  import Pupil from '../components/eyes/Pupil.vue'
  import EyeBall from '../components/eyes/EyeBall.vue'
  import { API_BASE_URL } from '../config/api'

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

  // Animation state
  const showPassword = ref(false)
  const mouseX = ref(0)
  const mouseY = ref(0)
  const isPurpleBlinking = ref(false)
  const isBlackBlinking = ref(false)
  const isTyping = ref(false)
  const isLookingAtEachOther = ref(false)
  const isPurplePeeking = ref(false)

  // 用于动画的密码计算属性
  const password = computed(() => loginForm.password)

  const purpleRef = ref(null)
  const blackRef = ref(null)
  const yellowRef = ref(null)
  const orangeRef = ref(null)

  // Handle mouse movement
  const handleMouseMove = (e) => {
    mouseX.value = e.clientX
    mouseY.value = e.clientY
  }

  onMounted(() => {
    window.addEventListener('mousemove', handleMouseMove)

    // Blinking effect for purple character
    const schedulePurpleBlink = () => {
      const getRandomBlinkInterval = () => Math.random() * 4000 + 3000
      const blinkTimeout = setTimeout(() => {
        isPurpleBlinking.value = true
        setTimeout(() => {
          isPurpleBlinking.value = false
          schedulePurpleBlink()
        }, 150)
      }, getRandomBlinkInterval())
      return blinkTimeout
    }

    // Blinking effect for black character
    const scheduleBlackBlink = () => {
      const getRandomBlinkInterval = () => Math.random() * 4000 + 3000
      const blinkTimeout = setTimeout(() => {
        isBlackBlinking.value = true
        setTimeout(() => {
          isBlackBlinking.value = false
          scheduleBlackBlink()
        }, 150)
      }, getRandomBlinkInterval())
      return blinkTimeout
    }

    const purpleBlinkTimeout = schedulePurpleBlink()
    const blackBlinkTimeout = scheduleBlackBlink()

    onUnmounted(() => {
      clearTimeout(purpleBlinkTimeout)
      clearTimeout(blackBlinkTimeout)
    })

    // Listen for Enter key
    document.onkeydown = (e) => {
      if (e.code === "Enter" || e.code === "enter" || e.code === "NumpadEnter") {
        if (loading.value) return
        handleLogin()
      }
    }
  })

  onUnmounted(() => {
    window.removeEventListener('mousemove', handleMouseMove)
  })

  onBeforeUnmount(() => {
    document.onkeydown = null
  })

  // Watch for typing to trigger looking at each other animation
  const setIsTyping = (value) => {
    isTyping.value = value
    if (value) {
      isLookingAtEachOther.value = true
      setTimeout(() => {
        isLookingAtEachOther.value = false
      }, 800)
    } else {
      isLookingAtEachOther.value = false
    }
  }

  // Calculate character positions based on mouse movement
  const calculatePosition = (ref) => {
    if (!ref) return { faceX: 0, faceY: 0, bodySkew: 0 }

    const rect = ref.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 3

    const deltaX = mouseX.value - centerX
    const deltaY = mouseY.value - centerY

    const faceX = Math.max(-15, Math.min(15, deltaX / 20))
    const faceY = Math.max(-10, Math.min(10, deltaY / 30))

    const bodySkew = Math.max(-6, Math.min(6, -deltaX / 120))

    return { faceX, faceY, bodySkew }
  }

  const purplePos = computed(() => calculatePosition(purpleRef.value))
  const blackPos = computed(() => calculatePosition(blackRef.value))
  const yellowPos = computed(() => calculatePosition(yellowRef.value))
  const orangePos = computed(() => calculatePosition(orangeRef.value))

  // 重置表单
  const resetForm = () => {
    if (loginFormRef.value) {
      loginFormRef.value.resetFields()
    }
  }

  // 登录处理
  const handleLogin = async () => {
    if (!loginFormRef.value) return

    await loginFormRef.value.validate(async (valid) => {
      if (!valid) return

      loading.value = true

      try {
        const response = await fetch(`${API_BASE_URL}/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(loginForm)
        })

        if (!response.ok) throw new Error('登录请求失败')

        const result = await response.json()

        if (result.success) {
          localStorage.setItem('isLoggedIn', 'true')
          localStorage.setItem('username', loginForm.username)
          if (result.menus) {
            localStorage.setItem('menus', JSON.stringify(result.menus))
          }
          if (result.roles) {
            localStorage.setItem('roles', JSON.stringify(result.roles))
          }

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
</script>

<style scoped>
  .bg-grid-white\/\[0\.05\] {
    background-image: linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
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
</style>