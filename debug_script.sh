#!/bin/bash

TODOLIST="doc/todolist.md"

echo "=== Debug Info ==="
echo "TODOLIST file: $TODOLIST"
echo "File exists: [ -f \"$TODOLIST\" ] && echo 'YES' || echo 'NO'"

echo ""
echo "=== Checking TODO-008 status ==="
TODO_008_COUNT=$(grep -A10 "TODO-008" "$TODOLIST" | grep -c "状态: ⏳ 待修复")
echo "TODO_008_COUNT: $TODO_008_COUNT"

echo ""
echo "=== Checking TODO-001 status ==="
TODO_001_COUNT=$(grep -A10 "TODO-001" "$TODOLIST" | grep -c "状态: ⏳ 待修复")
echo "TODO_001_COUNT: $TODO_001_COUNT"

echo ""
echo "=== Total conditions ==="
if [ "$TODO_008_COUNT" -gt 0 ]; then
    echo "✅ TODO-008 condition met"
else
    echo "❌ TODO-008 condition NOT met"
fi

if [ "$TODO_001_COUNT" -gt 0 ]; then
    echo "✅ TODO-001 condition met"
else
    echo "❌ TODO-001 condition NOT met"
fi

echo ""
echo "=== Exit code logic ==="
if [ "$TODO_008_COUNT" -gt 0 ] || [ "$TODO_001_COUNT" -gt 0 ]; then
    echo "Would enter IF block (conditions met)"
else
    echo "Would enter ELSE block (no conditions met)"
fi
