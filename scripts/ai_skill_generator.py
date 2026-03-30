#!/usr/bin/env python3
"""
AI驱动的技能生成器
使用 Claude Code 或其他 LLM API 生成高质量技能
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class AIContextPreparer:
    """为AI准备上下文信息"""
    
    def __init__(self, analysis_data: Dict):
        self.analysis = analysis_data
        
    def prepare_skill_context(self, module_name: str) -> Dict:
        """准备单个模块的技能生成上下文"""
        module_data = self.analysis['modules'].get(module_name, {})
        
        context = {
            'module_name': module_name,
            'file_count': len(module_data.get('files', [])),
            'key_files': self._select_key_files(module_data, max_files=5),
            'api_summary': self._summarize_apis(module_data),
            'dependencies': module_data.get('dependencies', []),
            'code_patterns': self._extract_patterns(module_data),
            'related_modules': self._find_related_modules(module_name)
        }
        
        return context
    
    def _select_key_files(self, module_data: Dict, max_files: int = 5) -> List[Dict]:
        """选择最关键的文件（用于AI理解）"""
        files = module_data.get('files', [])
        
        # 优先级：
        # 1. 包含主要类/函数的文件
        # 2. API 入口文件
        # 3. 配置文件
        # 4. 其他文件
        
        scored_files = []
        for file_info in files:
            score = 0
            file_path = file_info.get('path', '')
            
            # 评分规则
            if 'main' in file_path.lower() or 'index' in file_path.lower():
                score += 10
            if 'api' in file_path.lower() or 'route' in file_path.lower():
                score += 8
            if file_info.get('classes'):
                score += len(file_info['classes']) * 2
            if file_info.get('functions'):
                score += len(file_info['functions'])
                
            scored_files.append((score, file_info))
        
        # 排序并返回前N个
        scored_files.sort(reverse=True, key=lambda x: x[0])
        return [f[1] for f in scored_files[:max_files]]
    
    def _summarize_apis(self, module_data: Dict) -> List[Dict]:
        """总结API信息"""
        apis = []
        
        for file_info in module_data.get('files', []):
            # 提取函数签名
            for func in file_info.get('functions', []):
                apis.append({
                    'name': func.get('name'),
                    'params': func.get('params', []),
                    'docstring': func.get('docstring', ''),
                    'file': file_info.get('path')
                })
            
            # 提取类方法
            for cls in file_info.get('classes', []):
                for method in cls.get('methods', []):
                    apis.append({
                        'name': f"{cls['name']}.{method}",
                        'type': 'method',
                        'class': cls['name'],
                        'file': file_info.get('path')
                    })
        
        return apis[:20]  # 限制数量避免上下文过长
    
    def _extract_patterns(self, module_data: Dict) -> List[str]:
        """提取代码模式（供AI参考）"""
        patterns = []
        
        all_code = ""
        for file_info in module_data.get('files', []):
            # 只提取部分代码示例
            if file_info.get('source_snippet'):
                all_code += file_info['source_snippet'] + "\n"
        
        # 简单的模式识别（AI会做得更好）
        if 'class' in all_code and 'def' in all_code:
            patterns.append("OOP with methods")
        if 'async' in all_code or 'await' in all_code:
            patterns.append("Asynchronous programming")
        if '@' in all_code:
            patterns.append("Decorator/annotation usage")
        
        return patterns
    
    def _find_related_modules(self, module_name: str) -> List[str]:
        """查找相关模块"""
        related = []
        module_data = self.analysis['modules'].get(module_name, {})
        
        # 基于依赖关系
        deps = module_data.get('dependencies', [])
        for dep in deps:
            if dep in self.analysis['modules']:
                related.append(dep)
        
        return related[:3]
    
    def generate_ai_prompt(self, module_name: str, context: Dict) -> str:
        """生成给AI的提示词"""
        
        prompt = f"""# 任务：生成 Claude Code 技能文档

## 模块信息
- **模块名称**: {module_name}
- **文件数量**: {context['file_count']}
- **代码模式**: {', '.join(context['code_patterns']) if context['code_patterns'] else '未识别'}
- **相关模块**: {', '.join(context['related_modules']) if context['related_modules'] else '无'}

## 关键文件
{self._format_key_files(context['key_files'])}

## API 摘要
{self._format_apis(context['api_summary'])}

## 依赖
{', '.join(context['dependencies']) if context['dependencies'] else '无外部依赖'}

