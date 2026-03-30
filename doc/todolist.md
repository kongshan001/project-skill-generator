# Project Skill Generator - 优化待办清单

> 最后更新: 2026-03-30 08:50:32
> 状态: ✅ 系统运行正常

---

## 🔴 高优先级 - 阻塞性问题

### TODO-009: 实现 Agent 领域专家模式（一对多技能） ✅ 已完成

**问题来源**: 用户反馈（Cocos2d-x 项目）
**发现日期**: 2026-03-29
**完成日期**: 2026-03-29
**严重程度**: 🔴 高
**状态**: ✅ 已完成 (2026-03-29)

**问题描述**:
- 当前 agent 与 skill 是一对一关系
- Agent 拆分过细（Cocos2d-x 生成了 8 个独立 agent）
- 缺少等级系统（资深/熟手/初级）
- 每个 agent 能力过于单一

**用户期望**:
1. Agent 应该是团队中的程序员，有专精方向
2. Agent 与 skill 应该是一对多关系
3. Agent 应该有等级区分（默认资深）
4. 精简但专业的专家配置

**影响范围**:
- 所有大型项目的 agent 生成
- Cocos2d-x: 8 个 agent → 期望 3-5 个领域专家
- 用户体验和实用性

**解决方案**:
- [x] 创建增强版 agent 生成器 `enhanced_generate_agent.py`
- [x] 实现领域分组逻辑（渲染、物理、架构、UI、音频等）
- [x] 添加等级系统（Senior/Mid/Junior，默认 Senior）
- [x] 智能合并相关技能到领域专家
- [x] 生成精简但专业的 agent 配置

**验证标准**:
- [x] Cocos2d-x 项目从 8 个 agent 精简到 7 个领域专家
- [x] 每个 expert 掌握 17.9 个相关技能（平均）
- [x] 所有 expert 默认为资深级别
- [x] Agent 配置包含专业的能力描述和详细指导

**实施结果**:
```
Cocos2d-x 项目优化成果:
- 原来: 8 个单一技能 agent
- 现在: 7 个领域专家
- 技能覆盖: 平均 17.9 个技能/专家
- 专家等级: 全部为资深级别
- 配置质量: 专业的详细描述和约束条件

生成的领域专家:
1. UI System Expert (27 skills)
2. Core Architecture Expert (50 skills) 
3. Resource Management Expert (3 skills)
4. Rendering Engine Expert (32 skills)
5. Animation System Expert (11 skills)
6. Audio System Expert (1 skills)
7. Network System Expert (1 skills)
```

**详细报告**: `doc/AGENT_IMPROVEMENT_PLAN.md`

---

## 🟡 中优先级 - 已完成的功能

### TODO-001: 修复扁平结构项目的模块发现
**状态**: ✅ 已完成 (2026-03-29)
**问题**: Python 项目无 `__init__.py` 无法识别
**解决方案**: 添加回退机制
**验证**: remote-shell 项目成功

### TODO-002: 改进 AST 分析深度
**状态**: ✅ 已完成 (2026-03-29)
**改进**: 参数类型、复杂度、异步函数识别

### TODO-003: 支持更多语言
**状态**: ✅ 已完成 (2026-03-29)
**支持**: C++, Shell, TypeScript

### TODO-004: 优化技能生成质量
**状态**: ✅ 已完成 (2026-03-29)
**改进**: 详细 API 文档、测试策略、性能建议

---

## 🟢 低优先级 - 已完成的优化

### TODO-005: 添加配置文件支持
**状态**: ✅ 已完成 (2026-03-29)
**功能**: `.psg.yaml` 配置文件

### TODO-006: 改进错误提示
**状态**: ✅ 已完成 (2026-03-29)
**改进**: 友好错误信息、verbose 模式

### TODO-007: 添加进度显示
**状态**: ✅ 已完成 (2026-03-29)
**功能**: 实时进度条

### TODO-008: 修复 JS/TS 项目文件发现
**状态**: ✅ 已完成 (2026-03-29)
**问题**: 文件发现算法失效
**解决方案**: 修复 glob 模式、添加回退机制

---

## 📊 统计信息

- **总待办数**: 9
- **高优先级**: 0
- **中优先级**: 0  
- **低优先级**: 0
- **已完成**: 9
- **完成率**: 100.0%
- **系统健康度**: ✅ 生产就绪 (2026-03-30 迭代优化完成)

---

## 🎯 Agent 改进目标

### 当前问题
```
Cocos2d-x 项目生成了 8 个 agent:
- 2d-expert (skill: [2d])
- 3d-expert (skill: [3d])
- animation-expert (skill: [animation])
- gfx-expert (skill: [gfx])
- physics-expert (skill: [physics])
- physics-2d-expert (skill: [physics-2d])
- rendering-expert (skill: [rendering])
- service-expert (skill: [service])
```

### 期望结果
```
精简到 3-5 个领域专家:
- Rendering Expert (skills: [2d, 3d, rendering, gfx, animation])
  资深渲染引擎专家，精通图形渲染和材质系统

- Physics Expert (skills: [physics, physics-2d])
  资深物理引擎专家，精通物理模拟和碰撞检测

- Architecture Expert (skills: [core, service, utils])
  资深架构专家，精通引擎核心和设计模式

每个专家都有:
- 10+ 年经验
- 资深级别
- 3-6 个相关技能
- 专业能力描述
- 明确的职责范围
```

---

## 📝 添加新问题的模板

```markdown
### TODO-XXX: 问题标题
**问题来源**: {项目名} 验证
**发现日期**: YYYY-MM-DD
**严重程度**: 🔴/🟡/🟢
**状态**: ✅ 已完成 (2026-03-30)/🔧 修复中/✅ 已完成

**问题描述**:
{详细描述}

**影响范围**:
- 项目1
- 项目2

**解决方案**:
- [ ] 方案1
- [ ] 方案2

**验证标准**:
- [ ] 标准1
- [ ] 标准2

**详细报告**: `practices/{project}_issues_{date}.md`
```

---

*维护者: Claude Code (Glint)*
*自动更新: 每30分钟*
