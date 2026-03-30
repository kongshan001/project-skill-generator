# 集成指南 - 将 Project Skill Generator 集成到现有项目

## 🎯 快速集成（推荐方式）

### 步骤 1: 复制 Skill 到项目

```bash
# 方式 A: 直接复制
cp -r /path/to/project-skill-generator /your/project/.claude/skills/

# 方式 B: 使用 Git Submodule（推荐）
cd /your/project
git submodule add https://github.com/kongshan001/project-skill-generator.git .claude/skills/project-skill-generator
```

### 步骤 2: 首次运行分析

```bash
cd /your/project

# 分析整个代码库
python .claude/skills/project-skill-generator/scripts/analyze_codebase.py . \
  --output .claude/analysis.json \
  --depth standard

# 生成技能
python .claude/skills/project-skill-generator/scripts/enhanced_generate_skill.py \
  .claude/analysis.json \
  --output .claude/skills/

# 生成专家代理
python .claude/skills/project-skill-generator/scripts/enhanced_generate_agent.py \
  .claude/analysis.json \
  --output .claude/agents/
```

### 步骤 3: 配置 Claude Code

创建或更新 `.claude/CLAUDE.md`:

```markdown
# 项目概览

本项目使用 Project Skill Generator 自动生成技能和专家代理。

## 技能库结构

- `.claude/skills/`: 项目专属技能
  - `project-skill-generator/`: 技能生成工具
  - `[auto-generated]/`: 自动生成的技能

## 专家团队

查看 `.claude/agents/team.yaml` 了解专家配置。

## 更新技能

当项目结构发生变化时，运行：
\`\`\`bash
python .claude/skills/project-skill-generator/scripts/update_skills.py . --incremental
\`\`\`
```

## 🔄 增量更新工作流

### 场景 1: 日常开发更新

```bash
# 每周或在重大变更后运行
python .claude/skills/project-skill-generator/scripts/update_skills.py . \
  --since $(date -d '1 week ago' +%Y-%m-%d)
```

### 场景 2: 添加新模块

```bash
# 只更新特定模块
python .claude/skills/project-skill-generator/scripts/update_skills.py . \
  --module new-feature
```

### 场景 3: 大型重构

```bash
# 完全重新分析
python .claude/skills/project-skill-generator/scripts/update_skills.py . --full
```

## 📋 现有项目集成最佳实践

### 1. 保留现有技能

如果项目已有自定义技能：

```
.claude/
├── skills/
│   ├── custom-skill-1/       # 保留
│   │   └── SKILL.md
│   ├── custom-skill-2/       # 保留
│   │   └── SKILL.md
│   └── project-skill-generator/  # 新增
│       ├── SKILL.md
│       └── scripts/
└── agents/
    └── custom-agent.yaml     # 保留
```

**增量更新会**:
- ✅ 跳过已存在的 `custom-skill-1` 和 `custom-skill-2`
- ✅ 生成新发现的技能
- ✅ 在 `.claude/CHANGES.md` 记录更新

### 2. 使用 .psg.yaml 配置文件

创建 `.psg.yaml` 来自定义分析行为：

```yaml
# .psg.yaml
version: "1.0"

# 模块配置
modules:
  # 排除特定目录
  exclude:
    - legacy/
    - experimental/
    - temp/
  
  # 强制包含
  include:
    - src/core/
    - src/api/
  
  # 自定义模块名称
  rename:
    src/user/authentication: user-auth
    src/user/authorization: user-auth

# 技能生成配置
skills:
  depth: standard
  template: detailed
  
  # 保留的部分（不会被覆盖）
  preserve_sections:
    - custom_notes
    - team_specific_patterns

# 代理生成配置
agents:
  level: senior
  team_structure: auto
  
  # 自定义专家分组
  custom_groups:
    backend:
      - api
      - database
      - auth
    frontend:
      - ui
      - components
      - state

# 增量更新配置
incremental:
  backup: true
  max_backups: 10
  generate_changelog: true
  preserve_user_edits: true
```

### 3. CI/CD 集成

#### GitHub Actions

```yaml
# .github/workflows/update-skills.yml
name: Update Claude Skills

on:
  push:
    branches: [main, develop]
  schedule:
    # 每周一运行
    - cron: '0 0 * * 1'

jobs:
  update-skills:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Update Skills
        run: |
          python .claude/skills/project-skill-generator/scripts/update_skills.py . \
            --since ${{ github.event.before }}
            
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: "🔄 Update Claude Skills"
          body: "自动更新技能库"
          branch: "auto/update-skills"
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
update-skills:
  stage: build
  script:
    - python .claude/skills/project-skill-generator/scripts/update_skills.py . --incremental
  artifacts:
    paths:
      - .claude/
  only:
    - main
    - schedules
```

