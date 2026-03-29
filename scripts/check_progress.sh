#!/bin/bash
# 查看当前验证进度

PSG_DIR="/root/.openclaw/workspace-opengl/skills/project-skill-generator"
STATE_FILE="$PSG_DIR/doc/.validation_state"
REPORT_DIR="$PSG_DIR/doc/practices"

REPOS=(
    "remote-shell"
    "game-auto-test"
    "wangzhe-chess"
    "voice-chat-demo"
    "render-pipeline-framework"
    "game-frame-sync"
    "opencode-demo"
    "claudegui"
    "feishu_chatbot"
    "opencode-plugins"
    "clawhub-lab"
    "cc_skills"
    "cc_plugin"
    "research-reports"
    "brainstorm"
)

CURRENT_INDEX=$(cat "$STATE_FILE" 2>/dev/null || echo "0")

echo "=========================================="
echo "Project Skill Generator - 验证进度"
echo "=========================================="
echo ""
echo "总仓库数: ${#REPOS[@]}"
echo "已完成: $CURRENT_INDEX"
echo "进度: $((CURRENT_INDEX * 100 / ${#REPOS[@]}))%"
echo ""

if [ "$CURRENT_INDEX" -gt 0 ]; then
    echo "已验证的仓库:"
    for i in $(seq 0 $((CURRENT_INDEX - 1))); do
        echo "  ✅ ${REPOS[$i]}"
    done
    echo ""
fi

if [ "$CURRENT_INDEX" -lt "${#REPOS[@]}" ]; then
    echo "下一个仓库: ${REPOS[$CURRENT_INDEX]}"
    
    NEXT_TIME=$(date -d '+30 minutes' '+%H:%M:%S' 2>/dev/null || echo "未设置自动验证")
    echo "下次验证: $NEXT_TIME"
fi

echo ""
echo "生成的报告:"
ls -lt "$REPORT_DIR"/*.md 2>/dev/null | head -5 || echo "  暂无报告"
echo ""
echo "=========================================="
