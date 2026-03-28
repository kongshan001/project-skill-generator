#!/usr/bin/env python3
"""
Agent Generator - Generate expert agents from analysis results

Usage:
    generate_agent.py <analysis.json> [options]

Options:
    --output DIR          Output directory for agents (default: .claude/agents)
    --team                Generate team configuration
"""

import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


class AgentGenerator:
    """Generate expert agents from module analysis"""
    
    def __init__(self, analysis_path: str, output_dir: str = ".claude/agents"):
        with open(analysis_path, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_all_agents(self, generate_team: bool = False):
        """Generate agents for all modules"""
        print(f"🤖 Generating agents for {len(self.analysis['modules'])} modules...")
        
        agents = []
        
        # Group modules by category
        module_groups = self._group_modules_by_category()
        
        for category, modules in module_groups.items():
            print(f"   Creating agent: {category}-expert")
            agent = self._generate_expert_agent(category, modules)
            agents.append(agent)
        
        # Generate team configuration
        if generate_team:
            print(f"   Creating team configuration...")
            self._generate_team_config(agents)
        
        print(f"\n✅ Agents generated in: {self.output_dir}")
    
    def _group_modules_by_category(self) -> Dict[str, List[Dict]]:
        """Group modules by functional category"""
        groups = defaultdict(list)
        
        for module in self.analysis['modules']:
            category = self._detect_module_category(module)
            groups[category].append(module)
        
        return dict(groups)
    
    def _detect_module_category(self, module: Dict[str, Any]) -> str:
        """Detect module category from name and content"""
        name = module['name'].lower()
        patterns = [p.lower() for p in module.get('patterns', [])]
        
        # UI/Frontend
        if any(keyword in name for keyword in ['ui', 'component', 'view', 'page', 'screen', 'frontend']):
            return 'frontend'
        
        # API/Backend
        if any(keyword in name for keyword in ['api', 'route', 'endpoint', 'controller', 'handler']):
            return 'api'
        
        # Database
        if any(keyword in name for keyword in ['db', 'database', 'model', 'entity', 'repository', 'dao']):
            return 'database'
        
        # Authentication
        if any(keyword in name for keyword in ['auth', 'user', 'login', 'session', 'token']):
            return 'auth'
        
        # Services
        if any(keyword in name for keyword in ['service', 'business', 'logic', 'core']):
            return 'service'
        
        # Utils
        if any(keyword in name for keyword in ['util', 'helper', 'common', 'lib', 'tool']):
            return 'util'
        
        # Testing
        if any(keyword in name for keyword in ['test', 'spec', 'mock']):
            return 'testing'
        
        # Config
        if any(keyword in name for keyword in ['config', 'setting', 'env']):
            return 'config'
        
        # Default: use first part of module name
        first_part = name.split('.')[0].split('/')[0]
        return first_part if first_part else 'general'
    
    def _generate_expert_agent(self, category: str, modules: List[Dict]) -> Dict:
        """Generate expert agent for a category"""
        agent_name = f"{category}-expert"
        agent_file = self.output_dir / f"{agent_name}.yaml"
        
        # Collect skills from modules
        skills = []
        for module in modules:
            skill_name = self._normalize_skill_name(module['name'])
            skills.append(skill_name)
        
        # Generate capabilities from modules
        capabilities = self._extract_capabilities(modules)
        
        # Generate constraints
        constraints = self._generate_constraints(category, modules)
        
        # Create agent config
        agent_config = {
            'name': agent_name,
            'role': self._get_agent_role(category),
            'description': self._get_agent_description(category, modules),
            'skills': skills,
            'capabilities': capabilities,
            'constraints': constraints,
            'style': self._get_agent_style(category),
            'focuses_on': self._get_agent_focus(category),
            'avoids': self._get_agent_avoids(category),
            'modules': [m['name'] for m in modules],
            'file_patterns': self._get_file_patterns(modules)
        }
        
        # Write YAML file
        with open(agent_file, 'w', encoding='utf-8') as f:
            yaml.dump(agent_config, f, default_flow_style=False, allow_unicode=True)
        
        return agent_config
    
    def _normalize_skill_name(self, module_name: str) -> str:
        """Convert module name to skill name"""
        name = module_name.replace('.', '-').replace('/', '-')
        while '--' in name:
            name = name.replace('--', '-')
        return name.strip('-').lower()
    
    def _extract_capabilities(self, modules: List[Dict]) -> List[str]:
        """Extract capabilities from modules"""
        capabilities = []
        
        for module in modules:
            # From patterns
            for pattern in module.get('patterns', []):
                cap = self._pattern_to_capability(pattern)
                if cap and cap not in capabilities:
                    capabilities.append(cap)
            
            # From classes
            for cls in module.get('classes', []):
                cap = f"Work with {cls}"
                if cap not in capabilities:
                    capabilities.append(cap)
            
            # From functions
            for func in module.get('functions', [])[:5]:
                if '.' not in func:  # Top-level function
                    capabilities.append(f"Use {func}()")
        
        return capabilities[:10]  # Top 10
    
    def _pattern_to_capability(self, pattern: str) -> str:
        """Convert pattern to capability"""
        pattern_map = {
            'async/await': 'Handle async operations',
            'react-hooks': 'Implement React hooks',
            'decorators': 'Use decorators',
            'context-manager': 'Manage resources with context managers',
            'type-hints': 'Add type annotations',
            'dataclass': 'Design data classes',
            'pytest-testing': 'Write pytest tests',
        }
        return pattern_map.get(pattern, '')
    
    def _generate_constraints(self, category: str, modules: List[Dict]) -> List[str]:
        """Generate agent constraints"""
        constraints = [
            f"Only modify {category}-related files",
            "Follow existing code patterns",
            "Maintain backward compatibility",
            "Write tests for new functionality"
        ]
        
        # Add category-specific constraints
        if category == 'database':
            constraints.append("Always use transactions for data modifications")
            constraints.append("Create migrations for schema changes")
        elif category == 'api':
            constraints.append("Validate all input data")
            constraints.append("Document API endpoints")
        elif category == 'auth':
            constraints.append("Never log sensitive data")
            constraints.append("Use secure defaults")
        
        return constraints
    
    def _get_agent_role(self, category: str) -> str:
        """Get agent role title"""
        roles = {
            'frontend': 'Frontend UI Specialist',
            'api': 'Backend API Expert',
            'database': 'Database & Data Layer Expert',
            'auth': 'Authentication & Security Expert',
            'service': 'Business Logic Expert',
            'util': 'Utility & Helper Expert',
            'testing': 'Testing & QA Expert',
            'config': 'Configuration Expert'
        }
        return roles.get(category, f'{category.title()} Expert')
    
    def _get_agent_description(self, category: str, modules: List[Dict]) -> str:
        """Get agent description"""
        module_names = [m['name'] for m in modules[:3]]
        return f"Specialized agent for {category} domain. Expert in modules: {', '.join(module_names)}"
    
    def _get_agent_style(self, category: str) -> str:
        """Get agent working style"""
        styles = {
            'frontend': 'user-centric, detail-oriented, focused on UX',
            'api': 'systematic, performance-conscious, well-documented',
            'database': 'careful, transaction-aware, optimization-minded',
            'auth': 'security-first, paranoid, thorough',
            'service': 'business-focused, pragmatic, maintainable',
            'testing': 'thorough, edge-case-aware, comprehensive',
        }
        return styles.get(category, 'thorough, professional, detail-oriented')
    
    def _get_agent_focus(self, category: str) -> List[str]:
        """Get agent focus areas"""
        focuses = {
            'frontend': ['user experience', 'accessibility', 'performance', 'responsiveness'],
            'api': ['performance', 'scalability', 'documentation', 'error handling'],
            'database': ['data integrity', 'query performance', 'schema design', 'migrations'],
            'auth': ['security', 'compliance', 'audit trails', 'encryption'],
            'service': ['business logic', 'domain modeling', 'error handling', 'maintainability'],
        }
        return focuses.get(category, ['code quality', 'maintainability', 'best practices'])
    
    def _get_agent_avoids(self, category: str) -> List[str]:
        """Get what agent avoids"""
        avoids = {
            'frontend': ['over-engineering', 'unnecessary complexity', 'poor accessibility'],
            'api': ['breaking changes', 'undocumented features', 'performance regressions'],
            'database': ['N+1 queries', 'unindexed searches', 'data inconsistencies'],
            'auth': ['security shortcuts', 'plaintext storage', 'weak encryption'],
        }
        return avoids.get(category, ['technical debt', 'code duplication', 'poor documentation'])
    
    def _get_file_patterns(self, modules: List[Dict]) -> List[str]:
        """Get file patterns for this agent"""
        patterns = []
        for module in modules:
            for file in module.get('files', [])[:3]:
                # Extract pattern from file path
                path = file.replace('\\', '/')
                if '/' in path:
                    pattern = '/' + '/'.join(path.split('/')[-2:])
                    patterns.append(pattern)
        return list(set(patterns))[:5]
    
    def _generate_team_config(self, agents: List[Dict]):
        """Generate team configuration"""
        team_file = self.output_dir / "team.yaml"
        
        team_config = {
            'name': 'project-team',
            'description': 'Coordinated team of specialized agents',
            'agents': [agent['name'] for agent in agents],
            'workflow': self._generate_workflow(agents),
            'communication': {
                'style': 'async',
                'update_frequency': 'per-task',
                'conflict_resolution': 'escalate-to-user'
            },
            'coordination': {
                'task_routing': 'by-expertise',
                'parallel_execution': True,
                'review_process': 'peer-review'
            }
        }
        
        with open(team_file, 'w', encoding='utf-8') as f:
            yaml.dump(team_config, f, default_flow_style=False, allow_unicode=True)
    
    def _generate_workflow(self, agents: List[Dict]) -> List[Dict]:
        """Generate workflow configuration"""
        workflow = []
        
        # Typical development workflow
        if any('frontend' in a['name'] for a in agents):
            workflow.append({'step': 1, 'agent': 'frontend-expert', 'action': 'Design UI components'})
        
        if any('api' in a['name'] for a in agents):
            workflow.append({'step': 2, 'agent': 'api-expert', 'action': 'Implement API endpoints'})
        
        if any('auth' in a['name'] for a in agents):
            workflow.append({'step': 3, 'agent': 'auth-expert', 'action': 'Add authentication'})
        
        if any('database' in a['name'] for a in agents):
            workflow.append({'step': 4, 'agent': 'database-expert', 'action': 'Implement data layer'})
        
        if any('service' in a['name'] for a in agents):
            workflow.append({'step': 5, 'agent': 'service-expert', 'action': 'Add business logic'})
        
        if any('testing' in a['name'] for a in agents):
            workflow.append({'step': 6, 'agent': 'testing-expert', 'action': 'Write tests'})
        
        return workflow


def main():
    parser = argparse.ArgumentParser(description="Generate expert agents from analysis")
    parser.add_argument("analysis_file", help="Path to analysis.json")
    parser.add_argument("--output", default=".claude/agents", help="Output directory")
    parser.add_argument("--team", action="store_true", help="Generate team configuration")
    
    args = parser.parse_args()
    
    generator = AgentGenerator(args.analysis_file, args.output)
    generator.generate_all_agents(args.team)


if __name__ == "__main__":
    main()
