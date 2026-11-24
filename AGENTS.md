# AGENTS.md - Léa Personal Website

本文件适用于项目根目录 `E:\Léa个人网址开发` 及其全部子目录。

## 1. 项目目标

这是一个面向 Léa 的个人网站项目，包含：

- 对公众开放的个人网站：首页、关于、作品、联系方式。
- 基于 Django 的管理后台，使用 SimpleUI 主题。
- Django 负责后端、路由、静态资源服务和后台；Vue 负责公开前台。

## 2. 技术栈

| 层级 | 技术 | 当前基线 |
| --- | --- | --- |
| Python | CPython | 3.11.9 |
| 后端 | Django | 5.2.19 |
| 后台 | django-simpleui | 2026.1.13 |
| 前端 | Vue | 3.5.46 |
| 构建 | Vite | 8.3.8 |
| 语言 | TypeScript | 5.9.x |
| 数据库 | SQLite | `db.sqlite3` |
| 运行环境 | Windows PowerShell | 不使用 WSL |

## 3. 架构约定

```text
浏览器
  ├─ GET /          -> Django website.views.home
  │                  -> website/templates/website/home.html
  │                  -> Vue 构建产物（JS + CSS）
  └─ GET /admin/    -> Django Admin + SimpleUI
```

前端构建链路：

```text
frontend/src/App.vue
  -> Vite
  -> website/static/frontend/assets/*
  -> website/static/frontend/.vite/manifest.json
  -> website/views.py 读取 manifest
  -> Django 模板注入带哈希的 JS/CSS 地址
```

关键文件：

- `frontend/src/App.vue`：公开网站页面内容与 Vue 组件逻辑。
- `frontend/src/style.css`：公开网站全部视觉样式与响应式规则。
- `frontend/src/main.ts`：Vue 应用入口。
- `frontend/vite.config.ts`：构建目录、静态资源前缀和 manifest 配置。
- `website/views.py`：读取 Vite manifest，向前台模板传递资源。
- `website/templates/website/home.html`：只保留 `#app` 挂载点和资源标签。
- `website/urls.py`：公开网站路由。
- `lea_site/settings.py`：Django、SimpleUI、语言、时区和静态文件配置。
- `lea_site/urls.py`：后台与网站的顶层路由。

## 4. 必须遵守的约束

1. 公开前台继续使用 Vue，不要恢复为 Django 模板直接渲染整页内容。
2. Django Admin 和 SimpleUI 必须保留；不要用 Vue 替换 `/admin/`。
3. 不要在模板或 Python 代码中硬编码 `index-xxxxx.js`、`index-xxxxx.css` 等构建哈希。资源地址必须来自 manifest。
4. `frontend/vite.config.ts` 中的以下约定不能随意改动：
   - `base: "/static/frontend/"`
   - `outDir: "../website/static/frontend"`
   - `manifest: true`
5. 不要直接修改 `website/static/frontend/` 下的构建产物。修改 `frontend/src/` 后重新构建。
6. 不要直接修改 `.venv/`、`frontend/node_modules/`、`db.sqlite3` 或日志文件。
7. 开发后台默认语言保持 `zh-hans`，时区保持 `Asia/Shanghai`，除非需求明确要求改变。
8. 不要把管理员密码、密钥或邮箱凭据写入源码、文档、测试或提交记录。
9. 开发环境已有超级管理员，不要无故删除、重建或重置；需要调整账号时先确认需求。
10. 除非明确要求，不要引入 Vue Router、状态管理库、UI 框架或后端 API 框架。当前网站采用单页锚点导航，没有前端路由。

## 5. 环境初始化

在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm --prefix frontend install
```

如需激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows PowerShell 中如激活脚本受执行策略限制，可以继续使用 `.\.venv\Scripts\python.exe` 直接运行 Python 命令。

## 6. 常用命令

所有命令默认从项目根目录执行。

### Django

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

### Vue

```powershell
npm --prefix frontend run dev
npm --prefix frontend run build
npm --prefix frontend run preview
```

正式访问由 Django 提供：

- 前台：`http://127.0.0.1:8000/`
- 后台：`http://127.0.0.1:8000/admin/`

`npm run dev` 只用于前端快捷预览；要与当前 Django 集成方式保持一致，必须执行 `npm run build` 更新静态产物。

## 7. 开发流程

### 修改公开前台

1. 修改 `frontend/src/App.vue`、`frontend/src/style.css`，必要时调整 `frontend/src/main.ts`。
2. 执行 `npm --prefix frontend run build`。
3. 刷新 `http://127.0.0.1:8000/` 验证页面。
4. 检查桌面端和移动端布局，并确认控制台无错误。

