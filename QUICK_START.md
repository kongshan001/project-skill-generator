# 快速开始 - AI生成模式

## 🎯 三步开始

### Step 1: 复制工具到项目

```bash
cd /your/project

# 方式 A: 直接复制
cp -r /path/to/project-skill-generator .claude/skills/

# 方式 B: Git Submodule（推荐）
git submodule add https://github.com/kongshan001/project-skill-generator.git \
  .claude/skills/project-skill-generator
```

### Step 2: 分析项目

```bash
python .claude/skills/project-skill-generator/scripts/analyze_codebase.py . \
  --output .claude/analysis.json \
  --depth standard
```

### Step 3: AI生成

```bash
# 生成技能（自动选择AI后端）
python .claude/skills/project-skill-generator/scripts/ai_skill_generator.py \
  .claude/analysis.json \
  --output .claude/skills/

# 生成专家代理
python .claude/skills/project-skill-generator/scripts/ai_agent_generator.py \
  .claude/analysis.json \
  --output .claude/agents/
```

## 🤖 AI后端选择

### 自动模式（推荐）

```bash
# 自动选择最佳可用后端
python scripts/ai_skill_generator.py analysis.json --output skills/

# 优先级：Claude Code > OpenAI > Anthropic > Mock
```

### 指定后端

```bash
# Claude Code（免费，本地）
python scripts/ai_skill_generator.py analysis.json --ai claude-code --output skills/

# OpenAI（需要API Key）
export OPENAI_API_KEY="sk-..."
python scripts/ai_skill_generator.py analysis.json --ai openai --output skills/

# Anthropic（需要API Key）
export ANTHROPIC_API_KEY="..."
python scripts/ai_skill_generator.py analysis.json --ai anthropic --output skills/

# Mock（降级，无AI）
python scripts/ai_skill_generator.py analysis.json --ai mock --output skills/
```

## 📊 生成结果

```
.claude/
├── analysis.json           # 项目分析结果
├── skills/
│   ├── user-auth/
│   │   ├── SKILL.md       # AI生成的技能文档
│   │   └── PROMPT.md      # 使用的提示词（调试用）
│   ├── api-core/
│   │   └── SKILL.md
│   └── database/
│       └── SKILL.md
└── agents/
    ├── auth-expert.yaml    # AI生成的专家配置
    ├── api-expert.yaml
    └── team.yaml           # 团队配置
```

## 🔄 增量更新

```bash
# 基于时间的增量更新
python scripts/update_skills.py . --since 2024-01-01

# 完全重新生成
python scripts/update_skills.py . --full
```

## 🎨 对比：AI vs 规则生成

### 规则生成（旧版）
```markdown
# user-auth

## Key APIs
- login()
- logout()
- validate_token()
```

### AI生成（新版）
```markdown
# user-auth - 用户认证模块

## 领域专业知识

这个模块负责整个应用的用户认证和授权流程，实现了基于JWT的无状态认证机制。

核心概念：
- **JWT Token**: 使用RS256算法签名，有效期2小时
- **Refresh Token**: 存储在HttpOnly Cookie中，有效期7天
- **Session管理**: 采用Redis存储活跃会话

安全最佳实践：
- 密码使用bcrypt加密（cost factor: 12）
- 登录失败3次后锁定账户15分钟
...

## 关键API

### 1. `AuthService.login(credentials: LoginRequest) -> AuthResponse`
**用途**: 用户登录，获取访问令牌

**参数**:
- `username`: 用户名（3-20字符）
- `password`: 密码（至少8字符，包含大小写和数字）

**返回**:
- `access_token`: JWT访问令牌
- `refresh_token`: 刷新令牌
- `expires_in`: 过期时间（秒）

**示例**:
```python
auth = AuthService()
response = auth.login(LoginRequest(
    username="alice",
    password="SecurePass123"
))
```
```

## 📚 完整文档

- `README.md` - 完整使用文档
- `docs/AI_FIRST_ARCHITECTURE.md` - AI-First架构说明
- `docs/INTEGRATION_GUIDE.md` - 集成指南

## 🎊 下一步

1. ✅ 尝试在你的项目上运行
2. ✅ 对比AI生成和规则生成的结果
3. ✅ 调整AI提示词以适应你的需求
4. ✅ 将生成的内容提交到版本控制

**开始使用 AI-First 的技能生成吧！** 🚀
