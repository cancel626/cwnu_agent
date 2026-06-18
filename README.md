# 西华师大数智校园中枢 (CWNU Agent)

基于大模型的校园数智服务一体化平台，集成数字员工、智能问数、即时通讯、内容安全审核等能力。

---

## 项目简介

本项目面向高校数字化场景，提供：

- **数智员工库**：创建并管理专属数字员工，支持大模型配置、能力工具绑定。
- **智能问数**：选择数字员工进行自然语言问答，会话持久化、可续聊。
- **即时通讯**：私聊、群聊，支持 `@` 数字员工，实时 WebSocket 消息推送。
- **文件消息**：聊天中可发送/接收文件与图片。
- **内容审核**：基于大模型的聊天消息违规检测，支持增量扫描。
- **数据可视化**：控制台首页展示数字员工数量、调用次数、最近常用联系人等统计。

---

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 后端 | Python + FastAPI + SQLAlchemy + MySQL |
| 用户端 | Vue 3 + Vite + Tailwind CSS + Pinia + Material Symbols |
| 管理端 | Vue 3 + Vite |
| 网关 | Node.js + Express + http-proxy-middleware |
| 通信 | WebSocket + RESTful API |

---

## 目录结构

```
.
├── backend/            # FastAPI 后端服务
│   ├── app/
│   │   ├── api/        # API 路由
│   │   ├── core/       # 配置、安全、数据库
│   │   ├── models/     # SQLAlchemy 数据模型
│   │   ├── schemas/    # Pydantic 校验模型
│   │   └── services/   # 业务服务
│   └── main.py         # 应用入口
├── user_frontend/      # 用户端前端
├── admin_frontend/     # 管理端前端
├── gateway/            # 统一网关与静态文件服务
└── README.md           # 本文件
```

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/cancel626/cwnu_agent.git
cd cwnu_agent
```

### 2. 后端启动

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate          # Windows
# source venv/bin/activate        # Linux/Mac
pip install -r requirements.txt

# 配置环境变量或修改 app/core/config.py
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. 网关启动

```bash
cd gateway
npm install
node server.js
```

访问地址：

- 用户端：`http://localhost:3000/user/`
- 管理端：`http://localhost:3000/admin/`
- 用户登录：`http://localhost:3000/user-login/`
- 管理登录：`http://localhost:3000/admin-login/`
- 后端 API：`http://localhost:8000`

### 4. 用户端/管理端开发

```bash
cd user_frontend
npm install
npm run dev      # http://localhost:5173/user/

cd admin_frontend
npm install
npm run dev      # 默认端口由 Vite 自动分配
```

---

## 主要功能

### 控制台首页

- 数字员工总数与活跃数
- 调用智能体累计次数
- 最近常用联系人（私聊 + 群聊）
- 系统运行日志

### 数智员工库

- 创建/编辑/删除数字员工
- 配置大模型 API、系统提示词
- 绑定工具能力

### 智能问数

- 下拉选择数字员工提问
- 对话消息自动保存到数据库
- 新建会话、加载历史会话、继续对话

### 即时通讯

- 私聊、群聊
- WebSocket 实时收发消息
- 文件/图片消息
- 群聊中 `@` 数字员工自动入群并回复

### 内容审核

- 大模型扫描聊天消息
- `is_scanned` 标记实现增量审核
- 仅扫描未审核消息，避免重复调用

---

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License
