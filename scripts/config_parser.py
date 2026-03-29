#!/usr/bin/env python3
"""
Project Skill Generator - 配置文件解析器
支持 .psg.yaml 配置文件，用于自定义模块发现和分析选项
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ModuleConfig:
    """模块配置"""
    name: str
    path: str
    language: str = "python"
    analyze_depth: str = "deep"  # shallow, deep
    include_patterns: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)


@dataclass
class PSGConfig:
    """项目配置"""
    modules: List[ModuleConfig] = field(default_factory=list)
    default_language: str = "python"
    default_depth: str = "deep"
    global_exclude: List[str] = field(default_factory=list)
    global_include: List[str] = field(default_factory=list)
    max_file_size: int = 1024 * 1024  # 1MB
    enable_progress: bool = True
    verbose: bool = False


class ConfigParser:
    """配置文件解析器"""
    
    DEFAULT_CONFIG = {
        "default_language": "python",
        "default_depth": "deep",
        "global_exclude": [
            "__pycache__",
            ".git",
            "node_modules",
            "venv",
            "env",
            "build",
            "dist",
            "*.log",
            "*.tmp"
        ],
        "global_include": [],
        "max_file_size": 1024,
        "enable_progress": True,
        "verbose": False
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config = PSGConfig()
        
    def load_config(self, config_path: str) -> PSGConfig:
        """加载配置文件"""
        self.config_path = Path(config_path)
        
        if not self.config_path.exists():
            print(f"⚠️ 配置文件 {config_path} 不存在，将生成默认配置")
            self.generate_default_config()
            return self.config
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                
            if not config_data:
                print("⚠️ 配置文件为空，使用默认配置")
                self.config = PSGConfig(**self.DEFAULT_CONFIG)
                return self.config
                
            # 合并默认配置和用户配置
            merged_config = self.DEFAULT_CONFIG.copy()
            merged_config.update(config_data)
            
            # 解析模块配置
            modules = []
            for module_data in merged_config.get('modules', []):
                module = ModuleConfig(**module_data)
                modules.append(module)
                
            self.config = PSGConfig(
                modules=modules,
                default_language=merged_config.get('default_language'),
                default_depth=merged_config.get('default_depth'),
                global_exclude=merged_config.get('global_exclude', []),
                global_include=merged_config.get('global_include', []),
                max_file_size=merged_config.get('max_file_size') * 1024,  # 转换为字节
                enable_progress=merged_config.get('enable_progress', True),
                verbose=merged_config.get('verbose', False)
            )
            
            print(f"✅ 配置文件 {config_path} 加载成功")
            return self.config
            
        except yaml.YAMLError as e:
            print(f"❌ 配置文件语法错误: {e}")
            print("💡 使用默认配置")
            self.config = PSGConfig(**self.DEFAULT_CONFIG)
            return self.config
            
        except Exception as e:
            print(f"❌ 配置文件加载失败: {e}")
            print("💡 使用默认配置")
            self.config = PSGConfig(**self.DEFAULT_CONFIG)
            return self.config
    
    def generate_default_config(self) -> str:
        """生成默认配置文件"""
        config_path = self.config_path or Path(".psg.yaml")
        
        default_modules = [
            {
                "name": "root",
                "path": ".",
                "language": "python",
                "analyze_depth": "deep",
                "include_patterns": ["*.py"],
                "exclude_patterns": ["__pycache__", ".git"]
            }
        ]
        
        config_data = {
            "default_language": "python",
            "default_depth": "deep",
            "modules": default_modules,
            "global_exclude": [
                "__pycache__",
                ".git",
                "node_modules",
                "venv",
                "env",
                "build",
                "dist",
                "*.log",
                "*.tmp"
            ],
            "global_include": [],
            "max_file_size": 1024,
            "enable_progress": True,
            "verbose": False
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            
        print(f"✅ 默认配置文件已生成: {config_path}")
        return str(config_path)
    
    def should_exclude_file(self, file_path: Path) -> bool:
        """检查文件是否应该被排除"""
        file_str = str(file_path)
        
        # 检查全局排除规则
        for pattern in self.config.global_exclude:
            if pattern.startswith('*'):
                # 通配符匹配
                import fnmatch
                if fnmatch.fnmatch(file_str, pattern):
                    return True
            else:
                # 路径匹配
                if pattern in file_str:
                    return True
        
        return False
    
    def should_include_file(self, file_path: Path) -> bool:
        """检查文件是否应该被包含"""
        if not self.config.global_include:
            return True
            
        file_str = str(file_path)
        
        for pattern in self.config.global_include:
            if pattern.startswith('*'):
                import fnmatch
                if fnmatch.fnmatch(file_str, pattern):
                    return True
            else:
                if pattern in file_str:
                    return True
                    
        return False
    
    def get_manual_modules(self, root_path: Path) -> List[ModuleConfig]:
        """获取手动配置的模块"""
        manual_modules = []
        
        for module in self.config.modules:
            module_path = Path(module.path)
            if not module_path.is_absolute():
                module_path = root_path / module_path
                
            if module_path.exists():
                manual_modules.append(module)
                print(f"✅ 手动配置模块: {module.name} -> {module_path}")
            else:
                print(f"⚠️ 模块路径不存在: {module.name} -> {module_path}")
                
        return manual_modules
    
    def validate_config(self) -> bool:
        """验证配置有效性"""
        try:
            # 验证分析深度
            valid_depths = ["shallow", "deep"]
            if self.config.default_depth not in valid_depths:
                print(f"❌ 无效的分析深度: {self.config.default_depth}")
                return False
                
            # 验证文件大小
            if self.config.max_file_size <= 0:
                print(f"❌ 无效的文件大小限制: {self.config.max_file_size}")
                return False
                
            # 验证模块配置
            for module in self.config.modules:
                if not module.name:
                    print("❌ 模块名称不能为空")
                    return False
                if not module.path:
                    print(f"❌ 模块 {module.name} 路径不能为空")
                    return False
                    
            print("✅ 配置验证通过")
            return True
            
        except Exception as e:
            print(f"❌ 配置验证失败: {e}")
            return False


def main():
    """测试配置解析器"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Project Skill Generator 配置解析器")
    parser.add_argument("--config", "-c", help="配置文件路径", default=".psg.yaml")
    parser.add_argument("--generate", "-g", action="store_true", help="生成默认配置文件")
    parser.add_argument("--validate", "-v", action="store_true", help="验证配置文件")
    
    args = parser.parse_args()
    
    config_parser = ConfigParser(args.config)
    
    if args.generate:
        config_parser.generate_default_config()
        return
        
    if args.validate:
        config = config_parser.load_config(args.config)
        if config_parser.validate_config():
            print("✅ 配置文件验证成功")
        else:
            print("❌ 配置文件验证失败")
            return
    
    # 加载配置
    config = config_parser.load_config(args.config)
    
    print("\n📋 配置摘要:")
    print(f"默认语言: {config.default_language}")
    print(f"默认深度: {config.default_depth}")
    print(f"全局排除: {config.global_exclude}")
    print(f"模块数量: {len(config.modules)}")
    print(f"进度显示: {config.enable_progress}")
    print(f"详细输出: {config.verbose}")


if __name__ == "__main__":
    main()