<template>
  <el-card class="list-card">
    <template #header>
      <div class="card-header">
        <el-icon>
          <UserFilled />
        </el-icon>
        <span>用户管理列表</span>
      </div>
    </template>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <el-button type="primary" @click="handleAddUser">
        <el-icon>
          <Plus />
        </el-icon> 新增用户
      </el-button>
      <el-button type="primary" @click="handleRefresh">
        <el-icon>
          <Refresh />
        </el-icon> 刷新列表
      </el-button>
    </div>

    <!-- 表格 -->
    <el-table :data="users" v-loading="loading" stripe border class="user-table" empty-text="暂无用户记录">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="登录名" />
      <el-table-column prop="created_at" label="创建时间" width="200" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button size="small" type="primary" text @click="handleEditUser(scope.row)">
            <el-icon>
              <Edit />
            </el-icon>
          </el-button>
          <el-button size="small" type="danger" text @click="handleDeleteUser(scope.row.id)">
            <el-icon>
              <Delete />
            </el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑用户对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
      destroy-on-close
    >
      <UserForm
        :initial-data="currentEditUser"
        @submit="handleFormSubmit"
        @cancel="dialogVisible = false"
      />
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import UserForm from './UserForm.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UserFilled, Plus, Refresh, Edit, Delete } from '@element-plus/icons-vue'

const users = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const currentEditUser = ref({})
const dialogTitle = ref('新增用户')

const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/users')
    if (!response.ok) throw new Error('获取用户列表失败')
    users.value = await response.json()
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleAddUser = () => {
  dialogTitle.value = '新增用户'
  currentEditUser.value = {}
  dialogVisible.value = true
}

const handleEditUser = (user) => {
  dialogTitle.value = '编辑用户'
  currentEditUser.value = { ...user }
  dialogVisible.value = true
}

const handleDeleteUser = (userId) => {
  ElMessageBox.confirm('确定要删除该用户吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/users/${userId}`, {
        method: 'DELETE'
      })
      if (!response.ok) throw new Error('删除失败')
      await response.json()
      users.value = users.value.filter(user => user.id !== userId)
      ElMessage.success('删除成功')
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

const handleFormSubmit = async (userData) => {
  try {
    let response
    if (userData.id) {
      // 编辑用户
      response = await fetch(`http://localhost:8000/api/users/${userData.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
    } else {
      // 新增用户
      response = await fetch('http://localhost:8000/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
    }
    
    if (!response.ok) throw new Error('操作失败')
    const result = await response.json()
    
    if (userData.id) {
      // 更新本地数据
      const index = users.value.findIndex(user => user.id === userData.id)
      if (index !== -1) {
        users.value[index] = result
      }
      ElMessage.success('编辑成功')
    } else {
      // 添加到本地数据
      users.value.push(result)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    // 刷新列表
    fetchUsers()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

const handleRefresh = () => {
  fetchUsers()
  ElMessage.success('已刷新')
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.list-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.user-table {
  width: 100%;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .el-button {
    width: 100%;
  }
}
</style>