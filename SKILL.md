---
name: project-skill-generator
version: 0.1.7
status: production-ready
success_rate: 95%+
description: >
  分析大型代码库并生成项目专属的 Claude Code 技能和专家代理。
  使用场景：(1) 将新代码库接入 Claude Code，(2) 创建模块专属的专家代理，
  (3) 生成 .claude 目录的 skills/agents 结构，(4) 随代码库演进更新技能，
  (5) 为不同模块构建专业化的代理团队。
validated_repos: 15/15
---

# Project Skill Generator

**版本**: v0.1.7 | **状态**: ✅ 生产就绪 | **成功率**: 95%+

将任意代码库转换为 Claude Code 的专业技能和专家代理系统。

## 🎯 核心功能

**输入**: 代码库路径  
**输出**: 完整的 `.claude/` 目录，包含：
- 项目专属技能（API、模式、规范）
- **领域专家代理**（一对多技能关系）
- 代理团队配置（协同开发）
- 持续更新机制

## ✨ 最新特性 (v0.1.7)

### 🔥 Agent 领域专家模式（新功能！）

**传统方法**: 1 个代理 = 1 个技能（碎片化）
```
❌ 过度细分的代理：
- login-handler-agent
- password-validator-agent
- session-manager-agent
- token-generator-agent
... (8 个独立代理)
```

**领域专家方法**: 1 个代理 = 多个相关技能（专业化）
```
✅ 协调的专家团队：
- Authentication Expert（认证专家）
  * 处理登录、密码验证、会话、令牌
  * 管理 OAuth 集成、安全最佳实践
  * 监督授权和 RBAC 实现
  * 平均 17.9 个技能/专家
```

**核心优势**:
- **减少碎片化**: 从 8 个代理合并为 1 个专家
- **更好的上下文**: 每个专家具备全面的领域知识
- **资深级别**: 所有专家默认 10+ 年经验
- **团队协作**: 内置协作和任务分配机制

### 📊 经过验证的性能

在 **15 个仓库**中验证，**95%+ 成功率**：
- ✅ **最大项目**: 38 个模块, 85,844 行代码
- ✅ **平均生成**: 16.4 个技能 + 2.8 个代理/项目
- ✅ **语言支持**: Python, JavaScript/TypeScript, C++, Shell
- ✅ **框架支持**: Next.js, React, Vue, FastAPI

## 🚀 快速开始

### 方式一：直接放到项目中（推荐）

```bash
# 1. 将此 skill 复制到你的项目
cp -r project-skill-generator /your/project/.claude/skills/

# 2. 在项目目录下运行分析
cd /your/project
python .claude/skills/project-skill-generator/scripts/analyze_codebase.py . --output analysis.json

# 3. 生成技能
python .claude/skills/project-skill-generator/scripts/enhanced_generate_skill.py analysis.json --output .claude/skills/

# 4. 生成专家代理
python .claude/skills/project-skill-generator/scripts/enhanced_generate_agent.py analysis.json --output .claude/agents/
```

### 方式二：独立使用

```bash
# 1. 进入 skill 目录
cd /path/to/project-skill-generator

# 2. 分析目标代码库
python scripts/analyze_codebase.py /path/to/your/codebase --output analysis.json

# 3. 生成技能
python scripts/enhanced_generate_skill.py analysis.json --output /path/to/your/codebase/.claude/skills/

# 4. 生成专家代理
python scripts/enhanced_generate_agent.py analysis.json --output /path/to/your/codebase/.claude/agents/
```

## 🔄 增量更新现有技能库

当项目已有技能库时，使用增量更新模式：

```bash
# 基于最近的提交更新
python scripts/update_skills.py /path/to/codebase --since 2024-01-01

# 更新特定模块
python scripts/update_skills.py /path/to/codebase --module user-auth

# 完全重新分析（大型重构后）
python scripts/update_skills.py /path/to/codebase --full
```

**增量更新会**:
- ✅ 保留现有技能的元数据和配置
- ✅ 更新 API 文档和示例
- ✅ 添加新发现的模式
- ✅ 标记已废弃的代码
- ✅ 合并测试策略

