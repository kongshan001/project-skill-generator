# AI-First 架构说明

## 🎯 设计理念

**核心理念**: AI 负责创造，工具负责辅助

```
传统方式: 工具全包 →  AI增强 → 混合架构
   (纯规则)      (AI辅助)   (AI-First)
```

---

## 🏗️ 新架构设计

### 三层分离架构

```
┌─────────────────────────────────────────┐
│  Layer 1: AI Generation (AI生成层)      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  职责: 创造性内容生成                    │
│  - 理解语义和上下文                      │
│  - 生成专业化的技能文档                  │
│  - 创建智能的Agent配置                  │
│  - 适应不同项目特点                      │
│                                         │
│  技术: Claude Code / OpenAI / 其他LLM   │
└─────────────────────────────────────────┘
             ↑ 结构化数据
┌─────────────────────────────────────────┐
│  Layer 2: Tool Assistance (工具辅助层)  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  职责: 为AI提供高质量输入                │
│  - 代码库扫描和结构分析                 │
│  - 数据提取和格式化                     │
│  - 上下文优化和压缩                     │
│  - 结果验证和保存                       │
│                                         │
│  技术: Python AST + 文件系统 + 模板引擎 │
└─────────────────────────────────────────┘
             ↑ 原始代码
┌─────────────────────────────────────────┐
│  Layer 3: Code Base (代码层)            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  职责: 提供原始材料                      │
│  - 源代码文件                           │
│  - 配置文件                             │
│  - 测试代码                             │
│  - 文档和注释                           │
└─────────────────────────────────────────┘
```

---

## 🔄 工作流程

### 完整生成流程

```python
# 1. 工具层：代码分析
analysis_result = analyze_codebase(project_path)
# 输出: 结构化的JSON数据
{
  "modules": {
    "user-auth": {
      "files": [...],
      "classes": [...],
      "functions": [...],
      "dependencies": [...]
    }
  }
}

# 2. 工具层：上下文准备
context = prepare_context_for_ai(analysis_result)
# 输出: 优化的提示词材料
{
  "module": "user-auth",
  "key_files": [...],  # 最相关的5个文件
  "api_summary": ...,  # API概要
  "patterns": [...]     # 识别的模式
}

# 3. AI层：生成技能
skill_content = call_ai(prompt)
# 输入: 结构化的提示词
# 输出: 专业的技能文档（Markdown）

# 4. 工具层：验证和保存
validated_skill = validate_and_save(skill_content)
# 验证格式、完整性、质量
# 保存到 .claude/skills/
```

---

## 🛠️ 核心组件

### 1. 代码分析器 (analyze_codebase.py)

**职责**: 扫描代码，提取结构化信息

```python
class CodeAnalyzer:
    """纯工具实现，无AI依赖"""
    
    def scan_project(self, path):
        """扫描项目结构"""
        # 遍历文件系统
        # 识别模块边界
        # 提取文件列表
        return structure
    
    def extract_info(self, file):
        """提取文件信息"""
        # AST解析
        # 提取类/函数/变量
        # 分析依赖关系
        return info
    
    def generate_report(self):
        """生成分析报告"""
        # 汇总所有模块
        # 计算统计信息
        # 输出JSON
        return json_report
```

**输出**: 纯数据，无任何创造性内容

---

### 2. 上下文准备器 (AIContextPreparer)

**职责**: 为AI准备高质量输入

```python
class AIContextPreparer:
    """优化AI输入，减少token消耗"""
    
    def select_key_files(self, module, max=5):
        """选择最关键的文件"""
        # 优先级算法：
        # 1. main/index 文件
        # 2. API 入口
        # 3. 核心类定义
        # 4. 配置文件
        return top_files
    
    def summarize_apis(self, module):
        """总结API信息"""
        # 提取函数签名
        # 提取文档字符串
        # 格式化为简洁列表
        return api_summary
    
    def extract_patterns(self, module):
        """提取代码模式"""
        # 识别常用模式
        # 查找最佳实践
        # 标记反模式
        return patterns
    
    def optimize_context(self, module):
        """优化上下文大小"""
        # 压缩冗余信息
        # 保留关键细节
        # 平衡完整性和大小
        return optimized_context
```

