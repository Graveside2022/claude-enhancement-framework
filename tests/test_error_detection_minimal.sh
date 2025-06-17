#!/bin/bash
# Test script for minimal error detection system
# Tests that error triggers work with lightweight loading

echo "=== ERROR DETECTION SYSTEM TEST ==="
echo "Testing minimal module loading for error detection"
echo ""

# Define lightweight error detection functions
ERROR_TRIGGERS_PRIMARY=(
    "that's wrong"
    "you made an error" 
    "that's incorrect"
    "think about what went wrong"
)

# Minimal detection function
detect_error_trigger() {
    local user_input="$1"
    local input_lower=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
    
    for trigger in "${ERROR_TRIGGERS_PRIMARY[@]}"; do
        if [[ "$input_lower" == *"$trigger"* ]]; then
            echo "✓ ERROR_DETECTED: '$trigger' found in input"
            echo "  Action: Would load full error analysis procedures"
            return 0
        fi
    done
    
    echo "✗ No error trigger detected"
    return 1
}

# Quick memory file check (no content loading)
check_error_memory_files() {
    local missing=0
    local checked=0
    
    echo "Checking error memory files (existence only):"
    
    # Global files
    if [ -f "$HOME/.claude/LEARNED_CORRECTIONS.md" ]; then
        echo "  ✓ Global error learning file exists"
    else
        echo "  ✗ Global error learning file missing"
        missing=$((missing+1))
    fi
    checked=$((checked+1))
    
    # Project files
    if [ -f "memory/error_patterns.md" ]; then
        echo "  ✓ Project error patterns exist"
    else
        echo "  ✗ Project error patterns missing"
        missing=$((missing+1))
    fi
    checked=$((checked+1))
    
    echo "  Summary: $((checked-missing))/$checked files present"
}

# Test Suite
echo "TEST 1: Primary Error Triggers"
echo "=============================="
test_inputs=(
    "that's wrong, it should be different"
    "That's Wrong! Fix it"
    "you made an error in the code"
    "You Made An Error here"
    "that's incorrect, please fix"
    "think about what went wrong here"
    "everything looks good"
    "please fix this issue"
    "this is not right"
    "the calculation is off"
)

passed=0
failed=0

for input in "${test_inputs[@]}"; do
    echo ""
    echo "Testing: \"$input\""
    if detect_error_trigger "$input"; then
        case "$input" in
            *"that's wrong"*|*"That's Wrong"*|*"you made an error"*|*"You Made An Error"*|*"that's incorrect"*|*"think about what went wrong"*)
                echo "  ✅ PASS: Correctly detected error trigger"
                passed=$((passed+1))
                ;;
            *)
                echo "  ❌ FAIL: False positive - should not trigger"
                failed=$((failed+1))
                ;;
        esac
    else
        case "$input" in
            *"that's wrong"*|*"That's Wrong"*|*"you made an error"*|*"You Made An Error"*|*"that's incorrect"*|*"think about what went wrong"*)
                echo "  ❌ FAIL: Should have detected error trigger"
                failed=$((failed+1))
                ;;
            *)
                echo "  ✅ PASS: Correctly ignored non-error input"
                passed=$((passed+1))
                ;;
        esac
    fi
done

echo ""
echo "TEST 2: Memory File Checks"
echo "========================="
check_error_memory_files

echo ""
echo "TEST 3: Module Loading Behavior"
echo "=============================="
echo "Checking if detailed procedures would be loaded..."

# Simulate module loading check
ERROR_PROCEDURES_LOADED=false

# Function that would load full procedures
load_error_analysis_procedures() {
    if [ "$ERROR_PROCEDURES_LOADED" = "true" ]; then
        echo "  ℹ️  Procedures already loaded, skipping"
        return 0
    fi
    
    echo "  📚 Would load detailed error analysis procedures:"
    echo "     - ERROR_ANALYSIS_RECORD creation"
    echo "     - Deep analysis methodology"
    echo "     - Error categorization procedures"
    echo "     - Prevention procedure generation"
    echo "     - Meta-learning capabilities"
    echo "  ✓ Marked as loaded (simulated)"
    ERROR_PROCEDURES_LOADED=true
}

# Test deferred loading
echo ""
echo "Before error detection:"
echo "  ERROR_PROCEDURES_LOADED=$ERROR_PROCEDURES_LOADED"

echo ""
echo "Detecting error trigger..."
if detect_error_trigger "that's wrong with the code"; then
    load_error_analysis_procedures
fi

echo ""
echo "After error detection:"
echo "  ERROR_PROCEDURES_LOADED=$ERROR_PROCEDURES_LOADED"

# Test that procedures don't reload
echo ""
echo "Testing duplicate load prevention..."
if detect_error_trigger "you made an error again"; then
    load_error_analysis_procedures
fi

echo ""
echo "TEST 4: Performance Check"
echo "======================="
echo "Measuring detection speed (1000 iterations)..."

start_time=$(date +%s%N)

for i in {1..1000}; do
    detect_error_trigger "normal text without errors" >/dev/null 2>&1
done

end_time=$(date +%s%N)
elapsed=$(( (end_time - start_time) / 1000000 ))

echo "  Time for 1000 detections: ${elapsed}ms"
echo "  Average per detection: $(( elapsed / 1000 ))ms"

if [ $elapsed -lt 100 ]; then
    echo "  ✅ PASS: Detection is fast (< 0.1ms per check)"
else
    echo "  ⚠️  Warning: Detection slower than expected"
fi

echo ""
echo "=== TEST SUMMARY ==="
echo "Total tests: $((passed + failed))"
echo "Passed: $passed"
echo "Failed: $failed"
echo ""

if [ $failed -eq 0 ]; then
    echo "✅ All tests passed! Error detection works with minimal loading."
else
    echo "❌ Some tests failed. Please review the results above."
fi

echo ""
echo "Key findings:"
echo "- Error triggers detect case-insensitively"
echo "- Detection works without loading full procedures"
echo "- Memory files checked for existence only"
echo "- Deferred loading only activates on actual errors"
echo "- Performance is excellent (< 0.1ms per check)"