#!/usr/bin/env python3
"""
Enhanced Agent Generator - 生成领域专家级 Agent

核心改进：
1. 一对多技能（领域专家）
2. 等级系统（默认资深）
3. 精简但专业
4. 智能分组
"""

import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict


# 领域定义：将细粒度技能映射到领域专家
DOMAIN_EXPERTS = {
    'rendering': {
        'name': 'Rendering Engine Expert',
        'role': 'Senior Rendering Engineer',
        'level': 'senior',
        'experience': '10+ years',
        'keywords': ['2d', '3d', 'render', 'gfx', 'graphic', 'material', 'shader', 'draw', 'sprite', 'mesh', 'texture'],
        'description': '资深渲染引擎专家，精通2D/3D图形渲染、材质系统和着色器编程',
        'capabilities': [
            '设计和实现渲染架构',
            '优化渲染性能（Draw call batching、GPU instancing）',
            '实现自定义渲染管线',
            '处理复杂材质和着色器',
            '跨平台渲染优化',
            '图形API精通（OpenGL/Vulkan/DirectX）'
        ],
        'expertise': [
            'OpenGL/Vulkan/DirectX',
            'Shader编程',
            '渲染管线优化',
            '材质系统设计',
            'GPU性能优化'
        ],
        'focuses_on': ['性能优化', '渲染质量', '跨平台兼容'],
        'avoids': ['过度绘制', '性能回退', '平台特定代码']
    },
    
    'animation': {
        'name': 'Animation System Expert',
        'role': 'Senior Animation Engineer',
        'level': 'senior',
        'experience': '10+ years',
        'keywords': ['anim', 'skeleton', 'bone', 'tween', 'motion', 'frame', 'clip', 'state'],
        'description': '资深动画系统专家，精通骨骼动画、补间动画和动画状态机',
        'capabilities': [
            '实现骨骼动画系统',
            '优化动画性能',
            '设计动画状态机',
            '处理复杂动画混合',
            '实现IK/FK系统'
        ],
        'expertise': [
            '骨骼动画',
            '动画状态机',
            '补间动画',
            '动画混合',
            '性能优化'
        ],
        'focuses_on': ['流畅性', '性能', '可扩展性'],
        'avoids': ['动画卡顿', '内存泄漏', '复杂状态']
    },
    
    'physics': {
        'name': 'Physics Engine Expert',
        'role': 'Senior Physics Engineer',
        'level': 'senior',
        'experience': '10+ years',
        'keywords': ['physics', 'collision', 'rigid', 'body', 'force', 'velocity', 'contact', 'shape'],
        'description': '资深物理引擎专家，精通物理模拟、碰撞检测和刚体动力学',
        'capabilities': [
            '实现物理引擎',
            '优化碰撞检测',
            '处理物理交互',
            '性能调优',
            '实现自定义物理效果'
        ],
        'expertise': [
            '刚体动力学',
            '碰撞检测',
            '物理模拟',
            '性能优化'
        ],
        'focuses_on': ['物理真实性', '性能', '稳定性'],
        'avoids': ['物理穿透', '性能问题', '不稳定模拟']
    },
    
    'ui': {
        'name': 'UI System Expert',
        'role': 'Senior UI Engineer',
        'level': 'senior',
        'experience': '8+ years',
        'keywords': ['ui', 'widget', 'layout', 'input', 'event', 'button', 'view', 'component', 'interface'],
        'description': '资深UI系统专家，精通界面开发、布局系统和交互设计',
        'capabilities': [
            '设计UI系统架构',
            '实现自定义组件',
            '优化UI渲染性能',
            '处理复杂交互',
            '实现响应式布局'
        ],
        'expertise': [
            'UI组件开发',
            '布局系统',
            '事件处理',
            '性能优化'
        ],
        'focuses_on': ['用户体验', '性能', '可维护性'],
        'avoids': ['过度绘制', '布局抖动', '内存泄漏']
    },
    
    'audio': {
        'name': 'Audio System Expert',
        'role': 'Senior Audio Engineer',
        'level': 'senior',
        'experience': '8+ years',
        'keywords': ['audio', 'sound', 'music', 'voice', 'mixer', 'channel', 'effect'],
        'description': '资深音频系统专家，精通音频处理、音效混音和音频引擎',
        'capabilities': [
            '实现音频引擎',
            '处理音效混音',
            '优化音频性能',
            '实现3D音效'
        ],
        'expertise': [
            '音频处理',
            '音效混音',
            '3D音效',
            '性能优化'
        ],
        'focuses_on': ['音质', '性能', '低延迟'],
        'avoids': ['音频卡顿', '内存泄漏', '同步问题']
    },
    
    'core': {
        'name': 'Core Architecture Expert',
        'role': 'Senior Engine Architect',
        'level': 'senior',
        'experience': '12+ years',
        'keywords': ['core', 'base', 'util', 'helper', 'common', 'platform', 'system', 'manager'],
        'description': '资深引擎架构专家，精通引擎核心架构、设计模式和性能优化',
        'capabilities': [
            '设计引擎架构',
            '优化内存管理',
            '实现设计模式',
            '跨平台开发',
            '性能优化和调优',
            '代码重构和优化'
        ],
        'expertise': [
            '引擎架构',
            '内存管理',
            '设计模式',
            '跨平台开发',
            '性能优化'
        ],
        'focuses_on': ['架构设计', '性能', '可维护性', '跨平台'],
        'avoids': ['过度设计', '技术债务', '平台耦合']
    },
    
    'network': {
        'name': 'Network System Expert',
        'role': 'Senior Network Engineer',
        'level': 'senior',
        'experience': '10+ years',
        'keywords': ['network', 'net', 'socket', 'http', 'web', 'online', 'multiplayer', 'sync'],
        'description': '资深网络系统专家，精通网络通信、同步算法和多人游戏',
        'capabilities': [
            '实现网络通信',
            '处理状态同步',
            '优化网络性能',
            '实现防作弊机制'
        ],
        'expertise': [
            '网络协议',
            '状态同步',
            '延迟优化',
            '多人游戏'
        ],
        'focuses_on': ['网络性能', '同步准确性', '安全性'],
        'avoids': ['网络延迟', '同步问题', '安全漏洞']
    },
    
    'resource': {
        'name': 'Resource Management Expert',
        'role': 'Senior Resource Engineer',
        'level': 'senior',
        'experience': '8+ years',
        'keywords': ['resource', 'asset', 'loader', 'cache', 'bundle', 'preload', 'pool'],
        'description': '资深资源管理专家，精通资源加载、缓存策略和内存优化',
        'capabilities': [
            '实现资源管理系统',
            '优化加载性能',
            '设计缓存策略',
            '内存管理和优化'
        ],
        'expertise': [
            '资源加载',
            '缓存策略',
            '内存管理',
            '性能优化'
        ],
        'focuses_on': ['加载性能', '内存效率', '资源管理'],
        'avoids': ['内存泄漏', '加载卡顿', '资源浪费']
    }
}


