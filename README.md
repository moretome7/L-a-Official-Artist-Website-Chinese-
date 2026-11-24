# Léa 中文个人艺术家官网

Léa 的个人艺术家官网，以星球、星云、月相与深空为主题，采用安静克制、低饱和和大量留白的画廊视觉。公开前台使用 Vue 3，Django 负责网站入口、静态资源托管和管理后台。

## 技术栈

| 层级 | 技术 |
| --- | --- |
| Python | CPython 3.11.9 |
| 后端 | Django 5.2.19 |
| 管理后台 | django-simpleui 2026.1.13 |
| 前端 | Vue 3.5 + TypeScript 5.9 |
| 构建工具 | Vite 8 |
| 数据库 | SQLite |

## 网站内容

公开前台包含首页、作品、关于、委托和联系五个页面，支持：

- 星球、星云、月相、深空系列作品筛选
- 媒介标签组合筛选
- 4:5 响应式作品画廊
- 大图预览和上一张/下一张切换
- 委托咨询自动预填作品名称
- 委托需求表单和联系留言表单
- 桌面端与移动端响应式布局
- SimpleUI 中文管理后台

## 本地运行

要求 Windows PowerShell、Python 3.11 和 Node.js。

```powershell
# 1. 创建并激活虚拟环境
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. 安装依赖
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm --prefix frontend install

# 3. 初始化数据库
.\.venv\Scripts\python.exe manage.py migrate

# 4. 构建 Vue 前台
npm --prefix frontend run build

# 5. 启动 Django，同时提供前台和后台
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

如果 PowerShell 阻止激活脚本，无需激活，直接执行 `.\.venv\Scripts\python.exe` 命令即可。

访问地址：

- 前台：<http://127.0.0.1:8000/>
- 管理后台：<http://127.0.0.1:8000/admin/>

首次创建管理员：

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## 环境变量

本地开发可直接使用默认设置。部署到其他环境前，请设置安全的 `DJANGO_SECRET_KEY`，并按需设置：

```powershell
$env:DJANGO_SECRET_KEY = "your-long-random-secret"
$env:DJANGO_DEBUG = "False"
$env:DJANGO_ALLOWED_HOSTS = "example.com,www.example.com"
```

可参考 `.env.example`。项目不会提交本地数据库、虚拟环境、日志、真实环境变量或前端构建缓存。

## 构建方式

Vite 读取 `frontend/vite.config.ts`，将带哈希的构建文件输出到 `website/static/frontend/`，同时生成 `.vite/manifest.json`。Django 视图读取 manifest 后向前台模板注入实际资源路径，模板中不硬编码构建哈希。

修改 `frontend/src/` 后需要重新执行：

```powershell
npm --prefix frontend run build
```

## 常用验证命令

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
npm --prefix frontend run build
```

## 项目结构

```text
lea_site/       Django 项目配置
website/        Django 应用、视图、模板和静态资源
frontend/       Vue + TypeScript + Vite 前端源码
manage.py       Django 管理入口
requirements.txt
```

本项目的代理开发规范见 [AGENTS.md](AGENTS.md)。
