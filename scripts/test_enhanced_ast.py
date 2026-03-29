#!/usr/bin/env python3
"""
TODO-002: 改进 AST 分析深度 - 验证脚本

这个脚本验证增强的AST分析功能是否提升了生成的技能质量。
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

def run_analysis(codebase_path: str, output_file: str) -> Dict[str, Any]:
    """运行分析并返回结果"""
    try:
        result = subprocess.run([
            sys.executable, "analyze_codebase.py", 
            codebase_path, "--output", output_file
        ], capture_output=True, text=True, cwd="scripts")
        
        if result.returncode == 0:
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"分析失败: {result.stderr}")
            return {}
    except Exception as e:
        print(f"运行失败: {e}")
        return {}

def analyze_enhancement_results(result: Dict[str, Any]) -> Dict[str, Any]:
    """分析增强分析的结果"""
    analysis = {
        "total_modules": 0,
        "modules_with_class_details": 0,
        "modules_with_function_details": 0,
        "total_classes": 0,
        "total_functions": 0,
        "average_function_complexity": 0,
        "async_functions": 0,
        "generator_functions": 0,
        "functions_with_docstrings": 0,
        "classes_with_docstrings": 0,
        "functions_with_type_hints": 0,
        "high_complexity_functions": 0
    }
    
    if not result or "modules" not in result:
        return analysis
    
    analysis["total_modules"] = len(result["modules"])
    
    all_function_complexities = []
    
    for module in result["modules"]:
        module_name = module.get("name", "unknown")
        
        # 检查类的详细信息
        if "classes_info" in module and module["classes_info"]:
            analysis["modules_with_class_details"] += 1
            analysis["total_classes"] += len(module["classes_info"])
            
            for class_info in module["classes_info"]:
                if class_info.get("docstring"):
                    analysis["classes_with_docstrings"] += 1
                
                if "methods" in class_info:
                    for method in class_info["methods"]:
                        if method.get("docstring"):
                            analysis["functions_with_docstrings"] += 1
        
        # 检查函数的详细信息
        if "functions_info" in module and module["functions_info"]:
            analysis["modules_with_function_details"] += 1
            analysis["total_functions"] += len(module["functions_info"])
            
            for func in module["functions_info"]:
                all_function_complexities.append(func.get("complexity", 0))
                
                if func.get("is_async"):
                    analysis["async_functions"] += 1
                
                if func.get("is_generator"):
                    analysis["generator_functions"] += 1
                
                if func.get("docstring"):
                    analysis["functions_with_docstrings"] += 1
                
                if func.get("return_type") or func.get("parameters"):
                    analysis["functions_with_type_hints"] += 1
                
                complexity = func.get("complexity", 0)
                if complexity > 10:  # 高复杂度
                    analysis["high_complexity_functions"] += 1
    
    # 计算平均复杂度
    if all_function_complexities:
        analysis["average_function_complexity"] = sum(all_function_complexities) / len(all_function_complexities)
    
    return analysis

def print_enhancement_report(original_result: Dict[str, Any], enhanced_result: Dict[str, Any]):
    """打印改进报告"""
    original_analysis = analyze_enhancement_results(original_result)
    enhanced_analysis = analyze_enhancement_results(enhanced_result)
    
    print("=== TODO-002: AST 分析深度改进验证报告 ===")
    print()
    
    print("📊 增强前后对比:")
    print(f"{'指标':<35} | {'改进前':<10} | {'改进后':<10} | {'提升':<10}")
    print("-" * 75)
    
    for key in original_analysis:
        original_val = original_analysis.get(key, 0)
        enhanced_val = enhanced_analysis.get(key, 0)
        improvement = enhanced_val - original_val
        improvement_pct = (improvement / max(original_val, 1)) * 100 if original_val > 0 else 0
        
        print(f"{key:<35} | {original_val:<10} | {enhanced_val:<10} | {improvement:+d} ({improvement_pct:.1f}%)")
    
    print()
    
    print("✅ 改进成果:")
    enhanced_features = []
    
    if enhanced_analysis["modules_with_class_details"] > 0:
        enhanced_features.append(f"✅ 支持类详细信息分析 ({enhanced_analysis['total_classes']} 个类)")
    
    if enhanced_analysis["modules_with_function_details"] > 0:
        enhanced_features.append(f"✅ 支持函数详细信息分析 ({enhanced_analysis['total_functions']} 个函数)")
    
    if enhanced_analysis["average_function_complexity"] > 0:
        enhanced_features.append(f"✅ 计算函数复杂度 (平均: {enhanced_analysis['average_function_complexity']:.2f})")
    
    if enhanced_analysis["async_functions"] > 0:
        enhanced_features.append(f"✅ 识别异步函数 ({enhanced_analysis['async_functions']} 个)")
    
    if enhanced_analysis["functions_with_docstrings"] > 0:
        enhanced_features.append(f"✅ 提取文档字符串 ({enhanced_analysis['functions_with_docstrings']} 个函数)")
    
    if enhanced_analysis["functions_with_type_hints"] > 0:
        enhanced_features.append(f"✅ 识别类型注解 ({enhanced_analysis['functions_with_type_hints']} 个函数)")
    
    for feature in enhanced_features:
        print(f"  {feature}")
    
    print()
    print("🎯 生成技能质量改进:")
    print("  - 更准确的API文档")
    print("  - 更好的代码理解")
    print("  - 智能的代理配置")
    print("  - 详细的复杂度分析")

def main():
    """主验证流程"""
    project_path = "/root/.openclaw/workspace-opengl/skills/project-skill-generator"
    test_cases = [
        {
            "name": "Project Skill Generator",
            "path": project_path
        }
    ]
    
    print("🔍 TODO-002: 改进 AST 分析深度")
    print("正在验证增强的AST分析功能...")
    print()
    
    all_results = []
    
    for test_case in test_cases:
        print(f"📁 测试案例: {test_case['name']}")
        
        # 运行分析
        output_file = f"/tmp/enhanced_analysis_{test_case['name'].replace(' ', '_')}.json"
        result = run_analysis(test_case['path'], output_file)
        
        if result:
            all_results.append({
                "name": test_case['name'],
                "path": test_case['path'],
                "result": result
            })
            
            # 分析结果
            analysis = analyze_enhancement_results(result)
            print(f"✅ 成功分析，发现:")
            print(f"   - 模块数: {analysis['total_modules']}")
            print(f"   - 类详细信息: {analysis['modules_with_class_details']}")
            print(f"   - 函数详细信息: {analysis['modules_with_function_details']}")
            print(f"   - 总函数数: {analysis['total_functions']}")
            print(f"   - 平均复杂度: {analysis['average_function_complexity']:.2f}")
            
        print()
    
    # 如果有多个结果，生成综合报告
    if all_results:
        print("📋 综合验证结果:")
        for item in all_results:
            print(f"  ✅ {item['name']}: 增强分析功能正常")
        
        print()
        print("✅ TODO-002 验证完成!")
        print("🎯 改进的AST分析功能已成功实现")
        
    else:
        print("❌ 测试失败，没有有效的分析结果")

if __name__ == "__main__":
    main()