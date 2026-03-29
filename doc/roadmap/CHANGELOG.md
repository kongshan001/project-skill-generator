# Project Skill Generator - 版本更新日志

## 版本命名规范

- **主版本号 (MAJOR)**: 架构重大变更、不兼容更新
- **次版本号 (MINOR)**: 新增功能、改进
- **修订号 (PATCH)**: Bug 修复、小优化

格式: `v{MAJOR}.{MINOR}.{PATCH}`

---

## v0.1.0 - 2026-03-29 (初始版本)

### 新增功能
- ✅ 代码库分析脚本 `analyze_codebase.py`
- ✅ 技能生成脚本 `generate_skill.py`
- ✅ 代理生成脚本 `generate_agent.py`
- ✅ 技能更新脚本 `update_skills.py`
- ✅ 基础文档和示例

### 待验证
- ⏳ Python 项目适配
- ⏳ TypeScript 项目适配
- ⏳ C++ 项目适配
- ⏳ Claude Code 集成验证
- ⏳ 实际业务需求验证

### 已知问题
- 🔴 暂无实际项目验证
- 🔴 缺少错误处理和边界情况
- 🔴 未支持多语言 AST 解析

---

## v0.1.1 - 2026-03-29 (紧急修复)

### 问题修复
- 🔧 **模块发现逻辑改进**
  - 支持无 `__init__.py` 的 Python 项目
  - 添加目录分组策略
  - 混合发现策略（标准模块 + 扁平结构）

### 已知问题 (来自 remote-shell 验证)
- 🔴 模块发现失败：项目没有 `__init__.py` 导致识别 0 个模块
- 🟡 分析结果不准确：即使找到 entry points 也无法提取详细信息

### 验证进度
- ⏳ remote-shell - 发现问题，等待修复后重试

---

## 下一版本计划 (v0.2.0)

### 目标
- 完成 3 个 Python 项目验证
- 修复验证过程中发现的问题
- 优化技能生成质量

### 待办
- [x] remote-shell 验证 - 发现问题
- [ ] 修复模块发现问题
- [ ] 重试 remote-shell 验证
- [ ] game-auto-test 验证
- [ ] wangzhe-chess 验证
- [ ] 根据验证结果优化脚本
- [ ] 添加错误处理

---

## 长期路线图

### v0.3.0
- 支持多语言 AST 解析
- 深度语义分析
- 自动生成测试用例

### v0.4.0
- CI/CD 集成
- Pre-commit Hook 支持
- Web UI 管理界面

### v1.0.0
- 多仓库支持
- 技能市场
- ML 模式检测