**输出**: 优化的上下文，适合AI理解

---

### 3. AI生成器 (ai_skill_generator.py / ai_agent_generator.py)

**职责**: 调用AI生成专业内容

```python
class AISkillGenerator:
    """AI驱动的技能生成"""
    
    def generate_prompt(self, module, context):
        """构建AI提示词"""
        prompt = f"""
你是一位专业的软件工程师，现在需要创建一份技能文档。

## 模块信息
名称: {module['name']}
文件数: {module['file_count']}
主要API: {module['key_apis']}

## 代码片段
{module['code_samples']}

## 任务
生成包含以下部分的技能文档：
1. Domain Expertise (领域专业知识)
2. Key APIs (关键API列表)
3. Common Patterns (常见模式)
4. Code Conventions (代码规范)
5. Testing Strategies (测试策略)

要求：专业、详细、实用，避免泛泛而谈。
        """
        return prompt
    
    def call_ai(self, prompt):
        """调用AI后端"""
        # 支持多种后端：
        # 1. Claude Code (本地，免费)
        # 2. OpenAI API
        # 3. Anthropic API
        # 4. 其他LLM
        return ai_response
    
    def validate_output(self, content):
        """验证AI输出"""
        # 检查格式
        # 验证完整性
        # 评估质量
        return is_valid
```

**输出**: 专业的、语义化的内容

---

## 🎨 AI后端支持

### 优先级顺序

```python
1. Claude Code (最优先)
   ✅ 本地运行，免费
   ✅ 无需API Key
   ✅ 隐私安全
   ✅ 质量高
   
2. OpenAI API
   ✅ 质量稳定
   ❌ 需要API Key
   ❌ 有成本
   ❌ 隐私风险
   
3. Anthropic API
   ✅ 质量很高
   ❌ 需要API Key
   ❌ 成本较高
   ❌ 隐私风险
   
4. Mock/Template (降级)
   ✅ 总是可用
   ❌ 质量较低
   ❌ 缺少语义理解
```

### 自动选择逻辑

```python
def detect_best_backend():
    """自动检测最佳可用后端"""
    
    # 1. 检查Claude Code
    if os.environ.get('CLAUDE_CODE_SESSION'):
        return 'claude-code'
    
    # 2. 检查OpenAI
    if os.environ.get('OPENAI_API_KEY'):
        return 'openai'
    
    # 3. 检查Anthropic
    if os.environ.get('ANTHROPIC_API_KEY'):
        return 'anthropic'
    
    # 4. 降级到模板
    return 'mock'
```

---

## 📊 对比：旧 vs 新

### 旧架构（纯规则）

```python
# ❌ 缺点
1. 模式识别基于关键词 → 语义理解弱
2. 文档生成基于模板 → 内容泛化
3. Agent分组基于规则 → 缺少灵活性
4. 无法适应特殊项目 → 通用性差

# ✅ 优点
1. 速度快 → 秒级完成
2. 无成本 → 完全免费
3. 可预测 → 结果稳定
4. 无依赖 → 不需要API
```

### 新架构（AI-First）

```python
# ✅ 优点
1. 语义理解强 → 真正理解代码
2. 文档质量高 → 专业且详细
3. 适应性强 → 根据项目定制
4. 创造性好 → 提供深度见解

# ⚠️ 注意点
1. 需要AI后端 → 但支持多种选择
2. 有成本/时间 → 但Claude Code免费
3. 结果有随机性 → 但可以调参
```

---

## 🚀 使用示例

### 方式一：使用Claude Code（推荐）

```bash
# 1. 确保在Claude Code会话中
# CLAUDE_CODE_SESSION环境变量已设置

# 2. 分析代码
python scripts/analyze_codebase.py . --output analysis.json

# 3. AI生成技能
python scripts/ai_skill_generator.py analysis.json \
  --output .claude/skills/ \
  --ai claude-code

# 4. AI生成Agent
python scripts/ai_agent_generator.py analysis.json \
  --output .claude/agents/ \
  --ai claude-code
```

