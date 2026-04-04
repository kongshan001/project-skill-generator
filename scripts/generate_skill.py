#!/usr/bin/env python3
"""
Skill Generator - Generate Claude Code skills from analysis results

Usage:
    generate_skill.py <analysis.json> [options]

Options:
    --output DIR          Output directory for skills (default: .claude/skills)
    --template FILE       Custom skill template file
    --depth LEVEL         Skill depth: basic, detailed, comprehensive (default: detailed)
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class SkillTemplate:
    """Template for skill generation"""
    name: str
    description_template: str
    sections: List[str]


class SkillGenerator:
    """Generate Claude Code skills from analysis"""
    
    def __init__(self, analysis_path: str, output_dir: str = ".claude/skills"):
        with open(analysis_path, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_all_skills(self, depth: str = "detailed"):
        """Generate skills for all modules"""
        print(f"🎨 Generating skills for {len(self.analysis['modules'])} modules...")
        
        for module in self.analysis['modules']:
            print(f"   Creating skill for: {module['name']}")
            self._generate_module_skill(module, depth)
        
        print(f"\n✅ Skills generated in: {self.output_dir}")
    
    def _generate_module_skill(self, module: Dict[str, Any], depth: str):
        """Generate a skill for a single module"""
        skill_name = self._normalize_skill_name(module['name'])
        skill_dir = self.output_dir / skill_name
        skill_dir.mkdir(exist_ok=True)
        
        # Generate SKILL.md
        skill_content = self._generate_skill_markdown(module, depth)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(skill_content)
        
        # Generate references if comprehensive
        if depth == "comprehensive":
            self._generate_references(skill_dir, module)
    
    def _normalize_skill_name(self, module_name: str) -> str:
        """Convert module name to skill name"""
        # Handle empty or dot-only module names
        if not module_name or module_name.strip() == '.':
            return 'main-module'
        
        # Replace dots and slashes with hyphens
        name = module_name.replace('.', '-').replace('/', '-')
        # Remove consecutive hyphens
        while '--' in name:
            name = name.replace('--', '-')
        # Remove leading/trailing hyphens
        name = name.strip('-')
        return name.lower() if name else 'unnamed-module'
    
    def _generate_skill_markdown(self, module: Dict[str, Any], depth: str) -> str:
        """Generate SKILL.md content"""
        skill_name = self._normalize_skill_name(module['name'])
        
        # Build description
        description = self._build_description(module)
        
        # Build sections based on depth
        sections = []
        
        # Overview
        sections.append(self._generate_overview(module))
        
        # Domain Expertise
        if module.get('domain_knowledge') or depth in ['detailed', 'comprehensive']:
            sections.append(self._generate_domain_expertise(module))
        
        # Key APIs
        if module.get('classes') or module.get('functions'):
            sections.append(self._generate_key_apis(module))
        
        # Common Patterns
        if module.get('patterns'):
            sections.append(self._generate_patterns(module))
        
        # Code Examples
        if depth in ['detailed', 'comprehensive']:
            sections.append(self._generate_code_examples(module))
        
        # Dependencies
        if depth == 'comprehensive':
            sections.append(self._generate_dependencies(module))
        
        # Usage Guide
        sections.append(self._generate_usage_guide(module))
        
        # Compose full skill
        skill_content = f"""---
name: {skill_name}
description: {description}
---

# {self._title_case(skill_name)}

