#!/bin/bash

# Trigger Routing Test Script for CLAUDE.md
# Tests whether initialization triggers work correctly after the fix

echo "🔍 Testing Trigger Routing Logic for Christian"
echo "============================================="

# Test phrases that should trigger FULL INITIALIZATION
initialization_triggers=(
    "I'm Christian"
    "Hi"
    "hi" 
    "hello"
    "whats up"
    "what's up"
    "start"
    "setup" 
    "boot"
    "startup"
    "ready"
    "bootup"
    "boot up"
    "this is christian"
)

# Test phrases that should trigger TodoRead (not initialization)
todoread_triggers=(
    "whats next"
    "what's next"
    "what should I do"
    "next task"
    "todo list"
    "priorities"
    "tasks"
    "current tasks"
)

# Test phrases that should NOT trigger either (general requests)
general_phrases=(
    "fix this error"
    "help me with python"
    "create a new file"
    "analyze this code"
)

echo "📋 Testing INITIALIZATION triggers (should route to full initialization):"
echo "-----------------------------------------------------------------------"

for phrase in "${initialization_triggers[@]}"; do
    echo "Testing: '$phrase'"
    
    # Check if it would be caught by TodoRead pattern (SHOULD NOT BE)
    if echo "$phrase" | tr '[:upper:]' '[:lower:]' | grep -E "(what'?s next|whats next|what should.*do|next task|todo list|priorities|tasks|current tasks)" >/dev/null 2>&1; then
        echo "  ❌ PROBLEM: '$phrase' would be caught by TodoRead pattern"
    else
        echo "  ✓ Good: '$phrase' will not be caught by TodoRead"
    fi
    
    # Check if it matches initialization pattern (SHOULD MATCH)
    if echo "$phrase" | tr '[:upper:]' '[:lower:]' | grep -E "(i'm christian|this is christian|^hi$|^hello$|^start$|^setup$|^boot$|^startup$|^ready$|^bootup$|boot up|what's up|whats up)" >/dev/null 2>&1; then
        echo "  ✓ CORRECT: '$phrase' matches initialization pattern"
    else
        echo "  ❌ PROBLEM: '$phrase' does NOT match initialization pattern"
    fi
    echo ""
done

echo "📋 Testing TODOREAD triggers (should route to TodoRead only):"
echo "------------------------------------------------------------"

for phrase in "${todoread_triggers[@]}"; do
    echo "Testing: '$phrase'"
    
    # Check if it would be caught by initialization pattern (SHOULD NOT BE)
    if echo "$phrase" | tr '[:upper:]' '[:lower:]' | grep -E "(i'm christian|this is christian|^hi$|^hello$|^start$|^setup$|^boot$|^startup$|^ready$|^bootup$|boot up|what's up|whats up)" >/dev/null 2>&1; then
        echo "  ❌ PROBLEM: '$phrase' would be caught by initialization pattern"
    else
        echo "  ✓ Good: '$phrase' will not be caught by initialization"
    fi
    
    # Check if it matches TodoRead pattern (SHOULD MATCH)
    if echo "$phrase" | tr '[:upper:]' '[:lower:]' | grep -E "(what'?s next|whats next|what should.*do|next task|todo list|priorities|tasks|current tasks)" >/dev/null 2>&1; then
        echo "  ✓ CORRECT: '$phrase' matches TodoRead pattern"
    else
        echo "  ❌ PROBLEM: '$phrase' does NOT match TodoRead pattern"
    fi
    echo ""
done

echo "📋 Testing GENERAL phrases (should not trigger either system):"
echo "--------------------------------------------------------------"

for phrase in "${general_phrases[@]}"; do
    echo "Testing: '$phrase'"
    
    # Check if it would be caught by initialization pattern (SHOULD NOT BE)
    if echo "$phrase" | tr '[:upper:]' '[:lower:]' | grep -E "(i'm christian|this is christian|^hi$|^hello$|^start$|^setup$|^boot$|^startup$|^ready$|^bootup$|boot up|what's up|whats up)" >/dev/null 2>&1; then
        echo "  ❌ PROBLEM: '$phrase' would be caught by initialization pattern"
    else
        echo "  ✓ Good: '$phrase' will not trigger initialization"
    fi
    
    # Check if it matches TodoRead pattern (SHOULD NOT MATCH)
    if echo "$phrase" | tr '[:upper:]' '[:lower:]' | grep -E "(what'?s next|whats next|what should.*do|next task|todo list|priorities|tasks|current tasks)" >/dev/null 2>&1; then
        echo "  ❌ PROBLEM: '$phrase' would be caught by TodoRead pattern"
    else
        echo "  ✓ Good: '$phrase' will not trigger TodoRead"
    fi
    echo ""
done

echo "✅ Trigger routing test complete!"
echo ""
echo "Summary:"
echo "- Initialization triggers should route to FULL initialization"
echo "- TodoRead triggers should route to TodoRead only"
echo "- General phrases should not trigger either system"
echo "- The routing priority is: Initialization > TodoRead > General processing"