# 捐书网站

这是一个基于 Flask 后端和 Vue 3 前端的捐书网站示例项目。

## 目录结构

- `backend/` - Flask 后端应用
- `frontend/` - Vue 3 + Vite 前端应用

## 快速启动

### 后端

1. 进入后端目录：`cd backend`
2. 创建虚拟环境：`python -m venv venv`
3. 激活虚拟环境：
   - Windows: `venv\\Scripts\\Activate.ps1` 或 `venv\\Scripts\\activate.bat`
4. 安装依赖：`pip install -r requirements.txt`
5. 启动后端服务器：`python app.py`

### 前端

1. 进入前端目录：`cd frontend`
2. 安装依赖：`npm install`
3. 启动开发服务：`npm run dev`

## 功能说明

- 用户注册 / 登录 / 登出
- 用户详情页面
- 用户个人捐书记录页面
- 书籍分类筛选
- 捐书时选择分类并填写ISBN
- 首页展示两种视图模式：卡片视图和列表视图
- 书籍封面显示（支持ISBN自动获取封面）
- 弹窗捐书表单
- 查看当前捐书列表与捐赠者信息

## 技术特性

- **前端**: Vue 3 + Arco Design + Pinia 状态管理
- **后端**: Flask + SQLite
- **视图模式**: 卡片视图和列表视图切换
- **书籍封面**: 基于ISBN自动获取Google Books API封面
- **响应式设计**: 支持移动端和桌面端

## 默认测试账号

- `alice` / `password`
- `bob` / `password`

## 功能说明

- 查看捐书列表
- 添加新的捐书信息
- 前端与后端通过 REST API 通信
