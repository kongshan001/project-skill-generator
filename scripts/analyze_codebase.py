#!/usr/bin/env python3
"""
Codebase Analyzer - Deep analysis of code structure, patterns, and domain knowledge

Usage:
    analyze_codebase.py <codebase-path> [options]

Options:
    --output FILE         Output JSON file (default: analysis.json)
    --depth LEVEL         Analysis depth: quick, standard, deep (default: standard)
    --modules LIST        Comma-separated modules to analyze (default: auto-detect)
    --exclude LIST        Comma-separated patterns to exclude
    --language LANG       Primary language (default: auto-detect)
"""

import argparse
import ast
import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
import sys


@dataclass
class ModuleInfo:
    """Information about a code module"""
    name: str
    path: str
    language: str
    files: List[str] = field(default_factory=list)
    imports: Set[str] = field(default_factory=set)
    exports: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    patterns: List[str] = field(default_factory=list)
    domain_knowledge: List[str] = field(default_factory=list)
    conventions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CodePattern:
    """Detected code pattern"""
    name: str
    description: str
    examples: List[str]
    frequency: int
    files: List[str]


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    codebase_path: str
    language: str
    total_files: int
    total_lines: int
    modules: List[ModuleInfo]
    patterns: List[CodePattern]
    architecture: str
    entry_points: List[str]
    public_apis: Dict[str, List[str]]
    dependencies: Dict[str, List[str]]
    conventions: Dict[str, Any]
    domain_knowledge: List[str]


