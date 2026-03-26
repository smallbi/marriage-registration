<template>
  <div class="stats-page">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 stats-cards">
      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon purple">
            <el-icon :size="20">
              <User />
            </el-icon>
          </div>
          <Top class="trend-icon" />
        </div>
        <h3 class="stat-title">人员总数</h3>
        <p class="stat-value">{{ stats.total }}</p>
        <p class="stat-trend positive">全部登记人员</p>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon blue">
            <span style="font-size: 20px;">👨</span>
          </div>
          <Top class="trend-icon" />
        </div>
        <h3 class="stat-title">男性人员</h3>
        <p class="stat-value">{{ stats.male }}</p>
        <p class="stat-trend positive">占比 {{ malePercent }}%</p>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon pink">
            <span style="font-size: 20px;">👩</span>
          </div>
          <Top class="trend-icon" />
        </div>
        <h3 class="stat-title">女性人员</h3>
        <p class="stat-value">{{ stats.female }}</p>
        <p class="stat-trend positive">占比 {{ femalePercent }}%</p>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon purple">
            <el-icon :size="20">
              <Calendar />
            </el-icon>
          </div>
          <Top class="trend-icon" />
        </div>
        <h3 class="stat-title">本月新增</h3>
        <p class="stat-value">{{ stats.this_month }}</p>
        <p class="stat-trend positive">本月登记人员</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="chart-card">
        <div class="card-header">
          <div class="header-icon blue">
            <el-icon :size="18">
              <DataLine />
            </el-icon>
          </div>
          <h3 class="header-title">男性分布</h3>
        </div>
        <div class="chart-container" ref="maleChartRef"></div>
      </div>

      <div class="chart-card">
        <div class="card-header">
          <div class="header-icon green">
            <el-icon :size="18">
              <DataLine />
            </el-icon>
          </div>
          <h3 class="header-title">女性分布</h3>
        </div>
        <div class="chart-container" ref="femaleChartRef"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, nextTick, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import * as echarts from 'echarts/core'
  import { PieChart, BarChart } from 'echarts/charts'
  import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
  import { CanvasRenderer } from 'echarts/renderers'
  import 'echarts-liquidfill'
  import { User, Calendar, DataLine, Top } from '@element-plus/icons-vue'
  import { API_BASE_URL } from '../config/api'

  const router = useRouter()

  echarts.use([TitleComponent, TooltipComponent, LegendComponent, PieChart, BarChart, CanvasRenderer])

  const stats = ref({
    total: 0,
    male: 0,
    female: 0,
    unmarried: 0,
    divorced: 0,
    widowed: 0,
    this_month: 0
  })

  const malePercent = computed(() => {
    if (stats.value.total === 0) return 0
    return ((stats.value.male / stats.value.total) * 100).toFixed(1)
  })

  const femalePercent = computed(() => {
    if (stats.value.total === 0) return 0
    return ((stats.value.female / stats.value.total) * 100).toFixed(1)
  })

  const maleChartRef = ref(null)
  const femaleChartRef = ref(null)

  let maleChart = null, femaleChart = null

  const initMaleChart = () => {
    if (!maleChartRef.value) return
    maleChart = echarts.init(maleChartRef.value)
    const total = stats.value.total || 1
    const malePercentVal = (stats.value.male / total * 100).toFixed(1)

    maleChart.setOption({
      series: [{
        type: 'liquidFill',
        data: [{ value: stats.value.male / total, name: '男性' }],
        radius: '80%',
        center: ['50%', '50%'],
        color: ['#3b82f6'],
        backgroundStyle: { color: '#fff', borderColor: '#e4e7ed', borderWidth: 1, shadowColor: 'rgba(0, 0, 0, 0.05)', shadowBlur: 10 },
        label: { fontSize: 28, color: '#666', formatter: () => `${malePercentVal}%` },
        outline: { show: false }
      }]
    })

    maleChart.on('click', () => {
      router.push({ path: '/members', query: { gender: '男' } })
    })
  }

  const initFemaleChart = () => {
    if (!femaleChartRef.value) return
    femaleChart = echarts.init(femaleChartRef.value)
    const total = stats.value.total || 1
    const femalePercentVal = (stats.value.female / total * 100).toFixed(1)

    femaleChart.setOption({
      series: [{
        type: 'liquidFill',
        data: [{ value: stats.value.female / total, name: '女性' }],
        radius: '80%',
        center: ['50%', '50%'],
        color: ['#ec4899'],
        backgroundStyle: { color: '#fff', borderColor: '#e4e7ed', borderWidth: 1, shadowColor: 'rgba(0, 0, 0, 0.05)', shadowBlur: 10 },
        label: { fontSize: 28, color: '#666', formatter: () => `${femalePercentVal}%` },
        outline: { show: false }
      }]
    })

    femaleChart.on('click', () => {
      router.push({ path: '/members', query: { gender: '女' } })
    })
  }

  const refreshCharts = () => {
    nextTick(() => {
      initMaleChart()
      initFemaleChart()
    })
  }

  const handleResize = () => {
    maleChart?.resize()
    femaleChart?.resize()
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
    max-width: 1400px;
    margin: 0 auto;
  }

  .stats-cards {
    margin-bottom: 20px;
  }

  .stat-card {
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #e4e7ed;
    background: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: box-shadow 0.2s, transform 0.2s;
  }

  .stat-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
  }

  .stat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .stat-icon.purple {
    background: rgba(139, 92, 246, 0.1);
    color: #8b5cf6;
  }

  .stat-icon.blue {
    background: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
  }

  .stat-icon.pink {
    background: rgba(236, 72, 153, 0.1);
    color: #ec4899;
  }

  .trend-icon {
    width: 16px;
    height: 16px;
    color: #22c55e;
  }

  .stat-title {
    font-size: 14px;
    font-weight: 500;
    color: #6b7280;
    margin-bottom: 4px;
  }

  .stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
    line-height: 1.2;
  }

  .stat-trend {
    font-size: 13px;
    margin-top: 8px;
  }

  .stat-trend.positive {
    color: #22c55e;
  }

  .chart-card {
    border-radius: 16px;
    border: 1px solid #e4e7ed;
    background: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    padding: 24px;
  }

  .card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
  }

  .header-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .header-icon.blue {
    background: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
  }

  .header-icon.green {
    background: rgba(34, 197, 94, 0.1);
    color: #22c55e;
  }

  .header-title {
    font-size: 16px;
    font-weight: 600;
    color: #111827;
  }

  .chart-container {
    width: 100%;
    height: 280px;
  }

  @media (max-width: 768px) {
    .stats-page {
      padding: 0;
    }

    .stat-card {
      margin-bottom: 12px;
    }

    .chart-card {
      margin-bottom: 16px;
    }

    .chart-container {
      height: 220px;
    }
  }
</style>