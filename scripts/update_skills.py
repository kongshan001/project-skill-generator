#!/usr/bin/env python3
"""
增量更新技能库 - 基于现有技能进行智能更新
支持保留用户自定义内容，合并新发现的模式
"""

import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
import subprocess

class IncrementalSkillUpdater:
    """增量技能更新器"""
    
    def __init__(self, codebase_path: str, output_dir: str):
        self.codebase_path = Path(codebase_path)
        self.output_dir = Path(output_dir)
        self.skills_dir = self.output_dir / '.claude' / 'skills'
        self.backup_dir = self.output_dir / '.claude' / 'backups'
        self.changes_file = self.output_dir / '.claude' / 'CHANGES.md'
        
    def analyze_existing_skills(self) -> Dict[str, Dict]:
        """分析现有技能库"""
        existing_skills = {}
        
        if not self.skills_dir.exists():
            return existing_skills
            
        for skill_path in self.skills_dir.rglob('SKILL.md'):
            skill_name = skill_path.parent.name
            existing_skills[skill_name] = {
                'path': skill_path,
                'content': skill_path.read_text(encoding='utf-8'),
                'metadata': self._extract_skill_metadata(skill_path),
                'custom_sections': self._extract_custom_sections(skill_path)
            }
            
        return existing_skills
    
    def _extract_skill_metadata(self, skill_path: Path) -> Dict:
        """提取技能元数据"""
        content = skill_path.read_text(encoding='utf-8')
        metadata = {}
        
        # 提取 frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                except:
                    pass
                    
        return metadata
    
    def _extract_custom_sections(self, skill_path: Path) -> Dict[str, str]:
        """提取用户自定义部分"""
        content = skill_path.read_text(encoding='utf-8')
        custom_sections = {}
        
        # 查找标记为 <!-- custom --> 的部分
        import re
        pattern = r'<!-- custom: (\w+) -->(.*?)<!-- end: \1 -->'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for section_name, section_content in matches:
            custom_sections[section_name] = section_content.strip()
            
        return custom_sections
    
    def backup_existing_skills(self, existing_skills: Dict):
        """备份现有技能"""
        if not existing_skills:
            return
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / timestamp
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for skill_name, skill_data in existing_skills.items():
            src_path = skill_data['path']
            dst_path = backup_path / skill_name / 'SKILL.md'
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.write_text(skill_data['content'], encoding='utf-8')
            
        print(f"✅ 已备份 {len(existing_skills)} 个技能到 {backup_path}")
    
    def merge_skills(self, existing: Dict, new: Dict) -> Dict:
        """合并新旧技能"""
        merged = {
            'name': new.get('name', existing.get('name', 'unknown')),
            'version': f"{datetime.now().strftime('%Y.%m.%d')}",
            'last_updated': datetime.now().isoformat(),
            'metadata': {},
            'sections': {}
        }
        
        # 合并元数据
        merged['metadata'].update(existing.get('metadata', {}))
        merged['metadata'].update(new.get('metadata', {}))
        
        # 合并内容部分
        for section in ['domain_expertise', 'key_apis', 'common_patterns', 
                        'code_conventions', 'testing_strategies', 'performance']:
            existing_section = existing.get('custom_sections', {}).get(section)
            new_section = new.get('sections', {}).get(section)
            
            if existing_section and new_section:
                # 智能合并
                merged['sections'][section] = self._merge_section(
                    existing_section, new_section
                )
            elif existing_section:
                merged['sections'][section] = existing_section
            elif new_section:
                merged['sections'][section] = new_section
                
        return merged
    
    def _merge_section(self, existing: str, new: str) -> str:
        """合并单个部分"""
        # 简单的合并策略：保留现有内容，追加新内容
        # 可以根据需要实现更复杂的合并逻辑
        
        merged_lines = []
        existing_lines = set(existing.strip().split('\n'))
        
        # 保留现有内容
        merged_lines.append("<!-- preserved from previous version -->")
        merged_lines.append(existing.strip())
        
        # 添加新发现的内容
        new_lines = new.strip().split('\n')
        new_content = []
        for line in new_lines:
            if line.strip() and line not in existing_lines:
                new_content.append(line)
                
        if new_content:
            merged_lines.append("\n<!-- newly discovered -->")
            merged_lines.extend(new_content)
            
        return '\n'.join(merged_lines)
    
    def detect_deprecated_code(self, analysis: Dict, existing_skills: Dict) -> List[str]:
        """检测已废弃的代码"""
        deprecated = []
        
        current_modules = set(analysis.get('modules', {}).keys())
        existing_modules = set(existing_skills.keys())
        
        # 查找已删除的模块
        deleted_modules = existing_modules - current_modules
        
        for module in deleted_modules:
            deprecated.append(f"模块 '{module}' 已从代码库中移除")
            
        return deprecated
    
    def generate_update_report(self, updates: Dict, deprecated: List[str]):
        """生成更新报告"""
        report_lines = [
            f"# 技能库更新日志",
            f"",
            f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## 📊 更新统计",
            f"",
            f"- **新增技能**: {len(updates.get('new', []))}",
            f"- **更新技能**: {len(updates.get('updated', []))}",
            f"- **保留技能**: {len(updates.get('preserved', []))}",
            f"- **废弃技能**: {len(deprecated)}",
            f"",
        ]
        
        if updates.get('new'):
            report_lines.append("## ✨ 新增技能\n")
            for skill in updates['new']:
                report_lines.append(f"- **{skill}**: 新发现的模块")
            report_lines.append("")
            
        if updates.get('updated'):
            report_lines.append("## 🔄 更新技能\n")
            for skill in updates['updated']:
                report_lines.append(f"- **{skill}**: 内容已更新")
            report_lines.append("")
            
        if deprecated:
            report_lines.append("## ⚠️ 已废弃\n")
            for item in deprecated:
                report_lines.append(f"- {item}")
            report_lines.append("")
            
        report_content = '\n'.join(report_lines)
        
        # 追加到现有变更日志
        if self.changes_file.exists():
            existing_content = self.changes_file.read_text(encoding='utf-8')
            report_content = existing_content + "\n\n---\n\n" + report_content
            
        self.changes_file.parent.mkdir(parents=True, exist_ok=True)
        self.changes_file.write_text(report_content, encoding='utf-8')
        
        print(f"✅ 更新报告已保存到 {self.changes_file}")
    
    def run_incremental_update(self, since: Optional[str] = None, 
                               module: Optional[str] = None,
                               full: bool = False):
        """执行增量更新"""
        
        print("🔍 分析现有技能库...")
        existing_skills = self.analyze_existing_skills()
        
        if existing_skills:
            print(f"✅ 发现 {len(existing_skills)} 个现有技能")
            self.backup_existing_skills(existing_skills)
        else:
            print("ℹ️  未发现现有技能，将进行全新生成")
            
        # 运行代码库分析
        print("\n🔍 分析代码库...")
        analysis_cmd = [
            sys.executable,
            str(Path(__file__).parent / 'analyze_codebase.py'),
            str(self.codebase_path),
            '--output', str(self.output_dir / '.claude' / 'analysis_new.json')
        ]
        
        if not full and since:
            analysis_cmd.extend(['--since', since])
            
        subprocess.run(analysis_cmd, check=True)
        
        # 加载新分析结果
        analysis_file = self.output_dir / '.claude' / 'analysis_new.json'
        with open(analysis_file, 'r', encoding='utf-8') as f:
            new_analysis = json.load(f)
            
        # 生成/更新技能
        print("\n🔄 生成技能...")
        updates = {
            'new': [],
            'updated': [],
            'preserved': []
        }
        
        for module_name, module_data in new_analysis.get('modules', {}).items():
            if module and module != module_name:
                continue
                
            skill_path = self.skills_dir / module_name / 'SKILL.md'
            
            if module_name in existing_skills:
                # 增量更新现有技能
                print(f"  🔄 更新技能: {module_name}")
                merged_skill = self.merge_skills(
                    existing_skills[module_name],
                    {'name': module_name, 'metadata': {}, 'sections': module_data}
                )
                self._write_skill(skill_path, merged_skill)
                updates['updated'].append(module_name)
            else:
                # 生成新技能
                print(f"  ✨ 生成新技能: {module_name}")
                # 使用增强版技能生成器
                updates['new'].append(module_name)
                
        # 检测已废弃的代码
        print("\n⚠️  检测已废弃代码...")
        deprecated = self.detect_deprecated_code(new_analysis, existing_skills)
        
        if deprecated:
            for item in deprecated:
                print(f"  - {item}")
                
        # 生成更新报告
        print("\n📝 生成更新报告...")
        self.generate_update_report(updates, deprecated)
        
        print("\n✅ 增量更新完成！")
        print(f"   - 新增: {len(updates['new'])}")
        print(f"   - 更新: {len(updates['updated'])}")
        print(f"   - 废弃: {len(deprecated)}")
        
    def _write_skill(self, skill_path: Path, skill_data: Dict):
        """写入技能文件"""
        skill_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成技能文档内容
        content = self._generate_skill_content(skill_data)
        skill_path.write_text(content, encoding='utf-8')
        
    def _generate_skill_content(self, skill_data: Dict) -> str:
        """生成技能文档内容"""
        lines = [
            "---",
            f"name: {skill_data['name']}",
            f"version: {skill_data['version']}",
            f"last_updated: {skill_data['last_updated']}",
            "---",
            "",
            f"# {skill_data['name']}",
            ""
        ]
        
        for section_name, section_content in skill_data.get('sections', {}).items():
            section_title = section_name.replace('_', ' ').title()
            lines.extend([
                f"## {section_title}",
                "",
                section_content,
                ""
            ])
            
        # 保留自定义部分
        custom_sections = skill_data.get('metadata', {}).get('custom_sections', {})
        for section_name, section_content in custom_sections.items():
            lines.extend([
                f"<!-- custom: {section_name} -->",
                section_content,
                f"<!-- end: {section_name} -->",
                ""
            ])
            
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='增量更新 Claude Code 技能库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基于最近的提交更新
  %(prog)s /path/to/codebase --since 2024-01-01
  
  # 更新特定模块
  %(prog)s /path/to/codebase --module user-auth
  
  # 完全重新分析（大型重构后）
  %(prog)s /path/to/codebase --full
        """
    )
    
    parser.add_argument('codebase', help='代码库路径')
    parser.add_argument('--output', '-o', default='.', 
                       help='输出目录（默认：代码库根目录）')
    parser.add_argument('--since', help='分析指定日期后的变更（格式：YYYY-MM-DD）')
    parser.add_argument('--module', help='只更新特定模块')
    parser.add_argument('--full', action='store_true', 
                       help='完全重新分析（忽略增量更新）')
    
    args = parser.parse_args()
    
    updater = IncrementalSkillUpdater(args.codebase, args.output)
    updater.run_incremental_update(
        since=args.since,
        module=args.module,
        full=args.full
    )


if __name__ == '__main__':
    main()
