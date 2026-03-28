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

## Scripts

All scripts are in `scripts/` directory:

### analyze_codebase.py
Analyze codebase structure and patterns.

```bash
python scripts/analyze_codebase.py /path/to/codebase --depth standard --output analysis.json
```

Options:
- `--depth`: quick, standard, deep
- `--modules`: comma-separated modules to analyze
- `--exclude`: comma-separated patterns to exclude

### generate_skill.py
Generate Claude Code skills from analysis.

```bash
python scripts/generate_skill.py analysis.json --output .claude/skills/ --depth detailed
```

Options:
- `--output`: Output directory
- `--depth`: basic, detailed, comprehensive

### generate_agent.py
Generate expert agents from analysis.

```bash
python scripts/generate_agent.py analysis.json --output .claude/agents/ --team
```

Options:
- `--output`: Output directory
- `--team`: Generate team configuration

### update_skills.py
Incrementally update skills based on codebase changes.

```bash
python scripts/update_skills.py /path/to/codebase --since 2024-01-01
```

Options:
- `--since`: Changes since date
- `--diff`: Changes since git commit
- `--module`: Update specific module only
- `--full`: Full re-analysis

## Examples

### Example 1: FastAPI Project

```bash
# Generate everything
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
# Generate with specific modules
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

## Advanced: Multi-Repository Setup

For monorepos or multi-service architectures:

```bash
# Generate shared skills first
/generate-project-skills ./shared-libs --output .claude/shared/

# Then generate service-specific skills
/generate-project-skills ./service-a --inherit .claude/shared/
/generate-project-skills ./service-b --inherit .claude/shared/
```

## Advanced: Language-Specific Patterns

The skill generator adapts to different languages:

### Python
- AST parsing
- Type hints
- Decorators
- Context managers

### JavaScript/TypeScript
- ES6+ syntax
- JSX/TSX
- Hooks
- Modules

### Java
- Spring patterns
- Annotations
- DTOs
- Service layers

### Go
- Package structure
- Interfaces
- Concurrency patterns
- Testing

## Future Enhancements

- [ ] Support for more languages
- [ ] ML-based pattern detection
- [ ] Automated documentation generation
- [ ] Integration with CI/CD tools
- [ ] Web-based skill management UI
- [ ] Skill marketplace

---

**Transform your codebase into Claude Code expertise.** 🚀
