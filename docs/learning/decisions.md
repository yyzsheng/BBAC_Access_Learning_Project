# 技术决策记录

## 已确定的决策

| 日期 | 决策 | 原因 | 后续影响 |
|---|---|---|---|
| 初始化 | 后端使用 FastAPI | 已有少量 Python 基础，适合项目式学习 | 后端统一使用 Python 类型注解和 Pydantic |
| 初始化 | 前端使用 Vue 3 + TypeScript | 适合管理后台和组件化开发 | 必须先学习 JavaScript 和 TypeScript |
| 初始化 | 数据库使用 MySQL 8 | 适合内部正式系统和大量刷卡记录 | 学习 SQL、索引、事务和备份 |
| 初始化 | 第一版使用 Excel/CSV 导入 | 暂不对接供应商硬件和实时接口 | 必须实现校验、去重和错误报告 |
| 初始化 | 使用 Docker 部署到 Linux | 便于稳定部署、备份和迁移 | 后期学习 Linux、Docker 和 Nginx |
