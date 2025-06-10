# CollabW - 项目协作管理平台

CollabW 是一个现代化的项目协作管理平台，采用前后端分离架构，提供完整的项目管理、任务分配、团队协作和绩效分析功能。

## ✨ 主要特性

- **用户认证与权限管理**: 支持三级用户角色（总监/经理/员工），基于角色的权限控制
- **项目管理**: 创建、编辑、删除项目，支持项目状态跟踪和进度管理
- **任务管理**: 灵活的任务分配、状态更新和工作量评估
- **实时协作**: 团队成员实时协作，任务状态同步更新
- **甘特图可视化**: 项目时间线可视化，支持关键路径分析
- **燃尽图分析**: 项目进度跟踪和风险预警
- **绩效评估**: 基于任务完成情况的员工绩效自动计算
- **响应式设计**: 完美适配桌面端和移动端设备

## 🏗️ 技术架构

### 后端技术栈
- **FastAPI**: 现代化的Python Web框架
- **SQLAlchemy**: ORM数据库操作
- **SQLite**: 轻量级数据库
- **Pydantic**: 数据验证和序列化
- **JWT**: 用户认证和授权
- **NetworkX**: 关键路径算法

### 前端技术栈
- **Vue 3**: 渐进式JavaScript框架
- **Vite**: 快速构建工具
- **TypeScript**: 类型安全的JavaScript
- **Pinia**: 状态管理
- **Vue Router**: 前端路由
- **Axios**: HTTP客户端
- **ECharts**: 数据可视化
- **Frappe Gantt**: 甘特图组件

### 部署技术栈
- **Docker**: 容器化部署
- **Docker Compose**: 多容器编排
- **健康检查**: 服务监控和自动恢复
- **数据卷**: 数据持久化和热重载
- **网络隔离**: 服务间安全通信

## 📁 项目结构

```
CollabW/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由和端点
│   │   ├── core/           # 核心功能（配置、常量、工具）
│   │   ├── db/             # 数据库配置和初始化
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   └── services/       # 业务逻辑服务
│   ├── tests/              # 测试用例
│   ├── main.py             # 应用入口
│   ├── requirements.txt    # Python依赖
│   ├── Dockerfile          # 后端Docker配置
│   └── .dockerignore       # Docker忽略文件
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── stores/         # Pinia状态管理
│   │   ├── utils/          # 工具函数和常量
│   │   ├── views/          # 页面组件
│   │   └── types/          # TypeScript类型定义
│   ├── package.json        # NPM依赖
│   ├── vite.config.ts      # Vite配置
│   ├── Dockerfile          # 前端Docker配置
│   └── .dockerignore       # Docker忽略文件
├── logs/                   # 日志目录（Docker环境）
│   ├── backend/            # 后端日志
│   └── frontend/           # 前端日志
├── docker-compose.yml      # Docker容器编排配置
├── start-dev.ps1           # Windows开发环境启动脚本
├── start-dev.sh            # Linux/macOS开发环境启动脚本
└── README.md               # 项目文档
```

## 🚀 快速开始

### 环境要求

#### Docker部署（推荐）
- Docker 20.10+
- Docker Compose 2.0+

#### 本地开发
- Python 3.8+
- Node.js 16+
- Git

### Docker部署（推荐）

#### 一键启动
```powershell
# Windows PowerShell
.\start-dev.ps1

# Linux/macOS
./start-dev.sh
```

#### 手动启动
```bash
# 构建并启动所有服务
docker-compose up --build -d

# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 常用Docker命令
```bash
# 重启特定服务
docker-compose restart backend
docker-compose restart frontend

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 进入容器调试
docker-compose exec backend bash
docker-compose exec frontend sh

# 清理环境（删除容器、网络和数据卷）
docker-compose down -v --remove-orphans
```

### 本地开发部署

#### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd collabw
   ```

