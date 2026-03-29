#!/bin/bash

TODOLIST="doc/todolist.md"

echo "Testing TODO-008 pattern..."
echo "=== TODO-008 section ==="
grep -A5 "TODO-008" "$TODOLIST"

echo ""
echo "=== Looking for status line ==="
if grep -A10 "TODO-008" "$TODOLIST" | grep -q "状态: ⏳ 待修复"; then
    echo "✅ TODO-008 found with '待修复' status"
else
    echo "❌ TODO-008 not found with '待修复' status"
    echo "Available lines around TODO-008:"
    grep -A10 "TODO-008" "$TODOLIST" | grep "状态"
fi
