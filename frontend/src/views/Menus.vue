<template>
  <el-card class="list-card">
    <template #header>
      <div class="card-header">
        <el-icon>
          <Menu />
        </el-icon>
        <span>菜单管理</span>
      </div>
    </template>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <el-button type="primary" @click="handleAddMenu">
        <el-icon>
          <Plus />
        </el-icon> 新增菜单
      </el-button>
      <el-button type="primary" @click="handleRefresh">
        <el-icon>
          <Refresh />
        </el-icon> 刷新列表
      </el-button>
    </div>

    <!-- 表格 -->
    <el-table :data="menus" v-loading="loading" stripe border class="menu-table" empty-text="暂无菜单记录">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="菜单名称" />
      <el-table-column prop="path" label="路径" />
      <el-table-column prop="icon" label="图标" width="100" />
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column prop="is_visible" label="显示状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_visible ? 'success' : 'info'">
            {{ scope.row.is_visible ? '显示' : '隐藏' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button size="small" type="primary" text @click="handleEditMenu(scope.row)">
            <el-icon>
              <Edit />
            </el-icon>
          </el-button>
          <el-button size="small" type="danger" text @click="handleDeleteMenu(scope.row.id)">
            <el-icon>
              <Delete />
            </el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑菜单对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px" destroy-on-close>
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="菜单名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入菜单名称" />
        </el-form-item>
        <el-form-item label="路径" prop="path">
          <el-input v-model="formData.path" placeholder="请输入路径" />
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="formData.icon" placeholder="请输入图标名称" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="formData.sort" :min="0" :max="9999" />
        </el-form-item>
        <el-form-item label="显示状态">
          <el-switch v-model="formData.visible" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { Menu, Plus, Refresh, Edit, Delete } from '@element-plus/icons-vue'
  import { getMenus, createMenu, updateMenu, deleteMenu } from '../config/api'

  const menus = ref([])
  const loading = ref(false)
  const dialogVisible = ref(false)
  const formRef = ref(null)
  const dialogTitle = ref('新增菜单')
  const formData = ref({
    name: '',
    path: '',
    icon: '',
    sort: 0,
    visible: true
  })

  const formRules = {
    name: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
    path: [{ required: true, message: '请输入路径', trigger: 'blur' }]
  }

  const fetchMenus = async () => {
    loading.value = true
    try {
      menus.value = await getMenus()
    } catch (error) {
      console.error('获取菜单列表失败:', error)
      ElMessage.error('获取菜单列表失败')
    } finally {
      loading.value = false
    }
  }

  const handleAddMenu = () => {
    dialogTitle.value = '新增菜单'
    formData.value = { name: '', path: '', icon: '', sort: 0, visible: true }
    dialogVisible.value = true
  }

  const handleEditMenu = (menu) => {
    dialogTitle.value = '编辑菜单'
    formData.value = { ...menu }
    dialogVisible.value = true
  }

  const handleDeleteMenu = (menuId) => {
    ElMessageBox.confirm('确定要删除该菜单吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        await deleteMenu(menuId)
        menus.value = menus.value.filter(menu => menu.id !== menuId)
        ElMessage.success('删除成功')
      } catch (error) {
        console.error('删除失败:', error)
        ElMessage.error('删除失败')
      }
    }).catch(() => {})
  }

  const handleSubmit = async () => {
    try {
      if (formData.value.id) {
        await updateMenu(formData.value.id, formData.value)
        ElMessage.success('编辑成功')
      } else {
        await createMenu(formData.value)
        ElMessage.success('新增成功')
      }
      dialogVisible.value = false
      fetchMenus()
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }

  const handleRefresh = () => {
    fetchMenus()
    ElMessage.success('已刷新')
  }

  onMounted(() => {
    fetchMenus()
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

  .menu-table {
    width: 100%;
  }
</style>