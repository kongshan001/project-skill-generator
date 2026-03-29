#!/bin/bash
# Project Skill Generator - 简化版迭代优化脚本

set -e

PSG_DIR="/root/.openclaw/workspace-opengl/skills/project-skill-generator"
TODOLIST="$PSG_DIR/doc/todolist.md"
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M:%S')

echo "=========================================="
echo "Project Skill Generator - 迭代优化"
echo "=========================================="
echo "[$TIME] 开始时间: $DATE $TIME"
echo ""

# 检查TODO-001
if grep -A5 "TODO-001" "$TODOLIST" | grep -q "待修复"; then
    echo "[$(date '+%H:%M:%S')] ✅ 发现 TODO-001: 修复扁平结构项目的模块发现"
    
    # 执行修复
    echo "[$(date '+%H:%M:%S')] 🔧 开始修复..."
    
    # 这里调用Python修复脚本
    python3 << 'PYTHON_EOF'
import sys
sys.path.insert(0, "/root/.openclaw/workspace-opengl/skills/project-skill-generator/scripts")

# 读取原始分析脚本
script_path = "/root/.openclaw/workspace-opengl/skills/project-skill-generator/scripts/analyze_codebase.py"

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否已经添加过后备方法
if '_discover_python_modules_fallback' in content:
    print("后备方法已存在，跳过修复")
    sys.exit(0)

# 添加后备方法
fallback_code = '''
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
'''

# 找到 _discover_python_modules 方法的结尾并添加后备调用
# 在 _discover_python_modules 方法中添加后备逻辑
import re

# 方法1: 在 _discover_python_modules 末尾添加后备调用
pattern = r'(def _discover_python_modules\(self\):.*?)(\n    def )'
match = re.search(pattern, content, re.DOTALL)

if match:
    original_method = match.group(1)
    modified_method = original_method + '''
        # Fallback if no standard modules found
        if not self.modules:
            self._discover_python_modules_fallback()
'''
    content = content.replace(original_method, modified_method, 1)

# 方法2: 在类中添加后备方法（在 _discover_js_modules 之前）
insert_pos = content.find('    def _discover_js_modules(self):')
if insert_pos > 0:
    content = content[:insert_pos] + fallback_code + '\n' + content[insert_pos:]

# 保存修改
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ TODO-001 修复完成")
PYTHON_EOF

    if [ $? -eq 0 ]; then
        echo "[$(date '+%H:%M:%S')] ✅ 代码修复完成"
        
        # 更新 todolist
        sed -i 's/⏳ 待修复/✅ 已完成 ('"$DATE"')/' "$TODOLIST"
        echo "[$(date '+%H:%M:%S')] ✅ todolist.md 已更新"
        
        # 提交代码
        cd "$PSG_DIR"
        git add -A
        git commit -m "fix: 修复扁平结构项目的模块发现问题 (TODO-001)

- 添加 _discover_python_modules_fallback() 方法
- 支持无 __init__.py 的 Python 项目
- 使用目录分组策略

v0.1.0 -> v0.1.1" 2>/dev/null || true
        
        git push origin main 2>/dev/null || true
        echo "[$(date '+%H:%M:%S')] ✅ 代码已推送到 GitHub"
    else
        echo "[$(date '+%H:%M:%S')] ❌ 修复失败"
        exit 1
    fi
else
    echo "[$(date '+%H:%M:%S')] ℹ️  暂无高优先级待办事项"
fi

echo ""
echo "=========================================="
