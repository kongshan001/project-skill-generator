#!/usr/bin/env python3
"""
Validate Project Skill Generator installation

Checks that all required files exist and are properly configured.
"""

import os
import sys
from pathlib import Path


def check_file(path, description):
    """Check if a file exists and is readable"""
    path_obj = Path(path)
    
    if path_obj.exists():
        print(f"✅ {description}")
        print(f"   Path: {path_obj}")
        
        # Check if file has content
        if path_obj.stat().st_size > 0:
            print(f"   Size: {path_obj.stat().st_size} bytes")
        return True
    else:
        print(f"❌ {description}")
        print(f"   Path: {path_obj}")
        print(f"   ERROR: File does not exist")
        return False


def check_executable(path, description, allow_yaml=True):
    """Check if a script is executable or if it's a YAML file"""
    path_obj = Path(path)
    
    if not path_obj.exists():
        print(f"❌ {description}")
        print(f"   Path: {path_obj}")
        print(f"   ERROR: File does not exist")
        return False
    
    # YAML files don't need to be executable
    if allow_yaml and path_obj.suffix in ['.yaml', '.yml']:
        print(f"✅ {description}")
        print(f"   Path: {path_obj}")
        print(f"   Size: {path_obj.stat().st_size} bytes")
        return True
    
    # Check if Python script is executable
    if os.access(path_obj, os.X_OK):
        print(f"✅ {description}")
        print(f"   Path: {path_obj}")
        print(f"   Size: {path_obj.stat().st_size} bytes")
        return True
    else:
        print(f"⚠️  {description}")
        print(f"   Path: {path_obj}")
        print(f"   NOTE: Script may need to be made executable")
        return False


def main():
    print("=" * 70)
    print("Project Skill Generator - Installation Validation")
    print("=" * 70)
    
    skill_dir = Path(__file__).parent
    print(f"\n📁 Checking: {skill_dir}\n")
    
    all_checks_passed = True
    
    # Check SKILL.md
    if not check_file(skill_dir / "SKILL.md", "Main SKILL.md"):
        all_checks_passed = False
    
    # Check README.md
    if not check_file(skill_dir / "README.md", "README.md"):
        all_checks_passed = False
    
    # Check scripts
    print("\n🔧 Checking Scripts:")
    scripts = [
        ("scripts/analyze_codebase.py", "Codebase Analyzer"),
        ("scripts/generate_skill.py", "Skill Generator"),
        ("scripts/generate_agent.py", "Agent Generator"),
        ("scripts/update_skills.py", "Skill Updater"),
    ]
    
    for script_path, description in scripts:
        script_file = skill_dir / script_path
        if not check_executable(script_file, description):
            all_checks_passed = False
    
    # Check references
    print("\n📚 Checking References:")
    references = [
        ("references/skill-patterns.md", "Skill Patterns"),
        ("references/agent-patterns.md", "Agent Patterns"),
    ]
    
    for ref_path, description in references:
        if not check_file(skill_dir / ref_path, description):
            all_checks_passed = False
    
    # Check templates
    print("\n🎨 Checking Templates:")
    
    skill_template = skill_dir / "assets" / "skill-template" / "SKILL.md"
    if not check_file(skill_template, "Skill Template"):
        all_checks_passed = False
    
    agent_template = skill_dir / "assets" / "agent-template" / "agent.yaml"
    if not check_file(agent_template, "Agent Template"):
        all_checks_passed = False
    
    team_template = skill_dir / "assets" / "agent-template" / "team.yaml"
    if not check_file(team_template, "Team Template"):
        all_checks_passed = False
    
    # Check __init__.py
    print("\n📦 Checking Python Package:")
    if not check_file(skill_dir / "__init__.py", "Python Package Init"):
        all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_checks_passed:
        print("✅ All checks passed!")
        print("\n🎉 Project Skill Generator is ready to use!")
        print("\n📋 To use:")
        print("   1. Run: python demo.py")
        print("   2. Follow the prompts to analyze and generate skills/agents")
        print("   3. Integrate the .claude/ directory into your project")
        return 0
    else:
        print("❌ Some checks failed!")
        print("\n⚠️  Please ensure all files are in place.")
        print("   Run this script again after fixing any issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
