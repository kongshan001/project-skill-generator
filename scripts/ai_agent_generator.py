#!/usr/bin/env python3
"""
AI驱动的Agent生成器
使用 LLM 生成高质量的领域专家Agent
"""

import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class AIAgentGenerator:
    """AI驱动的Agent生成器"""
    
    def __init__(self, analysis_file: str, output_dir: str, ai_backend: str = 'auto'):
        self.analysis_file = Path(analysis_file)
        self.output_dir = Path(output_dir)
        
        with open(self.analysis_file, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        
        # 导入AI客户端
        sys.path.insert(0, str(Path(__file__).parent))
        from ai_skill_generator import AIClient, AIContextPreparer
        
        self.ai_client = AIClient(backend=ai_backend)
        self.context_preparer = AIContextPreparer(self.analysis)
    
    def generate_agent_prompt(self, domain: str, modules: List[str], context: Dict) -> str:
        """生成Agent创建提示词"""
        
        modules_info = []
        for module in modules:
            module_data = self.analysis['modules'].get(module, {})
            modules_info.append(f"""
### 模块: {module}
- 文件数: {module_data.get('file_count', 0)}
- 主要类: {', '.join(module_data.get('key_classes', []))}
- 主要函数: {', '.join(module_data.get('key_functions', []))}
""")
        
        prompt = f"""
你是一位专业的软件架构师，现在需要创建一个领域专家Agent配置。

## 项目背景
项目名称: {self.analysis.get('project_name', 'Unknown')}
项目类型: {self.analysis.get('project_type', 'Unknown')}
主要语言: {self.analysis.get('languages', [])}

## 领域信息
领域名称: {domain}
负责模块:
{''.join(modules_info)}

## 任务要求

请为这个领域创建一个专家Agent，生成YAML格式的配置文件，包含以下内容：

### 1. 基本信息
- name: 专家名称（中文，专业且易懂）
- level: 等级（junior/mid/senior，默认senior）
- experience: 经验描述（如"10+年{domain}领域经验"）

### 2. 技能列表 (skills)
- 列出这个专家应该掌握的所有技能
- 技能名称要具体且有实际意义
- 基于提供的模块信息推断

### 3. 能力描述 (capabilities)
- 这个专家能做什么？
- 5-10个具体的能力
- 要与领域高度相关

### 4. 约束条件 (constraints)
- 这个专家的工作边界是什么？
- 应该遵循哪些原则？
- 5-10个明确的约束

### 5. 工作原则 (principles)
- 这个领域的最佳实践
- 应该避免的反模式
- 代码质量要求

### 6. 协作说明 (collaboration)
- 这个专家需要与哪些其他专家协作？
- 在团队中的角色是什么？

请用中文撰写，确保内容专业、实用且易于理解。

输出格式：
```yaml
name: ...
level: ...
experience: ...

skills:
  - ...
  
capabilities:
  - ...
  
constraints:
  - ...
  
principles:
  - ...
  
collaboration:
  works_with: [...]
  role: ...
```
"""
        return prompt
    
    def generate_all_agents(self):
        """生成所有领域专家"""
        # 1. 分析模块，识别领域
        domains = self._identify_domains()
        
        print(f"🔍 识别到 {len(domains)} 个领域")
        for domain, modules in domains.items():
            print(f"   - {domain}: {len(modules)} 个模块")
        print()
        
        # 2. 为每个领域生成专家
        for domain, modules in domains.items():
            print(f"🤖 生成专家: {domain}")
            self.generate_agent(domain, modules)
            print()
        
        # 3. 生成团队配置
        print("👥 生成团队配置...")
        self.generate_team_config(domains)
    
    def _identify_domains(self) -> Dict[str, List[str]]:
        """识别领域并分组模块"""
        # 使用AI来识别领域（更智能）
        prompt = self._generate_domain_analysis_prompt()
        
        try:
            result = self.ai_client.generate(prompt)
            # 解析AI返回的领域分组
            domains = self._parse_domain_result(result)
        except:
            # 降级：使用规则引擎
            domains = self._fallback_domain_identification()
        
        return domains
    
    def _generate_domain_analysis_prompt(self) -> str:
        """生成领域分析提示词"""
        modules_info = []
        for module_name, module_data in self.analysis.get('modules', {}).items():
            modules_info.append(f"- {module_name}: {module_data.get('description', '无描述')}")
        
        prompt = f"""
分析以下模块，将它们分组到合适的领域。

模块列表:
{chr(10).join(modules_info)}

请按以下格式输出领域分组：
```
领域名称: 模块1, 模块2, 模块3
领域名称: 模块4, 模块5
...
```

要求：
1. 领域名称要专业且易懂（中文）
2. 相关性强的模块应该分到同一个领域
3. 每个领域建议3-7个模块
4. 如果模块太多，可以创建子领域
"""
        return prompt
    
    def _parse_domain_result(self, result: str) -> Dict[str, List[str]]:
        """解析AI返回的领域分组"""
        domains = {}
        
        for line in result.split('\n'):
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    domain = parts[0].strip()
                    modules = [m.strip() for m in parts[1].split(',')]
                    if domain and modules:
                        domains[domain] = modules
        
        # 验证模块是否存在
        all_modules = set(self.analysis.get('modules', {}).keys())
        validated_domains = {}
        
        for domain, modules in domains.items():
            valid_modules = [m for m in modules if m in all_modules]
            if valid_modules:
                validated_domains[domain] = valid_modules
        
        return validated_domains if validated_domains else self._fallback_domain_identification()
    
    def _fallback_domain_identification(self) -> Dict[str, List[str]]:
        """降级：基于规则的领域识别"""
        # 这里可以集成原有的领域识别逻辑
        # 简化版：按模块名称前缀分组
        domains = {}
        
        for module_name in self.analysis.get('modules', {}).keys():
            # 简单的前缀分组
            parts = module_name.split('-')
            if len(parts) > 1:
                domain = parts[0]
            else:
                domain = 'core'
            
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(module_name)
        
        return domains
    
    def generate_agent(self, domain: str, modules: List[str]):
        """生成单个领域专家"""
        # 1. 准备上下文
        context = {
            'domain': domain,
            'modules': modules,
            'project_info': {
                'name': self.analysis.get('project_name'),
                'type': self.analysis.get('project_type'),
                'languages': self.analysis.get('languages', [])
            }
        }
        
        # 2. 生成提示词
        prompt = self.generate_agent_prompt(domain, modules, context)
        
        # 3. 调用AI生成
        agent_content = self.ai_client.generate(prompt)
        
        # 4. 提取YAML内容
        yaml_content = self._extract_yaml(agent_content)
        
        # 5. 添加元数据
        full_yaml = f"""# {domain} 领域专家配置
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 生成方式: AI ({self.ai_client.backend})
# 负责模块: {', '.join(modules)}

{yaml_content}
"""
        
        # 6. 保存文件
        agent_file = self.output_dir / f"{self._sanitize_name(domain)}-expert.yaml"
        agent_file.parent.mkdir(parents=True, exist_ok=True)
        agent_file.write_text(full_yaml, encoding='utf-8')
        
        print(f"   ✅ 已保存到: {agent_file}")
        
        # 7. 保存提示词（调试用）
        prompt_file = self.output_dir / f"{self._sanitize_name(domain)}-expert-prompt.md"
        prompt_file.write_text(prompt, encoding='utf-8')
        print(f"   📄 提示词: {prompt_file}")
    
    def _extract_yaml(self, content: str) -> str:
        """从AI返回中提取YAML内容"""
        # 查找 ```yaml ... ``` 块
        if '```yaml' in content:
            start = content.find('```yaml') + 7
            end = content.find('```', start)
            return content[start:end].strip()
        elif '```' in content:
            start = content.find('```') + 3
            end = content.find('```', start)
            return content[start:end].strip()
        else:
            # 假设整个内容就是YAML
            return content
    
    def _sanitize_name(self, name: str) -> str:
        """清理名称用于文件名"""
        return name.lower().replace(' ', '-').replace('/', '-')
    
    def generate_team_config(self, domains: Dict[str, List[str]]):
        """生成团队配置"""
        team_config = {
            'name': f"{self.analysis.get('project_name', 'Project')} Expert Team",
            'description': 'AI生成的专家团队配置',
            'generated_at': datetime.now().isoformat(),
            'generated_by': f'ai-{self.ai_client.backend}',
            'agents': [],
            'workflow': []
        }
        
        # 添加所有专家
        for domain in domains.keys():
            team_config['agents'].append(f"{self._sanitize_name(domain)}-expert")
        
        # 生成简单的工作流
        team_config['workflow'] = [
            {
                'step': i+1,
                'agent': agent,
                'task': f'分析和优化{domain}相关代码'
            }
            for i, (domain, agent) in enumerate(zip(domains.keys(), team_config['agents']))
        ]
        
        # 保存团队配置
        team_file = self.output_dir / 'team.yaml'
        team_file.write_text(yaml.dump(team_config, allow_unicode=True, default_flow_style=False), 
                            encoding='utf-8')
        print(f"   ✅ 团队配置: {team_file}")


def main():
    parser = argparse.ArgumentParser(
        description='AI驱动的Agent生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 自动生成所有专家
  %(prog)s analysis.json --output .claude/agents/
  
  # 指定AI后端
  %(prog)s analysis.json --output .claude/agents/ --ai claude-code
  
  # 只生成特定领域的专家
  %(prog)s analysis.json --output .claude/agents/ --domain authentication
        """
    )
    
    parser.add_argument('analysis', help='分析结果文件 (JSON)')
    parser.add_argument('--output', '-o', required=True, 
                       help='输出目录')
    parser.add_argument('--ai', default='auto',
                       choices=['auto', 'claude-code', 'openai', 'anthropic', 'mock'],
                       help='AI后端选择 (默认: auto)')
    parser.add_argument('--domain', help='只生成指定领域的专家')
    
    args = parser.parse_args()
    
    generator = AIAgentGenerator(
        analysis_file=args.analysis,
        output_dir=args.output,
        ai_backend=args.ai
    )
    
    if args.domain:
        # 只生成指定领域的专家
        modules = []  # 需要从分析结果中提取
        generator.generate_agent(args.domain, modules)
    else:
        generator.generate_all_agents()
    
    print("\n✅ Agent生成完成！")


if __name__ == '__main__':
    main()
