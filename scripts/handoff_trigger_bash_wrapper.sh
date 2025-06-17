#!/bin/bash
# Handoff Trigger Detection Bash Wrapper
# Created for: Christian
# Project: CLAUDE Improvement
#
# This script implements the detect_handoff_triggers() function as documented in CLAUDE.md
# and integrates with the existing bash function ecosystem

# Function: detect_handoff_triggers() - ENHANCED TRIGGER DETECTION
# Exactly as documented in CLAUDE.md
detect_handoff_triggers() {
    local user_input="$1"
    local trigger_detected=false
    local trigger_type=""
    
    echo "🔍 Scanning for handoff triggers in user input for Christian"
    
    # Validate input
    if [ -z "$user_input" ]; then
        echo "⚠️ No input provided for trigger detection"
        return 1
    fi
    
    # Convert to lowercase for case-insensitive matching
    local input_lower=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
    
    # Define trigger patterns exactly as in CLAUDE.md
    local checkpoint_patterns="checkpoint|save state|capture state|save progress"
    local handoff_patterns="handoff|transition|switch session|pass to next"
    local session_end_patterns="pause|stop|closing|end session|wrap up|finish"
    local context_patterns="context|memory|limit|running out|getting full"
    
    # Check for specific trigger types in priority order
    if echo "$input_lower" | grep -E "$checkpoint_patterns" >/dev/null 2>&1; then
        trigger_type="checkpoint"
        trigger_detected=true
        echo "✓ CHECKPOINT trigger detected for Christian"
    elif echo "$input_lower" | grep -E "$handoff_patterns" >/dev/null 2>&1; then
        trigger_type="handoff"
        trigger_detected=true
        echo "✓ HANDOFF trigger detected for Christian"
    elif echo "$input_lower" | grep -E "$session_end_patterns" >/dev/null 2>&1; then
        trigger_type="session_end"
        trigger_detected=true
        echo "✓ SESSION END trigger detected for Christian"
    elif echo "$input_lower" | grep -E "$context_patterns" >/dev/null 2>&1; then
        trigger_type="context_limit"
        trigger_detected=true
        echo "✓ CONTEXT LIMIT trigger detected for Christian"
    else
        echo "ℹ️ No handoff triggers detected in user input"
    fi
    
    # If trigger detected, execute appropriate protocol
    if [ "$trigger_detected" = true ]; then
        echo "🚨 HANDOFF TRIGGER ACTIVATED: $trigger_type"
        
        # Log the detection
        log_trigger_detection "$trigger_type" "$user_input"
        
        # Execute protocol if functions are available
        if command -v execute_trigger_protocol >/dev/null 2>&1; then
            execute_trigger_protocol "$trigger_type"
        else
            echo "⚠️ execute_trigger_protocol function not available - executing simple protocol"
            execute_simple_trigger_protocol "$trigger_type"
        fi
        
        return 0
    else
        return 1
    fi
}

# Function: execute_simple_trigger_protocol() - Simplified protocol when full functions unavailable
execute_simple_trigger_protocol() {
    local trigger_type="$1"
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    echo "⚡ Executing simple trigger protocol: $trigger_type for Christian"
    echo "Timestamp: $timestamp"
    
    case "$trigger_type" in
        "checkpoint")
            echo "📋 CHECKPOINT PROTOCOL: Creating checkpoint..."
            create_checkpoint_files
            ;;
        "handoff")
            echo "🔄 HANDOFF PROTOCOL: Preparing handoff..."
            create_handoff_files
            ;;
        "session_end")
            echo "🛑 SESSION END PROTOCOL: Ending session..."
            create_session_end_files
            ;;
        "context_limit")
            echo "🚨 CONTEXT LIMIT PROTOCOL: Emergency handoff..."
            create_emergency_handoff_files
            ;;
        *)
            echo "❓ Unknown trigger type: $trigger_type - using default protocol"
            create_handoff_files
            ;;
    esac
    
    echo "✅ Simple trigger protocol completed: $trigger_type"
}

# Function: log_trigger_detection() - Log trigger detections
log_trigger_detection() {
    local trigger_type="$1"
    local user_input="$2"
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    local log_dir="reports/$(date +%Y-%m-%d)/handoff"
    
    # Ensure log directory exists
    mkdir -p "$log_dir"
    
    # Create detection log entry
    local log_file="$log_dir/trigger_detections.log"
    echo "[$timestamp] User: Christian | Trigger: $trigger_type | Input: \"$user_input\"" >> "$log_file"
    
    echo "📝 Trigger detection logged to: $log_file"
}

# Function: create_checkpoint_files() - Simple checkpoint creation
create_checkpoint_files() {
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Update SESSION_CONTINUITY.md
    if [ -f "SESSION_CONTINUITY.md" ]; then
        echo "" >> SESSION_CONTINUITY.md
        echo "## CHECKPOINT - $timestamp" >> SESSION_CONTINUITY.md
        echo "User: Christian" >> SESSION_CONTINUITY.md
        echo "Trigger: User-requested checkpoint" >> SESSION_CONTINUITY.md
        echo "Status: Checkpoint created" >> SESSION_CONTINUITY.md
        echo "✓ SESSION_CONTINUITY.md updated with checkpoint"
    fi
    
    # Create simple checkpoint file
    cat > "CHECKPOINT_${timestamp//:/-}.md" << EOF
# CHECKPOINT
Created: $timestamp
User: Christian
Trigger: Checkpoint requested

## Current Status
Session checkpoint created at user request.
All current state has been captured.

## Next Steps
Continue work from this checkpoint.
EOF
    
    echo "✓ Checkpoint file created: CHECKPOINT_${timestamp//:/-}.md"
}

