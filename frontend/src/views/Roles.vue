<template>
  <el-card class="list-card">
    <template #header>
      <div class="card-header">
        <el-icon>
          <UserFilled />
        </el-icon>
        <span>角色管理</span>
      </div>
    </template>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <el-button type="primary" @click="handleAddRole">
        <el-icon>
          <Plus />
        </el-icon> 新增角色
      </el-button>
      <el-button type="primary" @click="handleRefresh">
        <el-icon>
          <Refresh />
        </el-icon> 刷新列表
      </el-button>
    </div>

    <!-- 表格 -->
    <el-table :data="roles" v-loading="loading" stripe border class="role-table" empty-text="暂无角色记录">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="角色名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="scope">
          <el-button size="small" type="primary" text @click="handleEditRole(scope.row)">
            <el-icon>
              <Edit />
            </el-icon>
          </el-button>
          <el-button size="small" type="success" text @click="handleAssignMenus(scope.row)">
            <el-icon>
              <Menu />
            </el-icon>
            分配菜单
          </el-button>
          <el-button size="small" type="danger" text @click="handleDeleteRole(scope.row.id)">
            <el-icon>
              <Delete />
            </el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑角色对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px" destroy-on-close>
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 分配菜单对话框 -->
    <el-dialog title="分配菜单" v-model="menuDialogVisible" width="500px" destroy-on-close>
      <el-tree
        ref="menuTreeRef"
        :data="allMenus"
        :props="treeProps"
        show-checkbox
        node-key="id"
        :default-checked-keys="checkedMenuIds"
        :check-strictly="false"
      />
      <template #footer>
        <el-button @click="menuDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleMenuSubmit">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { UserFilled, Plus, Refresh, Edit, Delete, Menu } from '@element-plus/icons-vue'
  import { getRoles, createRole, updateRole, deleteRole, getRoleMenus, assignRoleMenus, getMenus } from '../config/api'

  const roles = ref([])
  const allMenus = ref([])
  const loading = ref(false)
  const dialogVisible = ref(false)
  const menuDialogVisible = ref(false)
  const formRef = ref(null)
  const menuTreeRef = ref(null)
  const dialogTitle = ref('新增角色')
  const currentRoleId = ref(null)
  const checkedMenuIds = ref([])

  const formData = ref({
    name: '',
    description: ''
  })

  const formRules = {
    name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }]
  }

  const treeProps = {
    children: 'children',
    label: 'name'
  }

  const fetchRoles = async () => {
    loading.value = true
    try {
      roles.value = await getRoles()
    } catch (error) {
      console.error('获取角色列表失败:', error)
      ElMessage.error('获取角色列表失败')
    } finally {
      loading.value = false
    }
  }

  const fetchAllMenus = async () => {
    try {
      allMenus.value = await getMenus()
    } catch (error) {
      console.error('获取菜单列表失败:', error)
    }
  }

  const handleAddRole = () => {
    dialogTitle.value = '新增角色'
    formData.value = { name: '', description: '' }
    dialogVisible.value = true
  }

  const handleEditRole = (role) => {
    dialogTitle.value = '编辑角色'
    formData.value = { ...role }
    dialogVisible.value = true
  }

  const handleDeleteRole = (roleId) => {
    ElMessageBox.confirm('确定要删除该角色吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        await deleteRole(roleId)
        roles.value = roles.value.filter(role => role.id !== roleId)
        ElMessage.success('删除成功')
      } catch (error) {
        console.error('删除失败:', error)
        ElMessage.error('删除失败')
      }
    }).catch(() => {})
  }

  const handleAssignMenus = async (role) => {
    currentRoleId.value = role.id
    try {
      const roleMenus = await getRoleMenus(role.id)
      // 提取菜单ID（所有节点，包括父节点）
      const extractIds = (menus) => {
        const ids = []
        menus.forEach(menu => {
          ids.push(menu.id)
          if (menu.children && menu.children.length > 0) {
            ids.push(...extractIds(menu.children))
          }
        })
        return ids
      }
      checkedMenuIds.value = roleMenus.length > 0 ? extractIds(roleMenus) : []
      await fetchAllMenus()
      menuDialogVisible.value = true
    } catch (error) {
      console.error('获取角色菜单失败:', error)
      ElMessage.error('获取角色菜单失败')
    }
  }

  const handleMenuSubmit = async () => {
    try {
      const checkedNodes = menuTreeRef.value.getCheckedNodes(false, true)
      const menuIds = checkedNodes.map(node => node.id)
      await assignRoleMenus(currentRoleId.value, menuIds)
      ElMessage.success('分配菜单成功')
      menuDialogVisible.value = false
    } catch (error) {
      console.error('分配菜单失败:', error)
      ElMessage.error('分配菜单失败')
    }
  }

  const handleSubmit = async () => {
    try {
      if (formData.value.id) {
        await updateRole(formData.value.id, formData.value)
        ElMessage.success('编辑成功')
      } else {
        await createRole(formData.value)
        ElMessage.success('新增成功')
      }
      dialogVisible.value = false
      fetchRoles()
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }

  const handleRefresh = () => {
    fetchRoles()
    ElMessage.success('已刷新')
  }

  onMounted(() => {
    fetchRoles()
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

  .role-table {
    width: 100%;
  }
</style>