#!/bin/bash
# CLAUDE Improvement Project - Session Update Wrapper
# Purpose: Convenience wrapper for handoff and checkpoint commands
# Usage: ./session_update.sh [handoff|checkpoint] [options]
# User: Christian

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

show_usage() {
    echo "Usage: $0 [handoff|checkpoint] [options]"
    echo ""
    echo "Commands:"
    echo "  handoff      - Execute project handoff operations"
    echo "  checkpoint   - Create backup checkpoint with optional save/commit"
    echo ""
    echo "Examples:"
    echo "  $0 handoff --prepare-handoff         # Prepare session end handoff"
    echo "  $0 handoff --status                  # Show handoff system status"
    echo "  $0 checkpoint \"Progress update\"       # Document only checkpoint"
    echo "  $0 checkpoint --save \"Work in progress\" # Document + git stash"
    echo "  $0 checkpoint --commit \"Feature complete\" # Document + git commit"
    echo ""
    echo "Available handoff options:"
    echo "  --check-timing      Check timing requirements"
    echo "  --execute-updates   Execute mandatory updates"
    echo "  --prepare-handoff   Prepare session end handoff"
    echo "  --status           Show system status"
    echo "  --context-usage N   Monitor context usage (percentage)"
    echo ""
    echo "Available checkpoint options:"
    echo "  \"message\"           Document only checkpoint"
    echo "  --save \"message\"     Document + git stash checkpoint"
    echo "  --commit \"message\"   Document + git commit checkpoint"
    echo ""
    echo "User: Christian"
}

case "$1" in
    "handoff")
        shift
        python3 "${SCRIPT_DIR}/project_handoff.py" "$@"
        ;;
    "checkpoint")
        shift
        # Handle different checkpoint modes
        if [[ "$1" == "--save" ]]; then
            # Document + stash mode
            shift
            python3 "${SCRIPT_DIR}/backup_integration.py" --create "checkpoint_stash" --message "$1" --stash
        elif [[ "$1" == "--commit" ]]; then
            # Document + commit mode
            shift
            python3 "${SCRIPT_DIR}/backup_integration.py" --create "checkpoint_commit" --message "$1" --commit
        else
            # Document only mode (default)
            python3 "${SCRIPT_DIR}/backup_integration.py" --create "checkpoint_document" --message "$1"
        fi
        ;;
    "-h"|"--help"|"help"|"")
        show_usage
        ;;
    *)
        echo "Error: Unknown command '$1'"
        echo ""
        show_usage
        exit 1
        ;;
esac