### 4. Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# 获取变更的文件
CHANGED_FILES=$(git diff --cached --name-only | grep -E '\.(py|ts|js|cpp|sh)$')

if [ ! -z "$CHANGED_FILES" ]; then
    echo "🔍 检测到代码变更，更新技能库..."
    python .claude/skills/project-skill-generator/scripts/update_skills.py . --incremental
    
    # 将更新的技能加入提交
    git add .claude/skills/
    git add .claude/CHANGES.md
fi
```

## 🎨 自定义技能模板

### 创建自定义模板

```yaml
# .claude/templates/skill-templates.yaml
templates:
  # API 模块模板
  api-module:
    sections:
      - domain_expertise
      - key_apis
      - common_patterns
      - error_handling
      - testing_guide
      - performance
    custom:
      - deployment_notes
      - monitoring
      
  # UI 组件模板
  ui-component:
    sections:
      - component_library
      - styling_guide
      - state_management
      - accessibility
      - testing_guide
    custom:
      - design_tokens
      - ux_guidelines
```

### 使用自定义模板

```bash
python scripts/enhanced_generate_skill.py analysis.json \
  --template-dir .claude/templates/ \
  --template api-module
```

## 📊 项目特定配置示例

### FastAPI 项目

```yaml
# .psg.yaml (FastAPI 项目)
modules:
  include:
    - app/api/
    - app/models/
    - app/services/
    
skills:
  template: api-module
  
agents:
  custom_groups:
    api:
      - fastapi-routes
      - pydantic-schemas
    database:
      - sqlalchemy-models
      - migrations
    auth:
      - jwt-auth
      - oauth
```

### React + TypeScript 项目

```yaml
# .psg.yaml (React 项目)
modules:
  exclude:
    - node_modules/
    - build/
    
skills:
  depth: standard
  
agents:
  custom_groups:
    frontend:
      - components
      - hooks
      - utils
    state:
      - redux
      - context
```

### Django 项目

```yaml
# .psg.yaml (Django 项目)
modules:
  include:
    - myapp/
    
skills:
  template: django-module
  
agents:
  custom_groups:
    views:
      - views
      - urls
      - serializers
    models:
      - models
      - managers
```

## 🔄 迁移现有项目

### 从手动技能库迁移

```bash
# 1. 备份现有技能
cp -r .claude/skills .claude/skills.backup

# 2. 运行首次分析
python .claude/skills/project-skill-generator/scripts/analyze_codebase.py . \
  --output .claude/analysis.json \
  --depth deep

# 3. 生成新技能（不会覆盖现有技能）
python .claude/skills/project-skill-generator/scripts/enhanced_generate_skill.py \
  .claude/analysis.json \
  --output .claude/skills/ \
  --preserve-existing

# 4. 审查更新报告
cat .claude/CHANGES.md

# 5. 手动合并（如需要）
# 比较新旧技能，合并有价值的内容
```

## 📝 常见问题

### Q: 会覆盖我现有的技能吗？

**A**: 不会。增量更新模式会：
- 跳过已存在的技能文件
- 保留用户自定义部分（标记为 `<!-- custom -->` 的内容）
- 生成新发现的技能
- 创建备份以防万一

### Q: 如何标记用户自定义内容？

**A**: 在 SKILL.md 中使用标记：
```markdown
<!-- custom: team_notes -->
这里是团队特定的注释，不会被自动更新覆盖。
<!-- end: team_notes -->
```

### Q: 多久更新一次技能库？

**A**: 建议：
- **活跃开发**: 每周或每次重大变更后
- **维护模式**: 每月或按需
- **CI/CD**: 每次合并到主分支时

### Q: 如何回滚到之前的版本？

**A**: 从备份恢复：
```bash
# 查看备份
ls .claude/backups/

# 恢复特定版本
cp -r .claude/backups/20240315_143022/* .claude/skills/
```

## 🎯 最佳实践总结

1. ✅ **使用 Git Submodule** 管理 Project Skill Generator
2. ✅ **创建 .psg.yaml** 自定义分析行为
3. ✅ **定期增量更新** 保持技能库新鲜
4. ✅ **保留现有技能** 避免意外覆盖
5. ✅ **集成到 CI/CD** 自动化更新流程
6. ✅ **审查变更日志** 了解更新内容
7. ✅ **版本控制 .claude/** 追踪技能演进

---

**开始使用**: `cp -r project-skill-generator /your/project/.claude/skills/` 🚀