class EnhancedAgentGenerator:
    """增强版 Agent 生成器"""
    
    def __init__(self, analysis_path: str, output_dir: str = ".claude/agents"):
        with open(analysis_path, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_all_agents(self):
        """生成所有领域专家 agent"""
        print(f"🤖 Generating domain expert agents...")
        print(f"   Found {len(self.analysis['modules'])} modules")
        
        # Step 1: 将模块映射到领域
        domain_skills = self._map_modules_to_domains()
        
        # Step 2: 为每个领域生成专家
        agents = []
        for domain, skills in domain_skills.items():
            if len(skills) > 0:  # 只生成有技能的领域
                agent = self._generate_domain_expert(domain, skills)
                agents.append(agent)
        
        # Step 3: 生成团队配置
        self._generate_team_config(agents)
        
        print(f"\n✅ Generated {len(agents)} domain experts")
        print(f"   Average skills per expert: {sum(len(a['skills']) for a in agents) / len(agents):.1f}")
        
        return agents
    
    def _map_modules_to_domains(self) -> Dict[str, List[str]]:
        """将模块映射到领域专家"""
        domain_skills = defaultdict(list)
        
        for module in self.analysis['modules']:
            module_name = module['name'].lower()
            matched = False
            
            # 查找匹配的领域
            for domain, config in DOMAIN_EXPERTS.items():
                keywords = config['keywords']
                
                # 检查模块名是否包含领域关键词
                if any(keyword in module_name for keyword in keywords):
                    # 使用原始模块名作为技能名
                    skill_name = module['name']
                    domain_skills[domain].append(skill_name)
                    matched = True
                    break
            
            # 如果没有匹配，归入 core 领域
            if not matched:
                domain_skills['core'].append(module['name'])
        
        return dict(domain_skills)
    
    def _generate_domain_expert(self, domain: str, skills: List[str]) -> Dict:
        """生成领域专家配置"""
        config = DOMAIN_EXPERTS.get(domain, DOMAIN_EXPERTS['core'])
        
        agent = {
            'name': f"{domain}-expert",
            'role': config['role'],
            'level': config['level'],
            'experience': config['experience'],
            'description': config['description'],
            'skills': skills,
            'capabilities': config['capabilities'],
            'expertise': config['expertise'],
            'focuses_on': config['focuses_on'],
            'avoids': config['avoids'],
            'style': 'thorough, professional, detail-oriented, performance-conscious',
            'constraints': [
                f'只修改 {domain} 相关的文件',
                '遵循现有代码模式',
                '保持向后兼容性',
                '优先考虑性能影响',
                '编写单元测试'
            ]
        }
        
        # 保存到文件
        agent_file = self.output_dir / f"{domain}-expert.yaml"
        with open(agent_file, 'w', encoding='utf-8') as f:
            yaml.dump(agent, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        
        print(f"   ✓ {config['name']}: {len(skills)} skills")
        
        return agent
    
    def _generate_team_config(self, agents: List[Dict]):
        """生成团队配置"""
        team = {
            'name': 'project-expert-team',
            'description': '领域专家团队，由资深工程师组成',
            'team_size': len(agents),
            'avg_experience': '10+ years',
            'agents': [agent['name'] for agent in agents],
            'workflow': [
                {'task': '分析需求', 'assigned_to': 'core-expert'},
                {'task': '设计方案', 'assigned_to': '相关领域专家'},
                {'task': '实现功能', 'assigned_to': '相关领域专家'},
                {'task': '代码审查', 'assigned_to': 'core-expert'},
                {'task': '性能优化', 'assigned_to': '所有专家'}
            ],
            'coordination': {
                'communication': '领域专家之间协调',
                'review_process': '资深专家审查',
                'task_routing': '按领域分配'
            }
        }
        
        team_file = self.output_dir / "team.yaml"
        with open(team_file, 'w', encoding='utf-8') as f:
            yaml.dump(team, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        
        print(f"   ✓ Team configuration")


def main():
    parser = argparse.ArgumentParser(description="Generate domain expert agents")
    parser.add_argument("analysis_path", help="Path to analysis.json")
    parser.add_argument("--output", default=".claude/agents", help="Output directory")
    
    args = parser.parse_args()
    
    generator = EnhancedAgentGenerator(args.analysis_path, args.output)
    generator.generate_all_agents()


if __name__ == "__main__":
    main()
