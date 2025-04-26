# 智能求职助手系统部署文档

## 项目概述

智能求职助手是一个集改简历、写自荐信、搜工作和投简历为一体的Web应用，能够自动优化简历，根据简历搜索全球招聘网站的信息，匹配工作岗位并自动投递简历。

系统主要功能包括：

1. **简历管理** - 上传、分析和优化简历
2. **工作搜索** - 从多个招聘网站搜索工作信息
3. **工作匹配** - 分析简历与工作的匹配度
4. **自荐信生成** - 根据简历和工作描述自动生成个性化自荐信
5. **自动申请** - 自动填表和提交简历到招聘网站

## 技术栈

- **前端**: Next.js, React, TailwindCSS
- **后端**: Next.js API Routes, Cloudflare Workers
- **数据库**: Cloudflare D1 (SQLite)
- **部署**: Cloudflare Pages

## 部署指南

### 前提条件

- Node.js 18.x 或更高版本
- npm 9.x 或更高版本
- Cloudflare 账户（用于部署）

### 本地开发

1. **克隆项目**

```bash
git clone https://github.com/yourusername/job-assistant-web.git
cd job-assistant-web
```

2. **安装依赖**

```bash
npm install
```

3. **准备开发环境**

```bash
npm run prepare-deploy
```

这个命令会安装所有依赖、初始化本地数据库并应用数据库迁移。

4. **启动开发服务器**

```bash
npm run dev
```

现在，您可以在浏览器中访问 http://localhost:3000 查看应用。

### 部署到 Cloudflare

1. **登录 Cloudflare**

```bash
npx wrangler login
```

按照提示在浏览器中完成登录。

2. **部署应用**

```bash
npm run deploy
```

这个命令会构建应用并将其部署到 Cloudflare Pages。部署完成后，您将收到一个可访问的 URL（通常是 https://job-assistant-web.pages.dev）。

### 手动部署步骤

如果您想手动控制部署过程，可以按照以下步骤操作：

1. **准备部署环境**

```bash
node deploy-prep.js
```

2. **构建应用**

```bash
npm run build
```

3. **部署到 Cloudflare**

```bash
npx wrangler deploy
```

## 数据库管理

### 初始化数据库

```bash
npx wrangler d1 create job_assistant_db
```

### 应用数据库迁移

```bash
npx wrangler d1 execute job_assistant_db --file=migrations/0001_initial.sql
```

### 查看数据库内容

```bash
npx wrangler d1 execute job_assistant_db --command="SELECT * FROM users"
```

## 项目结构

```
job-assistant-web/
├── migrations/              # 数据库迁移文件
│   └── 0001_initial.sql     # 初始数据库结构
├── public/                  # 静态资源
├── src/
│   ├── app/                 # Next.js 应用页面
│   │   ├── api/             # API 路由
│   │   │   ├── application/ # 申请相关 API
│   │   │   ├── cover-letter/ # 自荐信相关 API
│   │   │   ├── job-matching/ # 工作匹配相关 API
│   │   │   ├── job-search/  # 工作搜索相关 API
│   │   │   └── resume/      # 简历相关 API
│   │   ├── application/     # 申请页面
│   │   ├── cover-letter/    # 自荐信页面
│   │   ├── job-matching/    # 工作匹配页面
│   │   ├── job-search/      # 工作搜索页面
│   │   ├── resume/          # 简历页面
│   │   ├── layout.tsx       # 布局组件
│   │   └── page.tsx         # 首页
│   ├── components/          # 可复用组件
│   │   └── Navbar.tsx       # 导航栏组件
│   └── lib/                 # 工具函数和库
│       └── database.ts      # 数据库配置
├── deploy-prep.js           # 部署准备脚本
├── deploy.js                # 部署脚本
├── package.json             # 项目依赖和脚本
└── wrangler.toml            # Cloudflare Workers 配置
```

## 使用指南

### 简历管理

1. 访问 `/resume` 页面
2. 上传您的简历（支持 PDF、DOCX 和 TXT 格式）
3. 系统会自动分析简历并提供改进建议
4. 您可以根据建议修改简历并下载改进后的版本

### 工作搜索

1. 访问 `/job-search` 页面
2. 输入搜索关键词、位置和其他过滤条件
3. 点击"搜索"按钮
4. 查看搜索结果并使用过滤器进一步筛选
5. 点击"生成报告"查看搜索结果的统计分析

### 工作匹配

1. 访问 `/job-matching` 页面
2. 上传您的简历
3. 系统会自动分析简历并匹配合适的工作
4. 查看匹配结果和匹配分数
5. 点击"生成匹配报告"查看详细的匹配分析

### 自荐信生成

1. 访问 `/cover-letter` 页面
2. 填写必要的个人信息和工作信息
3. 选择自荐信模板
4. 点击"生成自荐信"
5. 预览生成的自荐信并根据需要编辑
6. 下载或保存自荐信

### 自动申请

1. 访问 `/application` 页面
2. 填写申请表单
3. 上传简历和自荐信
4. 点击"提交申请"或"批量申请匹配职位"
5. 查看申请状态和历史

## 常见问题解答

### Q: 如何更新已部署的应用？

A: 修改代码后，再次运行 `npm run deploy` 即可更新应用。

### Q: 如何备份数据库？

A: 使用以下命令导出数据库：

```bash
npx wrangler d1 backup job_assistant_db
```

### Q: 如何在本地重置数据库？

A: 删除 `.wrangler` 目录，然后重新运行 `npm run prepare-deploy`。

### Q: 如何添加新的数据库迁移？

A: 在 `migrations` 目录中创建新的 SQL 文件（例如 `0002_add_new_table.sql`），然后运行：

```bash
npx wrangler d1 execute job_assistant_db --file=migrations/0002_add_new_table.sql
```

### Q: 应用支持哪些浏览器？

A: 应用支持所有现代浏览器，包括 Chrome、Firefox、Safari 和 Edge 的最新版本。

## 故障排除

### 部署失败

- 确保您已登录 Cloudflare（`npx wrangler login`）
- 检查 `wrangler.toml` 文件中的配置是否正确
- 尝试手动部署步骤，查看详细错误信息

### 数据库错误

- 确保已创建数据库（`npx wrangler d1 create job_assistant_db`）
- 确保已应用数据库迁移（`npx wrangler d1 execute job_assistant_db --file=migrations/0001_initial.sql`）
- 检查数据库连接配置

### 应用无法启动

- 确保已安装所有依赖（`npm install`）
- 检查 Node.js 版本是否兼容（推荐 18.x 或更高）
- 检查控制台错误信息

## 联系与支持

如果您在部署或使用过程中遇到任何问题，请通过以下方式联系我们：

- 提交 GitHub Issue
- 发送邮件至 support@example.com

## 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。
