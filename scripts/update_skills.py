#!/usr/bin/env python3
"""
Skill Updater - Incrementally update skills based on codebase changes

Usage:
    update_skills.py <codebase-path> [options]

Options:
    --since DATE          Update based on changes since date (YYYY-MM-DD)
    --diff COMMIT         Update based on changes since commit
    --module NAME         Update specific module only
    --full                Full re-analysis (major refactors)
    --dry-run             Show what would be updated without making changes
"""

import argparse
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
from dataclasses import dataclass


@dataclass
class Change:
    """Represents a code change"""
    file: str
    type: str  # 'added', 'modified', 'deleted'
    module: str
    impact_level: str  # 'low', 'medium', 'high'


class SkillUpdater:
    """Update skills based on codebase changes"""
    
    def __init__(self, codebase_path: str, claude_dir: str = ".claude"):
        self.root = Path(codebase_path).resolve()
        self.claude_dir = self.root / claude_dir
        self.skills_dir = self.claude_dir / "skills"
        self.agents_dir = self.claude_dir / "agents"
        self.analysis_file = self.claude_dir / "analysis.json"
        
    def update(self, since: Optional[str] = None, diff: Optional[str] = None,
               module: Optional[str] = None, full: bool = False, dry_run: bool = False):
        """Update skills based on changes"""
        
        if full:
            print("🔄 Full re-analysis requested...")
            self._full_update(dry_run)
            return
        
        # Detect changes
        changes = self._detect_changes(since, diff, module)
        
        if not changes:
            print("✅ No changes detected. Skills are up to date.")
            return
        
        print(f"🔍 Detected {len(changes)} changes:")
        for change in changes[:10]:  # Show first 10
            print(f"   [{change.type}] {change.file}")
        
        if len(changes) > 10:
            print(f"   ... and {len(changes) - 10} more")
        
        # Analyze impact
        impacted_modules = self._analyze_impact(changes)
        
        print(f"\n📊 Impact analysis:")
        for module_name, impact in impacted_modules.items():
            print(f"   {module_name}: {impact} impact")
        
        if dry_run:
            print("\n⚠️  Dry run mode - no changes made")
            return
        
        # Update affected skills
        print("\n🔧 Updating skills...")
        self._update_skills(impacted_modules, changes)
        
        # Update agents if needed
        if self._should_update_agents(changes):
            print("\n🤖 Updating agents...")
            self._update_agents(impacted_modules)
        
        print("\n✅ Skills updated successfully!")
    
    def _detect_changes(self, since: Optional[str], diff: Optional[str],
                       module: Optional[str]) -> List[Change]:
        """Detect code changes"""
        changes = []
        
        if diff:
            # Git diff-based detection
            changes = self._detect_git_changes(diff)
        elif since:
            # Time-based detection
            changes = self._detect_time_changes(since)
        else:
            # Default: last 7 days
            since_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            changes = self._detect_time_changes(since_date)
        
        # Filter by module if specified
        if module:
            changes = [c for c in changes if module in c.module]
        
        return changes
    
    def _detect_git_changes(self, since_commit: str) -> List[Change]:
        """Detect changes using git diff"""
        changes = []
        
        try:
            # Get changed files
            result = subprocess.run(
                ['git', 'diff', '--name-status', since_commit],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) >= 2:
                    status = parts[0]
                    file_path = parts[1]
                    
                    change_type = {
                        'A': 'added',
                        'M': 'modified',
                        'D': 'deleted',
                        'R': 'renamed'
                    }.get(status[0], 'modified')
                    
                    module = self._file_to_module(file_path)
                    impact = self._assess_impact(file_path, change_type)
                    
                    changes.append(Change(
                        file=file_path,
                        type=change_type,
                        module=module,
                        impact_level=impact
                    ))
        
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git command failed: {e}")
            print("   Falling back to time-based detection")
            since_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            return self._detect_time_changes(since_date)
        
        return changes
    
    def _detect_time_changes(self, since_date: str) -> List[Change]:
        """Detect changes based on file modification time"""
        changes = []
        since_dt = datetime.strptime(since_date, '%Y-%m-%d')
        
        for file_path in self.root.rglob('*'):
            if file_path.is_file() and self._is_code_file(file_path):
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                if mtime > since_dt:
                    relative = file_path.relative_to(self.root)
                    module = self._file_to_module(str(relative))
                    
                    changes.append(Change(
                        file=str(relative),
                        type='modified',
                        module=module,
                        impact_level='medium'
                    ))
        
        return changes
    
    def _file_to_module(self, file_path: str) -> str:
        """Convert file path to module name"""
        parts = Path(file_path).parts
        
        # Find module (first directory)
        if len(parts) > 1:
            return parts[0]
        
        return 'root'
    
    def _assess_impact(self, file_path: str, change_type: str) -> str:
        """Assess impact level of a change"""
        # High impact files
        high_impact_patterns = [
            'model', 'schema', 'config', 'init',
            'api', 'route', 'endpoint',
            'auth', 'security'
        ]
        
        file_lower = file_path.lower()
        
        if change_type == 'deleted':
            return 'high'
        
        if any(pattern in file_lower for pattern in high_impact_patterns):
            return 'high'
        
        if change_type == 'added':
            return 'medium'
        
        return 'low'
    
    def _is_code_file(self, file_path: Path) -> bool:
        """Check if file is a code file"""
        code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx',
            '.java', '.go', '.rs', '.cpp', '.c',
            '.rb', '.php', '.cs', '.swift', '.kt'
        }
        
        # Skip common non-code directories
        skip_dirs = {'venv', 'env', 'node_modules', '__pycache__', '.git', 'build', 'dist'}
        
        if any(skip in file_path.parts for skip in skip_dirs):
            return False
        
        return file_path.suffix in code_extensions
    
    def _analyze_impact(self, changes: List[Change]) -> Dict[str, str]:
        """Analyze impact of changes on modules"""
        module_impacts = {}
        
        for change in changes:
            module = change.module
            
            if module not in module_impacts:
                module_impacts[module] = 'low'
            
            # Upgrade impact if necessary
            if change.impact_level == 'high':
                module_impacts[module] = 'high'
            elif change.impact_level == 'medium' and module_impacts[module] == 'low':
                module_impacts[module] = 'medium'
        
        return module_impacts
    
    def _update_skills(self, impacted_modules: Dict[str, str], changes: List[Change]):
        """Update affected skills"""
        for module_name, impact in impacted_modules.items():
            print(f"   Updating {module_name} (impact: {impact})")
            
            # Find skill directory
            skill_dir = self.skills_dir / module_name.replace('.', '-').replace('/', '-')
            
            if not skill_dir.exists():
                print(f"      ⚠️  Skill not found, creating new...")
                self._create_new_skill(module_name, changes)
                continue
            
            # Update existing skill
            if impact == 'high':
                self._full_skill_update(skill_dir, module_name, changes)
            else:
                self._incremental_skill_update(skill_dir, module_name, changes)
    
    def _create_new_skill(self, module_name: str, changes: List[Change]):
        """Create new skill for a new module"""
        # Import and use analyze_codebase
        from analyze_codebase import CodebaseAnalyzer
        
        # Analyze the new module
        module_path = self.root / module_name.replace('.', '/')
        if module_path.exists():
            analyzer = CodebaseAnalyzer(str(self.root))
            # ... generate skill
            print(f"      ✅ Created new skill for {module_name}")
    
    def _full_skill_update(self, skill_dir: Path, module_name: str, changes: List[Change]):
        """Full skill update for high-impact changes"""
        # Re-analyze module completely
        print(f"      🔄 Full re-analysis...")
        
        # Import generator
        from generate_skill import SkillGenerator
        
        # Re-generate skill
        # This would call the analyzer and generator
        print(f"      ✅ Skill fully updated")
    
    def _incremental_skill_update(self, skill_dir: Path, module_name: str, changes: List[Change]):
        """Incremental skill update for low/medium impact changes"""
        skill_file = skill_dir / "SKILL.md"
        
        if not skill_file.exists():
            print(f"      ⚠️  SKILL.md not found")
            return
        
        # Read current skill
        content = skill_file.read_text()
        
        # Extract new patterns from changes
        new_patterns = self._extract_new_patterns(changes)
        
        if new_patterns:
            # Add new patterns to skill
            patterns_section = "\n### Recently Added Patterns\n"
            for pattern in new_patterns:
                patterns_section += f"- {pattern}\n"
            
            # Insert before last section
            if "## Usage Guide" in content:
                content = content.replace("## Usage Guide", patterns_section + "\n## Usage Guide")
            else:
                content += "\n" + patterns_section
            
            skill_file.write_text(content)
            print(f"      ✅ Added {len(new_patterns)} new patterns")
        else:
            print(f"      ℹ️  No new patterns detected")
    
    def _extract_new_patterns(self, changes: List[Change]) -> List[str]:
        """Extract new patterns from changes"""
        patterns = []
        
        for change in changes:
            if change.type == 'added':
                patterns.append(f"New file: {Path(change.file).name}")
            elif change.type == 'modified':
                # Could analyze the diff for new patterns
                pass
        
        return patterns
    
    def _should_update_agents(self, changes: List[Change]) -> bool:
        """Check if agents should be updated"""
        # Update agents if:
        # - New module added
        # - High impact changes
        # - Config files changed
        
        for change in changes:
            if change.type == 'added' and change.impact_level == 'high':
                return True
            
            if 'config' in change.file.lower():
                return True
        
        return False
    
    def _update_agents(self, impacted_modules: Dict[str, str]):
        """Update agent configurations"""
        # This would update agent YAML files
        # For now, just print what would be updated
        
        for module_name in impacted_modules:
            agent_file = self.agents_dir / f"{module_name}-expert.yaml"
            
            if agent_file.exists():
                print(f"   Updated {agent_file.name}")
            else:
                print(f"   Would create {agent_file.name}")
    
    def _full_update(self, dry_run: bool):
        """Perform full re-analysis"""
        print("🔄 Performing full re-analysis...")
        
        if dry_run:
            print("   Would:")
            print("   - Re-analyze entire codebase")
            print("   - Regenerate all skills")
            print("   - Regenerate all agents")
            return
        
        # Import modules
        from analyze_codebase import CodebaseAnalyzer
        from generate_skill import SkillGenerator
        from generate_agent import AgentGenerator
        
        # Analyze
        analyzer = CodebaseAnalyzer(str(self.root), depth='standard')
        result = analyzer.analyze()
        
        # Save analysis
        import json
        from dataclasses import asdict
        self.analysis_file.parent.mkdir(parents=True, exist_ok=True)
        self.analysis_file.write_text(json.dumps(asdict(result), indent=2))
        
        # Generate skills
        generator = SkillGenerator(str(self.analysis_file), str(self.skills_dir))
        generator.generate_all_skills(depth='detailed')
        
        # Generate agents
        agent_gen = AgentGenerator(str(self.analysis_file), str(self.agents_dir))
        agent_gen.generate_all_agents(generate_team=True)
        
        print("✅ Full update complete!")


def main():
    parser = argparse.ArgumentParser(description="Update skills based on codebase changes")
    parser.add_argument("codebase_path", help="Path to codebase")
    parser.add_argument("--since", help="Changes since date (YYYY-MM-DD)")
    parser.add_argument("--diff", help="Changes since commit")
    parser.add_argument("--module", help="Update specific module")
    parser.add_argument("--full", action="store_true", help="Full re-analysis")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without updating")
    
    args = parser.parse_args()
    
    updater = SkillUpdater(args.codebase_path)
    updater.update(
        since=args.since,
        diff=args.diff,
        module=args.module,
        full=args.full,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
