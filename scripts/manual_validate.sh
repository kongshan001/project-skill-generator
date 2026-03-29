#!/bin/bash
# Project Skill Generator - 手动验证指定仓库

set -e

PSG_DIR="/root/.openclaw/workspace-opengl/skills/project-skill-generator"
REPOS_DIR="/root/.openclaw/workspace-opengl/repos"
LOG_DIR="$PSG_DIR/doc/practices"

if [ -z "$1" ]; then
    echo "用法: $0 <仓库名> [--depth quick|standard|deep]"
    echo ""
    echo "可用仓库:"
    echo "  - remote-shell"
    echo "  - game-auto-test"
    echo "  - wangzhe-chess"
    echo "  - voice-chat-demo"
    echo "  - render-pipeline-framework"
    echo "  - game-frame-sync"
    echo "  - opencode-demo"
    echo "  - claudegui"
    echo "  - feishu_chatbot"
    echo "  - opencode-plugins"
    echo "  - clawhub-lab"
    exit 1
fi

REPO=$1
DEPTH=${3:-standard}
DATE=$(date '+%Y-%m-%d')
REPORT_FILE="$LOG_DIR/${REPO}_${DATE}.md"

echo "=========================================="
echo "手动验证: $REPO"
echo "分析深度: $DEPTH"
echo "=========================================="

# 创建报告
cat > "$REPORT_FILE" << EOF
# ${REPO} 验证报告

**验证日期**: ${DATE}
**验证时间**: $(date '+%H:%M:%S')
**项目仓库**: https://github.com/kongshan001/${REPO}
**分析深度**: ${DEPTH}

---

EOF

# 创建仓库目录
mkdir -p "$REPOS_DIR"
cd "$REPOS_DIR"

# 克隆/更新仓库
echo "📦 Step 1: 克隆仓库..."
if [ -d "$REPO" ]; then
    echo "  仓库已存在，更新中..."
    cd "$REPO"
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
else
    git clone "https://github.com/kongshan001/${REPO}.git"
    cd "$REPO"
fi

echo "  ✅ 仓库准备完成: $(pwd)"

cat >> "$REPORT_FILE" << EOF
## 1. 代码库信息

- **路径**: $(pwd)
- **分支**: $(git branch --show-current)
- **最近提交**: $(git log -1 --oneline 2>/dev/null | head -c 80)

EOF

# 分析代码库
echo ""
echo "🔍 Step 2: 分析代码库..."
ANALYSIS_FILE="$REPOS_DIR/${REPO}_analysis.json"

python3 "$PSG_DIR/scripts/analyze_codebase.py" . \
    --depth "$DEPTH" \
    --output "$ANALYSIS_FILE" 2>&1 | tee /tmp/analysis_output.txt

if [ $? -eq 0 ]; then
    echo "  ✅ 分析完成"
    echo "- **分析状态**: ✅ 成功" >> "$REPORT_FILE"
else
    echo "  ❌ 分析失败"
    echo "- **分析状态**: ❌ 失败" >> "$REPORT_FILE"
    exit 1
fi

cat >> "$REPORT_FILE" << EOF

## 2. 代码库分析结果

\`\`\`
$(cat /tmp/analysis_output.txt)
\`\`\`

EOF

# 生成技能
echo ""
echo "🎨 Step 3: 生成技能..."
mkdir -p ".claude/skills"

python3 "$PSG_DIR/scripts/generate_skill.py" "$ANALYSIS_FILE" \
    --output ".claude/skills/" \
    --depth detailed 2>&1 | tee /tmp/skill_output.txt

if [ $? -eq 0 ]; then
    SKILL_COUNT=$(ls .claude/skills/ 2>/dev/null | wc -l)
    echo "  ✅ 生成了 $SKILL_COUNT 个技能"
    echo "- **技能状态**: ✅ 成功" >> "$REPORT_FILE"
    echo "- **技能数量**: $SKILL_COUNT" >> "$REPORT_FILE"
else
    echo "  ❌ 技能生成失败"
    echo "- **技能状态**: ❌ 失败" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

### 生成的技能

\`\`\`
$(cat /tmp/skill_output.txt)
\`\`\`

EOF

# 生成代理
echo ""
echo "🤖 Step 4: 生成代理..."
mkdir -p ".claude/agents"

python3 "$PSG_DIR/scripts/generate_agent.py" "$ANALYSIS_FILE" \
    --output ".claude/agents/" \
    --team 2>&1 | tee /tmp/agent_output.txt

if [ $? -eq 0 ]; then
    AGENT_COUNT=$(ls .claude/agents/ 2>/dev/null | wc -l)
    echo "  ✅ 生成了 $AGENT_COUNT 个代理"
    echo "- **代理状态**: ✅ 成功" >> "$REPORT_FILE"
    echo "- **代理数量**: $AGENT_COUNT" >> "$REPORT_FILE"
else
    echo "  ❌ 代理生成失败"
    echo "- **代理状态**: ❌ 失败" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

### 生成的代理

\`\`\`
$(cat /tmp/agent_output.txt)
\`\`\`

EOF

# 生成最终报告
cat >> "$REPORT_FILE" << EOF

## 3. 生成的目录结构

\`\`\`
.claude/
$(tree .claude 2>/dev/null || find .claude -type f 2>/dev/null | sed 's/^/│   /')
\`\`\`

## 4. 验证建议

### 测试任务
1. 理解项目架构: "请根据技能库，总结这个项目的架构和核心模块"
2. 定位代码: "找到处理 {核心功能} 的代码，并解释其工作原理"
3. 添加功能: "在 {模块} 中添加一个新功能"
4. 修复 Bug: "修复 {具体问题}"

### Claude Code 启动命令
\`\`\`bash
cd $(pwd)
# 启动 Claude Code 并加载技能库
\`\`\`

---

*报告生成时间: $(date '+%Y-%m-%d %H:%M:%S')*
EOF

echo ""
echo "=========================================="
echo "✅ 验证完成: $REPO"
echo "📄 报告文件: $REPORT_FILE"
echo "📂 项目目录: $(pwd)"
echo "=========================================="
