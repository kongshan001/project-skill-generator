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

## 🚀 快速开始（自然语言方式）

### 🎯 最简单的使用方式

**直接用自然语言和 Claude Code 对话**：

#### 场景 1: 首次为项目生成技能

```
你: 帮我分析这个项目并生成技能文档

Claude Code: 好的！我会：
1. 扫描项目结构
2. 识别模块和依赖
3. 生成专业的技能文档

开始分析... 
✅ 发现 15 个模块
✅ 已生成技能文档到 .claude/skills/
```

#### 场景 2: 为新模块生成技能

```
你: 我刚添加了一个支付模块，帮我生成对应的技能

Claude Code: 好的！让我扫描新模块...

发现模块：payment/
- 文件：payment_processor.py, stripe_client.py
- 主要类：PaymentProcessor, StripeClient
- API：process_payment(), refund(), get_status()

正在生成技能文档...
✅ 已生成 .claude/skills/payment/SKILL.md
```

#### 场景 3: 更新现有技能

```
你: 我重构了用户认证模块，更新一下技能文档

Claude Code: 明白！我会：
1. 对比新旧代码变化
2. 更新API文档
3. 保留你的自定义注释

正在更新...
✅ 已更新 .claude/skills/user-auth/SKILL.md
✅ 变更日志已记录到 .claude/CHANGES.md
```

#### 场景 4: 生成专家团队

```
你: 根据项目的模块，帮我配置专家团队

Claude Code: 好的！分析模块关系...

发现模块分组：
- 后端：api, database, auth
- 前端：ui, components
- 测试：test_utils, mocks

建议的专家配置：
1. Backend Expert (后端专家)
   - 负责：api, database, auth
   - 技能数：3
   
2. Frontend Expert (前端专家)
   - 负责：ui, components
   - 技能数：2
   
3. QA Expert (测试专家)
   - 负责：test_utils, mocks
   - 技能数：2

正在生成配置...
✅ 已生成 .claude/agents/backend-expert.yaml
✅ 已生成 .claude/agents/frontend-expert.yaml
✅ 已生成 .claude/agents/qa-expert.yaml
✅ 已生成 .claude/agents/team.yaml
```

### 💬 更多自然语言示例

#### 分析特定模块

```
你: 分析一下 api 模块，我想了解它的结构

Claude Code: 好的！分析 api 模块...

📁 api/
├── routes/
│   ├── user_routes.py (5个端点)
│   └── auth_routes.py (3个端点)
├── middleware/
│   └── auth_middleware.py
└── schemas/
    └── user_schema.py

主要功能：
- 用户CRUD操作
- 认证和授权
- 请求验证

需要我为这个模块生成技能文档吗？
```

#### 询问项目结构

```
你: 这个项目的模块之间有什么依赖关系？

Claude Code: 分析依赖关系...

依赖关系图：
api → auth → database
api → cache
frontend → api

关键发现：
- api 模块依赖 auth 和 database
- auth 提供认证服务给多个模块
- database 是核心数据层

建议：可以将 auth 独立为微服务
```

#### 获取建议

```
你: 我应该如何组织测试技能？

Claude Code: 根据项目分析，建议：

测试技能组织：
1. unit-tests/
   - 测试策略
   - Mock使用指南
   - 断言最佳实践
   
2. integration-tests/
   - API测试
   - 数据库测试
   - 端到端测试

3. performance-tests/
   - 负载测试
   - 基准测试

需要我生成这些技能文档吗？
```

### 🎯 支持的自然语言指令

**分析和生成**:
- "分析项目并生成技能"
- "为新模块生成技能"
- "更新所有技能文档"
- "重新生成 user-auth 模块的技能"

**查询和理解**:
- "项目有哪些模块？"
- "api 模块的主要功能是什么？"
- "模块之间有什么依赖关系？"
- "哪些模块需要技能文档？"

**专家团队**:
- "配置专家团队"
- "创建后端专家"
- "优化专家分组"
- "更新团队配置"

**增量更新**:
- "更新最近一周的变更"
- "只更新 api 模块"
- "检查哪些技能需要更新"

### 🔧 技术实现（可选）

如果你想了解底层实现，这些是 Claude Code 会调用的脚本：

```bash
# 分析项目
python scripts/analyze_codebase.py . --output analysis.json

# AI生成技能
python scripts/ai_skill_generator.py analysis.json --output .claude/skills/

# AI生成代理
python scripts/ai_agent_generator.py analysis.json --output .claude/agents/

# 增量更新
python scripts/update_skills.py . --since 2024-01-01
```

但通常你不需要直接运行这些命令，**用自然语言告诉我就行**！

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
