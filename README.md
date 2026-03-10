# 婚介信息管理系统 - 部署指南

## 项目结构
```
marriage-registration/
├── backend/           # 后端 (Python FastAPI)
│   ├── main.py       # 主程序
│   └── requirements.txt
├── frontend/         # 前端 (Vue 3 + Vite)
│   ├── src/
│   │   ├── components/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── SPEC.md           # 技术规格文档
```

## 快速启动

### 1. 后端启动
```bash
cd marriage-registration/backend

# 创建虚拟环境（推荐）
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```
后端服务将在 http://localhost:8000 运行

### 2. 前端启动
```bash
cd marriage-registration/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```
前端将在 http://localhost:3000 运行

### 3. 访问系统
打开浏览器访问 http://localhost:3000 即可使用

## 功能说明
- 📝 **新增登记**: 填写双方信息、登记日期、地点等
- 📋 **登记列表**: 查看所有登记记录，支持搜索和分页
- 👁️ **查看详情**: 点击查看完整登记信息
- 🗑️ **删除记录**: 删除不需要的登记记录

## 注意事项
- 首次启动后端会自动创建 SQLite 数据库文件 (marriage.db)
- 身份证号会进行脱敏显示，保护隐私
- 数据默认保存在本地数据库文件中

## 生产环境部署
### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 前端构建
```bash
cd frontend
npm install
npm run build
# 构建产物在 dist/ 目录
```
可以使用 Nginx 或任何静态文件服务器托管 dist/ 目录

---
💕 祝哥哥使用愉快！