class CodebaseAnalyzer:
    """Main analyzer class"""
    
    def __init__(self, codebase_path: str, depth: str = "standard"):
        self.root = Path(codebase_path).resolve()
        self.depth = depth
        self.modules: Dict[str, ModuleInfo] = {}
        self.patterns: Dict[str, CodePattern] = {}
        self.language = self._detect_language()
        
    def _detect_language(self) -> str:
        """Detect primary programming language"""
        extensions = defaultdict(int)
        for file in self.root.rglob("*"):
            if file.is_file():
                ext = file.suffix
                if ext in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp', '.c']:
                    extensions[ext] += 1
        
        if not extensions:
            return "unknown"
        
        # Map extensions to language
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c'
        }
        
        most_common = max(extensions.items(), key=lambda x: x[1])
        return lang_map.get(most_common[0], "unknown")
    
    def analyze(self) -> AnalysisResult:
        """Run full analysis"""
        print(f"🔍 Analyzing codebase: {self.root}")
        print(f"   Language: {self.language}")
        print(f"   Depth: {self.depth}")
        
        # Step 1: Discover modules
        print("\n📁 Discovering modules...")
        self._discover_modules()
        print(f"   Found {len(self.modules)} modules")
        
        # Step 2: Analyze each module
        print("\n🔬 Analyzing modules...")
        for module_name, module in self.modules.items():
            print(f"   Processing {module_name}...")
            self._analyze_module(module)
        
        # Step 3: Extract patterns
        print("\n🎨 Extracting patterns...")
        self._extract_patterns()
        print(f"   Found {len(self.patterns)} patterns")
        
        # Step 4: Analyze architecture
        print("\n🏗️  Detecting architecture...")
        architecture = self._detect_architecture()
        print(f"   Architecture: {architecture}")
        
        # Step 5: Extract conventions
        print("\n📜 Extracting conventions...")
        conventions = self._extract_conventions()
        
        # Step 6: Gather domain knowledge
        print("\n🧠 Extracting domain knowledge...")
        domain_knowledge = self._extract_domain_knowledge()
        
        # Compile results
        total_files = sum(len(m.files) for m in self.modules.values())
        total_lines = self._count_total_lines()
        
        result = AnalysisResult(
            codebase_path=str(self.root),
            language=self.language,
            total_files=total_files,
            total_lines=total_lines,
            modules=list(self.modules.values()),
            patterns=list(self.patterns.values()),
            architecture=architecture,
            entry_points=self._find_entry_points(),
            public_apis=self._extract_public_apis(),
            dependencies=self._build_dependency_graph(),
            conventions=conventions,
            domain_knowledge=domain_knowledge
        )
        
        print(f"\n✅ Analysis complete!")
        print(f"   Files: {total_files}")
        print(f"   Lines: {total_lines:,}")
        
        return result
    
    def _discover_modules(self):
        """Discover module boundaries"""
        if self.language == "python":
            self._discover_python_modules()
        elif self.language in ["javascript", "typescript"]:
            self._discover_js_modules()
        else:
            self._discover_generic_modules()
    
    def _discover_python_modules(self):
        """Discover Python modules based on __init__.py"""
        for init_file in self.root.rglob("__init__.py"):
            module_path = init_file.parent
            relative = module_path.relative_to(self.root)
            module_name = str(relative).replace(os.sep, ".")
            
            # Skip virtual environments and cache
            if any(skip in module_name for skip in ["venv", "env", "__pycache__", ".git", "node_modules"]):
                continue
            
            # Collect Python files in this module
            py_files = list(module_path.glob("*.py"))
            
            self.modules[module_name] = ModuleInfo(
                name=module_name,
                path=str(module_path),
                language="python",
                files=[str(f) for f in py_files]
            )
    
    def _discover_js_modules(self):
        """Discover JavaScript/TypeScript modules"""
        # Look for package.json or index files
        for index_file in self.root.rglob("index.{js,ts,jsx,tsx}"):
            module_path = index_file.parent
            relative = module_path.relative_to(self.root)
            module_name = str(relative).replace(os.sep, "/")
            
            # Skip node_modules
            if "node_modules" in module_name:
                continue
            
            # Collect JS/TS files
            js_files = list(module_path.glob("*.{js,ts,jsx,tsx}"))
            
            self.modules[module_name] = ModuleInfo(
                name=module_name,
                path=str(module_path),
                language=self.language,
                files=[str(f) for f in js_files]
            )
    
    def _discover_generic_modules(self):
        """Discover modules for other languages"""
        # Group by top-level directories
        for item in self.root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                files = list(item.rglob("*"))
                files = [str(f) for f in files if f.is_file()]
                
                self.modules[item.name] = ModuleInfo(
                    name=item.name,
                    path=str(item),
                    language=self.language,
                    files=files
                )
    
    def _analyze_module(self, module: ModuleInfo):
        """Deep analysis of a single module"""
        for file_path in module.files:
            if self.language == "python":
                self._analyze_python_file(file_path, module)
            elif self.language in ["javascript", "typescript"]:
                self._analyze_js_file(file_path, module)
    
    def _analyze_python_file(self, file_path: str, module: ModuleInfo):
        """Analyze a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module.imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module.imports.add(node.module)
            
            # Extract classes and functions
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.ClassDef):
                    module.classes.append(node.name)
                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            module.functions.append(f"{node.name}.{item.name}")
                elif isinstance(node, ast.FunctionDef):
                    module.functions.append(node.name)
            
            # Extract patterns
            self._extract_python_patterns(content, module, file_path)
            
        except Exception as e:
            print(f"   ⚠️  Error analyzing {file_path}: {e}")
    
    def _analyze_js_file(self, file_path: str, module: ModuleInfo):
        """Analyze a JavaScript/TypeScript file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract imports (regex-based for simplicity)
            import_pattern = r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'
            for match in re.finditer(import_pattern, content):
                module.imports.add(match.group(1))
            
            # Extract exports
            export_pattern = r'export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)'
            for match in re.finditer(export_pattern, content):
                module.exports.append(match.group(1))
            
            # Extract classes
            class_pattern = r'class\s+(\w+)'
            for match in re.finditer(class_pattern, content):
                module.classes.append(match.group(1))
            
            # Extract functions
            func_pattern = r'(?:function\s+(\w+)|(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[a-zA-Z_]\w*)\s*=>)'
            for match in re.finditer(func_pattern, content):
                module.functions.append(match.group(1) or match.group(2))
            
            # Extract patterns
            self._extract_js_patterns(content, module, file_path)
            
        except Exception as e:
            print(f"   ⚠️  Error analyzing {file_path}: {e}")
    
    def _extract_python_patterns(self, content: str, module: ModuleInfo, file_path: str):
        """Extract Python-specific patterns"""
        patterns_found = []
        
        # Decorator pattern
        if '@' in content:
            decorator_pattern = r'@(\w+)'
            decorators = re.findall(decorator_pattern, content)
            if decorators:
                patterns_found.append(f"decorators: {', '.join(set(decorators))}")
        
        # Context manager
        if 'with ' in content:
            patterns_found.append("context-manager")
        
        # Async patterns
        if 'async def' in content:
            patterns_found.append("async/await")
        
        # Type hints
        if '-> ' in content or ': ' in content:
            if any(keyword in content for keyword in ['str', 'int', 'List', 'Dict', 'Optional']):
                patterns_found.append("type-hints")
        
        # Data classes
        if '@dataclass' in content:
            patterns_found.append("dataclass")
        
        # Testing patterns
        if 'def test_' in content or 'pytest' in content:
            patterns_found.append("pytest-testing")
        
        module.patterns.extend(patterns_found)
        
        # Add to global patterns
        for pattern in patterns_found:
            if pattern not in self.patterns:
                self.patterns[pattern] = CodePattern(
                    name=pattern,
                    description=f"Usage of {pattern}",
                    examples=[],
                    frequency=0,
                    files=[]
                )
            self.patterns[pattern].frequency += 1
            if file_path not in self.patterns[pattern].files:
                self.patterns[pattern].files.append(file_path)
    
    def _extract_js_patterns(self, content: str, module: ModuleInfo, file_path: str):
        """Extract JavaScript/TypeScript patterns"""
        patterns_found = []
        
        # React hooks
        if 'useState' in content or 'useEffect' in content:
            patterns_found.append("react-hooks")
        
        # Async patterns
        if 'async ' in content or 'await ' in content:
            patterns_found.append("async/await")
        
        # TypeScript features
        if ': ' in content and ('string' in content or 'number' in content):
            patterns_found.append("typescript-types")
        
        # Export patterns
        if 'export default' in content:
            patterns_found.append("default-export")
        
        module.patterns.extend(patterns_found)
        
        # Add to global patterns
        for pattern in patterns_found:
            if pattern not in self.patterns:
                self.patterns[pattern] = CodePattern(
                    name=pattern,
                    description=f"Usage of {pattern}",
                    examples=[],
                    frequency=0,
                    files=[]
                )
            self.patterns[pattern].frequency += 1
            if file_path not in self.patterns[pattern].files:
                self.patterns[pattern].files.append(file_path)
    
    def _extract_patterns(self):
        """Extract code patterns across all modules"""
        # This is called after module analysis
        # Patterns are already extracted in _analyze_module
        pass
    
    def _detect_architecture(self) -> str:
        """Detect architectural pattern"""
        module_names = [m.lower() for m in self.modules.keys()]
        
        # MVC/MVT patterns
        if any('model' in m for m in module_names) and any('view' in m for m in module_names):
            return "MVC"
        
        # Clean architecture
        if any('domain' in m for m in module_names) and any('usecase' in m or 'service' in m for m in module_names):
            return "Clean Architecture"
        
        # Microservices
        if any('service' in m for m in module_names) and len(self.modules) > 5:
            return "Microservices"
        
        # Layered architecture
        if any('api' in m or 'route' in m for m in module_names) and any('db' in m or 'data' in m for m in module_names):
            return "Layered"
        
        # Monolithic
        if len(self.modules) <= 3:
            return "Monolithic"
        
        return "Unknown"
    
    def _find_entry_points(self) -> List[str]:
        """Find application entry points"""
        entry_points = []
        
        # Common entry point files
        entry_files = [
            'main.py', 'app.py', 'run.py', 'server.py',
            'index.js', 'index.ts', 'app.js', 'server.js',
            'main.go', 'main.rs', 'main.cpp'
        ]
        
        for entry in entry_files:
            for file in self.root.rglob(entry):
                relative = file.relative_to(self.root)
                entry_points.append(str(relative))
        
        return entry_points
    
    def _extract_public_apis(self) -> Dict[str, List[str]]:
        """Extract public API endpoints/functions"""
        apis = {}
        
        for module_name, module in self.modules.items():
            # Look for API-like functions
            api_funcs = []
            for func in module.functions:
                if any(keyword in func.lower() for keyword in ['api', 'route', 'endpoint', 'handler', 'view']):
                    api_funcs.append(func)
            
            if api_funcs:
                apis[module_name] = api_funcs
        
        return apis
    
    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build module dependency graph"""
        deps = {}
        
        for module_name, module in self.modules.items():
            module_deps = []
            for imp in module.imports:
                # Check if import is from another module in this project
                for other_module in self.modules:
                    if other_module in imp and other_module != module_name:
                        module_deps.append(other_module)
            
            if module_deps:
                deps[module_name] = list(set(module_deps))
        
        return deps
    
    def _extract_conventions(self) -> Dict[str, Any]:
        """Extract coding conventions"""
        conventions = {
            "naming": {},
            "formatting": {},
            "structure": {}
        }
        
        # Analyze naming conventions
        all_classes = []
        all_functions = []
        
        for module in self.modules.values():
            all_classes.extend(module.classes)
            all_functions.extend(module.functions)
        
        # Class naming
        if all_classes:
            camel_case = sum(1 for c in all_classes if c[0].isupper() and '_' not in c)
            snake_case = sum(1 for c in all_classes if '_' in c)
            
            if camel_case > snake_case:
                conventions["naming"]["classes"] = "PascalCase"
            else:
                conventions["naming"]["classes"] = "snake_case"
        
        # Function naming
        if all_functions:
            snake_case = sum(1 for f in all_functions if '_' in f)
            camel_case = sum(1 for f in all_functions if '_' not in f and f[0].islower())
            
            if snake_case > camel_case:
                conventions["naming"]["functions"] = "snake_case"
            else:
                conventions["naming"]["functions"] = "camelCase"
        
        return conventions
    
    def _extract_domain_knowledge(self) -> List[str]:
        """Extract domain-specific knowledge from code"""
        knowledge = []
        
        # Look for domain-specific terms in comments and docstrings
        for module in self.modules.values():
            for file_path in module.files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract docstrings
                    if self.language == "python":
                        docstrings = re.findall(r'"""(.*?)"""', content, re.DOTALL)
                        docstrings.extend(re.findall(r"'''(.*?)'''", content, re.DOTALL))
                        
                        for doc in docstrings:
                            # Look for domain terms
                            if len(doc) > 50:  # Significant docstring
                                knowledge.append(doc.strip()[:200])
                
                except Exception:
                    pass
        
        # Deduplicate and return top knowledge
        unique_knowledge = list(set(knowledge))
        return unique_knowledge[:20]  # Top 20
    
    def _count_total_lines(self) -> int:
        """Count total lines of code"""
        total = 0
        for module in self.modules.values():
            for file_path in module.files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        total += sum(1 for _ in f)
                except Exception:
                    pass
        return total


def main():
    parser = argparse.ArgumentParser(description="Analyze codebase structure and patterns")
    parser.add_argument("codebase_path", help="Path to codebase root")
    parser.add_argument("--output", default="analysis.json", help="Output JSON file")
    parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard", help="Analysis depth")
    parser.add_argument("--modules", help="Comma-separated modules to analyze")
    parser.add_argument("--exclude", help="Comma-separated patterns to exclude")
    parser.add_argument("--language", help="Primary language (auto-detect if not specified)")
    
    args = parser.parse_args()
    
    # Run analysis
    analyzer = CodebaseAnalyzer(args.codebase_path, depth=args.depth)
    result = analyzer.analyze()
    
    # Convert to dict for JSON serialization
    result_dict = asdict(result)
    
    # Save to file
    output_path = Path(args.output)
    output_path.write_text(json.dumps(result_dict, indent=2, ensure_ascii=False))
    print(f"\n💾 Results saved to: {output_path}")


if __name__ == "__main__":
    main()
