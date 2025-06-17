#!/bin/bash

# handoff.sh - Updates SESSION_CONTINUITY.md when Christian types "handoff"
# Usage: ./handoff.sh [optional_message]

# Set project root directory
PROJECT_ROOT="/Users/scarmatrix/Project/CLAUDE_improvement"
SESSION_FILE="$PROJECT_ROOT/SESSION_CONTINUITY.md"

# Function to get current timestamp
get_timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# Function to get current project status
get_project_status() {
    local status=""
    
    # Check if we're in a git repo and get status
    if git -C "$PROJECT_ROOT" status >/dev/null 2>&1; then
        local git_status=$(git -C "$PROJECT_ROOT" status --porcelain 2>/dev/null)
        if [ -n "$git_status" ]; then
            status="Git: Uncommitted changes present"
        else
            status="Git: Clean working directory"
        fi
    else
        status="Git: Not a repository"
    fi
    
    # Check if TODO.md exists and has content
    if [ -f "$PROJECT_ROOT/TODO.md" ]; then
        local todo_count=$(grep -c "^- \[ \]" "$PROJECT_ROOT/TODO.md" 2>/dev/null || echo "0")
        status="$status | TODO: $todo_count pending tasks"
    fi
    
    echo "$status"
}

# Function to update SESSION_CONTINUITY.md
update_session_continuity() {
    local handoff_message="$1"
    local timestamp=$(get_timestamp)
    local project_status=$(get_project_status)
    
    # Create SESSION_CONTINUITY.md if it doesn't exist
    if [ ! -f "$SESSION_FILE" ]; then
        cat > "$SESSION_FILE" << EOF
# SESSION CONTINUITY - CLAUDE IMPROVEMENT PROJECT

## Current Session Status
- Project: CLAUDE_improvement
- Owner: Christian
- Last Updated: $timestamp

## Session History

EOF
    fi
    
    # Prepare handoff entry
    local handoff_entry="### HANDOFF - $timestamp

**Status**: $project_status"
    
    if [ -n "$handoff_message" ]; then
        handoff_entry="$handoff_entry
**Message**: $handoff_message"
    fi
    
    handoff_entry="$handoff_entry

**Context**: Session handoff initiated by Christian
**Next Actions**: Ready for new session continuation

---

"
    
    # Insert the handoff entry after the "## Session History" line
    if grep -q "## Session History" "$SESSION_FILE"; then
        # Use a temporary file to safely insert the content
        local temp_file=$(mktemp)
        awk -v entry="$handoff_entry" '
            /^## Session History/ {
                print $0
                print ""
                print entry
                next
            }
            { print }
        ' "$SESSION_FILE" > "$temp_file"
        
        # Replace the original file
        mv "$temp_file" "$SESSION_FILE"
    else
        # If the structure is different, append to the end
        echo "$handoff_entry" >> "$SESSION_FILE"
    fi
    
    echo "✓ SESSION_CONTINUITY.md updated with handoff entry"
    echo "  Timestamp: $timestamp"
    echo "  Status: $project_status"
    if [ -n "$handoff_message" ]; then
        echo "  Message: $handoff_message"
    fi
}

# Main execution
main() {
    # Check if PROJECT_ROOT exists
    if [ ! -d "$PROJECT_ROOT" ]; then
        echo "Error: Project directory not found at $PROJECT_ROOT"
        exit 1
    fi
    
    # Get handoff message from command line argument or prompt
    local handoff_message="$1"
    
    if [ -z "$handoff_message" ]; then
        echo "Enter optional handoff message (press Enter to skip):"
        read -r handoff_message
    fi
    
    # Update SESSION_CONTINUITY.md
    update_session_continuity "$handoff_message"
    
    echo "Handoff complete. Ready for session continuation."
}

# Execute main function with all arguments
main "$@"