### 方式二：使用OpenAI

```bash
# 1. 设置API Key
export OPENAI_API_KEY="sk-..."

# 2. 分析代码
python scripts/analyze_codebase.py . --output analysis.json

# 3. AI生成（使用OpenAI）
python scripts/ai_skill_generator.py analysis.json \
  --output .claude/skills/ \
  --ai openai
```

### 方式三：自动选择

```bash
# 自动选择最佳可用后端
python scripts/ai_skill_generator.py analysis.json \
  --output .claude/skills/

# 输出: 🤖 AI后端: claude-code (自动选择)
```

---

## 🎯 工具的职责边界

### ✅ 工具负责

```
数据层：
  ├─ 文件系统遍历
  ├─ AST解析
  ├─ 依赖分析
  └─ 统计计算

辅助层：
  ├─ 上下文优化
  ├─ Token压缩
  ├─ 格式转换
  └─ 数据清洗

验证层：
  ├─ 格式检查
  ├─ 完整性验证
  ├─ 质量评估
  └─ 结果保存
```

### ✅ AI负责

```
理解层：
  ├─ 语义分析
  ├─ 业务逻辑理解
  └─ 模式识别

创造层：
  ├─ 技能文档生成
  ├─ Agent配置生成
  ├─ 最佳实践建议
  └─ 深度见解

适配层：
  ├─ 项目特点适应
  ├─ 领域专业性
  └─ 语言习惯
```

---

## 📈 质量对比

### 示例：生成技能文档

**规则生成（旧）**:
```markdown
# user-auth

## Key APIs
- login()
- logout()
- validate_token()

## Common Patterns
- 使用装饰器保护路由
- 使用JWT进行认证
```

**AI生成（新）**:
```markdown
# user-auth - 用户认证模块

## 领域专业知识

这个模块负责整个应用的用户认证和授权流程，实现了基于JWT的无状态认证机制。

核心概念：
- **JWT Token**: 使用RS256算法签名的Bearer Token，有效期2小时
- **Refresh Token**: 存储在HttpOnly Cookie中，有效期7天
- **Session管理**: 采用Redis存储活跃会话，支持快速失效

安全最佳实践：
- 密码使用bcrypt加密（cost factor: 12）
- 登录失败3次后锁定账户15分钟
- Token刷新有24小时冷却期

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
# 使用 access_token 调用受保护的API
```

**注意事项**:
- 登录成功会记录审计日志
- 返回的token需要存储在安全的存储中
- 移动端建议使用Keychain/Keystore

### 2. `TokenManager.refresh(refresh_token: str) -> AuthResponse`
**用途**: 刷新过期的访问令牌

**安全约束**:
- Refresh token只能使用一次
- 刷新后旧token立即失效
- 24小时内最多刷新3次

... (更多详细内容)
```

---

## 🔄 迁移指南

### 从旧版本迁移

```bash
# 1. 更新脚本
git pull

# 2. 重新生成（使用AI）
python scripts/ai_skill_generator.py analysis.json --output .claude/skills/

# 3. 对比结果
diff -r .claude/skills.old/ .claude/skills/

# 4. 选择性保留
# - 保留AI生成的高质量内容
# - 合并工具生成的基础数据
```

---

## 🎊 总结

**新的AI-First架构带来**:

1. ✅ **更高质量** - AI真正理解代码语义
2. ✅ **更专业** - 生成的文档和配置更贴近实际
3. ✅ **更灵活** - 适应不同类型的项目
4. ✅ **更智能** - 提供深度见解和最佳实践

**同时保持**:

1. ✅ **零成本选项** - Claude Code免费使用
2. ✅ **隐私安全** - 本地运行，代码不离开本地
3. ✅ **高质量输入** - 工具层提供优化的上下文
4. ✅ **可靠性** - 降级机制确保总是可用

**这是未来的方向！** 🚀