2. **后端设置**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m app.db.init_db
   ```

3. **前端设置**
   ```bash
   cd frontend
   npm install
   ```

#### 运行应用

1. **启动后端服务**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **启动前端服务**
   ```bash
   cd frontend
   npm run dev
   ```

### 访问应用

无论使用哪种部署方式，应用都将在以下地址可用：

- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000  
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/ 和 http://localhost:3000/

## 🔧 代码优化亮点

### 后端优化
- **统一常量管理**: 集中管理枚举、错误信息、状态码等常量
- **工具函数封装**: 统一错误处理、数据验证、分页查询等通用功能
- **权限检查装饰器**: 基于角色的权限控制，简化权限验证逻辑
- **标准化错误处理**: 统一的异常处理和响应格式
- **模块化架构**: 清晰的代码分层和模块划分

### 前端优化
- **统一状态管理**: 使用Pinia进行全局状态管理
- **类型安全**: 完整的TypeScript类型定义
- **工具函数复用**: 统一的工具函数和常量管理
- **API客户端封装**: 统一的HTTP请求处理和错误拦截
- **组件化设计**: 高度可复用的Vue组件
- **响应式布局**: 适配多种设备尺寸

### 代码质量提升
- ✅ 消除重复代码
- ✅ 统一命名规范
- ✅ 标准化错误处理
- ✅ 完善类型定义
- ✅ 模块化架构
- ✅ 可维护性增强

## 👥 用户角色

### 总监 (Director)
- 查看所有项目和任务
- 访问绩效看板
- 查看甘特图和关键路径分析

### 经理 (Manager)
- 创建和管理项目
- 分配任务和团队成员
- 查看项目进度和燃尽图
- 计算团队绩效

### 员工 (User)
- 查看分配的任务
- 更新任务状态
- 个人工作台管理
- 参与项目协作

## 🔐 权限控制

系统采用基于角色的访问控制(RBAC)：
- 后端使用JWT认证 + 角色装饰器
- 前端使用路由守卫 + 权限组件
- 细粒度的功能权限控制

## 📊 核心功能

### 项目管理
- 项目创建、编辑、删除
- 项目状态跟踪
- 项目依赖关系管理
- 团队成员分配

### 任务管理
- 任务创建和分配
- 工作量评估（轻量/中等/繁重）
- 任务状态更新
- 负责人指定

### 数据可视化
- **甘特图**: 项目时间线和依赖关系
- **燃尽图**: 项目进度和风险分析
- **关键路径**: 项目关键节点识别
- **绩效图表**: 团队和个人绩效展示

## 🧪 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

## 🐳 Docker部署详解

### Docker架构特性

- **服务隔离**: 前后端服务独立容器运行
- **健康检查**: 自动监控服务状态，异常时自动重启
- **数据持久化**: SQLite数据库和日志文件持久化存储
- **热重载**: 开发环境代码变更自动重载
- **网络隔离**: 专用Docker网络确保服务间安全通信
- **依赖管理**: 前端服务依赖后端服务健康状态

### 容器配置

#### 后端容器 (collabw-backend)
- **基础镜像**: Python 3.11-slim
- **端口映射**: 8000:8000
- **数据卷**: 
  - 源码热重载: `./backend:/app`
  - 数据库持久化: `db_data:/app/db`
  - 日志存储: `./logs/backend:/app/logs`
- **环境变量**: 开发模式、调试启用、CORS配置

#### 前端容器 (collabw-frontend)
- **基础镜像**: Node.js 18-alpine
- **端口映射**: 3000:3000
- **数据卷**:
  - 源码热重载: `./frontend:/app`
  - Node模块隔离: `/app/node_modules`
  - 日志存储: `./logs/frontend:/app/logs`
- **环境变量**: Vite开发配置、API代理设置

### 启动脚本使用

#### Windows PowerShell
```powershell
# 一键启动开发环境
.\start-dev.ps1

# 检查服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f
```

#### Linux/macOS
```bash
# 赋予执行权限
chmod +x start-dev.sh

# 一键启动开发环境
./start-dev.sh

# 检查服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f
```

### 数据管理

#### 数据卷说明
- `collabw_db_data`: SQLite数据库持久化存储
- `./logs/`: 应用日志文件（映射到主机目录）

#### 数据备份
```bash
# 备份数据库
docker-compose exec backend cp /app/db/database.db /app/logs/backup_$(date +%Y%m%d_%H%M%S).db

# 备份数据卷
docker run --rm -v collabw_db_data:/data -v $(pwd):/backup alpine tar czf /backup/db_backup.tar.gz -C /data .
```

#### 数据恢复
```bash
# 恢复数据卷
docker run --rm -v collabw_db_data:/data -v $(pwd):/backup alpine tar xzf /backup/db_backup.tar.gz -C /data
```

### 故障排除

#### 常见问题

1. **端口被占用**
   ```bash
   # 检查端口占用
   netstat -ano | findstr :3000
   netstat -ano | findstr :8000
   
   # 修改docker-compose.yml中的端口映射
   ```

2. **服务启动失败**
   ```bash
   # 查看详细日志
   docker-compose logs backend
   docker-compose logs frontend
   
   # 重新构建镜像
   docker-compose build --no-cache
   ```

3. **数据库连接问题**
   ```bash
   # 检查数据库文件权限
   docker-compose exec backend ls -la /app/db/
   
   # 重新初始化数据库
   docker-compose exec backend python -m app.db.init_db
   ```

4. **前端访问问题**
   ```bash
   # 检查CORS配置
   docker-compose exec backend env | grep CORS
   
   # 检查网络连接
   docker-compose exec frontend wget -qO- http://backend:8000/
   ```

## 📝 API文档

启动后端服务后访问 http://localhost:8000/docs 查看完整的API文档。

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔮 未来规划

### 功能扩展
- [ ] 实时消息通知
- [ ] 文件上传和管理
- [ ] 项目模板功能
- [ ] 移动端APP
- [ ] 集成第三方服务
- [ ] 高级报表分析

### 技术优化
- [ ] 生产环境Docker配置优化
- [ ] 多阶段Docker构建减小镜像体积
- [ ] 集成CI/CD自动化部署
- [ ] Kubernetes集群部署支持
- [ ] 数据库集群和缓存优化
- [ ] 微服务架构拆分

---

**CollabW** - 让团队协作更高效 🚀