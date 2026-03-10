# 婚姻登记管理系统 - 技术规格说明书

## 1. 项目概述

- **项目名称**: 婚姻登记管理系统
- **项目类型**: Web全栈应用
- **核心功能**: 婚姻登记信息录入与查询列表
- **目标用户**: 个人使用
- **技术栈**: Vue 3 + Vite + Tailwind CSS | Python FastAPI + SQLite

## 2. UI/UX 规格

### 2.1 整体风格
- **设计风格**: 简约现代，温重大气
- **配色方案**:
  - 主色: `#8B5CF6` (紫色 - 象征浪漫与庄重)
  - 辅色: `#F59E0B` (金色 - 象征美好祝福)
  - 背景: `#FAFAFA` (浅灰白)
  - 文字: `#1F2937` (深灰)
  - 边框: `#E5E7EB` (浅灰)
- **字体**: 系统默认无衬线字体

### 2.2 页面结构
- **顶部导航栏**: 系统标题 + 简洁Logo
- **主内容区**: 卡片式布局
- **两个核心功能**:
  1. 录入表单（新登记）
  2. 登记列表（查询）

### 2.3 响应式设计
- 移动端适配 (375px+)
- 桌面端优化 (1024px+)

## 3. 功能规格

### 3.1 录入功能
**表单字段**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| 登记编号 | 文本 | 是 | 自动生成 UUID |
| 新郎姓名 | 文本 | 是 | |
| 新郎身份证号 | 文本 | 是 | 18位身份证 |
| 新娘姓名 | 文本 | 是 | |
| 新娘身份证号 | 文本 | 是 | 18位身份证 |
| 登记日期 | 日期 | 是 | |
| 登记地点 | 文本 | 是 | |
| 结婚证编号 | 文本 | 否 | |
| 备注 | 文本 | 否 | |

### 3.2 列表查询功能
- **表格展示**: 分页列表，每页10条
- **搜索功能**: 按新郎/新娘姓名模糊搜索
- **操作**: 查看详情、删除记录

### 3.3 数据接口
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/registrations` | GET | 获取登记列表（支持搜索、分页） |
| `/api/registrations` | POST | 新增登记记录 |
| `/api/registrations/:id` | GET | 获取单条记录详情 |
| `/api/registrations/:id` | DELETE | 删除记录 |

## 4. 数据库设计

### 表: registrations
```sql
CREATE TABLE registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_no TEXT UNIQUE NOT NULL,
    groom_name TEXT NOT NULL,
    groom_id_card TEXT NOT NULL,
    bride_name TEXT NOT NULL,
    bride_id_card TEXT NOT NULL,
    registration_date DATE NOT NULL,
    registration_location TEXT NOT NULL,
    certificate_no TEXT,
    remark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 5. 验收标准
- [ ] 录入表单能正常提交并保存到数据库
- [ ] 列表页面能展示所有登记记录
- [ ] 搜索功能正常工作
- [ ] 删除功能正常工作
- [ ] 界面美观简约，响应式适配良好
- [ ] 前后端联调正常，无明显报错