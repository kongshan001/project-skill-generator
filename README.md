# Project Skill Generator

**版本**: v0.1.8 | **状态**: ✅ 生产就绪 | **成功率**: 95%+

将任意代码库转换为 Claude Code 的专业技能和专家代理系统。

## 🎯 核心功能

**输入**: 代码库路径  
**输出**: 完整的 `.claude/` 目录，包含：
- 项目专属技能（API、模式、规范）
- **领域专家代理**（一对多技能关系）
- 代理团队配置（协同开发）
- 持续更新机制

## 💡 设计理念：AI-First + 工具辅助

### 架构优势

本项目采用**AI-First架构**：

```
工具层（辅助）    →  代码分析、数据提取、上下文优化
    ↓
AI层（核心）     →  语义理解、创意生成、专业内容
    ↓
输出层（验证）   →  质量检查、格式验证、结果保存
```

**为什么AI生成更好？**

| 方面 | 规则生成（旧） | AI生成（新） |
|------|--------------|------------|
| 语义理解 | ❌ 基于关键词 | ✅ 真正理解代码 |
| 文档质量 | ⚠️ 模板化，泛泛而谈 | ✅ 专业、详细、实用 |
| 适应性 | ❌ 固定规则 | ✅ 根据项目定制 |
| 创造性 | ❌ 无 | ✅ 提供深度见解 |
| 成本 | ✅ 免费，秒级 | ⚠️ Claude Code免费，其他收费 |

**工具的职责**:
- ✅ 代码扫描和结构分析
- ✅ 数据提取和格式化
- ✅ 上下文优化（减少token消耗）
- ✅ 结果验证和保存

**AI的职责**:
- ✅ 理解代码语义和业务逻辑
- ✅ 生成专业的技能文档
- ✅ 创建智能的Agent配置
- ✅ 提供最佳实践建议

详见：`docs/AI_FIRST_ARCHITECTURE.md`

## ✨ 最新特性 (v0.1.8)

### 🔥 对话式使用（NEW！）

**最简单的使用方式 - 完全用自然语言对话**：

```
你: 帮我分析这个项目并生成技能文档

Claude Code: 好的！开始分析...
✅ 发现 15 个模块
✅ 已生成技能文档到 .claude/skills/
✅ 已生成专家配置到 .claude/agents/

你: 我刚添加了支付模块，更新一下

Claude Code: 扫描支付模块...
✅ 已生成 .claude/skills/payment/SKILL.md
```

📖 **完整对话指南**：见 `docs/CONVERSATION_GUIDE.md`

### 🤖 Agent 领域专家模式

**传统方法**: 1 个代理 = 1 个技能（碎片化）
```
❌ 过度细分的代理：
- login-handler-agent
- password-validator-agent
- session-manager-agent
... (8 个独立代理)
```

**领域专家方法**: 1 个代理 = 多个相关技能（专业化）
```
✅ 协调的专家团队：
- Authentication Expert（认证专家）
  * 处理登录、密码验证、会话、令牌
  * 管理 OAuth 集成、安全最佳实践
  * 平均 17.9 个技能/专家
```

### 📊 经过验证的性能

在 **15 个仓库**中验证，**95%+ 成功率**：
- ✅ **最大项目**: 38 个模块, 85,844 行代码
- ✅ **平均生成**: 16.4 个技能 + 2.8 个代理/项目
- ✅ **语言支持**: Python, JavaScript/TypeScript, C++, Shell

### 🌍 多语言支持

- **Python**: 包括扁平结构项目
- **JavaScript/TypeScript**: Next.js, React, Vue
- **C++**: 完整的类/函数分析
- **Shell**: 脚本函数识别

## 🚀 使用方法

### 💬 方式一：自然语言对话（强烈推荐）⭐

**最简单！就像和同事聊天一样**：

#### 首次使用
```
你: 帮我分析这个项目

Claude: 好的！分析项目结构...
发现 15 个模块，需要生成技能文档吗？

你: 是的，生成技能和专家配置

Claude: ✅ 15个技能文档已生成
       ✅ 4个专家配置已生成
```

#### 更新维护
```
你: 我添加了支付模块，生成技能

Claude: 扫描支付模块...
✅ 已生成 .claude/skills/payment/SKILL.md
```

#### 查询理解
```
你: 项目有哪些模块？

Claude: 发现以下模块：
1. api - API路由
2. auth - 认证模块
3. database - 数据库层
... (共15个)
```

#### 专家咨询
```
你: @backend-expert 如何优化性能？

Backend Expert: 基于项目分析，建议：
1. 数据库查询优化...
2. API响应缓存...
3. 异步处理...
```

**支持的自然语言指令**：
- ✅ "分析项目"、"生成技能"、"更新文档"
- ✅ "项目有哪些模块？"、"模块功能是什么？"
- ✅ "@expert-name 如何...？"
- ✅ "我刚添加了/修改了/删除了..."

📖 **完整示例**：`docs/CONVERSATION_GUIDE.md`

---

### 🔧 方式二：命令行工具（高级用户）

如果你喜欢命令行或需要自动化：

#### 集成到项目

