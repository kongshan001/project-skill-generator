#!/bin/bash
# 重置验证状态

PSG_DIR="/root/.openclaw/workspace-opengl/skills/project-skill-generator"
STATE_FILE="$PSG_DIR/doc/.validation_state"

echo "重置验证状态..."
echo "0" > "$STATE_FILE"
echo "✅ 已重置，将从第一个仓库重新开始验证"
echo "状态文件: $STATE_FILE"
