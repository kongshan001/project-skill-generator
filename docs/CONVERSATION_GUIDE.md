# 对话式使用指南 💬

**Project Skill Generator** 最强大的地方在于：你可以**完全用自然语言**来使用它！

不需要记住任何命令，就像和一个懂技术的同事对话一样。

---

## 🎯 核心理念

```
传统方式（繁琐）:
你: $ python scripts/analyze_codebase.py . --depth deep --output analysis.json
你: $ python scripts/ai_skill_generator.py analysis.json --output .claude/skills/
你: $ python scripts/ai_agent_generator.py analysis.json --output .claude/agents/

对话式（简单）:
你: 帮我分析项目并生成技能文档
Claude: 好的！开始分析... ✅ 完成！
```

---

## 💬 完整对话示例

### 示例 1: 第一次使用

```
你: 我刚clone了一个新项目，想快速了解它的结构

Claude Code: 好的！我来帮你分析这个项目。

🔍 正在扫描项目结构...

发现：
- 项目类型：Python Web应用（FastAPI）
- 主要模块：8个
  * api/ - API路由
  * models/ - 数据模型
  * auth/ - 认证模块
  * utils/ - 工具函数
  ...
- 代码行数：约5,000行
- 依赖框架：FastAPI, SQLAlchemy, Pydantic

需要我：
1. 生成技能文档？
2. 生成专家代理配置？
3. 详细分析某个模块？
```

```
你: 帮我生成技能文档和专家配置

Claude Code: 明白！我会生成完整的技能库。

📝 第1步：分析模块结构...
✅ 识别出8个模块

📝 第2步：生成技能文档（使用AI）...
✅ api/SKILL.md - API设计模式和最佳实践
✅ auth/SKILL.md - JWT认证和安全策略
✅ models/SKILL.md - SQLAlchemy使用指南
...

📝 第3步：生成专家配置...
✅ backend-expert.yaml - 后端开发专家
✅ database-expert.yaml - 数据库专家
✅ auth-expert.yaml - 认证安全专家
✅ team.yaml - 团队协作配置

🎉 完成！你现在可以：
- 查看技能：.claude/skills/[module]/SKILL.md
- 使用专家：@backend-expert 帮我重构api
- 查看团队：.claude/agents/team.yaml
```

---

### 示例 2: 增量更新

```
你: 我昨天重构了支付模块，更新一下相关技能

Claude Code: 好的！我来检查支付模块的变更。

🔍 对比变更...

发现变更：
- 新增文件：payment/stripe_client.py
- 修改文件：payment/processor.py
  * 添加了 refund() 方法
  * 修改了错误处理逻辑
- 删除文件：payment/old_gateway.py

📝 更新技能文档...

变更内容：
1. ✅ 添加了 Stripe API 文档
2. ✅ 更新了退款流程说明
3. ✅ 标记 old_gateway 为已废弃
4. ✅ 保留了你的性能优化注释

📄 变更日志已保存到 .claude/CHANGES.md
```

---

### 示例 3: 深度分析

```
你: 我想深入理解认证模块的安全性

Claude Code: 让我详细分析认证模块...

🔐 auth 模块安全分析：

**认证机制**:
- 方式：JWT (RS256签名)
- Token有效期：2小时
- Refresh Token：7天

**安全措施**:
✅ 密码：bcrypt加密（cost=12）
✅ 速率限制：5次/分钟
✅ 账户锁定：失败3次后锁定15分钟
⚠️ 发现：Session未设置HTTPOnly标志

**主要API**:
- login() - 用户登录
- refresh_token() - 刷新令牌
- logout() - 用户登出
- validate_token() - 验证令牌

**建议**:
1. 为Session Cookie添加HTTPOnly标志
2. 考虑添加2FA支持
3. 实现Token黑名单机制

需要我生成详细的安全审计报告吗？
```

---

### 示例 4: 专家咨询

```
你: @backend-expert 我需要优化API性能，有什么建议？

Backend Expert: 基于我对项目的了解，建议：

📊 性能优化建议：

1. **数据库查询优化**
   - 添加索引：users.email, orders.user_id
   - 使用 select_related() 减少N+1查询
   - 考虑查询缓存

2. **API响应优化**
   - 启用gzip压缩
   - 实现分页（默认20条/页）
   - 使用response caching

3. **异步处理**
   - 将邮件发送改为异步
   - 使用Celery处理后台任务

需要我帮你实现其中某项优化吗？
```

---

### 示例 5: 团队协作

