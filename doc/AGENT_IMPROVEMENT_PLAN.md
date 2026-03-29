# Agent 生成器改进方案

## 🎯 问题分析

### 当前问题
1. **一对一关系**：每个 agent 只对应一个 skill
   - 2d-expert → skills: [2d]
   - 3d-expert → skills: [3d]
   - animation-expert → skills: [animation]

2. **过度细分**：Cocos2d-x 生成了 8 个独立 agent
   - 2d-expert
   - 3d-expert
   - animation-expert
   - gfx-expert
   - physics-expert
   - physics-2d-expert
   - rendering-expert
   - service-expert

3. **缺少等级**：没有资深/初级区分
4. **能力分散**：每个 agent 能力过于单一

---

## ✅ 改进目标

### 1. 领域专家模式（一对多技能）

**渲染引擎专家** (Rendering Expert) - Senior
- skills: [2d, 3d, rendering, gfx, animation]
- 专精：图形渲染、材质系统、动画系统
- 等级：资深专家

**物理引擎专家** (Physics Expert) - Senior
- skills: [physics, physics-2d]
- 专精：物理模拟、碰撞检测
- 等级：资深专家

**架构专家** (Architecture Expert) - Senior
- skills: [core, service, base, utils]
- 专精：核心架构、设计模式、性能优化
- 等级：资深专家

### 2. 精简到 3-5 个核心专家

而不是现在的 8-10 个细粒度 agent

### 3. 等级系统

- **Senior Expert** (默认) - 10年+经验
  - 深度理解架构
  - 能处理复杂重构
  - 性能优化专家

- **Mid-Level Expert** - 5年+经验
  - 熟悉核心功能
  - 能独立开发
  - 代码质量优秀

- **Junior Expert** - 2年+经验
  - 基础功能开发
  - 需要指导
  - 学习成长期

---

## 📋 改进方案

### 方案 A：智能领域分组

```python
# 定义领域映射
DOMAIN_MAPPING = {
    'rendering': {
        'skills': ['2d', '3d', 'rendering', 'gfx', 'animation', 'material'],
        'name': 'Rendering Engine Expert',
        'level': 'senior',
        'description': '资深渲染引擎专家，精通2D/3D图形渲染、材质系统和动画',
        'capabilities': [
            '设计渲染架构',
            '优化渲染性能',
            '实现自定义渲染管线',
            '处理复杂材质和着色器',
            '优化动画系统性能'
        ]
    },
    'physics': {
        'skills': ['physics', 'physics-2d', 'collision'],
        'name': 'Physics Engine Expert',
        'level': 'senior',
        'description': '资深物理引擎专家，精通物理模拟和碰撞检测',
        'capabilities': [
            '实现物理引擎',
            '优化碰撞检测',
            '处理物理交互',
            '性能调优'
        ]
    },
    'architecture': {
        'skills': ['core', 'base', 'utils', 'service', 'platform'],
        'name': 'Core Architecture Expert',
        'level': 'senior',
        'description': '资深架构专家，精通引擎核心架构和设计模式',
        'capabilities': [
            '设计引擎架构',
            '优化内存管理',
            '实现设计模式',
            '跨平台开发',
            '性能优化'
        ]
    },
    'ui': {
        'skills': ['ui', 'widget', 'layout', 'input'],
        'name': 'UI System Expert',
        'level': 'senior',
        'description': '资深UI系统专家，精通界面开发和交互设计',
        'capabilities': [
            '设计UI系统',
            '实现自定义组件',
            '优化渲染性能',
            '处理用户交互'
        ]
    },
    'audio': {
        'skills': ['audio', 'sound', 'music'],
        'name': 'Audio System Expert',
        'level': 'senior',
        'description': '资深音频系统专家，精通音频处理和音效管理',
        'capabilities': [
            '实现音频引擎',
            '处理音效混音',
            '优化音频性能'
        ]
    }
}
```

### 方案 B：智能合并算法

```python
def merge_skills_to_domains(skills: List[str]) -> Dict[str, List[str]]:
    """将细粒度技能合并为领域专家"""
    domains = defaultdict(list)
    
    for skill in skills:
        # 查找技能属于哪个领域
        for domain, config in DOMAIN_MAPPING.items():
            if skill in config['skills']:
                domains[domain].append(skill)
                break
    
    return domains
```

### 方案 C：生成的 Agent 配置

```yaml
name: rendering-expert
role: Rendering Engine Expert
level: senior
experience: 10+ years

description: |
  资深渲染引擎专家，精通2D/3D图形渲染、材质系统和动画。
  拥有10年以上游戏引擎开发经验，深入理解现代渲染管线。

skills:
  - 2d           # 2D渲染系统
  - 3d           # 3D渲染系统
  - rendering    # 渲染核心
  - gfx          # 图形接口
  - animation    # 动画系统
  - material     # 材质系统

capabilities:
  - 设计和实现渲染架构
  - 优化渲染性能（Draw call batching、GPU instancing）
  - 实现自定义渲染管线
  - 处理复杂材质和着色器
  - 优化动画系统性能
  - 跨平台渲染优化

expertise:
  - OpenGL/Vulkan/DirectX
  - Shader编程
  - 渲染管线优化
  - 材质系统设计
  - 骨骼动画

style: |
  注重性能和代码质量
  遵循现代C++最佳实践
  善于优化和重构
  重视文档和测试

constraints:
  - 优先考虑性能影响
  - 保持向后兼容性
  - 遵循引擎架构规范
  - 编写单元测试

focuses_on:
  - 性能优化
  - 代码质量
  - 可维护性
  - 跨平台兼容

avoids:
  - 过度设计
  - 性能回退
  - 破坏性更改
  - 技术债务
```

---

## 🚀 实施步骤

### Step 1: 创建新的 agent 生成器
- `enhanced_generate_agent.py`
- 实现领域分组逻辑
- 添加等级系统

### Step 2: 更新配置
- 定义领域映射
- 定义等级标准
- 定义能力描述

### Step 3: 生成优化
- 智能合并技能
- 生成精简专家
- 添加资深描述

### Step 4: 验证效果
- 重新生成 Cocos2d-x 项目
- 对比 agent 数量（8 → 3-5）
- 验证能力覆盖

---

## 📊 预期效果

### Cocos2d-x 项目改进

**改进前**：
- 8 个独立 agent
- 每个 agent 1 个 skill
- 无等级区分
- 能力分散

**改进后**：
- 3-5 个领域专家
- 每个 expert 3-6 个 skills
- 默认资深级别
- 能力集中且专业

### 示例对比

| 原方案 | 新方案 |
|--------|--------|
| 2d-expert (skill: 2d) | Rendering Expert (skills: 2d, 3d, rendering, gfx, animation) |
| 3d-expert (skill: 3d) | ↑ |
| rendering-expert (skill: rendering) | ↑ |
| gfx-expert (skill: gfx) | ↑ |
| animation-expert (skill: animation) | ↑ |
| physics-expert (skill: physics) | Physics Expert (skills: physics, physics-2d) |
| physics-2d-expert (skill: physics-2d) | ↑ |
| service-expert (skill: service) | Architecture Expert (skills: core, service, utils) |

**从 8 个 agent → 3 个专家**

---

## 🎯 下一步

1. 立即实施：创建 `enhanced_generate_agent.py`
2. 重新生成：Cocos2d-x 项目的 agent
3. 验证效果：对比改进前后
4. 迭代优化：根据反馈调整

---

*改进方案 v1.0*
*2026-03-29*
