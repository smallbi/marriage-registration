<template>
  <div class="members-page">
    <!-- 人员列表 -->
    <MemberList ref="memberListRef" @delete="onDelete" :initial-filters="route.query" />
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import MemberList from '../components/MemberList.vue'
  import { API_BASE_URL } from '../config/api'

  const route = useRoute()

  const memberListRef = ref(null)

  // 删除记录
  const onDelete = async (record) => {
    try {
      // 第一次确认
      await ElMessageBox.confirm(
        `确定要删除人员 "${record.name}" 的信息吗？`,
        '删除确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )

      // 第二次确认
      await ElMessageBox.confirm(
        `再次确认要删除人员 "${record.name}" 的信息吗？删除后无法恢复。`,
        '再次确认',
        {
          confirmButtonText: '确认删除',
          cancelButtonText: '取消',
          type: 'danger',
        }
      )

      const response = await fetch(`${API_BASE_URL}/members/${record.id}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        ElMessage.success('删除成功')
        // 刷新列表
        if (memberListRef.value) {
          memberListRef.value.refresh()
        }
      }
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败: ' + error.message)
      }
    }
  }
</script>

<style scoped>

</style>