### 修改 Django 后端或路由

1. 修改 `website/` 或 `lea_site/` 中的源码。
2. 如有模型变更，创建并应用迁移。
3. 执行 `manage.py check` 和 `manage.py test`。
4. 重启 Django 服务并验证相关 URL。

### 新增后台功能

- 在 `website/models.py` 中定义模型。
- 在 `website/admin.py` 中注册并配置后台展示。
- 生成迁移：
  ```powershell
  .\.venv\Scripts\python.exe manage.py makemigrations
  .\.venv\Scripts\python.exe manage.py migrate
  ```
- 更新 `website/tests.py`，至少覆盖关键行为。
- 保持 SimpleUI 管理界面的中文显示。

### 新增前后端交互

当前项目没有 REST API 框架，也没有业务模型。若确实需要数据交互：

- 优先增加小而清晰的 Django JSON 视图或正式 API 端点。
- 明确 CSRF、错误处理、空状态和加载状态。
- 只有需求足够复杂时才考虑 Django REST Framework；不要仅因“以后可能用”而引入。

## 8. 前端开发规范

- 使用 Vue 3 Composition API 和 `<script setup lang="ts">`。
- 页面内容修改优先集中在 `frontend/src/App.vue`。
- 视觉设计修改优先集中在 `frontend/src/style.css`。
- 当前设计语言为米色、陶土色、浅绿色，保留柔和、编辑感和个人化风格。
- 保持响应式布局，重点检查 360px、768px、1280px 左右宽度。
- 使用语义化 HTML、可见的键盘焦点和合理的 ARIA 标签。
- 导航使用现有 `#about`、`#work`、`#contact` 锚点，除非明确要求扩展为多页面应用。
- 不使用未安装的依赖；新增依赖前先确认确有必要，并同步更新 `package.json` 和锁文件。
- 不要在 Vue 组件中写入真实密码、私密令牌或未脱敏的个人数据。

## 9. 后端开发规范

- 遵循 Django 项目结构，业务逻辑优先放在应用内，不把大量逻辑写进模板。
- 配置集中在 `lea_site/settings.py`，路由集中在 `lea_site/urls.py` 和应用自己的 `urls.py`。
- 模板只负责 DOM 挂载点和渲染所需资源，不复制 Vue 页面内容。
- 视图应保持清晰、可测试；当前首页视图负责读取构建 manifest。
- 模型变更必须包含迁移文件；不要手工修改数据库结构。
- 管理后台注册项应提供便于中文运营人员理解、搜索和筛选的配置。

## 10. 测试与验收

提交或声称完成前，至少执行：

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
npm --prefix frontend run build
```

验收标准：

- Django system check 无错误。
- Python 测试全部通过。
- Vue TypeScript 检查通过且 Vite 构建成功。
- `http://127.0.0.1:8000/` 返回 200，并包含 Vue 挂载点。
- 首页引用的 JS 和 CSS 静态资源均返回 200。
- `http://127.0.0.1:8000/admin/` 可访问，SimpleUI 和中文界面正常。
- 页面在桌面和移动视口下没有明显溢出、遮挡或不可点击问题。

不要只凭“代码看起来正确”宣布完成；需要实际运行检查。

## 11. Windows 与运行环境注意事项

- 当前环境是 Windows PowerShell，不要使用 bash、`source` 或 WSL 命令。
- 不要拼接出 `frontend\frontend` 等重复路径。
- PowerShell 的 `$HOME` 是只读变量，脚本中不要覆盖它。
- 启动服务前先检查 8000 端口：
  ```powershell
  Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
  ```
- 避免重复启动多个 Django 进程。修改 Python 或其配置后，需要重新启动服务。
- 使用 `--noreload` 启动时，后端代码变更不会自动重载。
- 构建输出目录已被 `.gitignore` 忽略；新环境首次运行前必须先构建前端。
- 日志文件是运行输出，不要作为源码编辑。

## 12. 当前项目状态

- `website/models.py` 尚无业务模型。
- `website/admin.py` 尚未注册自定义模型。
- 公开网站只有一个首页路由 `/`。
- 前台没有 Vue Router，使用锚点导航。
- 管理员账号和密码由用户管理，不在本文件记录。
- 当前开发服务器通常运行在 `127.0.0.1:8000`。

## 13. 交付风格

- 与用户沟通使用中文。
- 修改应聚焦用户当前需求，避免无关重构。
- 汇报时说明修改了什么、如何验证、当前访问地址，以及仍需用户处理的事项。
- 不要将未执行的测试或未验证的功能描述为已完成。