### 生成内容

**技能**（每个模块）:
- 带参数和返回类型的 API 文档
- 常见模式和反模式
- 带示例的测试策略
- 性能考虑和优化

**领域专家代理**（Cocos2d-x 项目示例）:
- **Rendering Engine Expert**（渲染引擎专家，32 个技能）: 2D/3D 渲染、图形管线、shader
- **Core Architecture Expert**（核心架构专家，50 个技能）: 服务管理、工具类、事件系统
- **UI System Expert**（UI 系统专家，27 个技能）: UI 组件、布局引擎、输入处理
- **Animation System Expert**（动画系统专家，11 个技能）: 精灵动画、补间动画、时间线
- **Physics Engine Expert**（物理引擎专家，2 个技能）: 2D/3D 物理模拟、碰撞检测
- **Resource Management Expert**（资源管理专家，3 个技能）: 资产加载、内存管理、缓存
- **Network System Expert**（网络系统专家，1 个技能）: 多人游戏网络、同步

## 🏗️ 输出结构

```
.claude/
├── CLAUDE.md                 # 项目概览
├── settings.json             # Claude Code 设置
├── skills/
│   ├── user-auth/            # 已有技能（保留）
│   │   └── SKILL.md
│   ├── api-core/             # 新生成技能
│   │   └── SKILL.md
│   ├── database/
│   │   └── SKILL.md
│   └── frontend-ui/
│       └── SKILL.md
├── agents/
│   ├── auth-expert.yaml      # 认证专家
│   ├── api-expert.yaml       # API 专家
│   ├── db-expert.yaml        # 数据库专家
│   ├── ui-expert.yaml        # UI 专家
│   └── team.yaml             # 团队配置
└── references/
    ├── architecture.md       # 系统架构
    ├── conventions.md        # 编码规范
    └── api-contracts.md      # API 文档
```

## 🔄 增量更新策略

### 1. 智能合并
```bash
# 系统会识别：
- 已存在的技能 → 更新内容，保留自定义配置
- 新发现的模块 → 生成新技能
- 已废弃的代码 → 标记为 deprecated
- 重命名的模块 → 迁移到新名称
```

### 2. 版本控制
```bash
# 每次更新都会：
- 备份现有技能到 .claude/backups/
- 生成更新日志 CHANGES.md
- 保留用户的自定义注释
- 记录技能的演进历史
```

### 3. 冲突处理
```bash
# 当检测到冲突时：
- 优先保留用户自定义内容
- 自动合并不冲突的部分
- 标记需要手动审核的部分
- 提供合并建议
```

## 🎯 工作流程

### 阶段 1: 代码库分析

分析提取内容：

**结构**:
- 模块边界和职责
- 依赖关系图
- 入口点和公共 API

**模式**:
- 编码规范（命名、格式）
- 架构模式（MVC、微服务等）
- 常用惯用法和工具

**领域知识**:
- 业务逻辑模式
- API 契约和数据模型
- 测试策略
- 配置模式

**输出**: 包含结构化代码库知识的 `analysis.json`

### 阶段 2: 技能生成

为每个识别的模块生成技能：

```markdown
# Module: user-auth

## Domain Expertise（领域专业知识）
- OAuth2 流程实现
- 会话管理模式
- 密码哈希（bcrypt）

## Key APIs（关键 API）
- `AuthService.login()` - 用户认证
- `TokenManager.refresh()` - 刷新访问令牌
- `SessionStore.get()` - 检索会话数据

## Common Patterns（常见模式）
```python
# 标准认证流程
auth = AuthService()
token = auth.login(credentials)
session = SessionStore.create(token)
```

## Code Conventions（代码规范）
- 对受保护的路由使用 `@require_auth` 装饰器
- 数据库操作前总是用 `UserSchema` 验证
- 从认证端点返回 `AuthResponse` 模型
```

### 阶段 3: 代理创建

创建具有聚焦技能集的专业化代理：

