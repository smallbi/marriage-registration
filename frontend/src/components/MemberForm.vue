<template>
  <div class="form-container">
    <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" label-position="left" class="person-form">
      <el-row :gutter="20">
        <!-- 姓名 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="form.name" placeholder="请输入姓名" />
          </el-form-item>
        </el-col>

        <!-- 性别 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="form.gender">
              <el-radio value="男">男</el-radio>
              <el-radio value="女">女</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>

        <!-- 年龄 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="年龄" prop="age">
            <el-input-number v-model="form.age" :min="18" :max="100" placeholder="请输入年龄" style="width: 100%" />
          </el-form-item>
        </el-col>

        <!-- 学历 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="学历" prop="education">
            <el-select v-model="form.education" placeholder="请选择学历" style="width: 100%">
              <el-option value="小学" label="小学" />
              <el-option value="初中" label="初中" />
              <el-option value="高中" label="高中" />
              <el-option value="大专" label="大专" />
              <el-option value="本科" label="本科" />
              <el-option value="硕士" label="硕士" />
              <el-option value="博士" label="博士" />
            </el-select>
          </el-form-item>
        </el-col>

        <!-- 职业 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="职业" prop="occupation">
            <el-input v-model="form.occupation" placeholder="请输入职业" />
          </el-form-item>
        </el-col>

        <!-- 婚姻状况 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="婚姻状况" prop="marital_status">
            <el-radio-group v-model="form.marital_status">
              <el-radio value="未婚">未婚</el-radio>
              <el-radio value="离异">离异</el-radio>
              <el-radio value="丧偶">丧偶</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>

        <!-- 户籍所在地 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="户籍所在地" prop="hukou_location">
            <el-input v-model="form.hukou_location" placeholder="请输入户籍所在地" />
          </el-form-item>
        </el-col>

        <!-- 现居住地 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="现居住地" prop="current_residence">
            <el-input v-model="form.current_residence" placeholder="请输入现居住地" />
          </el-form-item>
        </el-col>

        <!-- 联系方式 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="联系方式" prop="contact">
            <el-input v-model="form.contact" placeholder="手机号或微信号" />
          </el-form-item>
        </el-col>

        <!-- 身高 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="身高 (cm)">
            <el-input-number v-model="form.height" :min="100" :max="220" placeholder="选填" style="width: 100%" />
          </el-form-item>
        </el-col>

        <!-- 收入 -->
        <el-col :span="12" :xs="24">
          <el-form-item label="收入">
            <el-input v-model="form.income" placeholder="如：8k-10k（选填）" />
          </el-form-item>
        </el-col>

        <!-- 择偶要求 -->
        <el-col :span="24">
          <el-form-item label="择偶要求">
            <el-input v-model="form.partner_requirement" type="textarea" :rows="3" placeholder="请输入择偶要求（选填）" />
          </el-form-item>
        </el-col>

        <!-- 备注 -->
        <el-col :span="24">
          <el-form-item label="备注">
            <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="请输入备注信息（选填）" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 操作按钮 -->
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="loading" size="large">
          <el-icon>
            <Check />
          </el-icon>
          提交信息
        </el-button>
        <el-button @click="$emit('cancel')" size="large">
          <el-icon>
            <Close />
          </el-icon>
          取消
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
  import { ref, reactive, watch, onMounted } from 'vue'
  import { ElMessage } from 'element-plus'
  import { Edit, Check, Close } from '@element-plus/icons-vue'

  const emit = defineEmits(['success', 'cancel'])
  const props = defineProps({
    initialData: {
      type: Object,
      default: () => ({})
    }
  })

  const formRef = ref(null)
  const loading = ref(false)

  // 表单数据
  const form = reactive({
    id: '',
    name: '',
    gender: '',
    age: null,
    education: '',
    occupation: '',
    marital_status: '',
    hukou_location: '',
    current_residence: '',
    contact: '',
    height: null,
    income: '',
    partner_requirement: '',
    remark: ''
  })

  // 初始化表单数据
  const initFormData = () => {
    if (props.initialData) {
      Object.keys(props.initialData).forEach(key => {
        if (form.hasOwnProperty(key)) {
          form[key] = props.initialData[key]
        }
      })
    }
  }

  // 监听initialData变化
  watch(() => props.initialData, (newData) => {
    if (newData) {
      initFormData()
    }
  }, { deep: true })

  // 组件挂载时初始化数据
  onMounted(() => {
    initFormData()
  })

  // 表单验证规则
  const rules = {
    name: [
      { required: true, message: '请输入姓名', trigger: 'blur' }
    ],
    gender: [
      { required: true, message: '请选择性别', trigger: 'change' }
    ],
    age: [
      { required: true, message: '请输入年龄', trigger: 'blur' }
    ],
    education: [
      { required: true, message: '请选择学历', trigger: 'change' }
    ],
    occupation: [
      { required: true, message: '请输入职业', trigger: 'blur' }
    ],
    marital_status: [
      { required: true, message: '请选择婚姻状况', trigger: 'change' }
    ],
    hukou_location: [
      { required: true, message: '请输入户籍所在地', trigger: 'blur' }
    ],
    current_residence: [
      { required: true, message: '请输入现居住地', trigger: 'blur' }
    ],
    contact: [
      { required: true, message: '请输入联系方式', trigger: 'blur' }
    ]
  }

  // 提交表单
  const handleSubmit = async () => {
    if (!formRef.value) return

    await formRef.value.validate(async (valid) => {
      if (!valid) return

      loading.value = true

      try {
        // 构建请求数据
        const data = {
          name: form.name.trim(),
          gender: form.gender,
          age: form.age,
          education: form.education,
          occupation: form.occupation.trim(),
          marital_status: form.marital_status,
          hukou_location: form.hukou_location.trim(),
          current_residence: form.current_residence.trim(),
          contact: form.contact.trim(),
        }

        // 可选字段
        if (form.height) data.height = form.height
        if (form.income) data.income = form.income.trim()
        if (form.partner_requirement) data.partner_requirement = form.partner_requirement.trim()
        if (form.remark) data.remark = form.remark.trim()

        // 根据是否有id决定是新增还是编辑
        const url = form.id 
          ? `http://localhost:8000/api/members/${form.id}` 
          : 'http://localhost:8000/api/members'
        const method = form.id ? 'PUT' : 'POST'

        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || '提交失败')
        }

        // 重置表单
        formRef.value.resetFields()
        form.id = ''
        form.height = null
        form.income = ''
        form.partner_requirement = ''
        form.remark = ''

        emit('success', form.id ? '人员信息编辑成功！🎉' : '人员信息提交成功！🎉')
      } catch (error) {
        ElMessage.error('提交失败: ' + error.message)
      } finally {
        loading.value = false
      }
    })
  }
</script>

<style scoped>
  .form-container {
    padding: 20px;
  }

  .person-form {
    padding: 10px 0;
  }

  .el-form-item {
    margin-bottom: 18px;
  }

  @media (max-width: 768px) {
    .el-col {
      margin-bottom: 0;
    }
    
    .form-container {
      padding: 10px;
    }
  }
</style>