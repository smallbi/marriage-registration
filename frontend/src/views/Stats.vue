<template>
  <div class="stats-page">
    <!-- 第一行：统计卡片 -->
    <el-row :gutter="20">
      <el-col :span="6" :xs="12" :sm="12" :md="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: rgba(64, 158, 255, 0.1);">
            <el-icon :size="28" color="#409eff">
              <User />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">人员总数</div>
          </div>
        </div>
      </el-col>

      <el-col :span="6" :xs="12" :sm="12" :md="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: rgba(103, 194, 58, 0.1);">
            <span style="font-size: 28px;">👨</span>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.male }}</div>
            <div class="stat-label">男性人员</div>
          </div>
        </div>
      </el-col>

      <el-col :span="6" :xs="12" :sm="12" :md="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: rgba(230, 162, 60, 0.1);">
            <span style="font-size: 28px;">👩</span>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.female }}</div>
            <div class="stat-label">女性人员</div>
          </div>
        </div>
      </el-col>

      <el-col :span="6" :xs="12" :sm="12" :md="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: rgba(64, 158, 255, 0.1);">
            <el-icon :size="28" color="#409eff">
              <Calendar />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.this_month }}</div>
            <div class="stat-label">本月新增</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 第二行：两个性别水型图 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 男性水型图 -->
      <el-col :span="12" :xs="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <el-icon>
                <IconPieChart />
              </el-icon>
              <span>男性分布</span>
            </div>
          </template>
          <div class="chart-container" ref="maleChartRef"></div>
        </el-card>
      </el-col>

      <!-- 女性水型图 -->
      <el-col :span="12" :xs="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <el-icon>
                <IconPieChart />
              </el-icon>
              <span>女性分布</span>
            </div>
          </template>
          <div class="chart-container" ref="femaleChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 第三行：婚姻状况饼图 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24" :xs="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <el-icon>
                <DataLine />
              </el-icon>
              <span>婚姻状况分布</span>
            </div>
          </template>
          <div class="chart-container" ref="maritalChartRef"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
  import { ref, onMounted, nextTick } from 'vue'
  import { useRouter } from 'vue-router'
  import * as echarts from 'echarts/core'
  import { PieChart, BarChart } from 'echarts/charts'
  import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
  import { CanvasRenderer } from 'echarts/renderers'
  import 'echarts-liquidfill'
  import { UserFilled, User, Calendar, PieChart as IconPieChart, DataLine, Histogram, House, Odometer } from '@element-plus/icons-vue'
  import { API_BASE_URL } from '../config/api'

  const router = useRouter()

  // 注册 ECharts
  echarts.use([TitleComponent, TooltipComponent, LegendComponent, PieChart, BarChart, CanvasRenderer])

  const stats = ref({ total: 0, male: 0, female: 0, unmarried: 0, divorced: 0, widowed: 0, this_month: 0 })

  const maleChartRef = ref(null)
  const femaleChartRef = ref(null)
  const maritalChartRef = ref(null)

  let maleChart = null, femaleChart = null, maritalChart = null

  // 男性水型图
  const initMaleChart = () => {
    if (!maleChartRef.value) return
    maleChart = echarts.init(maleChartRef.value)
    const total = stats.value.total || 1
    const malePercent = (stats.value.male / total * 100).toFixed(1)

    maleChart.setOption({
      series: [{
        type: 'liquidFill',
        data: [{ value: stats.value.male / total, name: '男性' }],
        radius: '80%',
        center: ['50%', '50%'],
        color: ['#5470c6'],
        backgroundStyle: { color: '#fff', borderColor: '#ccc', borderWidth: 1, shadowColor: 'rgba(0, 0, 0, 0.1)', shadowBlur: 10 },
        label: { fontSize: 28, color: '#666', formatter: () => `${malePercent}%` },
        outline: { show: false }
      }]
    })

    // 添加点击事件
    maleChart.on('click', () => {
      router.push({ path: '/members', query: { gender: '男' } })
    })
  }

  // 女性水型图
  const initFemaleChart = () => {
    if (!femaleChartRef.value) return
    femaleChart = echarts.init(femaleChartRef.value)
    const total = stats.value.total || 1
    const femalePercent = (stats.value.female / total * 100).toFixed(1)

    femaleChart.setOption({
      series: [{
        type: 'liquidFill',
        data: [{ value: stats.value.female / total, name: '女性' }],
        radius: '80%',
        center: ['50%', '50%'],
        color: ['#91cc75'],
        backgroundStyle: { color: '#fff', borderColor: '#ccc', borderWidth: 1, shadowColor: 'rgba(0, 0, 0, 0.1)', shadowBlur: 10 },
        label: { fontSize: 28, color: '#666', formatter: () => `${femalePercent}%` },
        outline: { show: false }
      }]
    })

    // 添加点击事件
    femaleChart.on('click', () => {
      router.push({ path: '/members', query: { gender: '女' } })
    })
  }

  // 婚姻状况饼图
  const initMaritalChart = () => {
    if (!maritalChartRef.value) return
    maritalChart = echarts.init(maritalChartRef.value)

    const data = [
      { value: stats.value.unmarried, name: '未婚', itemStyle: { color: '#67c23a' } },
      { value: stats.value.divorced, name: '离异', itemStyle: { color: '#e6a23c' } },
      { value: stats.value.widowed, name: '丧偶', itemStyle: { color: '#909399' } }
    ].filter(item => item.value > 0)

    if (data.length === 0) data.push({ value: 1, name: '暂无数据', itemStyle: { color: '#f0f2f5' } })

    maritalChart.setOption({
      tooltip: { trigger: 'item', formatter: '{b}: {c} 人 ({d}%)' },
      legend: { orient: 'vertical', right: 10, top: 'center', textStyle: { color: '#666' } },
      series: [{
        type: 'pie', radius: ['40%', '70%'], center: ['40%', '50%'],
        avoidLabelOverlap: false, itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
        label: { show: false }, emphasis: { label: { show: true, fontSize: 16, fontWeight: 'bold' } }, labelLine: { show: false }, data
      }]
    })

    // 添加点击事件
    maritalChart.on('click', (params) => {
      if (params.name !== '暂无数据') {
        router.push({ path: '/members', query: { marital_status: params.name } })
      }
    })
  }

  const refreshCharts = () => {
    nextTick(() => {
      initMaleChart()
      initFemaleChart()
      initMaritalChart()
    })
  }

  const handleResize = () => {
    maleChart?.resize()
    femaleChart?.resize()
    maritalChart?.resize()
  }

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/stats`)
      if (response.ok) {
        const data = await response.json()
        stats.value = data
        refreshCharts()
      }
    } catch (error) {
      console.error('获取统计信息失败:', error)
    }
  }

  onMounted(() => {
    fetchStats()
    window.addEventListener('resize', handleResize)
  })
</script>

<style scoped>
  .stats-page {
    max-width: 1600px;
    margin: 0 auto;
  }

  .chart-card {
    border-radius: 12px;
    height: 340px;
  }

  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
  }

  .chart-container {
    width: 100%;
    height: 260px;
  }

  .stat-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s;
    margin-bottom: 16px;
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

  .stat-info {
    flex: 1;
  }

  .stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #303133;
  }

  .stat-label {
    font-size: 14px;
    color: #909399;
    margin-top: 4px;
  }

  @media (max-width: 768px) {
    .stats-page {
      padding: 12px;
    }

    .chart-card {
      margin-bottom: 16px;
      height: auto;
    }

    .chart-container {
      height: 200px;
    }
  }
</style>