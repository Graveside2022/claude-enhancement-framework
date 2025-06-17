#!/bin/bash
# Action Hooks for SESSION_LATEST_STATE.md Auto-Updates
# Automatically calls update_session_state() after significant actions

# Source the session state manager
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/session_state_manager.sh"

# Hook for file operations
hook_after_file_write() {
    local file_path="$1"
    local purpose="$2"
    
    if [ -n "$file_path" ]; then
        local filename=$(basename "$file_path")
        after_file_creation "$filename" "${purpose:-File creation}"
        echo "🔄 Auto-updated SESSION_LATEST_STATE.md after file creation"
    fi
}

hook_after_file_edit() {
    local file_path="$1"
    local changes="$2"
    
    if [ -n "$file_path" ]; then
        local filename=$(basename "$file_path")
        after_file_edit "$filename" "${changes:-File modification}"
        echo "🔄 Auto-updated SESSION_LATEST_STATE.md after file edit"
    fi
}

# Hook for command execution
hook_after_command() {
    local command="$1"
    local result="$2"
    
    auto_update_session_state "Executed command: $command" "Result: ${result:-Command completed}"
    echo "🔄 Auto-updated SESSION_LATEST_STATE.md after command execution"
}

# Hook for task completion
hook_after_task() {
    local task="$1"
    local status="$2"
    
    after_task_completion "$task" "${status:-Completed successfully}"
    echo "🔄 Auto-updated SESSION_LATEST_STATE.md after task completion"
}

# Hook for feature implementation
hook_after_feature() {
    local feature="$1"
    local details="$2"
    
    after_feature_implementation "$feature" "${details:-Feature implemented}"
    echo "🔄 Auto-updated SESSION_LATEST_STATE.md after feature implementation"
}

# Hook for testing
hook_after_testing() {
    local test_type="$1"
    local results="$2"
    
    after_testing "$test_type" "${results:-Tests completed}"
    echo "🔄 Auto-updated SESSION_LATEST_STATE.md after testing"
}

# Hook for documentation
hook_after_docs() {
    local doc_type="$1"
    local changes="$2"
    
    after_documentation_update "$doc_type" "${changes:-Documentation updated}"
    echo "🔄 Auto-updated SESSION_LATEST_STATE.md after documentation update"
}

# Hook for pattern creation
hook_after_pattern() {
    local pattern_name="$1"
    local category="$2"
    
    after_pattern_creation "$pattern_name" "${category:-general}"
    echo "🔄 Auto-updated SESSION_LATEST_STATE.md after pattern creation"
}

# Hook for backup creation
hook_after_backup() {
    local backup_id="$1"
    local reason="$2"
    
    after_backup_creation "$backup_id" "${reason:-Routine backup}"
    echo "🔄 Auto-updated SESSION_LATEST_STATE.md after backup creation"
}

# Generic hook for any significant action
hook_after_action() {
    local action="$1"
    local details="$2"
    
    auto_update_session_state "$action" "${details:-Action completed}"
    echo "🔄 Auto-updated SESSION_LATEST_STATE.md after: $action"
}

# Wrapper that detects action type and calls appropriate hook
smart_action_hook() {
    local action="$1"
    local details="$2"
    
    # Auto-detect action type based on keywords
    case "$action" in
        *"creat"*|*"writ"*|*"generat"*)
            if echo "$action" | grep -qi "file\|script\|document"; then
                hook_after_file_write "$action" "$details"
            elif echo "$action" | grep -qi "pattern"; then
                hook_after_pattern "$action" "$details"
            elif echo "$action" | grep -qi "backup"; then
                hook_after_backup "$action" "$details"
            else
                hook_after_action "$action" "$details"
            fi
            ;;
        *"edit"*|*"modif"*|*"updat"*|*"chang"*)
            if echo "$action" | grep -qi "file\|script\|document"; then
                hook_after_file_edit "$action" "$details"
            elif echo "$action" | grep -qi "doc"; then
                hook_after_docs "$action" "$details"
            else
                hook_after_action "$action" "$details"
            fi
            ;;
        *"test"*|*"verif"*|*"validat"*)
            hook_after_testing "$action" "$details"
            ;;
        *"implement"*|*"build"*|*"develop"*)
            hook_after_feature "$action" "$details"
            ;;
        *"complet"*|*"finish"*|*"done"*)
            hook_after_task "$action" "$details"
            ;;
        *"command"*|*"execut"*|*"run"*)
            hook_after_command "$action" "$details"
            ;;
        *)
            hook_after_action "$action" "$details"
            ;;
    esac
}

# Export functions for use in other scripts
export -f hook_after_file_write
export -f hook_after_file_edit
export -f hook_after_command
export -f hook_after_task
export -f hook_after_feature
export -f hook_after_testing
export -f hook_after_docs
export -f hook_after_pattern
export -f hook_after_backup
export -f hook_after_action
export -f smart_action_hook

# Demo function
demo_action_hooks() {
    echo "🎯 Demonstrating automatic SESSION_LATEST_STATE.md updates..."
    echo ""
    
    # Test different action types
    echo "1. Testing file creation hook:"
    hook_after_file_write "demo_file.txt" "Testing auto-update functionality"
    echo ""
    
    echo "2. Testing task completion hook:"
    hook_after_task "Implement SESSION_LATEST_STATE.md auto-updates" "System successfully implemented and tested"
    echo ""
    
    echo "3. Testing smart action detection:"
    smart_action_hook "Created comprehensive action hooks system" "All hook functions implemented with auto-detection capabilities"
    echo ""
    
    echo "✅ All hooks tested successfully!"
    echo "📂 Check SESSION_LATEST_STATE.md for the latest updates"
}

# Main execution
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    case "${1:-demo}" in
        "demo")
            demo_action_hooks
            ;;
        "hook")
            smart_action_hook "$2" "$3"
            ;;
        *)
            echo "Usage: $0 [demo|hook <action> <details>]"
            exit 1
            ;;
    esac
fi