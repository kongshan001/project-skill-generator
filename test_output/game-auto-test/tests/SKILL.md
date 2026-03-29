---
name: tests
description: Expert skills for tests module. Patterns: decorators: pytest, pytest-testing, decorators: pytest. Contains 7 key classes. Provides 75 functions. Use when working with tests related code.
---

# Tests

## Overview

This skill provides expertise for the **tests** module.

**Location**: `/root/.openclaw/workspace-opengl/repos/game-auto-test/tests`

**Language**: python

**Files**: 7 files

## Domain Expertise

### Patterns
- type-hints
- decorators: pytest
- context-manager
- pytest-testing
- decorators: patch

### Key Concepts
- `TestDecisionAgent`
- `TestScreenCapture`
- `TestConfig`
- `TestGLMClient`
- `TestTestCaseParser`

## Key APIs

### Classes
- `TestDecisionAgent`
- `TestScreenCapture`
- `TestConfig`
- `TestGLMClient`
- `TestTestCaseParser`
- `TestActionRecord`
- `TestStateMemory`

### Functions
- `TestDecisionAgent.mock_glm_client()`
- `TestDecisionAgent.mock_state_memory()`
- `TestDecisionAgent.decision_agent()`
- `TestDecisionAgent.test_init()`
- `TestDecisionAgent.test_init_with_custom_params()`
- `TestDecisionAgent.test_action_count_tracking()`
- `TestDecisionAgent.test_should_retry()`
- `TestDecisionAgent.test_reset_action_counts()`
- `TestDecisionAgent.test_build_history_context_empty()`
- `TestDecisionAgent.test_extract_json_valid()`

## Common Patterns

- **type-hints**: Common pattern in this module
- **decorators: pytest**: Common pattern in this module
- **context-manager**: Common pattern in this module
- **pytest-testing**: Common pattern in this module
- **decorators: patch**: Common pattern in this module

### Usage Examples

```python
// Pattern usage examples would go here
// Analyze actual code for specific implementations
```

## Code Examples

### Basic Usage

```python
# Import from tests

from tests import TestDecisionAgent, TestScreenCapture
```
## Usage Guide

### When to Use This Skill

- Working with tests module
- Implementing features related to this domain
- Refactoring code in this module
- Debugging issues in this area

### Best Practices

1. **Understand the domain**: Review the module's purpose and patterns
2. **Follow conventions**: Use the naming and structure patterns found in the codebase
3. **Check dependencies**: Be aware of module dependencies
4. **Test changes**: Ensure changes don't break existing functionality

### Common Tasks

- Adding new functionality to the module
- Refactoring existing code
- Fixing bugs
- Adding tests

