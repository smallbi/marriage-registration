<template>
  <div class="user-form">
    <el-form :model="formData" label-width="80px" :rules="rules" ref="formRef">
      <el-form-item label="登录名" prop="username">
        <el-input v-model="formData.username" placeholder="请输入登录名" />
      </el-form-item>
      <el-form-item label="登录密码" prop="password">
        <el-input v-model="formData.password" type="password" placeholder="请输入登录密码" show-password />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formRef = ref(null)
const formData = reactive({
  id: props.initialData.id || null,
  username: props.initialData.username || '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入登录名', trigger: 'blur' },
    { min: 2, max: 20, message: '登录名长度应在2-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入登录密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    emit('submit', { ...formData })
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<style scoped>
.user-form {
  padding: 20px;
}
</style>