# BBAC 门禁管理系统学习项目

这是一个从零学习并逐步完成的正式 Web 项目，不复制现有单文件 Demo 代码。

## 项目目标

- 管理约 20,000 名持卡人员和 NFC 卡号。
- 管理 MRA、PT1、PT2 及内部属地权限。
- 通过 Excel/CSV 导入和查询刷卡记录。
- 提供访客、重点人员、审批、审计和总览功能。
- 最终部署到 Linux 服务器并由 Docker 运行。
- 不涉及门锁、控制器、读卡器等物理硬件。

## 计划技术栈

- 前端：Vue 3、TypeScript、Vite、Element Plus、Pinia、Vue Router、Axios、ECharts。
- 后端：Python 3.12、FastAPI、SQLAlchemy 2、Alembic、Pydantic、Pytest。
- 数据库：MySQL 8。
- 部署：Docker Compose、Nginx、Linux。

## 当前状态

- [x] 学习项目初始化
- [ ] 第 1 周第 1 天：环境检查与第一个 Python 程序
- [ ] Vue 前端初始化
- [ ] FastAPI 后端初始化
- [ ] MySQL 数据库初始化
- [ ] 内部测试部署

## 学习规则

1. 每天亲手输入和运行代码。
2. 先理解原因，再使用代码。
3. 每完成一个小功能就运行检查并提交 Git。
4. 错误必须记录在 `docs/learning/error-book.md`。
5. 每周完成一次复盘和验收。

详细安排见 [BBAC门禁管理系统学习计划.md](./BBAC门禁管理系统学习计划.md)。