```
你: 我要添加一个新的文件上传功能，需要哪些专家配合？

Claude Code: 根据功能需求，建议团队协作：

👥 推荐工作流：

1. **Backend Expert** (后端专家)
   - 设计上传API端点
   - 实现文件验证逻辑
   - 处理存储和安全

2. **Frontend Expert** (前端专家)
   - 设计上传组件UI
   - 实现进度显示
   - 处理错误反馈

3. **QA Expert** (测试专家)
   - 编写单元测试
   - 测试边界情况
   - 性能压力测试

建议执行顺序：
backend-expert → frontend-expert → qa-expert

需要我帮你：
1. 生成详细的任务分解？
2. 创建代码模板？
3. 配置协作流程？
```

---

### 示例 6: 学习和文档

```
你: 帮我理解这个项目的认证流程

Claude Code: 好的！我来详细解释认证流程。

📖 认证流程图：

1. 用户登录
   ↓
2. 验证用户名/密码
   ↓
3. 生成 JWT Token (2小时有效)
   ↓
4. 生成 Refresh Token (7天有效)
   ↓
5. 返回给客户端

🔄 Token刷新流程：

客户端 → refresh_token()
   ↓
验证 Refresh Token
   ↓
生成新的 JWT Token
   ↓
返回给客户端

📁 相关文件：
- auth/service.py - 认证服务
- auth/jwt_handler.py - JWT处理
- auth/middleware.py - 认证中间件

需要我：
1. 展示某个具体文件的代码？
2. 解释某个函数的实现？
3. 生成认证流程的详细文档？
```

---

## 🎨 支持的自然语言模式

### ✅ 分析类

- "分析项目结构"
- "这个项目有什么特点？"
- "分析 [模块名] 的依赖关系"
- "项目的架构模式是什么？"

### ✅ 生成类

- "生成技能文档"
- "为新模块生成技能"
- "配置专家团队"
- "创建测试专家"

### ✅ 更新类

- "更新技能文档"
- "同步最新的代码变更"
- "重新生成 [模块名] 的技能"

### ✅ 查询类

- "项目有哪些模块？"
- "[模块名] 的主要功能是什么？"
- "专家团队有谁？"
- "哪些技能需要更新？"

### ✅ 建议类

- "如何优化性能？"
- "安全性有什么问题？"
- "如何重构这个模块？"
- "测试策略建议？"

---

## 🌟 高级用法

### 组合指令

```
你: 分析项目，生成技能文档，然后配置一个5人的专家团队

Claude Code: 好的！我会按顺序完成：

1️⃣ 分析项目...
✅ 发现12个模块

2️⃣ 生成技能文档...
✅ 生成12份技能文档

3️⃣ 配置专家团队...
根据模块分析，建议团队：
- Frontend Expert (3个技能)
- Backend Expert (5个技能)
- Database Expert (2个技能)
- DevOps Expert (1个技能)
- QA Expert (1个技能)

✅ 已生成团队配置

全部完成！需要查看详情吗？
```

### 条件指令

```
你: 如果发现测试覆盖率低于50%，生成测试技能

Claude Code: 检查测试覆盖率...

⚠️ 当前测试覆盖率：35%

生成测试技能文档：
✅ unit-testing/SKILL.md
✅ integration-testing/SKILL.md
✅ mocking-strategies/SKILL.md

建议：
1. 优先为 core 模块添加测试
2. 使用 pytest-cov 监控覆盖率
3. 目标：提升到80%
```

---

## 💡 提示技巧

### 更具体的描述 = 更好的结果

```
❌ 太模糊：
"生成技能"

✅ 清晰具体：
"为 api 模块生成详细的技能文档，重点关注：
 1. RESTful API 设计原则
 2. 错误处理最佳实践
 3. 性能优化建议"
```

### 利用上下文

```
你: 上次你说要优化数据库查询，现在帮我生成相关的技能

Claude Code: 好的！基于之前的分析，我会生成：

📊 数据库优化技能：
✅ query-optimization/SKILL.md
  - 索引策略
  - N+1查询优化
  - 查询计划分析

✅ caching-strategies/SKILL.md
  - Redis缓存
  - 查询缓存
  - 缓存失效策略

✅ connection-pooling/SKILL.md
  - 连接池配置
  - 连接管理最佳实践
```

---

## 🎯 最佳实践

### 1. 首次使用项目

```
推荐对话流程：
1. "分析项目结构" → 了解项目
2. "生成技能文档" → 创建知识库
3. "配置专家团队" → 设置开发助手
```

### 2. 日常开发

```
推荐习惯：
- 每周："更新技能文档"
- 新功能："为新模块生成技能"
- 重构后："同步变更到技能"
```

### 3. 问题排查

```
推荐方法：
1. 描述问题
2. 让专家分析
3. 获取建议和方案
```

---

## 🚀 立即开始

**现在就试试！直接说**：

- "帮我分析这个项目"
- "生成技能文档"
- "配置专家团队"

**不需要命令行，不需要脚本，就像和同事聊天一样！** 💬✨
