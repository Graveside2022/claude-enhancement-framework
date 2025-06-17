#!/bin/bash
# SESSION_LATEST_STATE.md Auto-Update Manager
# Extracted from ~/.claude/CLAUDE.md for Christian's project

# Find project root function (needed by update_session_state)
find_project_root() {
    local current_dir="$PWD"
    local max_depth=20
    local depth=0
    
    # Search up directory tree for project markers
    while [ "$current_dir" != "/" ] && [ $depth -lt $max_depth ]; do
        # Primary markers (highest confidence)
        if [ -f "$current_dir/CLAUDE.md" ]; then
            echo "$current_dir"
            return 0
        fi
        
        # Secondary markers with Claude memory structure
        if [ -d "$current_dir/memory" ] && [ -f "$current_dir/memory/learning_archive.md" ]; then
            echo "$current_dir"
            return 0
        fi
        
        # Tertiary markers - common project indicators with Claude structure
        if [ -f "$current_dir/package.json" ] || [ -f "$current_dir/requirements.txt" ] || [ -d "$current_dir/.git" ]; then
            # Verify it also has Claude learning structure
            if [ -d "$current_dir/memory" ] || [ -f "$current_dir/SESSION_CONTINUITY.md" ]; then
                echo "$current_dir"
                return 0
            fi
        fi
        
        # Move up one directory
        current_dir="$(dirname "$current_dir")"
        depth=$((depth + 1))
    done
    
    # No project root found - use current directory
    echo "$PWD"
    return 1
}

# Auto-continuity function (exactly as specified in CLAUDE.md)
update_session_state() {
    local action="$1"
    local details="$2"
    local project_root=$(find_project_root)
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Create or update SESSION_LATEST_STATE.md in project root
    cat > "$project_root/SESSION_LATEST_STATE.md" << EOF
# SESSION LATEST STATE
Updated: $timestamp
User: Christian

## Last Action
$action

## Details
$details

## Current Context
Working directory: $(pwd)
Project root: $project_root

## Next Step
Check TODO.md for current priorities
EOF
}

# Create auto-update wrapper for significant actions
auto_update_session_state() {
    local action_type="$1"
    local action_details="$2"
    
    # Validate inputs
    if [ -z "$action_type" ]; then
        echo "❌ Error: Action type required for session state update"
        return 1
    fi
    
    if [ -z "$action_details" ]; then
        action_details="No additional details provided"
    fi
    
    # Call the documented function
    update_session_state "$action_type" "$action_details"
    
    # Provide feedback
    local project_root=$(find_project_root)
    echo "✅ SESSION_LATEST_STATE.md updated in $project_root"
    echo "📝 Action: $action_type"
    echo "📋 Details: $action_details"
}

# Wrapper functions for common significant actions
after_file_creation() {
    local filename="$1"
    local purpose="$2"
    auto_update_session_state "Created file: $filename" "Purpose: $purpose"
}

after_file_edit() {
    local filename="$1"
    local changes="$2"
    auto_update_session_state "Modified file: $filename" "Changes: $changes"
}

after_task_completion() {
    local task_name="$1"
    local outcome="$2"
    auto_update_session_state "Completed task: $task_name" "Outcome: $outcome"
}

after_feature_implementation() {
    local feature_name="$1"
    local details="$2"
    auto_update_session_state "Implemented feature: $feature_name" "Details: $details"
}

after_pattern_creation() {
    local pattern_name="$1"
    local category="$2"
    auto_update_session_state "Created pattern: $pattern_name" "Category: $category, available for reuse"
}

after_backup_creation() {
    local backup_id="$1"
    local reason="$2"
    auto_update_session_state "Created backup: $backup_id" "Reason: $reason"
}

after_testing() {
    local test_type="$1"
    local results="$2"
    auto_update_session_state "Ran tests: $test_type" "Results: $results"
}

after_documentation_update() {
    local doc_type="$1"
    local changes="$2"
    auto_update_session_state "Updated documentation: $doc_type" "Changes: $changes"
}

# Demo/test function
test_session_state_update() {
    echo "🧪 Testing SESSION_LATEST_STATE.md auto-update system..."
    
    # Test basic function
    auto_update_session_state "Testing auto-update system" "Verifying that SESSION_LATEST_STATE.md is created/updated correctly"
    
    # Test that file was created
    local project_root=$(find_project_root)
    if [ -f "$project_root/SESSION_LATEST_STATE.md" ]; then
        echo "✅ SESSION_LATEST_STATE.md successfully created/updated"
        echo "📂 Location: $project_root/SESSION_LATEST_STATE.md"
        echo ""
        echo "📄 Contents:"
        cat "$project_root/SESSION_LATEST_STATE.md"
        return 0
    else
        echo "❌ Failed to create SESSION_LATEST_STATE.md"
        return 1
    fi
}

# Integration hooks (to be called after significant actions)
integrate_with_existing_functions() {
    echo "🔗 Session state auto-update integration active"
    echo "📋 Available wrapper functions:"
    echo "   - after_file_creation <filename> <purpose>"
    echo "   - after_file_edit <filename> <changes>"
    echo "   - after_task_completion <task> <outcome>"
    echo "   - after_feature_implementation <feature> <details>"
    echo "   - after_pattern_creation <pattern> <category>"
    echo "   - after_backup_creation <backup_id> <reason>"
    echo "   - after_testing <test_type> <results>"
    echo "   - after_documentation_update <doc_type> <changes>"
    echo ""
    echo "💡 Usage: Call these functions after significant actions"
    echo "🎯 Result: SESSION_LATEST_STATE.md will be automatically updated"
}

# Main execution
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    # Script is being run directly, not sourced
    case "${1:-test}" in
        "test")
            test_session_state_update
            ;;
        "integrate")
            integrate_with_existing_functions
            ;;
        "update")
            auto_update_session_state "$2" "$3"
            ;;
        *)
            echo "Usage: $0 [test|integrate|update <action> <details>]"
            exit 1
            ;;
    esac
fi