```yaml
# .claude/agents/auth-expert.yaml
name: auth-expert
role: 认证与授权专家
level: senior
experience: 10+ years
skills:
  - user-auth
  - api-security
  - session-management
capabilities:
  - 实现 OAuth 流程
  - 设计认证中间件
  - 审计安全问题
  - 重构认证逻辑
constraints:
  - 只修改认证相关文件
  - 遵循现有的安全模式
  - 保持向后兼容性
```

### 阶段 4: 代理团队配置

```yaml
# .claude/agents/team.yaml
name: backend-team
agents:
  - auth-expert
  - api-expert
  - db-expert
  - cache-expert
workflow:
  - api-expert: 设计端点
  - auth-expert: 添加认证
  - db-expert: 实现数据层
  - cache-expert: 优化性能
```

## 📚 最佳实践

### 1. 模块边界检测
- 从目录结构开始
- 基于导入分析细化
- 使用 `__init__.py` 或 `index.ts` 验证
- 考虑语义内聚性

### 2. 技能粒度
- **太粗**: "backend" 技能（过于通用）
- **太细**: "user-login-function" 技能（过于狭窄）
- **恰到好处**: "user-authentication" 技能（聚焦且可复用）

### 3. 代理专业化
- 匹配真实团队结构
- 明确的责任边界
- 最小化技能重叠
- 互补的能力

### 4. 迭代策略
- 活跃项目每周更新
- 重大重构后更新
- 对 `.claude/` 目录进行版本控制
- 在 PR 中审查技能变更

## 🛠️ 故障排除

### 技能过于通用
**问题**: 生成的技能太高层  
**解决**: 增加分析深度或提供更具体的代码示例

### 代理重叠
**问题**: 多个代理有相同技能  
**解决**: 细化模块边界，创建更具体的代理角色

### 缺少领域知识
**问题**: 技能没有捕获业务逻辑  
**解决**: 使用 `--depth deep` 或手动补充 `references/`

### 生成速度慢
**问题**: 大型代码库耗时太长  
**解决**: 先分析特定模块，使用 `--depth quick`

## 📈 分析深度级别

### Quick（快速，默认）
- 模块结构
- 公共 API
- 基本模式
- **时间**: 每 1万行代码约 1 分钟

### Standard（标准）
- Quick + 私有 API
- 依赖分析
- 规范提取
- **时间**: 每 1万行代码约 3 分钟

### Deep（深度）
- Standard + 语义分析
- 业务逻辑提取
- 测试覆盖模式
- 性能模式
- **时间**: 每 1万行代码约 10 分钟

```bash
python scripts/analyze_codebase.py /path --depth deep
```

## 🎨 自定义

### 技能模板

创建 `skill-templates.yaml` 自定义生成的技能：

```yaml
templates:
  api-module:
    sections:
      - domain-expertise
      - key-apis
      - common-patterns
      - error-handling
      - testing-guide
  
  ui-module:
    sections:
      - component-library
      - styling-guide
      - state-management
      - accessibility
```

### 代理人格

在 `agent-personas.yaml` 中定义代理个性：

```yaml
personas:
  senior-backend:
    style: thorough, security-conscious
    focuses_on: performance, scalability
    avoids: shortcuts, technical debt
  
  frontend-specialist:
    style: user-centric, detail-oriented
    focuses_on: UX, accessibility
    avoids: over-engineering
```

## 🔮 未来增强

- [x] Agent 领域专家模式（v0.1.7）
- [x] 多语言支持（Python, JS/TS, C++, Shell）
- [x] Next.js/React 框架支持
- [x] 自动化验证系统（15/15 仓库）
- [x] 增量更新模式
- [ ] 支持更多语言（Rust, Go, Java）
- [ ] 基于机器学习的模式检测
- [ ] Web 界面的技能管理
- [ ] 技能市场

---

**将你的代码库转换为 Claude Code 的专业知识。** 🚀

**状态**: ✅ 生产就绪 | **版本**: v0.1.7 | **成功率**: 95%+