{chr(10).join(sections)}
"""
        
        return skill_content
    
    def _build_description(self, module: Dict[str, Any]) -> str:
        """Build skill description"""
        module_name = module['name']
        patterns = module.get('patterns', [])
        classes = module.get('classes', [])
        functions = module.get('functions', [])
        files = module.get('files', [])
        language = module.get('language', 'unknown')
        
        # Handle empty module name
        if not module_name or module_name.strip() == '.':
            module_name = 'main'
        
        desc_parts = [f"Expert skills for {module_name} module."]
        
        # Add language information
        desc_parts.append(f"Language: {language}.")
        
        # Add file count
        desc_parts.append(f"Manages {len(files)} source files.")
        
        # Add patterns if available
        if patterns:
            unique_patterns = list(set(patterns))[:3]  # Top 3 unique patterns
            desc_parts.append(f"Key patterns: {', '.join(unique_patterns)}.")
        else:
            desc_parts.append("Focuses on code structure and best practices.")
        
        # Add classes if available
        if classes:
            desc_parts.append(f"Contains {len(classes)} core classes including {classes[0] if classes else 'key components'}.")
        
        # Add functions if available
        if functions:
            desc_parts.append(f"Provides {len(functions)} utility functions.")
        
        # Add file type information based on language
        file_extensions = set()
        for file in files:
            if '.' in file:
                ext = file.split('.')[-1].lower()
                if ext in ['js', 'ts', 'jsx', 'tsx', 'py', 'java', 'cpp', 'c', 'h', 'go', 'rs', 'rb']:
                    file_extensions.add(ext)
        
        if file_extensions:
            desc_parts.append(f"Supports: {', '.join(sorted(file_extensions))} files.")
        
        # Usage guidance
        desc_parts.append(f"Essential for {module_name} development, testing, and maintenance.")
        
        return " ".join(desc_parts)
    
    def _generate_overview(self, module: Dict[str, Any]) -> str:
        """Generate overview section"""
        return f"""## Overview

This skill provides expertise for the **{module['name']}** module.

**Location**: `{module['path']}`

**Language**: {module['language']}

**Files**: {len(module['files'])} files
"""
    
    def _generate_domain_expertise(self, module: Dict[str, Any]) -> str:
        """Generate domain expertise section"""
        expertise = []
        
        # Add patterns as expertise
        if module.get('patterns'):
            expertise.append("### Patterns")
            for pattern in set(module['patterns']):
                expertise.append(f"- {pattern}")
        
        # Add classes as domain concepts
        if module.get('classes'):
            expertise.append("\n### Key Concepts")
            for cls in module['classes'][:5]:  # Top 5 classes
                expertise.append(f"- `{cls}`")
        
        return f"""## Domain Expertise

{chr(10).join(expertise)}
"""
    
    def _generate_key_apis(self, module: Dict[str, Any]) -> str:
        """Generate key APIs section"""
        sections = []
        
        # Classes
        if module.get('classes'):
            sections.append("### Classes")
            for cls in module['classes']:
                sections.append(f"- `{cls}`")
        
        # Functions
        if module.get('functions'):
            sections.append("\n### Functions")
            for func in module['functions'][:10]:  # Top 10 functions
                sections.append(f"- `{func}()`")
        
        # Public exports
        if module.get('exports'):
            sections.append("\n### Public API")
            for export in module['exports'][:10]:
                sections.append(f"- `{export}`")
        
        return f"""## Key APIs

{chr(10).join(sections)}
"""
    
    def _generate_patterns(self, module: Dict[str, Any]) -> str:
        """Generate patterns section"""
        patterns = module.get('patterns', [])
        
        if not patterns:
            return ""
        
        pattern_list = [f"- **{p}**: Common pattern in this module" for p in set(patterns)]
        
        return f"""## Common Patterns

{chr(10).join(pattern_list)}

### Usage Examples

```{module['language']}
// Pattern usage examples would go here
// Analyze actual code for specific implementations
```
"""
    
    def _generate_code_examples(self, module: Dict[str, Any]) -> str:
        """Generate code examples section"""
        lang = module['language']
        files = module.get('files', [])
        
        examples = [f"""## Code Examples

### Basic Usage

