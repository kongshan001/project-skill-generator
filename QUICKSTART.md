# Project Skill Generator - Quick Start Guide

## 🎯 What This Generates

From a codebase, generates:

1. **Skills** - Project-specific expertise (10KB - 100KB per skill)
2. **Agents** - Expert specialists (UI expert, API expert, DB expert, etc.)
3. **Team Config** - Agent coordination setup
4. **References** - Architecture docs, conventions, API contracts

## 🚀 Quick Start

### Option 1: Demo Mode (Easiest)

```bash
cd /root/.openclaw/workspace-opengl/skills/project-skill-generator
python3 demo.py
```

Follow the prompts to:
1. Analyze a codebase
2. Generate skills
3. Generate agents
4. See the results

### Option 2: Full Claude Code Integration

```bash
# 1. Copy the skill to your Claude Code skills directory
cp -r /root/.openclaw/workspace-opengl/skills/project-skill-generator ~/.openclaw/skills/project-skill-generator

# 2. Analyze and generate in your project
cd /path/to/your/project
/openclaw skill activate project-skill-generator

# 3. Generate everything
/generate-project-skills .

# 4. Done! Your project now has .claude/ directory with:
#    - skills/ (project-specific skills)
#    - agents/ (expert agents)
#    - references/ (documentation)
```

## 📊 What You Get

### Example Output for a FastAPI Project:

```
your-project/
├── .claude/
│   ├── CLAUDE.md                    # Project overview
│   ├── settings.json                # Claude Code config
│   ├── skills/
│   │   ├── api-routes/              # FastAPI routes
│   │   │   └── SKILL.md
│   │   ├── database/                # SQLAlchemy models
│   │   │   └── SKILL.md
│   │   ├── auth/                    # JWT authentication
│   │   │   └── SKILL.md
│   │   └── schemas/                 # Pydantic schemas
│   │       └── SKILL.md
│   ├── agents/
│   │   ├── api-expert.yaml          # API specialist
│   │   ├── db-expert.yaml           # Database specialist
│   │   ├── auth-expert.yaml         # Security specialist
│   │   └── team.yaml                # Team configuration
│   └── references/
│       ├── architecture.md
│       ├── conventions.md
│       └── api-contracts.md
```

## 🎨 Skills Content

Each skill includes:

```markdown
---
name: api-routes
description: Expert knowledge of API routes, request handling, and endpoint design
---

# API Routes

## Overview
FastAPI route handlers for user management API

## Key APIs
- GET /api/users - List all users
- POST /api/users - Create new user
- PUT /api/users/{id} - Update user
- DELETE /api/users/{id} - Delete user

## Common Patterns
### Request Validation
```python
@app.post("/api/users")
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user)
):
    # Implementation
    pass
```

### Error Handling
```python
from fastapi import HTTPException

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    user = await get_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```
```

## 🤖 Agents Content

Each agent includes:

```yaml
name: api-expert
role: Backend API Specialist
description: Expert in REST API design, authentication, and server architecture
skills:
  - api-routes
  - api-authentication
  - api-validation
capabilities:
  - Design API endpoints
  - Implement authentication
  - Handle API requests
  - Optimize server performance
constraints:
  - Only modify backend code
  - Maintain API backward compatibility
  - Follow API design patterns
  - Document all endpoints
style: systematic, performance-conscious, well-documented
focuses_on:
  - Performance
  - Scalability
  - Documentation
  - Error handling
avoids:
  - Breaking changes
  - Undocumented features
  - Performance regressions
modules:
  - backend
  - api
  - routes
file_patterns:
  - /backend/**/*.py
  - /api/**/*.py
```

## 🔄 Iteration & Updates

After codebase changes:

```bash
# Quick update (last 7 days)
python scripts/update_skills.py . --quick

# Update based on git commits
python scripts/update_skills.py . --diff HEAD~5

# Full re-analysis (major refactor)
python scripts/update_skills.py . --full
```

## 📖 Available Commands

### Main Commands (Claude Code)

- `/generate-project-skills <path>` - Generate everything
- `/analyze-codebase <path>` - Analyze codebase only
- `/generate-skills <analysis.json>` - Generate skills only
- `/generate-agents <analysis.json>` - Generate agents only
- `/update-skills <path>` - Update based on changes

### Scripts (Terminal)

```bash
# Analyze codebase
python scripts/analyze_codebase.py . --depth deep

# Generate skills
python scripts/generate_skill.py analysis.json --depth detailed

# Generate agents
python scripts/generate_agent.py analysis.json --team

# Update skills
python scripts/update_skills.py . --since 2024-01-01

# Validate installation
python validate.py

# Run demo
python demo.py
```

## 💡 How It Works

### Phase 1: Analysis
- Detects module boundaries
- Extracts code patterns
- Identifies public APIs
- Analyzes dependencies
- Determines conventions

### Phase 2: Skill Generation
- Creates module-specific skills
- Includes code examples
- Documents APIs
- Records patterns
- Adds usage guides

### Phase 3: Agent Generation
- Creates expert agents per module
- Defines skills per agent
- Sets capabilities
- Defines constraints
- Configures styles

### Phase 4: Team Configuration
- Orchestrates agents
- Defines workflow
- Sets communication patterns
- Configures coordination

## 🎯 Use Cases

### 1. Onboarding New Developers
```bash
/generate-project-skills .
# Gives new developers instant context
```

### 2. Faster Feature Development
```bash
# Developers can now use:
/use-skill api-routes
/use-skill database
/use-skill auth

# Or let agents handle specific tasks:
/run-agent backend-expert "Add user profile endpoint"
```

### 3. Code Reviews
```bash
# Run agents for review:
/run-agent frontend-expert "Review UI changes"
/run-agent backend-expert "Review API changes"
```

### 4. Refactoring
```bash
# Update skills:
/update-skills . --full

# Then use updated skills:
/use-skill api-routes
```

## 🚨 Troubleshooting

### Skill too generic?
- Increase analysis depth: `--depth deep`
- Provide specific examples

### Agent overlap?
- Refine module boundaries
- Create more specific agent roles

### Missing domain knowledge?
- Use `--depth deep`
- Manually augment with `references/`

### Slow generation?
- Use `--depth quick` for large codebases
- Analyze specific modules first

## 📚 Next Steps

1. **Run the demo**: `python demo.py`
2. **Analyze your project**: `python scripts/analyze_codebase.py .`
3. **Generate skills**: `python scripts/generate_skill.py analysis.json`
4. **Generate agents**: `python scripts/generate_agent.py analysis.json --team`
5. **Integrate into Claude Code**: Move `.claude/` to your project
6. **Start using**: `/use-skill <skill-name>` or run agents

## 🎉 Benefits

- **Faster development**: Domain expertise instantly available
- **Consistent code**: Follows project patterns and conventions
- **Better quality**: Built-in best practices and constraints
- **Scalable**: Works for small projects to large codebases
- **Maintainable**: Skills update automatically with code changes

---

**Ready to transform your codebase into Claude Code expertise?** 🚀