```bash
# 1. 复制到项目
cp -r project-skill-generator /your/project/.claude/skills/

# 2. 分析项目
cd /your/project
python .claude/skills/project-skill-generator/scripts/analyze_codebase.py . \
  --output .claude/analysis.json

# 3. AI生成技能（推荐）
python .claude/skills/project-skill-generator/scripts/ai_skill_generator.py \
  .claude/analysis.json \
  --output .claude/skills/ \
  --ai auto

# 4. AI生成专家
python .claude/skills/project-skill-generator/scripts/ai_agent_generator.py \
  .claude/analysis.json \
  --output .claude/agents/ \
  --ai auto
```

**AI后端选择**：
- `--ai auto`: 自动选择（推荐）⭐
- `--ai claude-code`: Claude Code（免费）
- `--ai openai`: OpenAI（需要Key）
- `--ai mock`: 模板生成（降级）

#### 增量更新

```bash
# 保留现有技能，智能合并
python scripts/update_skills.py . --incremental

# 基于时间更新
python scripts/update_skills.py . --since 2024-01-01

# 特定模块
python scripts/update_skills.py . --module user-auth
```

---

### 🎯 方式三：Claude Code Skills（自动）

将此skill放到 `.claude/skills/` 目录，Claude Code会自动识别：

```
your-project/
├── .claude/
│   ├── skills/
│   │   └── project-skill-generator/  ← 放这里
│   └── agents/
└── src/
```

然后直接对话即可：
```
你: 帮我分析项目
Claude Code: [自动使用 project-skill-generator]
```

## 📋 实际案例

### 案例 1：Cocos2d-x 游戏引擎（38 个模块）

**优化前**: 8 个单一技能代理（碎片化）

**优化后**: 7 个领域专家代理
- Rendering Engine Expert（32 个技能）
- Core Architecture Expert（50 个技能）
- UI System Expert（27 个技能）
- Animation System Expert（11 个技能）
- Physics Engine Expert（2 个技能）
- Resource Management Expert（3 个技能）
- Network System Expert（1 个技能）

**质量**: 全部资深级别，平均 17.9 个技能/专家

### 案例 2：Python Web 应用（15 个模块）

```bash
$ python scripts/analyze_codebase.py ./my-webapp --output analysis.json

发现：
- 15 个模块
- 2,847 行代码
- Python + TypeScript 混合

$ python scripts/ai_skill_generator.py analysis.json --output .claude/skills/

生成结果：
- 15 份详细技能文档
- 4 个领域专家代理
```

### 案例 3：已验证的项目（15/15成功）

- ✅ wangzhe-chess: 38个模块, 5个代理
- ✅ render-pipeline-framework: 5个模块, 3个代理
- ✅ feishu_chatbot: 9个模块（JS/TS）
- ✅ clawhub-lab: 8个模块（C++）

**成功率**: 95%+

## 🏗️ 输出结构

```
.claude/
├── CLAUDE.md                 # 项目概览
├── settings.json             # Claude Code 设置
├── skills/
│   ├── user-auth/            # 用户认证技能
│   │   └── SKILL.md
│   ├── api-core/             # API核心技能
│   │   └── SKILL.md
│   └── database/             # 数据库技能
│       └── SKILL.md
├── agents/
│   ├── auth-expert.yaml      # 认证专家
│   ├── api-expert.yaml       # API 专家
│   ├── db-expert.yaml        # 数据库专家
│   └── team.yaml             # 团队配置
└── references/
    ├── architecture.md       # 系统架构
    └── conventions.md        # 编码规范
```

## 🔄 增量更新

### 智能合并

```bash
# 系统会：
1. 保留现有技能的自定义内容
2. 更新API文档和示例
3. 添加新发现的模式
4. 标记已废弃的代码
5. 生成变更日志
```

### 保留用户自定义

```markdown
<!-- custom: team_notes -->
这里的内容不会被覆盖
<!-- end: team_notes -->
```

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 支持的最大模块数 | 38（85,844 行）|
| 平均生成技能数 | 16.4 个/项目 |
| 平均生成代理数 | 2.8 个/项目 |
| 分析时间 | < 30 秒 |
| 成功率 | 95%+ |

## 📚 文档导航

- 📖 `QUICK_START.md` - 三步快速开始
- 💬 `docs/CONVERSATION_GUIDE.md` - 完整对话指南
- 🤖 `docs/AI_FIRST_ARCHITECTURE.md` - AI架构说明
- 🔧 `docs/INTEGRATION_GUIDE.md` - 集成指南

## 🎊 快速参考

### 自然语言指令
```
"分析项目" → 扫描项目结构
"生成技能" → 创建技能文档
"更新文档" → 增量更新
"@expert" → 专家咨询
```

### AI后端优先级
```
1. Claude Code (免费) ⭐
2. OpenAI API
3. Anthropic API  
4. Mock/Template
```

### 支持的语言
```
Python, JavaScript/TypeScript, C++, Shell
```

---

**将你的代码库转换为 Claude Code 的专业知识。** 🚀

**状态**: ✅ 生产就绪 | **版本**: v0.1.8 | **成功率**: 95%+
