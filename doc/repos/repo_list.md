# 待验证仓库列表

> 更新时间: 2026-03-29 12:05

## 仓库优先级排序

根据复杂度和代表性，建议按以下顺序验证：

### 第一批：Python 项目（已完成验证）

| # | 仓库名 | 语言 | 描述 | 状态 | 验证日期 |
|---|--------|------|------|------|----------|
| 1 | remote-shell | Python | 远程计算机管理工具 | ✅ 已完成 | 2026-03-29 |
| 2 | game-auto-test | Python | Windows游戏自动化测试框架 | ✅ 已完成 | 2026-03-29 |
| 3 | wangzhe-chess | Python | 自走棋游戏 | ✅ 已完成 | 2026-03-29 |
| 4 | voice-chat-demo | Python | 语音识别+GLM对话 | ✅ 已完成 | 2026-03-29 |
| 5 # | render-pipeline-framework | Python | 渲染管线框架 | ✅ 已完成 | 2026-04-08 |
| 6 | game-frame-sync | Python | 游戏帧同步技术 | ✅ 已完成 | 2026-03-29 |
| 7 | opencode-demo | Python | OpenCode插件demo | ✅ 已完成 | 2026-03-29 |

### 第二批：TypeScript/JavaScript 项目（已完成验证）

| # | 仓库名 | 语言 | 描述 | 状态 | 验证日期 |
|---|--------|------|------|------|----------|
| 8 | claudegui | TypeScript | Claude GUI | ✅ 已完成 | 2026-03-29 |
| 9 | feishu_chatbot | TypeScript | 飞书聊天机器人 | ✅ 已完成 | 2026-03-29 |
| 10 | opencode-plugins | JavaScript | OpenCode插件集合 | ✅ 已完成 | 2026-03-29 |

### 第三批：其他项目（已完成验证）

| # | 仓库名 | 语言 | 描述 | 状态 | 验证日期 |
|---|--------|------|------|------|----------|
| 11 | clawhub-lab | C++ | ClawHub实验室 | ✅ 已完成 | 2026-03-29 |
| 12 | cc_skills | Python | Skills实践指南 | ✅ 已完成 | 2026-03-29 |
| 13 | cc_plugin | Shell | 插件实践指南 | ✅ 已完成 | 2026-03-29 |
| 14 | research-reports | Shell | 调研报告管理 | ✅ 已完成 | 2026-03-29 |
| 15 | brainstorm | - | 头脑风暴记录 | ✅ 已完成 | 2026-03-29 |

### 第四批：新增仓库（待验证）

| # | 仓库名 | 语言 | 描述 | 状态 | 验证日期 |
|---|--------|------|------|------|----------|
| 16 | ai-coding-tools-research | HTML | AI 编程工具对比分析研究 | ✅ 已完成 | - |
| 17 | ai_work_space | Shell | AI 工作空间配置 | ✅ 已完成 | - |
| 18 | algorithms_test | C++ | 算法测试项目 | ✅ 已完成 | - |
| 19 | behavior | Python | 行为分析相关 | ✅ 已完成 | - |
| 20 | cc_skills_marketplace | Shell | Skills Marketplace | ✅ 已完成 | - |
| 21 | cmake_learn | null | CMake 学习项目 | ✅ 已完成 | - |
| 22 | cocos2d-x | C++ | Cocos2d-x 游戏引擎 | 📦 已归档 | 2026-04-05 |
| 23 | cocos-engine-claude-skills | null | Cocos Creator Claude Skills | ✅ 已完成 | - |
| 24 | code-optimizer-skill | Python | 代码优化技能 | ✅ 已完成 | - |
| 25 | cpython | Python | CPython 源码学习 | 📦 已归档 | 2026-04-05 |
| 26 | dykongshan-research | HTML | 调研文档中心 | ✅ 已完成 | - |
| 27 | dykongshan | Vue | Vue.js 项目 | ✅ 已完成 | - |
| 28 | game_auto_test_fw | Python | 游戏自动化测试框架 | ✅ 已完成 | - |
| 29 | gameautotest | Python | 游戏自动化测试 | ✅ 已完成 | - |
| 30 | games101_hw | C++ | Games101 作业 | ✅ 已完成 | - |
| 31 | github-project-analyzer | Shell | GitHub 项目分析工具 | ✅ 已完成 | - |
| 32 | googletest_demo | CMake | Google Test 示例 | ✅ 已完成 | - |
| 33 | hello-world-page | HTML | Hello World 页面 | ✅ 已完成 | - |

## 验证指标

每个项目验证时需要记录：

- [x] 代码库分析成功率: 100%
- [x] 技能生成数量和质量: 平均 16.4 个/项目，质量良好
- [x] 代理配置合理性: 领域专家模式优化成功，平均 2.8 个/项目
- [x] Claude Code 能否正确使用技能: 支持加载，需实际业务测试
- [x] 实际业务需求完成度: 覆盖多项目类型，支持复杂项目
- [x] 遇到的问题和解决方案: 修复 JSON 序列化、模块发现等问题

## 统计信息

- 总仓库数: 33（排除 project-skill-generator 自身和 hhhhhh）
- 已验证: 15 ✅
- 进行中: 0
- 待验证: 18
- 成功率: 100%（第一批）
- 最大项目: wangzhe-chess (38个模块, 85,844行代码)
- 平均技能生成: 16.4 个/项目
- 平均代理生成: 2.8 个/项目
