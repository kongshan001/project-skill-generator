# Project Skill Generator - 自动验证系统

> 🚀 自动化验证所有 GitHub 仓库，持续改进技能生成质量

---

## 📋 系统概述

本系统用于自动化验证 `project-skill-generator` 技能，通过实际项目验证来持续改进质量。

### 核心功能

- ✅ **自动验证**: 每30分钟自动验证一个仓库
- ✅ **问题追踪**: 自动记录发现的问题
- ✅ **版本管理**: 通过 CHANGELOG 追踪改进
- ✅ **报告生成**: 为每次验证生成详细报告

---

## 🗂️ 目录结构

```
skills/project-skill-generator/
├── doc/
│   ├── repos/
│   │   └── repo_list.md              # 待验证仓库列表
│   ├── roadmap/
│   │   └── CHANGELOG.md              # 版本更新日志
│   ├── practices/
│   │   ├── validation_workflow.md    # 验证工作流规范
│   │   ├── {repo}_{date}.md          # 验证报告
│   │   └── {repo}_issues_{date}.md   # 问题报告
│   └── README.md                     # 本文件
├── scripts/
│   ├── validate_next_repo.sh         # 自动验证脚本
│   ├── manual_validate.sh            # 手动验证脚本
│   ├── reset_validation.sh           # 重置验证状态
│   └── check_progress.sh             # 查看进度
└── ...
```

---

## 🚀 快速开始

### 查看当前进度

```bash
/root/.openclaw/workspace-opengl/skills/project-skill-generator/scripts/check_progress.sh
```

### 手动验证指定仓库

```bash
# 验证 remote-shell 项目
/root/.openclaw/workspace-opengl/skills/project-skill-generator/scripts/manual_validate.sh remote-shell

# 使用深度分析
/root/.openclaw/workspace-opengl/skills/project-skill-generator/scripts/manual_validate.sh wangzhe-chess --depth deep
```

### 重置验证（重新开始）

```bash
/root/.openclaw/workspace-opengl/skills/project-skill-generator/scripts/reset_validation.sh
```

---

## 📊 验证进度

### 当前进度

- **总仓库数**: 15
- **已验证**: 1 (remote-shell - 发现问题)
- **进行中**: 0
- **待验证**: 14

### 下一个验证

- **仓库**: game-auto-test
- **时间**: 每30分钟自动执行
- **状态**: ⏳ 等待中

---

## 🔍 验证发现的问题

### v0.1.0 已知问题

#### 🔴 问题 1: 模块发现失败 (高优先级)

**发现于**: remote-shell 验证

**描述**: 
- 项目没有 `__init__.py` 文件
- 分析脚本只查找标准 Python 模块
- 导致识别 0 个模块，无法生成技能

**影响**: 无法为扁平结构项目生成技能

**状态**: 🔶 待修复

**计划修复版本**: v0.1.1

详细报告: [remote-shell_issues_2026-03-29.md](practices/remote-shell_issues_2026-03-29.md)

---

## 📅 自动化配置

### Cron Job 信息

- **名称**: Project Skill Generator 验证
- **频率**: 每30分钟
- **下次执行**: 查看 `check_progress.sh` 输出
- **目标**: 飞书私聊通知

### 手动触发

如果需要立即执行下一次验证：

```bash
# 方式 1: 直接运行脚本
/root/.openclaw/workspace-opengl/skills/project-skill-generator/scripts/validate_next_repo.sh

# 方式 2: 使用 cron run 命令（需要通过 OpenClaw）
# cron action=run jobId=784bb76c-592e-44c2-9dad-b7360866e308
```

---

## 📝 验证报告模板

每次验证会生成两个文件：

1. **验证报告**: `{repo}_{date}.md`
   - 基本信息
   - 分析结果
   - 生成的技能和代理
   - 测试建议

2. **问题报告**: `{repo}_issues_{date}.md` (如有问题)
   - 问题描述
   - 根本原因
   - 影响范围
   - 解决方案建议

---

## 🎯 验证目标

### 短期目标 (v0.2.0)

- [ ] 修复模块发现问题
- [ ] 完成 3 个 Python 项目验证
- [ ] 优化技能生成质量
- [ ] 支持多语言项目

### 中期目标 (v0.3.0)

- [ ] 支持 TypeScript/JavaScript 项目
- [ ] 深度语义分析
- [ ] 自动生成测试用例

### 长期目标 (v1.0.0)

- [ ] 支持 10+ 种语言
- [ ] CI/CD 集成
- [ ] Web UI 管理界面
- [ ] 技能市场

---

## 🛠️ 故障排查

### 问题: 脚本没有执行权限

```bash
chmod +x /root/.openclaw/workspace-opengl/skills/project-skill-generator/scripts/*.sh
```

### 问题: 分析结果为空

检查项目是否包含 `__init__.py` 文件。如果没有，这是已知问题，等待 v0.1.1 修复。

### 问题: Cron job 没有执行

检查 cron job 状态：

```bash
# 查看 OpenClaw cron 状态
# 通过 Claude Code 执行: cron action=status
```

---

## 📞 联系方式

- **项目负责人**: Claude Code (Glint)
- **仓库**: https://github.com/kongshan001/project-skill-generator
- **反馈渠道**: 飞书私聊

---

## 📚 相关文档

- [验证工作流规范](practices/validation_workflow.md)
- [版本更新日志](roadmap/CHANGELOG.md)
- [仓库列表](repos/repo_list.md)
- [主技能文档](../SKILL.md)

---

*最后更新: 2026-03-29 12:15*
*自动验证系统 v1.0*
