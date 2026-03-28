---
name: project-skill-generator
description: >
  Analyze large codebases and generate project-specific Claude Code skills and expert agents.
  Use when: (1) Onboarding a new codebase to Claude Code, (2) Creating module-specific expert agents,
  (3) Generating .claude directory with skills/agents structure, (4) Updating skills as codebase evolves,
  (5) Building a team of specialized agents for different modules.
---

# Project Skill Generator

Transform any codebase into a Claude Code powerhouse with specialized skills and expert agents.

## What This Skill Does

**Input**: A codebase path
**Output**: Complete `.claude/` directory with:
- Project-specific skills (APIs, patterns, conventions)
- Expert agents for each module (UI expert, API expert, DB expert, etc.)
- Agent team configuration for coordinated development
- Continuous update mechanism

## Quick Start

### Generate Everything (One Command)

```bash
/generate-project-skills /path/to/your/codebase
```

This will:
1. Analyze codebase structure and patterns
2. Generate module-specific skills
3. Create expert agents
4. Output `.claude/` directory ready to use

### Step-by-Step (More Control)

```bash
# 1. Analyze codebase first
/analyze-codebase /path/to/codebase --output analysis.json

# 2. Generate skills
/generate-skills analysis.json --output .claude/skills/

# 3. Create expert agents
/generate-agents analysis.json --output .claude/agents/

# 4. Update existing skills (after codebase changes)
/update-skills /path/to/codebase --diff HEAD~10
```

## Workflow

### Phase 1: Codebase Analysis

The analysis extracts:

**Structure**:
- Module boundaries and responsibilities
- Dependency graph
- Entry points and public APIs

**Patterns**:
- Coding conventions (naming, formatting)
- Architectural patterns (MVC, microservices, etc.)
- Common idioms and utilities

**Domain Knowledge**:
- Business logic patterns
- API contracts and data models
- Testing strategies
- Configuration patterns

**Output**: `analysis.json` containing structured codebase knowledge

### Phase 2: Skill Generation

For each identified module, generate a skill containing:

```markdown
# Module: user-auth

## Domain Expertise
- OAuth2 flow implementation
- Session management patterns
- Password hashing (bcrypt)

## Key APIs
- `AuthService.login()` - Authenticate user
- `TokenManager.refresh()` - Refresh access token
- `SessionStore.get()` - Retrieve session data

## Common Patterns
```python
# Standard auth flow
auth = AuthService()
token = auth.login(credentials)
session = SessionStore.create(token)
```

## Code Conventions
- Use `@require_auth` decorator for protected routes
- Always validate with `UserSchema` before DB operations
- Return `AuthResponse` model from auth endpoints
```

### Phase 3: Agent Creation

Create specialized agents with focused skill sets:

```yaml
# .claude/agents/auth-expert.yaml
name: auth-expert
role: Authentication & Authorization Specialist
skills:
  - user-auth
  - api-security
  - session-management
capabilities:
  - Implement OAuth flows
  - Design auth middleware
  - Audit security issues
  - Refactor auth logic
constraints:
  - Only modify auth-related files
  - Follow existing security patterns
  - Maintain backward compatibility
```

### Phase 4: Agent Team Configuration

```yaml
# .claude/agents/team.yaml
name: backend-team
agents:
  - auth-expert
  - api-expert
  - db-expert
  - cache-expert
workflow:
  - api-expert: Design endpoints
  - auth-expert: Add authentication
  - db-expert: Implement data layer
  - cache-expert: Optimize performance
```

## Output Structure

```
.claude/
├── CLAUDE.md                 # Project overview
├── settings.json             # Claude Code settings
├── skills/
│   ├── user-auth/
│   │   └── SKILL.md
│   ├── api-core/
│   │   └── SKILL.md
│   ├── database/
│   │   └── SKILL.md
│   └── frontend-ui/
│       └── SKILL.md
├── agents/
│   ├── auth-expert.yaml
│   ├── api-expert.yaml
│   ├── db-expert.yaml
│   ├── ui-expert.yaml
│   └── team.yaml
└── references/
    ├── architecture.md       # System architecture
    ├── conventions.md        # Coding standards
    └── api-contracts.md      # API documentation
```

## Continuous Iteration

### Update Skills After Changes

```bash
# Update based on recent commits
/update-skills /path/to/codebase --since 2024-01-01

# Update specific module
/update-skills /path/to/codebase --module user-auth

# Full re-analysis (major refactors)
/update-skills /path/to/codebase --full
```

### What Gets Updated

- **New patterns**: Detected and added to skills
- **API changes**: Reflected in skill documentation
- **Deprecated code**: Marked in skills
- **New modules**: Generate new skills and agents
- **Agent capabilities**: Updated based on module changes

