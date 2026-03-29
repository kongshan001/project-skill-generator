#!/usr/bin/env python3
"""
Enhanced Skill Generator - Generate high-quality Claude Code skills from analysis results

This is an enhanced version with:
- Better API documentation
- Detailed code examples
- Testing recommendations
- Performance optimization suggestions
- Error handling patterns
- Best practices based on actual code analysis

Usage:
    enhanced_generate_skill.py <analysis.json> [options]

Options:
    --output DIR          Output directory for skills (default: .claude/skills)
    --template FILE       Custom skill template file
    --depth LEVEL         Skill depth: basic, detailed, comprehensive (default: detailed)
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EnhancedSkillTemplate:
    """Enhanced template for skill generation"""
    name: str
    description_template: str
    sections: List[str]
    complexity_metrics: Dict[str, Any]


class EnhancedSkillGenerator:
    """Generate high-quality Claude Code skills from analysis with enhanced features"""
    
    def __init__(self, analysis_path: str, output_dir: str = ".claude/skills"):
        with open(analysis_path, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_all_skills(self, depth: str = "detailed"):
        """Generate enhanced skills for all modules"""
        print(f"🎨 Generating enhanced skills for {len(self.analysis['modules'])} modules...")
        
        for module in self.analysis['modules']:
            print(f"   Creating enhanced skill for: {module['name']}")
            self._generate_enhanced_module_skill(module, depth)
        
        print(f"\n✅ Enhanced skills generated in: {self.output_dir}")
    
    def _generate_enhanced_module_skill(self, module: Dict[str, Any], depth: str):
        """Generate an enhanced skill for a single module"""
        skill_name = self._normalize_skill_name(module['name'])
        
        # Calculate complexity metrics
        complexity = self._calculate_complexity_metrics(module)
        
        # Build enhanced sections
        sections = []
        
        # Required sections
        sections.append(self._generate_enhanced_description(module, complexity))
        sections.append(self._generate_module_overview(module))
        sections.append(self._generate_enhanced_apis(module, depth))
        
        # Enhanced patterns
        if depth in ['detailed', 'comprehensive']:
            sections.append(self._generate_detailed_patterns(module))
        
        # Enhanced code examples
        sections.append(self._generate_enhanced_code_examples(module, depth))
        
        # Testing recommendations
        if depth in ['detailed', 'comprehensive']:
            sections.append(self._generate_testing_recommendations(module))
        
        # Performance optimization
        if depth == 'comprehensive':
            sections.append(self._generate_performance_optimizations(module))
        
        # Error handling
        if depth in ['detailed', 'comprehensive']:
            sections.append(self._generate_error_handling_patterns(module))
        
        # Dependencies
        if depth == 'comprehensive':
            sections.append(self._generate_enhanced_dependencies(module))
        
        # Usage guide with best practices
        sections.append(self._generate_enhanced_usage_guide(module, complexity))
        
        # Compose full skill
        skill_content = f"""---
name: {skill_name}
description: {self._build_enhanced_description(module, complexity)}
complexity: {complexity['overall_level']}
last_updated: {datetime.now().isoformat()}
---

# {self._title_case(skill_name)} - Enhanced Skill