## 要求

请生成一份详细的 Claude Code 技能文档，包含以下部分：

### 1. Domain Expertise（领域专业知识）
- 这个模块的核心职责是什么？
- 它解决了什么问题？
- 需要哪些领域知识才能理解和维护这个模块？

### 2. Key APIs（关键 API）
- 列出最重要的 5-10 个 API
- 每个API包含：名称、参数、返回值、使用场景、示例

### 3. Common Patterns（常见模式）
- 这个模块中常用的代码模式
- 最佳实践
- 反模式（应避免的做法）

### 4. Code Conventions（代码规范）
- 命名约定
- 错误处理方式
- 测试要求

### 5. Testing Strategies（测试策略）
- 单元测试重点
- 集成测试建议
- Mock策略

### 6. Performance Considerations（性能考虑）
- 性能瓶颈
- 优化建议
- 缓存策略

请用中文撰写，内容要详细且实用，避免泛泛而谈。
"""
        return prompt
    
    def _format_key_files(self, files: List[Dict]) -> str:
        """格式化关键文件信息"""
        lines = []
        for i, file_info in enumerate(files, 1):
            lines.append(f"\n### 文件 {i}: {file_info.get('path', 'unknown')}")
            
            if file_info.get('classes'):
                lines.append(f"**类**: {', '.join(file_info['classes'])}")
            
            if file_info.get('functions'):
                funcs = [f['name'] if isinstance(f, dict) else f for f in file_info['functions'][:5]]
                lines.append(f"**主要函数**: {', '.join(funcs)}")
        
        return '\n'.join(lines) if lines else "无关键文件"
    
    def _format_apis(self, apis: List[Dict]) -> str:
        """格式化API信息"""
        if not apis:
            return "无API信息"
        
        lines = []
        for i, api in enumerate(apis[:10], 1):
            name = api.get('name', 'unknown')
            params = ', '.join(api.get('params', []))
            doc = api.get('docstring', '')
            
            lines.append(f"{i}. `{name}({params})`")
            if doc:
                lines.append(f"   - {doc[:100]}...")
        
        return '\n'.join(lines)


class AIClient:
    """AI客户端 - 支持多种后端"""
    
    def __init__(self, backend: str = 'auto'):
        self.backend = backend
        self._detect_backend()
    
    def _detect_backend(self):
        """检测可用的AI后端"""
        if self.backend == 'auto':
            # 检测优先级：
            # 1. Claude Code (本地)
            # 2. OpenAI API
            # 3. 其他 LLM API
            
            if self._check_claude_code():
                self.backend = 'claude-code'
            elif self._check_openai():
                self.backend = 'openai'
            elif self._check_anthropic():
                self.backend = 'anthropic'
            else:
                self.backend = 'mock'  # 降级到模板生成
    
    def _check_claude_code(self) -> bool:
        """检查Claude Code是否可用"""
        # 检查是否在Claude Code环境中
        return os.environ.get('CLAUDE_CODE_SESSION') is not None
    
    def _check_openai(self) -> bool:
        """检查OpenAI API是否可用"""
        return os.environ.get('OPENAI_API_KEY') is not None
    
    def _check_anthropic(self) -> bool:
        """检查Anthropic API是否可用"""
        return os.environ.get('ANTHROPIC_API_KEY') is not None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成内容"""
        if self.backend == 'claude-code':
            return self._generate_with_claude_code(prompt, **kwargs)
        elif self.backend == 'openai':
            return self._generate_with_openai(prompt, **kwargs)
        elif self.backend == 'anthropic':
            return self._generate_with_anthropic(prompt, **kwargs)
        else:
            return self._generate_with_template(prompt, **kwargs)
    
    def _generate_with_claude_code(self, prompt: str, **kwargs) -> str:
        """使用Claude Code生成"""
        # 调用Claude Code的skill-creator
        # 这里需要实际的集成代码
        
        # 临时实现：输出到文件，等待Claude Code处理
        prompt_file = Path('/tmp/claude_code_prompt.md')
        prompt_file.write_text(prompt, encoding='utf-8')
        
        return f"""
<!-- Generated by Claude Code -->
# 技能文档

**提示**: 请使用 Claude Code 的 skill-creator 处理以下提示词：
```
{prompt_file}
```

或者手动调用：
```bash
claude-code skill-create --prompt {prompt_file}
```
"""
    
    def _generate_with_openai(self, prompt: str, **kwargs) -> str:
        """使用OpenAI API生成"""
        try:
            import openai
            
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=kwargs.get('model', 'gpt-4'),
                messages=[
                    {"role": "system", "content": "你是专业的技术文档撰写专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API调用失败: {e}")
            return self._generate_with_template(prompt, **kwargs)
    
    def _generate_with_anthropic(self, prompt: str, **kwargs) -> str:
        """使用Anthropic API生成"""
        try:
            import anthropic
            
            client = anthropic.Anthropic()
            message = client.messages.create(
                model=kwargs.get('model', 'claude-3-sonnet-20240229'),
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            print(f"Anthropic API调用失败: {e}")
            return self._generate_with_template(prompt, **kwargs)
    
    def _generate_with_template(self, prompt: str, **kwargs) -> str:
        """降级：使用模板生成"""
        # 这里可以集成原有的模板生成逻辑
        return f"""
<!-- 模板生成（AI不可用） -->
# 技能文档（模板版本）

**注意**: AI服务不可用，使用模板生成。建议配置AI API以获得更好的效果。

{prompt}
"""


class AISkillGenerator:
    """AI驱动的技能生成器"""
    
    def __init__(self, analysis_file: str, output_dir: str, ai_backend: str = 'auto'):
        self.analysis_file = Path(analysis_file)
        self.output_dir = Path(output_dir)
        
        with open(self.analysis_file, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        
        self.context_preparer = AIContextPreparer(self.analysis)
        self.ai_client = AIClient(backend=ai_backend)
    
    def generate_all_skills(self):
        """生成所有模块的技能"""
        modules = self.analysis.get('modules', {})
        
        print(f"🔍 发现 {len(modules)} 个模块")
        print(f"🤖 AI后端: {self.ai_client.backend}")
        print()
        
        for module_name in modules.keys():
            print(f"📝 生成技能: {module_name}")
            self.generate_skill(module_name)
            print()
    
    def generate_skill(self, module_name: str):
        """生成单个技能"""
        # 1. 准备上下文
        context = self.context_preparer.prepare_skill_context(module_name)
        
        # 2. 生成提示词
        prompt = self.context_preparer.generate_ai_prompt(module_name, context)
        
        # 3. 调用AI生成
        skill_content = self.ai_client.generate(prompt)
        
        # 4. 保存技能文档
        skill_dir = self.output_dir / module_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_file = skill_dir / 'SKILL.md'
        
        # 添加元数据
        full_content = f"""---
name: {module_name}
generated_by: ai-{self.ai_client.backend}
generated_at: {datetime.now().isoformat()}
version: 1.0
---

{skill_content}
"""
        
        skill_file.write_text(full_content, encoding='utf-8')
        print(f"   ✅ 已保存到: {skill_file}")
        
        # 5. 保存提示词（用于调试）
        prompt_file = skill_dir / 'PROMPT.md'
        prompt_file.write_text(prompt, encoding='utf-8')
        print(f"   📄 提示词已保存到: {prompt_file}")


def main():
    parser = argparse.ArgumentParser(
        description='AI驱动的技能生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 自动选择AI后端
  %(prog)s analysis.json --output .claude/skills/
  
  # 指定使用Claude Code
  %(prog)s analysis.json --output .claude/skills/ --ai claude-code
  
  # 指定使用OpenAI
  %(prog)s analysis.json --output .claude/skills/ --ai openai
  
  # 只生成特定模块
  %(prog)s analysis.json --output .claude/skills/ --module user-auth
        """
    )
    
    parser.add_argument('analysis', help='分析结果文件 (JSON)')
    parser.add_argument('--output', '-o', required=True, 
                       help='输出目录')
    parser.add_argument('--ai', default='auto',
                       choices=['auto', 'claude-code', 'openai', 'anthropic', 'mock'],
                       help='AI后端选择 (默认: auto)')
    parser.add_argument('--module', help='只生成指定模块的技能')
    
    args = parser.parse_args()
    
    generator = AISkillGenerator(
        analysis_file=args.analysis,
        output_dir=args.output,
        ai_backend=args.ai
    )
    
    if args.module:
        generator.generate_skill(args.module)
    else:
        generator.generate_all_skills()
    
    print("\n✅ 技能生成完成！")


if __name__ == '__main__':
    main()
