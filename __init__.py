"""
Project Skill Generator - Generate Claude Code skills and expert agents

This package provides tools to analyze codebases and generate
project-specific Claude Code skills and expert agents.
"""

__version__ = "1.0.0"
__author__ = "Project Skill Generator Team"

__all__ = [
    'CodebaseAnalyzer',
    'SkillGenerator',
    'AgentGenerator',
    'SkillUpdater'
]

# Import main classes for convenience
try:
    from scripts.analyze_codebase import CodebaseAnalyzer
    from scripts.generate_skill import SkillGenerator
    from scripts.generate_agent import AgentGenerator
    from scripts.update_skills import SkillUpdater
    _imported_modules = True
except ImportError:
    _imported_modules = False
    print("Warning: Some modules could not be imported. Please ensure all scripts are in the scripts/ directory.")