{chr(10).join(sections)}
"""
        
        # Write skill file
        skill_file = self.output_dir / f"{skill_name}.md"
        skill_file.write_text(skill_content, encoding='utf-8')
        
        # Generate agent file
        self._generate_agent_file(skill_name, module, complexity)
    
    def _calculate_complexity_metrics(self, module: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate complexity metrics for the module"""
        complexity = {
            'total_classes': len(module.get('classes_info', [])),
            'total_functions': len(module.get('functions_info', [])),
            'avg_function_complexity': 0,
            'high_complexity_functions': 0,
            'async_functions': 0,
            'functions_with_docstrings': 0,
            'functions_with_type_hints': 0,
            'overall_level': 'simple'
        }
        
        # Calculate function metrics
        if module.get('functions_info'):
            complexities = []
            for func in module['functions_info']:
                complexities.append(func.get('complexity', 0))
                complexity['async_functions'] += 1 if func.get('is_async') else 0
                complexity['functions_with_docstrings'] += 1 if func.get('docstring') else 0
                complexity['functions_with_type_hints'] += 1 if func.get('return_type') or func.get('parameters') else 0
            
            complexity['avg_function_complexity'] = sum(complexities) / len(complexities) if complexities else 0
            complexity['high_complexity_functions'] = sum(1 for c in complexities if c > 10)
        
        # Determine overall complexity level
        if complexity['avg_function_complexity'] > 15 or complexity['total_classes'] > 10:
            complexity['overall_level'] = 'complex'
        elif complexity['avg_function_complexity'] > 8 or complexity['total_classes'] > 5:
            complexity['overall_level'] = 'moderate'
        
        return complexity
    
    def _build_enhanced_description(self, module: Dict[str, Any], complexity: Dict[str, Any]) -> str:
        """Build enhanced skill description"""
        module_name = module['name']
        patterns = module.get('patterns', [])
        has_classes = len(module.get('classes', [])) > 0
        has_functions = len(module.get('functions', [])) > 0
        
        desc_parts = [f"Enhanced expertise for {module_name} module."]
        
        if patterns:
            desc_parts.append(f"Key patterns: {', '.join(list(set(patterns))[:3])}.")
        
        if has_classes:
            desc_parts.append(f"Expertise in {len(module['classes'])} classes with detailed analysis.")
        
        if has_functions:
            desc_parts.append(f"Mastery of {len(module['functions'])} functions including complexity analysis.")
        
        desc_parts.append(f"Complexity level: {complexity['overall_level']}.")
        desc_parts.append(f"Comprehensive testing and optimization guidance included.")
        
        return " ".join(desc_parts)
    
    def _generate_enhanced_description(self, module: Dict[str, Any], complexity: Dict[str, Any]) -> str:
        """Generate enhanced description section"""
        return f"""## Enhanced Description

This skill provides **expert-level** guidance for the **{module['name']}** module, including:

- **Detailed API documentation** with parameter and return type information
- **Complexity analysis** with optimization recommendations
- **Code examples** for common use cases
- **Testing strategies** and best practices
- **Performance optimization** suggestions
- **Error handling patterns** and debugging guidance

### Module Complexity Analysis

- **Overall Complexity**: {complexity['overall_level']}
- **Classes**: {complexity['total_classes']}
- **Functions**: {complexity['total_functions']}
- **Average Function Complexity**: {complexity['avg_function_complexity']:.2f}
- **High-Complexity Functions**: {complexity['high_complexity_functions']}
- **Async Functions**: {complexity['async_functions']}
- **Documented Functions**: {complexity['functions_with_docstrings']}
- **Type-Annotated Functions**: {complexity['functions_with_type_hints']}

This skill adapts to your project's complexity level and provides targeted guidance.
"""
    
    def _generate_module_overview(self, module: Dict[str, Any]) -> str:
        """Generate enhanced overview section"""
        return f"""## Module Overview

### Purpose

The **{module['name']}** module serves as a key component of the codebase with specialized functionality.

### Key Components

{self._generate_component_summary(module)}

### Architecture Context

{self._generate_architecture_context(module)}

### Domain Knowledge

{self._generate_domain_knowledge(module)}
"""
    
    def _generate_component_summary(self, module: Dict[str, Any]) -> str:
        """Generate component summary"""
        parts = []
        
        if module.get('classes_info'):
            classes_summary = []
            for class_info in module['classes_info'][:5]:  # Top 5 classes
                class_name = class_info['name']
                methods_count = len(class_info.get('methods', []))
                docstring = class_info.get('docstring', 'No documentation')
                
                classes_summary.append(f"""
- **{class_name}** ({methods_count} methods)
  - {docstring[:100]}...
""")
            
            parts.append("#### Key Classes")
            parts.extend(classes_summary)
        
        if module.get('functions_info'):
            functions_summary = []
            for func in module['functions_info'][:5]:  # Top 5 functions
                func_name = func['name']
                complexity = func.get('complexity', 0)
                is_async = " (async)" if func.get('is_async') else ""
                
                functions_summary.append(f"""
- **{func_name}{is_async}** (complexity: {complexity})
  - Detailed parameters and documentation available
""")
            
            parts.append("#### Key Functions")
            parts.extend(functions_summary)
        
        return "\n".join(parts)
    
    def _generate_architecture_context(self, module: Dict[str, Any]) -> str:
        """Generate architecture context"""
        architecture = self.analysis.get('architecture', 'Unknown')
        entry_points = self.analysis.get('entry_points', [])
        
        context = f"""
**Architecture Pattern**: {architecture}

**Entry Points**:
{chr(10).join(f"- {ep}" for ep in entry_points)}

**Module Relationships**:
{self._generate_relationship_summary(module)}
"""
        
        return context
    
    def _generate_relationship_summary(self, module: Dict[str, Any]) -> str:
        """Generate module relationship summary"""
        imports = module.get('imports', [])
        dependencies = module.get('dependencies', set())
        
        summary = []
        if imports:
            summary.append("- Depends on: " + ", ".join(list(imports)[:5]))
        if dependencies:
            summary.append("- Used by: external modules")
        
        return "\n".join(summary) if summary else "No external dependencies identified."
    
    def _generate_domain_knowledge(self, module: Dict[str, Any]) -> str:
        """Generate domain knowledge section"""
        domain_knowledge = self.analysis.get('domain_knowledge', [])
        conventions = self.analysis.get('conventions', {})
        
        knowledge = []
        if domain_knowledge:
            knowledge.extend(domain_knowledge[:3])
        
        if conventions:
            knowledge.extend([
                "Follows established coding conventions",
                "Adheres to project-specific patterns"
            ])
        
        return "\n".join(f"- {k}" for k in knowledge) if knowledge else "Standard domain practices apply."
    
    def _generate_enhanced_apis(self, module: Dict[str, Any], depth: str) -> str:
        """Generate enhanced API documentation"""
        return f"""## Enhanced API Documentation

### Public APIs

{self._generate_detailed_api_docs(module)}

### Usage Patterns

{self._generate_usage_patterns(module)}

### API Examples

{self._generate_api_examples(module)}
"""
    
    def _generate_detailed_api_docs(self, module: Dict[str, Any]) -> str:
        """Generate detailed API documentation"""
        docs = []
        
        # Classes
        if module.get('classes_info'):
            for class_info in module['classes_info']:
                docs.append(self._generate_class_doc(class_info))
        
        # Functions
        if module.get('functions_info'):
            for func in module['functions_info']:
                docs.append(self._generate_function_doc(func))
        
        return "\n\n".join(docs) if docs else "No detailed API information available."
    
    def _generate_class_doc(self, class_info: Dict[str, Any]) -> str:
        """Generate class documentation"""
        name = class_info['name']
        methods = class_info.get('methods', [])
        docstring = class_info.get('docstring', '')
        inheritance = class_info.get('inheritance', [])
        
        doc = f"""#### `{name}`

{docstring or f"Class {name}"}

**Inheritance**: {', '.join(inheritance) if inheritance else "None"}

**Methods** ({len(methods)}):
"""
        
        for method in methods[:3]:  # Show top 3 methods
            method_name = method.get('name', 'unknown')
            complexity = method.get('complexity', 0)
            docstring = method.get('docstring', '')
            
            doc += f"- `{method_name}` (complexity: {complexity})"
            if docstring:
                doc += f" - {docstring[:50]}..."
            doc += "\n"
        
        if len(methods) > 3:
            doc += f"... and {len(methods) - 3} more methods"
        
        return doc
    
    def _generate_function_doc(self, func: Dict[str, Any]) -> str:
        """Generate function documentation"""
        name = func['name']
        params = func.get('parameters', [])
        return_type = func.get('return_type', '')
        complexity = func.get('complexity', 0)
        is_async = func.get('is_async', False)
        is_generator = func.get('is_generator', False)
        docstring = func.get('docstring', '')
        
        doc = f"""#### `{name}`

{docstring or f"Function {name}"}

**Complexity**: {complexity}
**Type**: {'Async' if is_async else ''}{'Generator' if is_generator else ''}

**Parameters** ({len(params)}):
"""
        
        for param in params:
            param_name = param.get('name', 'unknown')
            param_type = param.get('type_annotation', '')
            default_value = param.get('default_value', '')
            
            param_doc = f"- `{param_name}`"
            if param_type:
                param_doc += f": {param_type}"
            if default_value:
                param_doc += f" = {default_value}"
            doc += param_doc + "\n"
        
        if return_type:
            doc += f"**Returns**: {return_type}\n"
        
        return doc
    
    def _generate_usage_patterns(self, module: Dict[str, Any]) -> str:
        """Generate usage patterns"""
        patterns = module.get('patterns', [])
        if not patterns:
            return "No specific patterns identified."
        
        pattern_docs = []
        for pattern in set(patterns):
            pattern_docs.append(f"- **{pattern}**: Common usage pattern in this module")
        
        return "\n".join(pattern_docs)
    
    def _generate_api_examples(self, module: Dict[str, Any]) -> str:
        """Generate API usage examples"""
        lang = module['language']
        examples = []
        
        # Basic usage
        examples.append(f"""### Basic Usage

```{lang}
# Import and use the module
""")
        
        if lang == "python":
            if module.get('classes'):
                examples.append(f"from {module['name']} import {module['classes'][0]}")
                examples.append(f"instance = {module['classes'][0]}()")
            elif module.get('functions'):
                examples.append(f"from {module['name']} import {module['functions'][0]}")
                examples.append(f"result = {module['functions'][0]}()")
        
        examples.append("```")
        
        # Advanced usage
        examples.append(f"""
### Advanced Usage

```{lang}
# Advanced usage examples
""")
        
        if module.get('classes_info'):
            for cls in module['classes_info'][:2]:
                if cls.get('methods'):
                    examples.append(f"# Using {cls['name']}")
                    for method in cls['methods'][:2]:
                        examples.append(f"result = instance.{method.get('name', 'method')}()")
        
        examples.append("```")
        
        return "\n".join(examples)
    
    def _generate_detailed_patterns(self, module: Dict[str, Any]) -> str:
        """Generate detailed patterns section"""
        patterns = module.get('patterns', [])
        if not patterns:
            return ""
        
        pattern_docs = [f"""## Detailed Code Patterns

### Identified Patterns"""]
        
        # Group patterns by type
        pattern_groups = {}
        for pattern in patterns:
            if 'class' in pattern.lower():
                pattern_groups['classes'] = pattern_groups.get('classes', []) + [pattern]
            elif 'function' in pattern.lower() or 'method' in pattern.lower():
                pattern_groups['functions'] = pattern_groups.get('functions', []) + [pattern]
            elif 'async' in pattern.lower():
                pattern_groups['async'] = pattern_groups.get('async', []) + [pattern]
            else:
                pattern_groups['general'] = pattern_groups.get('general', []) + [pattern]
        
        # Generate detailed pattern documentation
        for group_name, group_patterns in pattern_groups.items():
            pattern_docs.append(f"\n#### {group_title(group_name)} Patterns")
            pattern_docs.extend(f"- **{p}**" for p in set(group_patterns))
        
        # Pattern examples
        pattern_docs.append(f"""
### Pattern Implementation Examples

```{module['language']}
# Pattern implementation examples based on actual code
""")
        
        # Add actual pattern examples
        for pattern in list(set(patterns))[:3]:  # Top 3 patterns
            pattern_docs.append(f"# {pattern} pattern")
            pattern_docs.append(f"# Example implementation would go here")
        
        pattern_docs.append("```")
        
        return "\n".join(pattern_docs)
    
    def _generate_enhanced_code_examples(self, module: Dict[str, Any], depth: str) -> str:
        """Generate enhanced code examples"""
        lang = module['language']
        
        examples = [f"""## Enhanced Code Examples

### Basic Usage

```{lang}
# Enhanced basic usage with error handling
"""]
        
        # Import examples with error handling
        if lang == "python":
            imports = []
            if module.get('classes'):
                imports.extend(module['classes'][:3])
            if module.get('functions'):
                imports.extend(module['functions'][:3])
            
            if imports:
                examples.append(f"try:")
                examples.append(f"    from {module['name']} import {', '.join(imports)}")
                examples.append(f"except ImportError as e:")
                examples.append(f"    print(f\"Import error: {{e}}\")")
        
        elif lang in ["javascript", "typescript"]:
            exports = module.get('exports', [])[:3]
            if exports:
                examples.append(f"import {{ {', '.join(exports)} }} from '{module['name']}';")
        
        examples.append("```")
        
        # Intermediate examples
        examples.extend([
            f"""
### Intermediate Usage

```{lang}
# Intermediate usage with best practices
""",
        ])
        
        # Add intermediate examples based on analysis
        if module.get('functions_info'):
            for func in module['functions_info'][:2]:
                examples.append(f"# Using {func['name']}")
                if func.get('parameters'):
                    examples.append(f"# {func['name']}({', '.join(p.get('name', 'p') for p in func['parameters'])})")
                examples.append("```")
        
        # Advanced examples
        if depth == 'comprehensive':
            examples.extend([
                f"""
### Advanced Usage

```{lang}
# Advanced usage with optimization
""",
            ])
            
            # Add optimization examples
            if module.get('functions_info'):
                for func in module['functions_info']:
                    if func.get('complexity', 0) > 5:
                        examples.append(f"# Optimized usage for {func['name']} (complexity: {func['complexity']})")
                        examples.append("# Consider breaking down or caching this function")
            
            examples.append("```")
        
        return "\n".join(examples)
    
    def _generate_testing_recommendations(self, module: Dict[str, Any]) -> str:
        """Generate testing recommendations"""
        tests = [
            f"""## Testing Recommendations

### Unit Testing Strategy

{self._generate_unit_test_strategy(module)}

### Integration Testing

{self._generate_integration_test_strategy(module)}

### Testing Best Practices

{self._generate_testing_best_practices(module)}
"""
        ]
        
        return "\n".join(tests)
    
    def _generate_unit_test_strategy(self, module: Dict[str, Any]) -> str:
        """Generate unit test strategy"""
        strategy = []
        
        if module.get('classes_info'):
            strategy.append("#### Class Testing")
            for class_info in module['classes_info']:
                strategy.append(f"- **{class_info['name']}**: Test all public methods, edge cases")
        
        if module.get('functions_info'):
            strategy.append("#### Function Testing")
            for func in module['functions_info']:
                complexity = func.get('complexity', 0)
                if complexity > 10:
                    strategy.append(f"- **{func['name']}**: Consider parameterized testing for high complexity")
                else:
                    strategy.append(f"- **{func['name']}**: Standard unit testing approach")
        
        return "\n".join(strategy)
    
    def _generate_integration_test_strategy(self, module: Dict[str, Any]) -> str:
        """Generate integration test strategy"""
        imports = module.get('imports', [])
        dependencies = module.get('dependencies', set())
        
        if imports or dependencies:
            strategy = [
                "#### Module Integration",
                "- Test interactions with dependent modules",
                "- Verify external API calls",
                "- Mock external dependencies when possible"
            ]
            
            if len(imports) > 5:
                strategy.append("- Consider integration testing for critical dependencies")
            
            return "\n".join(strategy)
        else:
            return "No external dependencies to test."
    
    def _generate_testing_best_practices(self, module: Dict[str, Any]) -> str:
        """Generate testing best practices"""
        practices = [
            "#### Best Practices",
            "- Write tests before implementing features (TDD)",
            "- Maintain high test coverage (>80%)",
            "- Use descriptive test names",
            "- Mock external services and databases",
            "- Test both success and failure scenarios",
            "- Regularly run regression tests"
        ]
        
        # Add language-specific practices
        if module['language'] == 'python':
            practices.extend([
                "- Use pytest framework",
                "- Utilize fixtures for setup/teardown",
                "- Parameterize tests for different inputs"
            ])
        elif module['language'] in ['javascript', 'typescript']:
            practices.extend([
                "- Use Jest or Mocha frameworks",
                "- Implement snapshot testing",
                "- Mock DOM elements for frontend tests"
            ])
        elif module['language'] == 'cpp':
            practices.extend([
                "- Use Google Test framework",
                "- Mock external libraries with Google Mock",
                "- Focus on memory management testing"
            ])
        
        return "\n".join(practices)
    
    def _generate_performance_optimizations(self, module: Dict[str, Any]) -> str:
        """Generate performance optimization suggestions"""
        optimizations = [
            f"""## Performance Optimization

### Complexity Analysis

{self._generate_complexity_analysis(module)}

### Optimization Recommendations

{self._generate_optimization_recommendations(module)}

### Performance Testing

{self._generate_performance_test_suggestions(module)}
"""
        ]
        
        return "\n".join(optimizations)
    
    def _generate_complexity_analysis(self, module: Dict[str, Any]) -> str:
        """Generate complexity analysis"""
        complexity = self._calculate_complexity_metrics(module)
        
        analysis = [
            f"**Overall Complexity**: {complexity['overall_level']}",
            f"**Average Function Complexity**: {complexity['avg_function_complexity']:.2f}",
            f"**High Complexity Functions**: {complexity['high_complexity_functions']}",
            f"**Async Functions**: {complexity['async_functions']}"
        ]
        
        if complexity['high_complexity_functions'] > 0:
            analysis.append("⚠️  High complexity functions may impact performance")
        
        if complexity['async_functions'] > 0:
            analysis.append("⚡ Async functions can improve throughput")
        
        return "\n".join(f"- {item}" for item in analysis)
    
    def _generate_optimization_recommendations(self, module: Dict[str, Any]) -> str:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Check for high complexity functions
        if module.get('functions_info'):
            high_complex_funcs = [f for f in module['functions_info'] if f.get('complexity', 0) > 10]
            if high_complex_funcs:
                recommendations.append("#### High Complexity Functions")
                for func in high_complex_funcs[:3]:
                    recommendations.append(f"- **{func['name']}** (complexity: {func['complexity']}): Consider refactoring")
        
        # Check for potential optimizations
        if module.get('patterns'):
            if any('async' in p for p in module['patterns']):
                recommendations.append("#### Async Optimization")
                recommendations.append("- Consider using async operations for I/O bound tasks")
            
            if any('smart-pointers' in p for p in module['patterns']):
                recommendations.append("#### Memory Optimization")
                recommendations.append("- Use smart pointers to prevent memory leaks")
        
        # General recommendations
        recommendations.extend([
            "#### General Optimizations",
            "- Profile code to identify bottlenecks",
            "- Use appropriate data structures",
            "- Cache frequently accessed data",
            "- Minimize unnecessary object creation"
        ])
        
        return "\n".join(recommendations)
    
    def _generate_performance_test_suggestions(self, module: Dict[str, Any]) -> str:
        """Generate performance test suggestions"""
        tests = [
            "#### Performance Testing Strategy",
            "- Benchmark critical functions",
            "- Memory usage analysis",
            "- Profile application under load",
            "- Compare performance before and after optimizations"
        ]
        
        if module['language'] == 'python':
            tests.extend([
                "- Use timeit for micro-benchmarks",
                "- Consider cProfile for profiling",
                "- Use memory_profiler for memory analysis"
            ])
        elif module['language'] in ['javascript', 'typescript']:
            tests.extend([
                "- Use Chrome DevTools for profiling",
                "- Implement benchmarking with benchmark.js",
                "- Use Lighthouse for web performance"
            ])
        elif module['language'] == 'cpp':
            tests.extend([
                "- Use Google Benchmark",
                "- Implement custom timing utilities",
                "- Profile with gprof or Valgrind"
            ])
        
        return "\n".join(f"- {item}" for item in tests)
    
    def _generate_error_handling_patterns(self, module: Dict[str, Any]) -> str:
        """Generate error handling patterns"""
        patterns = [
            f"""## Error Handling Patterns

### Common Error Types

{self._identify_error_types(module)}

### Error Handling Best Practices

{self._generate_error_handling_practices(module)}

### Error Handling Examples

{self._generate_error_handling_examples(module)}
"""
        ]
        
        return "\n".join(patterns)
    
    def _identify_error_types(self, module: Dict[str, Any]) -> str:
        """Identify common error types in the module"""
        error_types = [
            "#### Runtime Errors",
            "- Null/undefined reference errors",
            "- Type mismatches",
            "- Resource not found errors",
            "- Permission denied errors",
            "- Network connectivity errors"
        ]
        
        # Language-specific error types
        if module['language'] == 'python':
            error_types.extend([
                "#### Python-specific Errors",
                "- ImportError/ModuleNotFoundError",
                "- AttributeError",
                "- KeyError/ValueError",
                "- IOError/OSError"
            ])
        elif module['language'] in ['javascript', 'typescript']:
            error_types.extend([
                "#### JavaScript/TypeScript Errors",
                "- ReferenceError",
                "- TypeError",
                "- RangeError",
                "- NetworkError"
            ])
        elif module['language'] == 'cpp':
            error_types.extend([
                "#### C++ Errors",
                "- Memory access violations",
                "- Container bounds errors",
                "- Resource allocation failures",
                "- System call failures"
            ])
        
        return "\n".join(error_types)
    
    def _generate_error_handling_practices(self, module: Dict[str, Any]) -> str:
        """Generate error handling best practices"""
        practices = [
            "#### Best Practices",
            "- Validate inputs before processing",
            "- Use appropriate exception types",
            "- Provide meaningful error messages",
            "- Log errors for debugging",
            "- Implement graceful degradation",
            "- Avoid catching exceptions without handling"
        ]
        
        # Language-specific practices
        if module['language'] == 'python':
            practices.extend([
                "- Use custom exception classes for domain-specific errors",
                "- Prefer context managers for resource cleanup",
                "- Use `try-except-else-finally` blocks properly"
            ])
        elif module['language'] in ['javascript', 'typescript']:
            practices.extend([
                "- Use Promise rejection for async errors",
                "- Implement proper error boundaries in React",
                "- Use async/await with proper error handling"
            ])
        elif module['language'] == 'cpp':
            practices.extend([
                "- Use RAII for resource management",
                "- Prefer exceptions over error codes for exceptional cases",
                "- Validate pointers before dereferencing"
            ])
        
        return "\n".join(f"- {item}" for item in practices)
    
    def _generate_error_handling_examples(self, module: Dict[str, Any]) -> str:
        """Generate error handling examples"""
        lang = module['language']
        
        examples = [
            f"```{lang}",
            "# Enhanced error handling examples"
        ]
        
        if module['language'] == 'python':
            examples.extend([
                "# Example with comprehensive error handling",
                "def safe_function(param):",
                "    try:",
                "        # Validate input",
                "        if param is None:",
                "            raise ValueError('Parameter cannot be None')",
                "        ",
                "        # Process with error handling",
                "        result = process_data(param)",
                "        return result",
                "    except ValueError as ve:",
                "        logger.error(f'Validation error: {ve}')",
                "        raise",
                "    except Exception as e:",
                "        logger.error(f'Unexpected error: {e}')",
                "        raise CustomError('Processing failed') from e"
            ])
        elif module['language'] in ['javascript', 'typescript']:
            examples.extend([
                "// Example with async error handling",
                "async function safeAsyncOperation(data) {",
                "    try {",
                "        // Validate input",
                "        if (!data) {",
                "            throw new Error('Data is required');",
                "        }",
                "        ",
                "        // Execute async operation",
                "        const result = await fetchWithRetry(data);",
                "        return result;",
                "    } catch (error) {",
                "        logger.error('Async operation failed:', error);",
                "        throw new CustomError('Operation failed');",
                "    }",
                "}"
            ])
        elif module['language'] == 'cpp':
            examples.extend([
                "// Example with RAII and error handling",
                "void safeOperation() {",
                "    try {",
                "        // Resource management with RAII",
                "        std::unique_ptr<Resource> resource = createResource();",
                "        ",
                "        // Process with error checking",
                "        if (!resource->isValid()) {",
                "            throw std::runtime_error('Invalid resource');",
                "        }",
                "        ",
                "        // Perform operation",
                "        performOperation(*resource);",
                "    } catch (const std::exception& e) {",
                "        std::cerr << 'Error: ' << e.what() << std::endl;",
                "        throw;",
                "    }",
                "}"
            ])
        
        examples.append("```")
        return "\n".join(examples)
    
    def _generate_enhanced_dependencies(self, module: Dict[str, Any]) -> str:
        """Generate enhanced dependencies section"""
        imports = module.get('imports', [])
        dependencies = module.get('dependencies', set())
        
        if not imports and not dependencies:
            return ""
        
        sections = [
            f"""## Enhanced Dependencies

### Direct Dependencies

{self._generate_direct_dependencies(imports)}

### Indirect Dependencies

{self._generate_indirect_dependencies(dependencies)}

### Dependency Management

{self._generate_dependency_management(module)}
"""
        ]
        
        return "\n".join(sections)
    
    def _generate_direct_dependencies(self, imports: List[str]) -> str:
        """Generate direct dependencies list"""
        if not imports:
            return "No direct dependencies identified."
        
        deps = []
        for imp in imports[:10]:  # Top 10 dependencies
            deps.append(f"- `{imp}`")
        
        if len(imports) > 10:
            deps.append(f"... and {len(imports) - 10} more dependencies")
        
        return "\n".join(deps)
    
    def _generate_indirect_dependencies(self, dependencies: set) -> str:
        """Generate indirect dependencies list"""
        if not dependencies:
            return "No indirect dependencies identified."
        
        return "\n".join(f"- `{dep}`" for dep in list(dependencies)[:10])
    
    def _generate_dependency_management(self, module: Dict[str, Any]) -> str:
        """Generate dependency management guidance"""
        guidance = [
            "#### Management Best Practices",
            "- Regularly update dependencies to get security patches",
            "- Use dependency locking for reproducible builds",
            "- Monitor for security vulnerabilities in dependencies",
            "- Consider dependency deduplication",
            "- Implement proper versioning strategy"
        ]
        
        # Language-specific guidance
        if module['language'] == 'python':
            guidance.extend([
                "- Use pipenv or poetry for dependency management",
                "- Consider virtual environments for isolation",
                "- Review dependency conflicts"
            ])
        elif module['language'] in ['javascript', 'typescript']:
            guidance.extend([
                "- Use npm or yarn for dependency management",
                "- Implement semantic versioning",
                "- Consider dependency pruning"
            ])
        elif module['language'] == 'cpp':
            guidance.extend([
                "- Use package managers like Conan or vcpkg",
                "- Consider CMake dependency management",
                "- Implement build-time dependency validation"
            ])
        
        return "\n".join(f"- {item}" for item in guidance)
    
    def _generate_enhanced_usage_guide(self, module: Dict[str, Any], complexity: Dict[str, Any]) -> str:
        """Generate enhanced usage guide"""
        return f"""## Enhanced Usage Guide

### When to Use This Skill

This skill is designed to help you work effectively with the **{module['name']}** module. Use it when:

- Developing new features or modifying existing functionality
- Debugging issues and understanding error patterns
- Refactoring code to improve performance or maintainability
- Writing tests and ensuring code quality
- Understanding the module's architecture and best practices

### Skill Level Recommendations

**Beginner**: Focus on basic usage and API documentation  
**Intermediate**: Study patterns and best practices  
**Advanced**: Dive into performance optimization and complex scenarios

### Complexity-Specific Guidance

Since this module has **{complexity['overall_level']}** complexity:
{self._generate_complexity_guidance(complexity)}

### Best Practices

{self._generate_best_practices(module)}

### Common Tasks and Workflows

{self._generate_workflows(module)}
"""
    
    def _generate_complexity_guidance(self, complexity: Dict[str, Any]) -> str:
        """Generate complexity-specific guidance"""
        guidance = []
        
        if complexity['overall_level'] == 'complex':
            guidance.extend([
                "🎯 **Focus Areas**:",
                "- Start with small, focused changes",
                "- Understand the high-level architecture first",
                "- Use debugging tools extensively",
                "- Consider refactoring high-complexity functions",
                "- Write comprehensive tests before making changes"
            ])
        elif complexity['overall_level'] == 'moderate':
            guidance.extend([
                "🎯 **Focus Areas**:",
                "- Understand key patterns and conventions",
                "- Focus on specific areas rather than the whole module",
                "- Use existing code as reference for new features",
                "- Test changes thoroughly"
            ])
        else:  # simple
            guidance.extend([
                "🎯 **Focus Areas**:",
                "- Easy to modify and extend",
                "- Good for learning the codebase",
                "- Quick to iterate and experiment"
            ])
        
        return "\n".join(f"  {item}" for item in guidance)
    
    def _generate_best_practices(self, module: Dict[str, Any]) -> str:
        """Generate best practices"""
        practices = [
            "#### Coding Practices",
            "- Follow established naming conventions",
            "- Maintain consistent code style",
            "- Write clear and maintainable code",
            "- Add appropriate comments for complex logic",
            "- Use meaningful variable and function names"
        ]
        
        # Add language-specific practices
        if module['language'] == 'python':
            practices.extend([
                "#### Python-specific Practices",
                "- Use type hints where appropriate",
                "- Prefer list comprehensions over loops for simple operations",
                "- Use context managers for resource management",
                "- Follow PEP 8 style guidelines"
            ])
        elif module['language'] in ['javascript', 'typescript']:
            practices.extend([
                "#### JavaScript/TypeScript Practices",
                "- Use const and let appropriately",
                "- Prefer async/await over callbacks",
                "- Use arrow functions for callbacks",
                "- Implement proper error handling for async operations"
            ])
        elif module['language'] == 'cpp':
            practices.extend([
                "#### C++ Practices",
                "- Use smart pointers for memory management",
                "- Prefer references to pointers where possible",
                "- Use const correctly for immutability",
                "- Follow RAII principles"
            ])
        
        # Add testing practices
        practices.extend([
            "#### Testing Practices",
            "- Write tests before implementing features (TDD)",
            "- Maintain high test coverage",
            "- Use meaningful test names",
            "- Test edge cases and error conditions",
            "- Mock external dependencies"
        ])
        
        return "\n".join(f"- {item}" for item in practices)
    
    def _generate_workflows(self, module: Dict[str, Any]) -> str:
        """Generate common workflows"""
        workflows = [
            "#### Development Workflow",
            """
1. **Understand Requirements**: Review the task and identify affected components
2. **Analyze Existing Code**: Study similar implementations and patterns
3. **Plan Changes**: Design the solution considering edge cases
4. **Implement**: Write clean, well-documented code
5. **Test**: Write unit and integration tests
6. **Review**: Test thoroughly and review for performance impact
7. **Deploy**: Make changes with confidence
""",
            "#### Debugging Workflow",
            """
1. **Reproduce Issue**: Create a minimal test case
2. **Isolate Problem**: Narrow down to specific component/function
3. **Analyze Root Cause**: Use logging and debugging tools
4. **Fix Issue**: Implement targeted solution
5. **Prevent Recurrence**: Add tests and monitoring
6. **Verify Fix**: Ensure issue is resolved
"""
        ]
        
        return "\n".join(workflows)
    
    def _generate_agent_file(self, skill_name: str, module: Dict[str, Any], complexity: Dict[str, Any]):
        """Generate agent file for the skill"""
        agent_content = f"""# {skill_name} Agent

name: {skill_name}-agent
description: Expert agent for {skill_name} module with enhanced capabilities
target: {skill_name}
model: default

skills:
  - ./{skill_name}.md

capabilities:
  - code_analysis
  - debugging
  - performance_optimization
  - testing
  - documentation
  - refactoring

complexity: {complexity['overall_level']}

last_updated: {datetime.now().isoformat()}

# Agent Configuration
---
skills_dir: .claude/skills
output_format: markdown
include_tests: true
include_performance: true
include_error_handling: true
"""
        
        agent_file = self.output_dir / f"{skill_name}-agent.yaml"
        agent_file.write_text(agent_content, encoding='utf-8')
    
    def _normalize_skill_name(self, name: str) -> str:
        """Normalize skill name for file generation"""
        # Replace dots and slashes with hyphens
        normalized = re.sub(r'[./\\]', '-', name)
        # Remove leading/trailing hyphens
        normalized = normalized.strip('-')
        # Ensure it's a valid filename
        normalized = re.sub(r'[^a-zA-Z0-9-]', '', normalized)
        return normalized
    
    def _title_case(self, name: str) -> str:
        """Convert to title case"""
        return ' '.join(word.capitalize() for word in name.replace('-', ' ').split(' '))


def group_title(group_name: str) -> str:
    """Get readable title for pattern group"""
    titles = {
        'classes': 'Class',
        'functions': 'Function',
        'async': 'Asynchronous',
        'general': 'General'
    }
    return titles.get(group_name, group_name.capitalize())


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate enhanced skills from analysis")
    parser.add_argument("analysis", help="Analysis JSON file")
    parser.add_argument("--output", default=".claude/skills", help="Output directory")
    parser.add_argument("--depth", default="detailed", choices=["basic", "detailed", "comprehensive"],
                       help="Skill depth level")
    
    args = parser.parse_args()
    
    generator = EnhancedSkillGenerator(args.analysis, args.output)
    generator.generate_all_skills(args.depth)


if __name__ == "__main__":
    main()