#!/bin/bash
# Project Skill Generator - 自动验证下一个仓库
# 每30分钟执行一次

set -e

# 配置
PSG_DIR="/root/.openclaw/workspace-opengl/skills/project-skill-generator"
REPOS_DIR="/root/.openclaw/workspace-opengl/repos"
STATE_FILE="$PSG_DIR/doc/.validation_state"
REPO_LIST="$PSG_DIR/doc/repos/repo_list.md"
LOG_DIR="$PSG_DIR/doc/practices"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}"
}

# 待验证仓库列表（按优先级排序）
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

# 获取当前应该验证的仓库索引
get_current_index() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo "0"
    fi
}

# 保存当前索引
save_index() {
    echo "$1" > "$STATE_FILE"
}

# 创建验证报告
create_report() {
    local repo=$1
    local date=$(date '+%Y-%m-%d')
    local report_file="$LOG_DIR/${repo}_${date}.md"
    
    cat > "$report_file" << EOF
# ${repo} 验证报告

**验证日期**: ${date}
**验证时间**: $(date '+%H:%M:%S')
**项目仓库**: https://github.com/kongshan001/${repo}

---

## 验证状态

⏳ 进行中...

## 1. 代码库克隆

EOF
    echo "$report_file"
}

# 主函数
main() {
    log "=========================================="
    log "Project Skill Generator - 自动验证"
    log "=========================================="
    
    # 获取当前索引
    CURRENT_INDEX=$(get_current_index)
    
    # 检查是否已完成所有仓库
    if [ "$CURRENT_INDEX" -ge "${#REPOS[@]}" ]; then
        log_success "所有仓库验证完成！"
        log "共验证 ${#REPOS[@]} 个仓库"
        exit 0
    fi
    
    # 获取当前仓库
    REPO="${REPOS[$CURRENT_INDEX]}"
    log "当前验证: $REPO (第 $((CURRENT_INDEX + 1))/${#REPOS[@]} 个)"
    
    # 创建报告文件
    REPORT_FILE=$(create_report "$REPO")
    log "报告文件: $REPORT_FILE"
    
    # 创建仓库目录
    mkdir -p "$REPOS_DIR"
    cd "$REPOS_DIR"
    
    # Step 1: 克隆/更新仓库
    log "Step 1: 克隆仓库..."
    if [ -d "$REPO" ]; then
        log_warn "仓库已存在，跳过克隆"
        cd "$REPO"
        git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
    else
        git clone "https://github.com/kongshan001/${REPO}.git"
        cd "$REPO"
    fi
    
    # 更新报告
    cat >> "$REPORT_FILE" << EOF

- 状态: ✅ 成功
- 仓库路径: $(pwd)
- 分支: $(git branch --show-current)

## 2. 代码库分析

EOF
    
    # Step 2: 分析代码库
    log "Step 2: 分析代码库..."
    cd "$REPOS_DIR/$REPO"
    
    ANALYSIS_FILE="$REPOS_DIR/${REPO}_analysis.json"
    
    python3 "$PSG_DIR/scripts/analyze_codebase.py" . \
        --depth standard \
        --output "$ANALYSIS_FILE" 2>&1 | tee -a "$REPORT_FILE"
    
    if [ $? -eq 0 ]; then
        log_success "代码库分析完成"
        echo "- 状态: ✅ 成功" >> "$REPORT_FILE"
        echo "- 分析文件: $ANALYSIS_FILE" >> "$REPORT_FILE"
    else
        log_error "代码库分析失败"
        echo "- 状态: ❌ 失败" >> "$REPORT_FILE"
    fi
    
    # Step 3: 生成技能
    log "Step 3: 生成技能..."
    
    cat >> "$REPORT_FILE" << EOF

## 3. 技能生成

EOF
    
    mkdir -p ".claude/skills"
    
    python3 "$PSG_DIR/scripts/generate_skill.py" "$ANALYSIS_FILE" \
        --output ".claude/skills/" \
        --depth detailed 2>&1 | tee -a "$REPORT_FILE"
    
    if [ $? -eq 0 ]; then
        log_success "技能生成完成"
        echo "- 状态: ✅ 成功" >> "$REPORT_FILE"
        echo "- 技能数量: $(ls .claude/skills/ 2>/dev/null | wc -l)" >> "$REPORT_FILE"
    else
        log_error "技能生成失败"
        echo "- 状态: ❌ 失败" >> "$REPORT_FILE"
    fi
    
    # Step 4: 生成代理
    log "Step 4: 生成代理..."
    
    cat >> "$REPORT_FILE" << EOF

## 4. 代理生成

EOF
    
    mkdir -p ".claude/agents"
    
    python3 "$PSG_DIR/scripts/generate_agent.py" "$ANALYSIS_FILE" \
        --output ".claude/agents/" \
        --team 2>&1 | tee -a "$REPORT_FILE"
    
    if [ $? -eq 0 ]; then
        log_success "代理生成完成"
        echo "- 状态: ✅ 成功" >> "$REPORT_FILE"
        echo "- 代理数量: $(ls .claude/agents/ 2>/dev/null | wc -l)" >> "$REPORT_FILE"
    else
        log_error "代理生成失败"
        echo "- 状态: ❌ 失败" >> "$REPORT_FILE"
    fi
    
    # Step 5: 记录验证结果
    cat >> "$REPORT_FILE" << EOF

## 5. 验证总结

**状态**: ⏳ 等待 Claude Code 验证

### 生成的文件结构

\`\`\`
.claude/
$(tree .claude 2>/dev/null || find .claude -type f 2>/dev/null | sed 's/^/│   /')
\`\`\`

### 下一步

1. 启动 Claude Code
2. 加载生成的技能库
3. 执行测试任务验证
4. 记录验证结果

---

*自动生成于 $(date '+%Y-%m-%d %H:%M:%S')*
EOF
    
    # 更新 repo_list.md
    log "更新仓库列表状态..."
    sed -i "s/| $REPO | \(.*\) | ⏳ 待验证/| $REPO | \1 | ✅ 已完成/" "$REPO_LIST" 2>/dev/null || true
    
    # 保存下一个索引
    NEXT_INDEX=$((CURRENT_INDEX + 1))
    save_index "$NEXT_INDEX"
    
    log_success "验证完成: $REPO"
    log "下一个仓库: ${REPOS[$NEXT_INDEX]} (索引: $NEXT_INDEX)"
    log "报告已保存: $REPORT_FILE"
    
    # 如果还有仓库，计算下次执行时间
    if [ "$NEXT_INDEX" -lt "${#REPOS[@]}" ]; then
        NEXT_TIME=$(date -d '+30 minutes' '+%H:%M:%S')
        log "下次验证时间: $NEXT_TIME"
    fi
}

main "$@"
