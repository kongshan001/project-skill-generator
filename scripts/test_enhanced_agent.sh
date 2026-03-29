#!/bin/bash
# 测试增强版 Agent 生成器

echo "=========================================="
echo "测试增强版 Agent 生成器"
echo "=========================================="

# 检查分析文件
ANALYSIS_FILE="/root/.openclaw/workspace-opengl/test-cocos/cocos-analysis.json"

if [ ! -f "$ANALYSIS_FILE" ]; then
    echo "❌ 找不到分析文件: $ANALYSIS_FILE"
    exit 1
fi

# 统计原始 agent 数量
echo ""
echo "📊 原始 Agent 数量:"
ORIGINAL_COUNT=$(find /root/.openclaw/workspace-opengl/test-cocos/.claude/agents -name "*-expert.yaml" 2>/dev/null | wc -l)
echo "   原始: $ORIGINAL_COUNT 个 agent"

# 备份原始 agent
echo ""
echo "💾 备份原始 agent..."
BACKUP_DIR="/root/.openclaw/workspace-opengl/test-cocos/.claude/agents_backup_$(date +%s)"
cp -r /root/.openclaw/workspace-opengl/test-cocos/.claude/agents "$BACKUP_DIR" 2>/dev/null || true
echo "   备份位置: $BACKUP_DIR"

# 生成新的 agent
echo ""
echo "🚀 生成新的领域专家 agent..."
cd /root/.openclaw/workspace-opengl/skills/project-skill-generator

python3 scripts/enhanced_generate_agent.py "$ANALYSIS_FILE" \
    --output /root/.openclaw/workspace-opengl/test-cocos/.claude/agents_enhanced

# 统计新的 agent 数量
echo ""
echo "📊 新的 Agent 数量:"
NEW_COUNT=$(find /root/.openclaw/workspace-opengl/test-cocos/.claude/agents_enhanced -name "*-expert.yaml" 2>/dev/null | wc -l)
echo "   新版: $NEW_COUNT 个 agent"

# 对比
echo ""
echo "📈 改进效果:"
echo "   从 $ORIGINAL_COUNT 个 → $NEW_COUNT 个 agent"
REDUCTION=$((ORIGINAL_COUNT - NEW_COUNT))
PERCENT=$((REDUCTION * 100 / ORIGINAL_COUNT))
echo "   精简了 $REDUCTION 个 ($PERCENT%)"

echo ""
echo "✅ 测试完成"
echo "=========================================="