## Analysis Depth Levels

### Quick (Default)
- Module structure
- Public APIs
- Basic patterns
- **Time**: ~1 min per 10k LOC

### Standard
- Quick + private APIs
- Dependency analysis
- Convention extraction
- **Time**: ~3 min per 10k LOC

### Deep
- Standard + semantic analysis
- Business logic extraction
- Test coverage patterns
- Performance patterns
- **Time**: ~10 min per 10k LOC

```bash
/analyze-codebase /path --depth deep
```

## Customization

### Skill Templates

Create `skill-templates.yaml` to customize generated skills:

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

### Agent Personas

Define agent personalities in `agent-personas.yaml`:

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

## Best Practices

### 1. Module Boundary Detection
- Start with directory structure
- Refine based on import analysis
- Validate with `__init__.py` or `index.ts`
- Consider semantic cohesion

### 2. Skill Granularity
- **Too coarse**: "backend" skill (too generic)
- **Too fine**: "user-login-function" skill (too narrow)
- **Just right**: "user-authentication" skill (focused, reusable)

### 3. Agent Specialization
- Match real team structure
- Clear responsibility boundaries
- Minimal skill overlap
- Complementary capabilities

### 4. Iteration Strategy
- Update weekly for active projects
- Update after major refactors
- Version control `.claude/` directory
- Review skill changes in PRs

## Troubleshooting

### Skill Too Generic
**Problem**: Generated skill is too high-level
**Solution**: Increase analysis depth or provide more specific code examples

### Agent Overlap
**Problem**: Multiple agents have same skills
**Solution**: Refine module boundaries, create more specific agent roles

### Missing Domain Knowledge
**Problem**: Skill doesn't capture business logic
**Solution**: Use `--depth deep` or manually augment with `references/`

### Slow Generation
**Problem**: Large codebase takes too long
**Solution**: Analyze specific modules first, use `--depth quick`

## Scripts

All scripts are in `scripts/` directory:

- `analyze_codebase.py` - Main analysis engine
- `extract_patterns.py` - Pattern extraction
- `generate_skill.py` - Skill generation
- `generate_agent.py` - Agent configuration generator
- `update_skills.py` - Incremental update logic
- `validate_output.py` - Validate generated structure

Run any script directly:
```bash
python scripts/analyze_codebase.py /path/to/codebase
```

## Examples

### Example 1: FastAPI Project

```bash
/generate-project-skills ./my-fastapi-app

# Output:
.claude/
├── skills/
│   ├── api-routes/      # FastAPI route handlers
│   ├── models/          # SQLAlchemy models
│   ├── auth/            # JWT authentication
│   └── schemas/         # Pydantic schemas
├── agents/
│   ├── api-expert.yaml
│   ├── db-expert.yaml
│   └── auth-expert.yaml
```

### Example 2: React + Node.js Monorepo

```bash
/generate-project-skills ./monorepo --modules frontend,backend,shared

# Output:
.claude/
├── skills/
│   ├── frontend/
│   │   ├── components/
│   │   └── state-management/
│   ├── backend/
│   │   ├── api/
│   │   └── services/
│   └── shared/
│       └── types/
├── agents/
│   ├── frontend-expert.yaml
│   ├── backend-expert.yaml
│   └── fullstack-expert.yaml
```

### Example 3: Legacy Code Migration

```bash
# Step 1: Analyze legacy code
/analyze-codebase ./legacy-app --output legacy-analysis.json

# Step 2: Generate skills for understanding
/generate-skills legacy-analysis.json --mode documentation

# Step 3: After modernization, regenerate
/update-skills ./modernized-app --baseline legacy-analysis.json
```

## Advanced: Multi-Repository Setup

For monorepos or multi-service architectures:

```bash
# Generate shared skills first
/generate-project-skills ./shared-libs --output .claude/shared/

# Then generate service-specific skills
/generate-project-skills ./service-a --inherit .claude/shared/
/generate-project-skills ./service-b --inherit .claude/shared/
```

## Integration with Development Workflow

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
python .claude/scripts/update_skills.py . --quick
git add .claude/
```

### CI/CD Pipeline
```yaml
# .github/workflows/update-skills.yml
- name: Update Claude Skills
  run: |
    python .claude/scripts/update_skills.py . --diff ${{ github.event.before }}
    # Create PR if skills changed
```

### IDE Integration
Skills are automatically loaded when:
- Opening project in Claude Code
- Running `/use-skill <skill-name>`
- Agent activation

---

**Transform your codebase into Claude Code expertise.** 🚀
