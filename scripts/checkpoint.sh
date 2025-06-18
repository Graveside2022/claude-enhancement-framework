#!/bin/bash

# Checkpoint Script for SESSION_CONTINUITY.md Updates
# Usage: 
#   ./scripts/checkpoint.sh [message]           - Document only (default)
#   ./scripts/checkpoint.sh --save [message]    - Document + git stash
#   ./scripts/checkpoint.sh --commit [message]  - Document + git commit
# Creates a checkpoint entry with timestamp in SESSION_CONTINUITY.md

SESSION_FILE="/Users/scarmatrix/Project/CLAUDE_improvement/SESSION_CONTINUITY.md"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
READABLE_TIME=$(date +"%Y-%m-%d %H:%M:%S")

# Parse arguments
SAVE_MODE="document"  # default: document only
CHECKPOINT_MESSAGE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --save)
            SAVE_MODE="stash"
            shift
            ;;
        --commit)
            SAVE_MODE="commit"
            shift
            ;;
        --help|-h)
            echo "Checkpoint Script for SESSION_CONTINUITY.md Updates"
            echo ""
            echo "Usage:"
            echo "  ./scripts/checkpoint.sh [message]           - Document only (default)"
            echo "  ./scripts/checkpoint.sh --save [message]    - Document + git stash"
            echo "  ./scripts/checkpoint.sh --commit [message]  - Document + git commit"
            echo ""
            echo "Options:"
            echo "  --save     Save changes to git stash after documenting"
            echo "  --commit   Commit changes to git after documenting"
            echo "  --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./scripts/checkpoint.sh \"Testing new feature\""
            echo "  ./scripts/checkpoint.sh --save \"Work in progress\""
            echo "  ./scripts/checkpoint.sh --commit \"Feature complete\""
            exit 0
            ;;
        *)
            # If no message set yet, use this as the message
            if [ -z "$CHECKPOINT_MESSAGE" ]; then
                CHECKPOINT_MESSAGE="$1"
            fi
            shift
            ;;
    esac
done

# Set default message if none provided
CHECKPOINT_MESSAGE="${CHECKPOINT_MESSAGE:-Manual checkpoint}"

# Capture current working state
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
GIT_STATUS=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
MODIFIED_FILES=""
if [ "$GIT_STATUS" -gt 0 ]; then
    MODIFIED_FILES=$(git status --porcelain 2>/dev/null | head -5 | sed 's/^/  - /')
fi

# Create checkpoint entry with save mode info
SAVE_MODE_TEXT=""
case $SAVE_MODE in
    "stash")
        SAVE_MODE_TEXT="**Save Mode**: Document + Git Stash  "
        ;;
    "commit")
        SAVE_MODE_TEXT="**Save Mode**: Document + Git Commit  "
        ;;
    *)
        SAVE_MODE_TEXT="**Save Mode**: Document Only  "
        ;;
esac

CHECKPOINT_ENTRY="## CHECKPOINT - $TIMESTAMP

### 📍 CHECKPOINT: $CHECKPOINT_MESSAGE
**Timestamp**: $READABLE_TIME  
**Branch**: $CURRENT_BRANCH  
**Modified Files**: $GIT_STATUS files  
$MODIFIED_FILES
$SAVE_MODE_TEXT

**Working State**: Checkpoint created by Christian  
**Session Status**: Active  

"

# Add checkpoint to SESSION_CONTINUITY.md
if [ -f "$SESSION_FILE" ]; then
    # Create temporary file with checkpoint entry
    echo "$CHECKPOINT_ENTRY" > "${SESSION_FILE}.checkpoint"
    
    # Insert checkpoint after current session line
    awk '
    /^## Current Session/ {
        print $0
        getline
        print $0
        print ""
        system("cat \"'${SESSION_FILE}.checkpoint'\"")
        next
    }
    { print }
    ' "$SESSION_FILE" > "${SESSION_FILE}.tmp"
    
    # Check if temporary file was created successfully
    if [ -f "${SESSION_FILE}.tmp" ]; then
        mv "${SESSION_FILE}.tmp" "$SESSION_FILE"
    else
        echo "❌ Error: Failed to create temporary file for checkpoint"
        rm -f "${SESSION_FILE}.checkpoint"
        exit 1
    fi
    
    # Clean up temporary file
    rm -f "${SESSION_FILE}.checkpoint"
    
    echo "✅ Checkpoint added to SESSION_CONTINUITY.md"
    echo "📍 Message: $CHECKPOINT_MESSAGE"
    echo "⏰ Timestamp: $READABLE_TIME"
    echo "🔄 Branch: $CURRENT_BRANCH"
    echo "📝 Modified files: $GIT_STATUS"
    
    # Perform git operations based on save mode
    case $SAVE_MODE in
        "stash")
            if [ "$GIT_STATUS" -gt 0 ]; then
                echo ""
                echo "💾 Saving changes to git stash..."
                if git stash push -m "Checkpoint: $CHECKPOINT_MESSAGE - $READABLE_TIME"; then
                    echo "✅ Changes saved to git stash"
                else
                    echo "❌ Error: Failed to create git stash"
                    exit 1
                fi
            else
                echo ""
                echo "ℹ️  No changes to stash (working directory clean)"
            fi
            ;;
        "commit")
            if [ "$GIT_STATUS" -gt 0 ]; then
                echo ""
                echo "💾 Committing changes to git..."
                # Add all changes
                if git add .; then
                    echo "✅ Changes staged"
                else
                    echo "❌ Error: Failed to stage changes"
                    exit 1
                fi
                # Create commit
                if git commit -m "Checkpoint: $CHECKPOINT_MESSAGE

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"; then
                    echo "✅ Changes committed to git"
                else
                    echo "❌ Error: Failed to create commit"
                    exit 1
                fi
            else
                echo ""
                echo "ℹ️  No changes to commit (working directory clean)"
            fi
            ;;
        *)
            echo ""
            echo "ℹ️  Document-only checkpoint (no git operations)"
            ;;
    esac
else
    echo "❌ Error: SESSION_CONTINUITY.md not found at $SESSION_FILE"
    exit 1
fi