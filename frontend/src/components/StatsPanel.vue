<template>
  <el-row :gutter="16" class="stats-panel">
    <el-col :span="6" :xs="24" :sm="12" :md="6">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(64, 158, 255, 0.1); color: #409eff;">
          <el-icon :size="24">
            <UserFilled />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">人员总数</div>
        </div>
      </div>
    </el-col>

    <el-col :span="6" :xs="24" :sm="12" :md="6">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
          <span style="font-size: 24px;">👨</span>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.male }}</div>
          <div class="stat-label">男性人员</div>
        </div>
      </div>
    </el-col>

    <el-col :span="6" :xs="24" :sm="12" :md="6">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(236, 72, 153, 0.1); color: #ec4899;">
          <span style="font-size: 24px;">👩</span>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.female }}</div>
          <div class="stat-label">女性人员</div>
        </div>
      </div>
    </el-col>

    <el-col :span="6" :xs="24" :sm="12" :md="6">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(64, 158, 255, 0.1); color: #409eff;">
          <el-icon :size="24">
            <Calendar />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.this_month }}</div>
          <div class="stat-label">本月新增</div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { UserFilled, Calendar } from '@element-plus/icons-vue'

  const stats = ref({
    total: 0,
    male: 0,
    female: 0,
    unmarried: 0,
    divorced: 0,
    widowed: 0,
    this_month: 0
  })

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/stats')
      if (response.ok) {
        stats.value = await response.json()
      }
    } catch (error) {
      console.error('获取统计信息失败:', error)
    }
  }

  onMounted(() => {
    fetchStats()
  })

  // 暴露刷新方法
  defineExpose({
    refresh: fetchStats
  })
</script>

<style scoped>
  .stats-panel {
    margin-bottom: 20px;
  }

  .stat-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .stat-content {
    flex: 1;
  }

  .stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #303133;
    line-height: 1.2;
  }

  .stat-label {
    font-size: 14px;
    color: #909399;
    margin-top: 4px;
  }

  @media (max-width: 768px) {
    .stats-panel .el-col {
      margin-bottom: 12px;
    }
  }
</style>