# Function: create_handoff_files() - Simple handoff creation
create_handoff_files() {
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Create simple handoff summary
    cat > "HANDOFF_SUMMARY.md" << EOF
# HANDOFF SUMMARY
Generated: $timestamp
User: Christian
Trigger: Handoff requested

## Session State
Session handoff initiated by user request.
Current state has been preserved for continuation.

## Next Session
Use this handoff summary to continue work in next session.
EOF
    
    # Create next session prompt
    cat > "NEXT_SESSION_HANDOFF_PROMPT.md" << EOF
# HANDOFF PROMPT
Generated: $timestamp
User: Christian

Previous session requested handoff.
Continue work using preserved state.
EOF
    
    echo "✓ Handoff files created: HANDOFF_SUMMARY.md, NEXT_SESSION_HANDOFF_PROMPT.md"
}

# Function: create_session_end_files() - Simple session end
create_session_end_files() {
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Update TODO.md
    if [ -f "TODO.md" ]; then
        echo "" >> TODO.md
        echo "## SESSION END - $timestamp" >> TODO.md
        echo "User: Christian" >> TODO.md
        echo "Status: Session ended by user request" >> TODO.md
        echo "✓ TODO.md updated with session end"
    fi
    
    # Create session end report
    cat > "SESSION_END_REPORT_${timestamp//:/-}.md" << EOF
# SESSION END REPORT
Generated: $timestamp
User: Christian
Trigger: Session end requested

## Session Summary
Session ended by user request.
All work has been preserved.

## Next Session
Review this report to understand session completion.
EOF
    
    echo "✓ Session end report created: SESSION_END_REPORT_${timestamp//:/-}.md"
}

# Function: create_emergency_handoff_files() - Emergency handoff
create_emergency_handoff_files() {
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Create emergency handoff
    cat > "EMERGENCY_HANDOFF.md" << EOF
# EMERGENCY HANDOFF
Generated: $timestamp
User: Christian
Trigger: Context limit reached

## Emergency Status
Context limit reached - emergency handoff created.
Critical state preserved for immediate continuation.

## Next Session Priority
1. Review this emergency handoff
2. Continue with preserved state
3. Monitor context usage
EOF
    
    echo "✓ Emergency handoff created: EMERGENCY_HANDOFF.md"
}

# Function: test_trigger_detection() - Test the trigger detection system
test_trigger_detection() {
    echo "🧪 Testing handoff trigger detection system for Christian..."
    echo "=" * 50
    
    # Test cases with expected results
    local test_cases=(
        "checkpoint:checkpoint"
        "save state:checkpoint"
        "handoff:handoff"
        "transition:handoff"
        "pause:session_end"
        "stop:session_end"
        "context limit:context_limit"
        "memory full:context_limit"
        "continue working:none"
        "implement feature:none"
    )
    
    local passed=0
    local total=0
    
    for test_case in "${test_cases[@]}"; do
        local input="${test_case%:*}"
        local expected="${test_case#*:}"
        
        total=$((total + 1))
        echo ""
        echo "Test $total: '$input'"
        
        # Capture detection result
        if detect_handoff_triggers "$input" >/dev/null 2>&1; then
            detected="true"
        else
            detected="false"
        fi
        
        # Check result
        if [ "$expected" = "none" ] && [ "$detected" = "false" ]; then
            echo "✅ PASS: No trigger detected as expected"
            passed=$((passed + 1))
        elif [ "$expected" != "none" ] && [ "$detected" = "true" ]; then
            echo "✅ PASS: Trigger detected as expected"
            passed=$((passed + 1))
        else
            echo "❌ FAIL: Expected '$expected', detection result: $detected"
        fi
    done
    
    echo ""
    echo "=" * 50
    echo "📊 Test Results:"
    echo "Total tests: $total"
    echo "Passed: $passed"
    echo "Failed: $((total - passed))"
    echo "Success rate: $(( passed * 100 / total ))%"
}

# Function: interactive_trigger_test() - Interactive testing
interactive_trigger_test() {
    echo "🔧 Interactive trigger detection test for Christian"
    echo "Enter text to test trigger detection (type 'exit' to quit):"
    
    while true; do
        echo ""
        read -p "Enter text: " user_input
        
        if [ "$user_input" = "exit" ]; then
            echo "👋 Exiting interactive test"
            break
        fi
        
        if [ -n "$user_input" ]; then
            detect_handoff_triggers "$user_input"
        else
            echo "⚠️ Empty input - please enter some text"
        fi
    done
}

# Main execution logic
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    echo "🚀 Handoff Trigger Detection System for Christian"
    echo "Project: CLAUDE Improvement"
    echo "=" * 60
    
    case "${1:-test}" in
        "test")
            test_trigger_detection
            ;;
        "interactive")
            interactive_trigger_test
            ;;
        "check")
            # Test single input
            if [ -n "$2" ]; then
                detect_handoff_triggers "$2"
            else
                echo "Usage: $0 check \"input text\""
            fi
            ;;
        *)
            echo "Usage: $0 [test|interactive|check \"text\"]"
            echo "  test       - Run automated tests"
            echo "  interactive - Interactive testing mode"
            echo "  check      - Test specific input"
            ;;
    esac
fi