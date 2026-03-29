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
    classes_info: List[Dict[str, Any]] = field(default_factory=list)
    functions_info: List[Dict[str, Any]] = field(default_factory=list)


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
        self.total_files = 0
        self.processed_files = 0
        self.show_progress = True
        
    def _detect_language(self) -> str:
        """Detect primary programming language"""
        extensions = defaultdict(int)
        for file in self.root.rglob("*"):
            if file.is_file():
                ext = file.suffix
                if ext in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp', '.c', '.h', '.hpp', '.sh']:
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
            '.c': 'c',
            '.h': 'cpp',  # Treat header files as C++
            '.hpp': 'cpp',
            '.sh': 'shell'  # Shell scripts
        }
        
        most_common = max(extensions.items(), key=lambda x: x[1])
        return lang_map.get(most_common[0], "unknown")
    
    def _update_progress(self, message=""):
        """Update and display progress"""
        if not self.show_progress:
            return
            
        if self.total_files > 0:
            progress = (self.processed_files / self.total_files) * 100
            bar_length = 40
            filled_length = int(bar_length * progress / 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            if message:
                print(f"\r📊 Progress: [{bar}] {progress:.1f}% ({self.processed_files}/{self.total_files}) - {message}", end='')
            else:
                print(f"\r📊 Progress: [{bar}] {progress:.1f}% ({self.processed_files}/{self.total_files})", end='')
            
            if self.processed_files >= self.total_files:
                print()  # New line when complete
    
    def analyze(self) -> AnalysisResult:
        """Run full analysis"""
        print(f"🔍 Analyzing codebase: {self.root}")
        print(f"   Language: {self.language}")
        print(f"   Depth: {self.depth}")
        
        # Step 1: Discover modules
        print("\n📁 Discovering modules...")
        self._discover_modules()
        print(f"   Found {len(self.modules)} modules")
        
        # Count total files for progress tracking
        self.total_files = sum(len(m.files) for m in self.modules.values())
        self.processed_files = 0
        
        # Step 2: Analyze each module
        print("\n🔬 Analyzing modules...")
        for module_name, module in self.modules.items():
            print(f"   Processing {module_name}...")
            self._analyze_module(module)
            self._update_progress(f"Completed {module_name}")
        
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
        elif self.language == "cpp":
            self._discover_cpp_modules()
        elif self.language == "shell":
            self._discover_shell_modules()
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
    
        # Fallback if no standard modules found
        if not self.modules:
            self._discover_python_modules_fallback()


    def _discover_python_modules_fallback(self):
        """Fallback module discovery for projects without __init__.py"""
        # Group Python files by directory
        dir_files = defaultdict(list)
        
        for py_file in self.root.rglob("*.py"):
            # Skip excluded directories
            if any(skip in str(py_file) for skip in ["venv", "env", "__pycache__", ".git", "node_modules", "build", "dist"]):
                continue
            
            module_path = py_file.parent
            relative = module_path.relative_to(self.root)
            
            # Skip root directory
            if str(relative) == ".":
                module_name = "root"
            else:
                module_name = str(relative).replace(os.sep, ".")
            
            dir_files[module_name].append(str(py_file))
        
        # Create modules from directory groups
        for module_name, files in dir_files.items():
            if files:
                module_path = Path(files[0]).parent
                self.modules[module_name] = ModuleInfo(
                    name=module_name,
                    path=str(module_path),
                    language="python",
                    files=files
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
    
    def _discover_cpp_modules(self):
        """Discover C++ modules based on header/source files"""
        # Look for common C++ project structures
        for root_dir, dirs, files in os.walk(self.root):
            # Skip common build directories
            dirs[:] = [d for d in dirs if not d.startswith(('build', 'dist', 'obj', 'bin', '.git', 'node_modules'))]
            
            root_path = Path(root_dir)
            relative = root_path.relative_to(self.root)
            
            if str(relative) == ".":
                module_name = "root"
            else:
                module_name = str(relative).replace(os.sep, "/")
            
            # Collect C++ files
            cpp_files = []
            for file in files:
                if file.endswith(('.cpp', '.cc', '.cxx', '.c++', '.h', '.hpp', '.hxx')):
                    cpp_files.append(str(root_path / file))
            
            if cpp_files:
                self.modules[module_name] = ModuleInfo(
                    name=module_name,
                    path=str(root_path),
                    language="cpp",
                    files=cpp_files
                )
    
    def _discover_shell_modules(self):
        """Discover Shell script modules"""
        # Group shell scripts by directory
        for shell_file in self.root.rglob("*.sh"):
            module_path = shell_file.parent
            relative = module_path.relative_to(self.root)
            
            # Skip if too deep in nested directories
            if len(relative.parts) > 3:
                continue
            
            if str(relative) == ".":
                module_name = "shell"
            else:
                module_name = f"shell-{str(relative).replace(os.sep, '-')}"
            
            # Collect shell scripts
            shell_files = list(module_path.glob("*.sh"))
            if module_name not in self.modules:
                self.modules[module_name] = ModuleInfo(
                    name=module_name,
                    path=str(module_path),
                    language="shell",
                    files=[str(f) for f in shell_files]
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
            elif self.language == "cpp":
                self._analyze_cpp_file(file_path, module)
            elif self.language == "shell":
                self._analyze_shell_file(file_path, module)
            
            self.processed_files += 1
            self._update_progress()
    
    def _analyze_python_file(self, file_path: str, module: ModuleInfo):
        """Analyze a Python file with enhanced AST analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                print(f"   ⚠️  Syntax error in {file_path}: {e}")
                return
            
            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module.imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module.imports.add(node.module)
            
            # Enhanced analysis for classes and functions
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.ClassDef):
                    # Enhanced class analysis
                    class_info = {
                        'name': node.name,
                        'methods': [],
                        'properties': [],
                        'complexity': 0,
                        'docstring': ast.get_docstring(node),
                        'inheritance': [base.id for base in node.bases] if node.bases else []
                    }
                    
                    # Calculate complexity for class (method counts)
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = self._analyze_function_def(item)
                            class_info['methods'].append(method_info)
                            class_info['complexity'] += method_info['complexity']
                    
                    # Add enhanced class info
                    if hasattr(module, 'classes_info'):
                        module.classes_info.append(class_info)
                    else:
                        module.classes_info = [class_info]
                    
                    module.classes.append(node.name)
                    
                elif isinstance(node, ast.FunctionDef):
                    # Enhanced function analysis
                    func_info = self._analyze_function_def(node)
                    if hasattr(module, 'functions_info'):
                        module.functions_info.append(func_info)
                    else:
                        module.functions_info = [func_info]
                    
                    module.functions.append(node.name)
            
            # Extract patterns
            self._extract_python_patterns(content, module, file_path)
            
        except Exception as e:
            print(f"   ⚠️  Error analyzing {file_path}: {e}")
    
    def _analyze_function_def(self, func_node):
        """Analyze a function definition in detail"""
        complexity = self._calculate_complexity(func_node)
        
        # Extract parameter information
        params = []
        for arg in func_node.args.args:
            param_info = {
                'name': arg.arg,
                'type_annotation': None,
                'default_value': None
            }
            
            # Extract default value (compatible with different Python versions)
            if func_node.args.kw_defaults and hasattr(func_node.args, 'kwonlydefaults'):
                # Python 3.11+ style
                if func_node.args.kwonlydefaults and arg.arg in func_node.args.kwonlydefaults:
                    param_info['default_value'] = func_node.args.kwonlydefaults[arg.arg]
            elif func_node.args.kw_defaults and hasattr(func_node.args, 'kw_defaults'):
                # Older Python versions
                kwonly_args = [arg.arg for arg in func_node.args.kwonlyargs or []]
                if arg.arg in kwonly_args:
                    idx = kwonly_args.index(arg.arg)
                    if idx < len(func_node.args.kw_defaults) and func_node.args.kw_defaults[idx] is not None:
                        param_info['default_value'] = func_node.args.kw_defaults[idx]
            
            # Extract type hints
            if hasattr(func_node.args, 'annotations') and func_node.args.annotations:
                if arg.arg in func_node.args.annotations:
                    param_info['type_annotation'] = self._get_type_annotation(func_node.args.annotations[arg.arg])
            
            params.append(param_info)
        
        # Extract return type
        return_type = None
        if func_node.returns:
            return_type = self._get_type_annotation(func_node.returns)
        
        # Extract function info
        return {
            'name': func_node.name,
            'parameters': params,
            'return_type': return_type,
            'is_async': isinstance(func_node, ast.AsyncFunctionDef),
            'is_generator': any(isinstance(node, ast.Yield) for node in ast.walk(func_node)),
            'complexity': complexity,
            'docstring': ast.get_docstring(func_node),
            'line_count': func_node.end_lineno - func_node.lineno + 1 if hasattr(func_node, 'end_lineno') else 0,
            'call_count': self._count_function_calls(func_node)
        }
    
    def _get_type_annotation(self, annotation_node):
        """Extract type annotation from AST node"""
        if isinstance(annotation_node, ast.Name):
            return annotation_node.id
        elif isinstance(annotation_node, ast.Attribute):
            return f"{annotation_node.value.id}.{annotation_node.attr}"
        elif isinstance(annotation_node, ast.Subscript):
            value = self._get_type_annotation(annotation_node.value)
            slice_str = self._get_type_annotation(annotation_node.slice)
            return f"{value}[{slice_str}]"
        elif isinstance(annotation_node, ast.Constant):
            return str(annotation_node.value)
        else:
            return str(annotation_node)
    
    def _calculate_complexity(self, func_node):
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.With):
                complexity += 1
            elif isinstance(node, ast.comprehension):
                complexity += 1
        
        return complexity
    
    def _count_function_calls(self, func_node):
        """Count function calls within this function"""
        call_count = 0
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                call_count += 1
        
        return call_count
    
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
    
    def _analyze_cpp_file(self, file_path: str, module: ModuleInfo):
        """Analyze a C++ file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract includes
            include_pattern = r'#include\s*[<"]([^>"]+)[>"]'
            for match in re.finditer(include_pattern, content):
                module.imports.add(match.group(1))
            
            # Extract class definitions
            class_pattern = r'class\s+(\w+)\s*[{:;]'
            for match in re.finditer(class_pattern, content):
                module.classes.append(match.group(1))
            
            # Extract function definitions
            try:
                func_pattern = r'(?:static\s+)?(?:inline\s+)?(?:template\s+[^{]*\s+)?(?:[\w:*&<>\s]+)?\s+(\w+)\s*\([^)]*\)\s*(?:const|volatile|noexcept|override|final)?\s*[;{]'
                for match in re.finditer(func_pattern, content):
                    func_name = match.group(1)
                    # Avoid mistaking classes as functions
                    if func_name not in module.classes:
                        module.functions.append(func_name)
            except Exception as e:
                print(f"   ⚠️  正则表达式解析错误: {e}")
            
            # Extract patterns
            self._extract_cpp_patterns(content, module, file_path)
            
        except Exception as e:
            print(f"   ⚠️  Error analyzing {file_path}: {e}")
    
    def _analyze_shell_file(self, file_path: str, module: ModuleInfo):
        """Analyze a Shell script file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract source (similar to imports)
            source_pattern = r'source\s+["\']([^"\']+)["\']'
            for match in re.finditer(source_pattern, content):
                module.imports.add(match.group(1))
            
            # Extract function definitions
            func_pattern = r'(\w+)\s*\(\s*\)\s*\{'
            for match in re.finditer(func_pattern, content):
                module.functions.append(match.group(1))
            
            # Extract variables (common global variables)
            var_pattern = r'export\s+(\w+)'
            for match in re.finditer(var_pattern, content):
                module.exports.append(match.group(1))
            
            # Extract patterns
            self._extract_shell_patterns(content, module, file_path)
            
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
    
    def _extract_cpp_patterns(self, content: str, module: ModuleInfo, file_path: str):
        """Extract C++-specific patterns"""
        patterns_found = []
        
        # Smart pointers
        if 'std::unique_ptr' in content or 'std::shared_ptr' in content:
            patterns_found.append("smart-pointers")
        
        # STL containers
        if any(container in content for container in ['std::vector', 'std::map', 'std::list', 'std::string']):
            patterns_found.append("stl-containers")
        
        # Templates
        if 'template' in content:
            patterns_found.append("templates")
        
        # RAII patterns
        if 'explicit' in content and 'constructor' in content:
            patterns_found.append("raii")
        
        # Exception handling
        if 'try' in content and 'catch' in content:
            patterns_found.append("exception-handling")
        
        # Virtual functions
        if 'virtual' in content:
            patterns_found.append("virtual-functions")
        
        # Const correctness
        if content.count('const') > 5:
            patterns_found.append("const-correctness")
        
        module.patterns.extend(patterns_found)
        
        # Add to global patterns
        for pattern in patterns_found:
            if pattern not in self.patterns:
                self.patterns[pattern] = CodePattern(
                    name=pattern,
                    description=f"C++ {pattern}",
                    examples=[],
                    frequency=0,
                    files=[]
                )
            self.patterns[pattern].frequency += 1
            if file_path not in self.patterns[pattern].files:
                self.patterns[pattern].files.append(file_path)
    
    def _extract_shell_patterns(self, content: str, module: ModuleInfo, file_path: str):
        """Extract Shell-specific patterns"""
        patterns_found = []
        
        # Functions
        if 'function' in content or re.search(r'\w+\(\)\s*\{', content):
            patterns_found.append("shell-functions")
        
        # Environment variables
        if re.search(r'\$\w+', content):
            patterns_found.append("env-variables")
        
        # Command piping
        if '|' in content:
            patterns_found.append("pipe-commands")
        
        # Conditional blocks
        if 'if ' in content and 'fi' in content:
            patterns_found.append("conditionals")
        
        # Loops
        if 'for ' in content or 'while ' in content:
            patterns_found.append("loops")
        
        # Error handling
        if 'set -e' in content or 'trap' in content:
            patterns_found.append("error-handling")
        
        # Process substitution
        if '<(' in content or '>' in content:
            patterns_found.append("process-substitution")
        
        module.patterns.extend(patterns_found)
        
        # Add to global patterns
        for pattern in patterns_found:
            if pattern not in self.patterns:
                self.patterns[pattern] = CodePattern(
                    name=pattern,
                    description=f"Shell {pattern}",
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
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress all output except errors")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bar display")
    
    args = parser.parse_args()
    
    # Setup logging
    if args.quiet:
        quiet = True
        verbose = False
    else:
        quiet = False
        verbose = args.verbose
    
    def log(message, level="info"):
        """Conditional logging based on verbosity and quiet flags"""
        if quiet:
            return
        
        if level == "error":
            print(f"❌ {message}")
        elif level == "warning":
            print(f"⚠️  {message}")
        elif level == "success":
            print(f"✅ {message}")
        elif verbose:
            print(f"🔍 {message}")
        else:
            print(f"   {message}")
    
    try:
        # Validate codebase path
        codebase_path = Path(args.codebase_path).resolve()
        if not codebase_path.exists():
            raise FileNotFoundError(f"Codebase path does not exist: {codebase_path}")
        
        if not codebase_path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {codebase_path}")
        
        log(f"Analyzing codebase: {codebase_path}", "info")
        
        # Run analysis
        analyzer = CodebaseAnalyzer(str(codebase_path), depth=args.depth)
        analyzer.show_progress = not args.no_progress
        result = analyzer.analyze()
        
    except FileNotFoundError as e:
        log(f"Path not found: {e}", "error")
        log("Please provide a valid path to your codebase directory.", "warning")
        sys.exit(1)
        
    except NotADirectoryError as e:
        log(f"Invalid path: {e}", "error")
        log("The specified path must be a directory.", "warning")
        sys.exit(1)
        
    except KeyboardInterrupt:
        log("\nAnalysis interrupted by user.", "warning")
        sys.exit(130)
        
    except Exception as e:
        log(f"Unexpected error during analysis: {e}", "error")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    # Convert to dict for JSON serialization and handle sets
    result_dict = asdict(result)
    
    # Convert sets to lists for JSON serialization
    def convert_sets_to_lists(obj):
        if isinstance(obj, dict):
            return {k: convert_sets_to_lists(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_sets_to_lists(item) for item in obj]
        elif isinstance(obj, set):
            return list(obj)
        else:
            return obj
    
    # Convert sets to lists
    result_dict_converted = convert_sets_to_lists(result_dict)
    
    # Save to file
    output_path = Path(args.output)
    output_path.write_text(json.dumps(result_dict_converted, indent=2, ensure_ascii=False))
    print(f"\n💾 Results saved to: {output_path}")


if __name__ == "__main__":
    main()
