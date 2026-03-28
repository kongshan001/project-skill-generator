#!/usr/bin/env python3
"""
Demo script for Project Skill Generator

This script demonstrates how to use the project-skill-generator skill
to analyze a codebase and generate skills and agents.
"""

import json
from pathlib import Path
from datetime import datetime
import sys


def demo_full_pipeline():
    """Run a complete demo pipeline"""
    
    print("=" * 70)
    print("Project Skill Generator - Demo")
    print("=" * 70)
    
    # Ask for codebase path
    codebase_path = input("\nEnter codebase path (or press Enter for demo): ").strip()
    
    if not codebase_path:
        codebase_path = "/root/.openclaw/workspace-opengl/ai-gateway"
        print(f"Using demo path: {codebase_path}")
    
    # Check if path exists
    if not Path(codebase_path).exists():
        print(f"❌ Path does not exist: {codebase_path}")
        return
    
    print(f"\n🔍 Analyzing codebase: {codebase_path}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Analyze codebase
    print("\n⏳ Step 1: Analyzing codebase...")
    print("   (This may take a moment for large codebases)")
    
    # Call analyze_codebase.py
    from analyze_codebase import CodebaseAnalyzer
    
    analyzer = CodebaseAnalyzer(codebase_path, depth='standard')
    result = analyzer.analyze()
    
    # Save analysis
    analysis_file = Path("demo_analysis.json")
    result_dict = result.__dict__
    analysis_file.write_text(json.dumps(result_dict, indent=2, ensure_ascii=False))
    print(f"   ✅ Analysis complete: {len(result.modules)} modules found")
    print(f"   💾 Saved to: {analysis_file}")
    
    # Show analysis summary
    print("\n📊 Analysis Summary:")
    print(f"   Language: {result.language}")
    print(f"   Modules: {len(result.modules)}")
    print(f"   Files: {result.total_files}")
    print(f"   Lines of Code: {result.total_lines:,}")
    print(f"   Architecture: {result.architecture}")
    
    print("\n📁 Detected Modules:")
    for i, module in enumerate(result.modules[:10], 1):
        print(f"   {i}. {module.name}")
        print(f"      - Files: {len(module.files)}")
        print(f"      - Classes: {len(module.classes)}")
        print(f"      - Functions: {len(module.functions)}")
    
    if len(result.modules) > 10:
        print(f"   ... and {len(result.modules) - 10} more")
    
    # Step 2: Generate skills
    print("\n⏳ Step 2: Generating skills...")
    
    from generate_skill import SkillGenerator
    
    skills_dir = Path("demo_skills")
    generator = SkillGenerator(str(analysis_file), str(skills_dir))
    generator.generate_all_skills(depth='detailed')
    
    print(f"   ✅ Skills generated in: {skills_dir}")
    print(f"      Skills created: {len(list(skills_dir.iterdir()))}")
    
    # Show skill files
    print("\n🎨 Generated Skills:")
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                content = skill_file.read_text()
                lines = len(content.split('\n'))
                print(f"   - {skill_dir.name} ({lines} lines)")
    
    # Step 3: Generate agents
    print("\n⏳ Step 3: Generating agents...")
    
    from generate_agent import AgentGenerator
    
    agents_dir = Path("demo_agents")
    agent_gen = AgentGenerator(str(analysis_file), str(agents_dir))
    agent_gen.generate_all_agents(generate_team=True)
    
    print(f"   ✅ Agents generated in: {agents_dir}")
    print(f"      Agents created: {len(list(agents_dir.glob('*.yaml')))}")
    print(f"      Team config: team.yaml")
    
    # Show agent files
    print("\n🤖 Generated Agents:")
    for agent_file in sorted(agents_dir.glob('*.yaml')):
        if agent_file.name != 'team.yaml':
            with open(agent_file, 'r') as f:
                data = yaml.safe_load(f)
            print(f"   - {data.get('name', agent_file.name)}")
            print(f"      Role: {data.get('role', 'N/A')}")
            print(f"      Skills: {len(data.get('skills', []))}")
    
    # Step 4: Show team configuration
    team_file = agents_dir / "team.yaml"
    if team_file.exists():
        print("\n🤝 Team Configuration:")
        with open(team_file, 'r') as f:
            team = yaml.safe_load(f)
        
        print(f"   Team Name: {team.get('name', 'N/A')}")
        print(f"   Agents: {len(team.get('agents', []))}")
        print(f"   Workflow Steps: {len(team.get('workflow', []))}")
        
        print("\n   Workflow:")
        for step in team.get('workflow', [])[:5]:
            print(f"   - {step.get('step')}: {step.get('agent')} → {step.get('action')}")
    
    # Step 5: Cleanup
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\n📊 Summary:")
    print(f"   ✅ Analysis complete: {len(result.modules)} modules")
    print(f"   ✅ Skills generated: {len(list(skills_dir.iterdir()))}")
    print(f"   ✅ Agents generated: {len(list(agents_dir.glob('*.yaml')))}")
    
    print("\n📁 Output Files:")
    print(f"   - {analysis_file}")
    print(f"   - {skills_dir}/")
    print(f"   - {agents_dir}/")
    
    print("\n💡 Next Steps:")
    print("   1. Review generated skills in demo_skills/")
    print("   2. Review generated agents in demo_agents/")
    print("   3. Integrate .claude/ directory into your project")
    print("   4. Use skills in Claude Code for faster development")
    print("   5. Run update_skills.py for incremental updates")
    
    print("\n🔧 To use in Claude Code:")
    print("   1. Place the project-skill-generator in your .claude/skills/")
    print("   2. Run: /generate-project-skills /path/to/your/codebase")
    print("   3. Open your project in Claude Code")
    print("   4. Use generated skills: /use-skill <skill-name>")


def demo_incremental_update():
    """Demonstrate incremental updates"""
    
    print("\n" + "=" * 70)
    print("Incremental Update Demo")
    print("=" * 70)
    
    codebase_path = input("\nEnter codebase path (or press Enter for demo): ").strip()
    
    if not codebase_path:
        codebase_path = "/root/.openclaw/workspace-opengl/ai-gateway"
        print(f"Using demo path: {codebase_path}")
    
    # Check if .claude directory exists
    claude_dir = Path(codebase_path) / ".claude"
    if not claude_dir.exists():
        print(f"❌ No .claude directory found in {codebase_path}")
        print("   Please run full generation first.")
        return
    
    print(f"\n🔍 Checking for changes in: {codebase_path}")
    
    # Use update_skills.py
    from update_skills import SkillUpdater
    
    updater = SkillUpdater(codebase_path, claude_dir=str(claude_dir))
    
    # Auto-detect changes
    print("   Auto-detecting changes...")
    print("   (Checking last 7 days)")
    
    updater.update(dry_run=True)
    
    print("\n✅ Ready for update!")
    print("   Run without --dry-run to apply changes")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Project Skill Generator - Demo Scripts")
    print("=" * 70)
    
    print("\nChoose a demo:")
    print("1. Full Pipeline Demo")
    print("2. Incremental Update Demo")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        demo_full_pipeline()
    elif choice == '2':
        demo_incremental_update()
    elif choice == '3':
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