```{lang}
# Import from {module['name']}
"""]
        
        # Add import examples based on available data
        if lang == "python":
            exports = module.get('classes', [])[:2] or module.get('functions', [])[:2]
            if exports:
                examples.append(f"from {module['name']} import {', '.join(exports)}")
        elif lang in ["javascript", "typescript"]:
            exports = module.get('exports', [])[:2]
            if exports:
                examples.append(f"import {{ {', '.join(exports)} }} from '{module['name']}';")
        
        examples.append("```")
        
        # Extract actual code snippets from the module files
        if files:
            examples.append(f"""
### Code Snippets

""")
            
            # Try to read and extract meaningful code from files
            for file_path in files[:3]:  # Top 3 files
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                        # Skip if file is empty or too large
                        if not lines or len(lines) > 200:
                            continue
                        
                        # Extract meaningful code sections
                        code_lines = []
                        comment_block = False
                        for line in lines:
                            stripped = line.strip()
                            
                            # Skip empty lines and comments
                            if not stripped or stripped.startswith('//') or stripped.startswith('#'):
                                continue
                            
                            # Skip import statements (already covered in basic usage)
                            if stripped.startswith('import ') or stripped.startswith('from '):
                                continue
                            
                            # Add code line
                            code_lines.append(f"    {line.rstrip()}")
                            
                            # Limit code example length
                            if len(code_lines) >= 15:
                                break
                        
                        if code_lines:
                            filename = file_path.split('/')[-1]
                            examples.append(f"#### {filename}")
                            examples.append("```" + lang)
                            examples.extend(code_lines[:15])
                            examples.append("```")
                            examples.append("")
                            
                except Exception:
                    # If we can't read the file, skip it
                    continue
        
        return chr(10).join(examples)
    
    def _generate_dependencies(self, module: Dict[str, Any]) -> str:
        """Generate dependencies section"""
        imports = module.get('imports', [])
        
        if not imports:
            return ""
        
        deps = [f"- `{imp}`" for imp in list(imports)[:10]]
        
        return f"""## Dependencies

### External Dependencies

{chr(10).join(deps)}
"""
    
    def _generate_usage_guide(self, module: Dict[str, Any]) -> str:
        """Generate usage guide"""
        return f"""## Usage Guide

### When to Use This Skill

- Working with {module['name']} module
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
"""
    
    def _generate_references(self, skill_dir: Path, module: Dict[str, Any]):
        """Generate reference files"""
        refs_dir = skill_dir / "references"
        refs_dir.mkdir(exist_ok=True)
        
        # API reference
        api_ref = refs_dir / "api_reference.md"
        api_content = self._generate_api_reference(module)
        api_ref.write_text(api_content)
        
        # Architecture reference
        arch_ref = refs_dir / "architecture.md"
        arch_content = self._generate_architecture_reference(module)
        arch_ref.write_text(arch_content)
    
    def _generate_api_reference(self, module: Dict[str, Any]) -> str:
        """Generate detailed API reference"""
        content = f"""# API Reference - {module['name']}

## Classes

"""
        for cls in module.get('classes', []):
            content += f"### `{cls}`\n\nClass from {module['name']} module.\n\n"
        
        content += "\n## Functions\n\n"
        for func in module.get('functions', []):
            content += f"### `{func}()`\n\nFunction from {module['name']} module.\n\n"
        
        return content
    
    def _generate_architecture_reference(self, module: Dict[str, Any]) -> str:
        """Generate architecture reference"""
        return f"""# Architecture - {module['name']}

## Module Structure

- **Path**: {module['path']}
- **Files**: {len(module['files'])}
- **Language**: {module['language']}

## Design Patterns

{chr(10).join([f'- {p}' for p in module.get('patterns', [])])}

## Dependencies

{chr(10).join([f'- {d}' for d in module.get('imports', [])[:10]])}
"""
    
    def _title_case(self, text: str) -> str:
        """Convert to title case"""
        return ' '.join(word.capitalize() for word in text.split('-'))


def main():
    parser = argparse.ArgumentParser(description="Generate Claude Code skills from analysis")
    parser.add_argument("analysis_file", help="Path to analysis.json")
    parser.add_argument("--output", default=".claude/skills", help="Output directory")
    parser.add_argument("--depth", choices=["basic", "detailed", "comprehensive"], default="detailed")
    
    args = parser.parse_args()
    
    generator = SkillGenerator(args.analysis_file, args.output)
    generator.generate_all_skills(args.depth)


if __name__ == "__main__":
    main()
