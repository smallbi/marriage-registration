<template>
  <el-card class="list-card">
    <template #header>
      <div class="card-header">
        <el-icon>
          <List />
        </el-icon>
        <span>会员信息</span>
      </div>
    </template>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <!-- 快捷操作按钮 -->
      <div class="action-buttons">
        <el-button type="primary" @click="showForm = true">
          <el-icon>
            <Plus />
          </el-icon> 新增会员
        </el-button>
        <el-button type="primary" @click="handleRefresh">
          <el-icon>
            <Refresh />
          </el-icon> 刷新列表
        </el-button>
        <el-button @click="handleReset">
          <el-icon>
            <RefreshLeft />
          </el-icon> 重置查询
        </el-button>
        <el-button type="success" @click="handleExport">
          <el-icon>
            <Download />
          </el-icon> 导出数据
        </el-button>
        <el-button type="danger" @click="handleBatchDelete" :disabled="selectedRows.length === 0">
          <el-icon>
            <Delete />
          </el-icon> 批量删除
        </el-button>
      </div>

      <!-- 筛选条件 -->
      <div class="filter-section">
        <el-input v-model="filters.search" placeholder="姓名关键字搜索..." class="filter-input" clearable
          @input="debouncedSearch" @clear="handleSearch">
          <template #prefix>
            <el-icon>
              <Search />
            </el-icon>
          </template>
        </el-input>

        <el-select v-model="filters.gender" placeholder="性别" clearable class="filter-select" @change="handleSearch">
          <el-option value="男" label="男" />
          <el-option value="女" label="女" />
        </el-select>

        <el-input-number v-model="filters.ageMin" :min="18" :max="100" placeholder="最小年龄" class="filter-number"
          controls-position="right" @change="handleSearch" />

        <el-input-number v-model="filters.ageMax" :min="18" :max="100" placeholder="最大年龄" class="filter-number"
          controls-position="right" @change="handleSearch" />

        <el-select v-model="filters.education" placeholder="学历" clearable class="filter-select" @change="handleSearch">
          <el-option value="小学" label="小学" />
          <el-option value="初中" label="初中" />
          <el-option value="高中" label="高中" />
          <el-option value="大专" label="大专" />
          <el-option value="本科" label="本科" />
          <el-option value="硕士" label="硕士" />
          <el-option value="博士" label="博士" />
        </el-select>

        <el-select v-model="filters.marital_status" placeholder="婚姻状况" clearable class="filter-select"
          @change="handleSearch">
          <el-option value="未婚" label="未婚" />
          <el-option value="离异" label="离异" />
          <el-option value="丧偶" label="丧偶" />
        </el-select>
      </div>
    </div>

    <!-- 表格 -->
    <el-table :data="members" v-loading="loading" stripe border class="member-table" empty-text="暂无人员记录"
      @sort-change="handleSortChange" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="member_no" label="人员编号" width="180" sortable="custom">
        <template #default="{ row }">
          <el-tag size="small" type="info">{{ row.member_no }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="name" label="姓名" width="100" sortable="custom" />

      <el-table-column prop="gender" label="性别" width="80" sortable="custom">
        <template #default="{ row }">
          <el-tag :type="row.gender === '男' ? '' : 'warning'" size="small">
            {{ row.gender }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="age" label="年龄" width="80" sortable="custom" />

      <el-table-column prop="education" label="学历" width="100" sortable="custom" />

      <el-table-column prop="occupation" label="职业" min-width="120" />

      <el-table-column prop="marital_status" label="婚姻状况" width="100" sortable="custom">
        <template #default="{ row }">
          <el-tag :type="row.marital_status === '未婚' ? 'success' : row.marital_status === '离异' ? 'warning' : 'info'"
            size="small">
            {{ row.marital_status }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="hukou_location" label="户籍" min-width="150" show-overflow-tooltip />

      <el-table-column prop="current_residence" label="现居地" min-width="150" show-overflow-tooltip />

      <el-table-column prop="contact" label="联系方式" width="130" />

      <el-table-column prop="zodiac" label="生肖" width="80" />

      <el-table-column prop="personality" label="性格" width="100" show-overflow-tooltip />

      <el-table-column prop="family_members" label="家庭人员" width="120" show-overflow-tooltip />

      <el-table-column prop="property" label="房车情况" width="120" show-overflow-tooltip />

      <!-- 照片列 - 已禁用 -->
      <!--
      <el-table-column label="照片" width="80">
        <template #default="{ row }">
          <el-image v-if="row.photos" :src="(JSON.parse(row.photos) || [])[0]" fit="cover"
            style="width:40px;height:40px" :preview-src-list="JSON.parse(row.photos)" preview-teleported />
        </template>
      </el-table-column>
      -->

      <el-table-column prop="registration_time" label="登记时间" width="160" sortable="custom">
        <template #default="{ row }">
          {{ formatDate(row.registration_time) }}
        </template>
      </el-table-column>

      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button size="small" type="primary" text @click="viewDetail(row)">
            <el-icon>
              <View />
            </el-icon>
          </el-button>
          <el-button size="small" type="warning" text @click="editMember(row)">
            <el-icon>
              <Edit />
            </el-icon>
          </el-button>
          <el-button size="small" type="info" text @click="handlePrint(row)">
            <el-icon>
              <Printer />
            </el-icon>
          </el-button>
          <el-button size="small" type="danger" text @click="$emit('delete', row)">
            <el-icon>
              <Delete />
            </el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-wrapper">
      <el-pagination v-model:current-page="page" v-model:page-size="pageSize" :page-sizes="[10, 20, 50, 100]"
        :total="total" layout="total, sizes, prev, pager, next, jumper" background @size-change="handleSizeChange"
        @current-change="handleCurrentChange" />
    </div>

    <!-- 详情弹窗 -->
    <el-dialog v-model="showDetail" title="人员详情" width="750px" destroy-on-close>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="人员编号">
          {{ currentDetail.member_no }}
        </el-descriptions-item>
        <el-descriptions-item label="登记时间">
          {{ currentDetail.registration_time }}
        </el-descriptions-item>
        <el-descriptions-item label="姓名">
          {{ currentDetail.name }}
        </el-descriptions-item>
        <el-descriptions-item label="性别">
          <el-tag :type="currentDetail.gender === '男' ? '' : 'warning'">
            {{ currentDetail.gender }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="年龄">
          {{ currentDetail.age }}岁
        </el-descriptions-item>
        <el-descriptions-item label="学历">
          {{ currentDetail.education }}
        </el-descriptions-item>
        <el-descriptions-item label="职业">
          {{ currentDetail.occupation }}
        </el-descriptions-item>
        <el-descriptions-item label="婚姻状况">
          <el-tag
            :type="currentDetail.marital_status === '未婚' ? 'success' : currentDetail.marital_status === '离异' ? 'warning' : 'info'">
            {{ currentDetail.marital_status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="户籍所在地" :span="2">
          {{ currentDetail.hukou_location }}
        </el-descriptions-item>
        <el-descriptions-item label="现居住地" :span="2">
          {{ currentDetail.current_residence }}
        </el-descriptions-item>
        <el-descriptions-item label="联系方式">
          {{ currentDetail.contact }}
        </el-descriptions-item>
        <el-descriptions-item label="生肖">
          {{ currentDetail.zodiac || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="性格" v-if="currentDetail.personality">
          {{ currentDetail.personality }}
        </el-descriptions-item>
        <el-descriptions-item label="家庭人员" v-if="currentDetail.family_members">
          {{ currentDetail.family_members }}
        </el-descriptions-item>
        <el-descriptions-item label="房车情况" v-if="currentDetail.property">
          {{ currentDetail.property }}
        </el-descriptions-item>
        <!-- 照片展示 - 已禁用 -->
        <!--
        <el-descriptions-item label="照片" :span="2" v-if="currentDetail.photos">
          <div class="detail-photos">
            <el-image v-for="(photo, index) in (currentDetail.photos ? JSON.parse(currentDetail.photos) : [])"
              :key="index" :src="photo"
              :preview-src-list="(currentDetail.photos ? JSON.parse(currentDetail.photos) : [])" :initial-index="index"
              fit="cover" style="width:80px;height:80px;margin-right:8px" preview-teleported />
          </div>
        </el-descriptions-item>
        -->
        <el-descriptions-item label="身高">
          {{ currentDetail.height ? currentDetail.height + 'cm' : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="收入">
          {{ currentDetail.income || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="择偶要求" :span="2" v-if="currentDetail.partner_requirement">
          {{ currentDetail.partner_requirement }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2" v-if="currentDetail.remark">
          {{ currentDetail.remark }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="showDetail = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 新增人员弹窗 -->
    <el-dialog v-model="showForm" title="新增人员信息" width="800px" destroy-on-close>
      <MemberForm @success="onFormSuccess" @cancel="showForm = false" />
    </el-dialog>

    <!-- 编辑人员弹窗 -->
    <el-dialog v-model="showEditForm" title="编辑人员信息" width="800px" destroy-on-close>
      <MemberForm :initial-data="currentEditItem" @success="onEditSuccess" @cancel="showEditForm = false" />
    </el-dialog>

    <!-- 打印预览弹窗 -->
    <el-dialog v-model="printDialogVisible" title="打印预览" width="800px" destroy-on-close>
      <el-select v-model="printTemplate" style="margin-bottom:20px;width:200px" placeholder="选择打印模板">
        <el-option value="classic" label="经典版" />
        <el-option value="minimal" label="极简版" />
      </el-select>

      <!-- 打印内容 -->
      <div class="print-preview" :class="printTemplate">
        <div class="watermark">丽姐·锦绣谱</div>

        <!-- 经典版 -->
        <div v-if="printTemplate === 'classic'" class="print-content-classic">
          <h2 style="text-align:center;font-family:'微软雅黑';margin-bottom:20px;color:#333">丽姐·锦绣谱信息表</h2>

          <table style="width:100%;border-collapse:collapse;font-family:'微软雅黑';font-size:14px;margin-bottom:20px">
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>姓名</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.name }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>性别</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.gender }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>年龄</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.age }}岁</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>学历</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.education }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>身高</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.height || '-' }}cm</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>职业</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.occupation }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>身高</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.height || '-' }}cm</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>现居住地</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.current_residence }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>联系方式</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.contact }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>生肖</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.zodiac || '-' }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>性格</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.personality || '-' }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>家庭人员</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.family_members || '-' }}</td>
            </tr>
          </table>

          <hr style="border:1px solid #ddd;margin:20px 0" />

          <h3 style="font-family:'微软雅黑';margin-top:20px;margin-bottom:10px;color:#333">个人情况及补充信息</h3>
          <div style="border:1px solid #ddd;padding:10px;margin-bottom:20px;min-height:100px;font-family:'微软雅黑';">
            {{ printData.remark || '' }}
          </div>

          <hr style="border:1px solid #ddd;margin:20px 0" />

          <h3 style="font-family:'微软雅黑';margin-top:20px;margin-bottom:10px;color:#333">择偶要求</h3>
          <div style="border:1px solid #ddd;padding:10px;margin-bottom:30px;min-height:100px;font-family:'微软雅黑';">
            {{ printData.partner_requirement || '无' }}
          </div>

          <hr style="border:1px solid #ddd;margin:20px 0" />

          <p style="text-align:center;font-family:'微软雅黑';font-size:14px;margin-top:30px">
            温馨提示：本信息内容由登记人提供真实信息；丽姐仅提供平台，不收取任何费用；谨防诈骗。
          </p>
        </div>



        <!-- 极简版 -->
        <div v-else class="print-content-minimal">
          <h2 style="text-align:center;font-family:'微软雅黑';margin-bottom:20px;color:#333">丽姐·锦绣谱信息表</h2>

          <table style="width:100%;border-collapse:collapse;font-family:'微软雅黑';font-size:14px;margin-bottom:20px">
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>姓名</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.name }}</td>
              <td style="border:1px solid #333;padding:8px"><strong>性别</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.gender }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>年龄</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.age }}岁</td>
              <td style="border:1px solid #333;padding:8px"><strong>身高</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.height || '-' }}cm</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>婚姻状况</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.marital_status }}</td>
              <td style="border:1px solid #333;padding:8px"><strong>学历</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.education }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>职业</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.occupation }}</td>
              <td style="border:1px solid #333;padding:8px"><strong>现居住地</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.current_residence }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>联系方式</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.contact }}</td>
              <td style="border:1px solid #333;padding:8px"><strong>生肖</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.zodiac || '-' }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>收入</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.income || '-' }}</td>
              <td style="border:1px solid #333;padding:8px"><strong>性格</strong></td>
              <td style="border:1px solid #333;padding:8px">{{ printData.personality || '-' }}</td>
            </tr>
            <tr>
              <td style="border:1px solid #333;padding:8px"><strong>家庭人员</strong></td>
              <td style="border:1px solid #333;padding:8px" colspan="3">{{ printData.family_members || '-' }}</td>
            </tr>
          </table>

          <h3 style="font-family:'微软雅黑';margin-top:20px;margin-bottom:10px;color:#333">个人情况及信息补充：</h3>
          <div style="border:1px solid #ddd;padding:10px;margin-bottom:20px;min-height:100px;">
            {{ printData.remark || '无' }}
          </div>

          <h3 style="font-family:'微软雅黑';margin-top:20px;margin-bottom:10px;color:#333">择偶标准：</h3>
          <div style="border:1px solid #ddd;padding:10px;margin-bottom:30px;min-height:100px;">
            {{ printData.partner_requirement || '无' }}
          </div>

          <div style="font-size:12px;color:#666;line-height:1.5;">
            <p>温馨提示：本信息内容由登记人提供真实信息；丽姐仅提供平台，不收取任何费用；谨防诈骗。</p>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="printDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmPrint">打印</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
  import { ref, reactive, onMounted, defineEmits, defineProps, watch } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { List, Search, View, Delete, Edit, Plus, Refresh, RefreshLeft, Download, Printer } from '@element-plus/icons-vue'
  import MemberForm from './MemberForm.vue'
  import { API_BASE_URL } from '../config/api'

  const emit = defineEmits(['delete'])
  const props = defineProps({
    initialFilters: {
      type: Object,
      default: () => ({})
    }
  })

  // 数据状态
  const members = ref([])
  const loading = ref(false)
  const page = ref(1)
  const pageSize = ref(10)
  const total = ref(0)
  const selectedRows = ref([])

  // 筛选条件
  const filters = reactive({
    search: '',
    gender: '',
    ageMin: null,
    ageMax: null,
    education: '',
    marital_status: '',
    sortField: 'created_at',
    sortOrder: 'desc'
  })

  // 详情弹窗
  const showDetail = ref(false)
  const currentDetail = ref({})

  // 新增人员弹窗
  const showForm = ref(false)

  // 编辑人员弹窗
  const showEditForm = ref(false)
  const currentEditItem = ref({})

  // 打印相关
  const printDialogVisible = ref(false)
  const printTemplate = ref('classic')
  const printData = ref({})

  // 打印方法
  const handlePrint = (row) => {
    printData.value = { ...row }
    printDialogVisible.value = true
  }

  const confirmPrint = () => {
    const printContent = document.querySelector('.print-preview')
    if (!printContent) return

    const printWindow = window.open('', '_blank')
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>打印会员资料</title>
        <style>
          body { margin: 20px; }
          .print-preview { position: relative; padding: 20px; background: #fff; }
          .print-preview.classic { font-family: "宋体"; }
          .print-preview.modern { font-family: "微软雅黑"; }
          .print-preview.minimal { font-family: "Arial"; }
          table { border-collapse: collapse; }
          table td { border: 1px solid #333; padding: 8px; }
          .watermark {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 60px;
            color: rgba(0, 0, 0, 0.05);
            pointer-events: none;
            white-space: nowrap;
            z-index: 0;
          }
          .print-content-classic, .print-content-modern, .print-content-minimal {
            position: relative;
            z-index: 1;
          }
          @media print {
            body { margin: 0; }
            .watermark { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
          }
        </style>
      </head>
      <body>${printContent.innerHTML}</body>
      </html>
    `)
    printWindow.document.close()
    printWindow.focus()
    setTimeout(() => {
      printWindow.print()
      printWindow.close()
    }, 500)
  }

  // 格式化日期
  const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return dateStr.substring(0, 16)
  }

  // 防抖搜索
  let searchTimer = null
  const debouncedSearch = () => {
    clearTimeout(searchTimer)
    searchTimer = setTimeout(() => {
      page.value = 1
      fetchMembers()
    }, 300)
  }

  // 搜索
  const handleSearch = () => {
    page.value = 1
    fetchMembers()
  }

  // 刷新列表
  const handleRefresh = () => {
    fetchMembers()
    ElMessage.success('已刷新')
  }

  // 重置查询
  const handleReset = () => {
    filters.search = ''
    filters.gender = ''
    filters.ageMin = null
    filters.ageMax = null
    filters.education = ''
    filters.marital_status = ''
    filters.sortField = 'created_at'
    filters.sortOrder = 'desc'
    page.value = 1
    fetchMembers()
    ElMessage.success('已重置查询条件')

    // 移除URL中的所有查询参数
    if (window.history.replaceState) {
      const url = new URL(window.location.href)
      // 对于hash模式，需要清空hash部分的查询参数
      if (url.hash) {
        const hash = url.hash.split('?')[0] // 只保留hash路径部分，移除查询参数
        url.hash = hash
      }
      window.history.replaceState({}, '', url.toString())
    }
  }

  // 排序变化
  const handleSortChange = ({ prop, order }) => {
    filters.sortField = prop || 'created_at'
    if (order === 'ascending') {
      filters.sortOrder = 'asc'
    } else if (order === 'descending') {
      filters.sortOrder = 'desc'
    } else {
      filters.sortOrder = 'desc'
    }
    fetchMembers()
  }

  // 导出数据
  const handleExport = async () => {
    try {
      loading.value = true

      const params = new URLSearchParams()
      if (filters.search) params.append('search', filters.search)
      if (filters.gender) params.append('gender', filters.gender)
      if (filters.ageMin) params.append('age_min', filters.ageMin)
      if (filters.ageMax) params.append('age_max', filters.ageMax)
      if (filters.education) params.append('education', filters.education)
      if (filters.marital_status) params.append('marital_status', filters.marital_status)

      const response = await fetch(`${API_BASE_URL}/members/export?${params}`)

      if (!response.ok) {
        throw new Error('导出失败')
      }

      const data = await response.json()

      if (data.total === 0) {
        ElMessage.warning('没有数据可导出')
        return
      }

      // 生成 CSV
      const headers = ['人员编号', '姓名', '性别', '年龄', '学历', '职业', '婚姻状况', '户籍所在地', '现居住地', '联系方式', '身高', '收入', '择偶要求', '登记时间', '备注']
      const rows = data.items.map(item => [
        item.member_no,
        item.name,
        item.gender,
        item.age,
        item.education,
        item.occupation,
        item.marital_status,
        item.hukou_location,
        item.current_residence,
        item.contact,
        item.height,
        item.income,
        item.partner_requirement,
        item.registration_time,
        item.remark
      ])

      const csvContent = [headers, ...rows]
        .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
        .join('\n')

      // 下载文件
      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `人员数据_${new Date().toISOString().slice(0, 10)}.csv`
      link.click()

      ElMessage.success(`导出成功，共 ${data.total} 条数据`)
    } catch (error) {
      ElMessage.error('导出失败: ' + error.message)
    } finally {
      loading.value = false
    }
  }

  // 分页大小变化
  const handleSizeChange = () => {
    page.value = 1
    fetchMembers()
  }

  // 页码变化
  const handleCurrentChange = () => {
    fetchMembers()
  }

  // 查看详情
  const viewDetail = (item) => {
    currentDetail.value = item
    showDetail.value = true
  }

  // 编辑人员
  const editMember = (item) => {
    currentEditItem.value = { ...item }
    showEditForm.value = true
  }

  // 表单提交成功
  const onFormSuccess = (message) => {
    ElMessage.success(message)
    showForm.value = false
    // 刷新列表
    fetchMembers()
  }

  // 编辑表单提交成功
  const onEditSuccess = (message) => {
    ElMessage.success(message)
    showEditForm.value = false
    // 刷新列表
    fetchMembers()
  }

  // 获取人员列表
  const fetchMembers = async () => {
    loading.value = true

    try {
      const params = new URLSearchParams({
        page: page.value,
        page_size: pageSize.value,
        sort_field: filters.sortField,
        sort_order: filters.sortOrder
      })

      if (filters.search) params.append('search', filters.search)
      if (filters.gender) params.append('gender', filters.gender)
      if (filters.ageMin) params.append('age_min', filters.ageMin)
      if (filters.ageMax) params.append('age_max', filters.ageMax)
      if (filters.education) params.append('education', filters.education)
      if (filters.marital_status) params.append('marital_status', filters.marital_status)

      const response = await fetch(`${API_BASE_URL}/members?${params}`)

      if (!response.ok) {
        throw new Error('获取数据失败')
      }

      const data = await response.json()
      members.value = data.items
      total.value = data.total
    } catch (error) {
      console.error('获取人员列表失败:', error)
      ElMessage.error('获取数据失败')
    } finally {
      loading.value = false
    }
  }

  // 页面加载时获取数据
  onMounted(() => {
    // 应用初始筛选条件
    if (props.initialFilters) {
      Object.keys(props.initialFilters).forEach(key => {
        if (filters.hasOwnProperty(key)) {
          filters[key] = props.initialFilters[key]
        }
      })
    }
    fetchMembers()
  })

  // 监听初始筛选条件变化
  watch(() => props.initialFilters, (newFilters) => {
    if (newFilters) {
      Object.keys(newFilters).forEach(key => {
        if (filters.hasOwnProperty(key)) {
          filters[key] = newFilters[key]
        }
      })
      fetchMembers()
    }
  }, { deep: true })

  // 处理选择变化
  const handleSelectionChange = (selection) => {
    selectedRows.value = selection
  }

  // 批量删除
  const handleBatchDelete = async () => {
    if (selectedRows.value.length === 0) return

    try {
      // 第一次确认
      await ElMessageBox.confirm(
        `确定要删除选中的 ${selectedRows.value.length} 条记录吗？`,
        '批量删除确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )

      // 第二次确认
      await ElMessageBox.confirm(
        `再次确认要删除选中的 ${selectedRows.value.length} 条记录吗？删除后无法恢复。`,
        '再次确认',
        {
          confirmButtonText: '确认删除',
          cancelButtonText: '取消',
          type: 'danger',
        }
      )

      // 批量删除逻辑
      const response = await fetch(`${API_BASE_URL}/members/batch-delete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ids: selectedRows.value.map(row => row.id)
        })
      })

      if (response.ok) {
        const result = await response.json()
        ElMessage.success(`删除成功，共删除 ${result.deleted_count} 条记录`)
        // 清空选择
        selectedRows.value = []
        // 刷新列表
        fetchMembers()
      } else {
        ElMessage.error('删除失败')
      }
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败: ' + error.message)
      }
    }
  }

  // 暴露方法给父组件
  defineExpose({
    refresh: fetchMembers
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

  .search-section {
    margin-bottom: 20px;
  }

  .action-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }

  .filter-section {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 8px;
  }

  .filter-input {
    width: 200px;
  }

  .filter-select {
    width: 130px;
  }

  .filter-number {
    width: 120px;
  }

  .member-table {
    width: 100%;
  }

  .pagination-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  @media (max-width: 768px) {
    .action-buttons {
      flex-direction: column;
    }

    .action-buttons .el-button {
      width: 100%;
    }

    .filter-section {
      flex-direction: column;
    }

    .filter-input,
    .filter-select,
    .filter-number {
      width: 100%;
    }
  }

  /* 打印样式 */
  .print-preview {
    position: relative;
    padding: 20px;
    background: #fff;
    min-height: 300px;
  }

  .print-preview.classic {
    font-family: "宋体";
  }

  .print-preview.modern {
    font-family: "微软雅黑";
  }

  .print-preview.minimal {
    font-family: "Arial";
  }

  .watermark {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-30deg);
    font-size: 60px;
    color: rgba(0, 0, 0, 0.05);
    pointer-events: none;
    white-space: nowrap;
    z-index: 0;
  }

  .print-content-classic,
  .print-content-modern,
  .print-content-minimal {
    position: relative;
    z-index: 1;
  }

  .detail-photos {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  @media print {
    .watermark {
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
  }
</style>