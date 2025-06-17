#!/bin/bash
# Session Start Handler - Automatic Timing Check Execution
# Triggered when Christian starts a session or uses setup/start commands
# Created: 2025-06-16T21:40:00Z
# User: Christian

# Detect session start triggers
detect_session_start() {
    local user_input="$1"
    
    # Convert to lowercase for case-insensitive matching
    local input_lower=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
    
    # Session start trigger patterns
    local start_patterns="setup|startup|boot|start|init|begin|session|timing"
    
    if echo "$input_lower" | grep -E "$start_patterns" >/dev/null 2>&1; then
        return 0  # Match found
    else
        return 1  # No match
    fi
}

# Auto-execute timing checks on session start
if detect_session_start "${1:-startup}"; then
    echo "🚀 SESSION START DETECTED FOR CHRISTIAN"
    echo "Triggering automatic 120-minute timing enforcement..."
    echo ""
    
    # Source and execute timing enforcement
    source "$(dirname "$0")/timing_enforcement.sh"
    
    echo ""
    echo "🎯 SESSION READY FOR CHRISTIAN"
    echo "⏰ Timing rules active and verified"
    echo "📋 Project state current and backed up"
else
    echo "ℹ️ No session start trigger detected"
    echo "To manually execute timing checks, run: ./scripts/timing_enforcement.sh"
fi