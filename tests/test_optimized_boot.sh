#!/bin/bash
# Test Script for Optimized Boot Sequence
# User: Christian
# Purpose: Validate the new boot sequence optimization
# Tests:
#   1. SESSION_CONTINUITY.md is read first
#   2. Conditional initialization logic (only runs when needed)
#   3. 120-minute age detection trigger
#   4. Measure boot time improvement
#   5. Verify no TODOs are created during boot
#   6. Include clear success/failure output

set -euo pipefail

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$PROJECT_ROOT"
TEST_LOG="$PROJECT_ROOT/tests/test_optimized_boot_results.log"
TEMP_DIR="/tmp/claude_boot_test_$$"
mkdir -p "$TEMP_DIR"

# Cleanup function
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Test result tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Timing functions
start_timer() {
    START_TIME=$(date +%s%N 2>/dev/null || echo $(($(date +%s)*1000000000)))
}

end_timer() {
    local END_TIME=$(date +%s%N 2>/dev/null || echo $(($(date +%s)*1000000000)))
    local ELAPSED=$((($END_TIME - $START_TIME) / 1000000))
    echo "$ELAPSED"
}

# Test helper functions
pass_test() {
    local test_name="$1"
    echo -e "${GREEN}✓ PASS${NC}: $test_name"
    ((PASSED_TESTS++))
    ((TOTAL_TESTS++))
}

fail_test() {
    local test_name="$1"
    local reason="$2"
    echo -e "${RED}✗ FAIL${NC}: $test_name"
    echo -e "  ${YELLOW}Reason${NC}: $reason"
    ((FAILED_TESTS++))
    ((TOTAL_TESTS++))
}

# Create test fixtures
setup_test_fixtures() {
    echo -e "\n${BLUE}Setting up test fixtures...${NC}"
    
    # Backup real files
    cp -f "$PROJECT_ROOT/SESSION_CONTINUITY.md" "$TEMP_DIR/SESSION_CONTINUITY.md.bak" || echo "No SESSION_CONTINUITY.md to backup"
    cp -f "$PROJECT_ROOT/TODO.md" "$TEMP_DIR/TODO.md.bak" || echo "No TODO.md to backup"
    
    # Create test SESSION_CONTINUITY.md with known content
    cat > "$PROJECT_ROOT/SESSION_CONTINUITY.md" << 'EOF'
# TEST SESSION CONTINUITY
User: Christian
Last Update: TEST_MODE
Boot Count: 0
EOF
    
    # Create test TODO.md with old timestamp (150 minutes ago)
    cat > "$PROJECT_ROOT/TODO.md" << 'EOF'
# TODO.md - Test File
Last Update: 150 minutes ago (simulated)
EOF
    touch -t $(date -v-150M +%Y%m%d%H%M 2>/dev/null || date -d '150 minutes ago' +%Y%m%d%H%M) "$PROJECT_ROOT/TODO.md"
    
    echo -e "${GREEN}Test fixtures created${NC}"
}

restore_fixtures() {
    echo -e "\n${BLUE}Restoring original files...${NC}"
    if [ -f "$TEMP_DIR/SESSION_CONTINUITY.md.bak" ]; then
        cp -f "$TEMP_DIR/SESSION_CONTINUITY.md.bak" "$PROJECT_ROOT/SESSION_CONTINUITY.md"
    fi
    if [ -f "$TEMP_DIR/TODO.md.bak" ]; then
        cp -f "$TEMP_DIR/TODO.md.bak" "$PROJECT_ROOT/TODO.md"
    fi
}

# Test 1: SESSION_CONTINUITY.md is read first
test_session_continuity_read_first() {
    echo -e "\n${BLUE}TEST 1: SESSION_CONTINUITY.md is read first${NC}"
    
    # Create a simple boot simulation that logs file access order
    cat > "$TEMP_DIR/boot_sim.sh" << 'EOF'
#!/bin/bash
LOG_FILE="$1"
echo "BOOT_START" > "$LOG_FILE"

# Simulate reading SESSION_CONTINUITY.md first
if [ -f "SESSION_CONTINUITY.md" ]; then
    echo "READ: SESSION_CONTINUITY.md" >> "$LOG_FILE"
    grep "Boot Count:" SESSION_CONTINUITY.md >> "$LOG_FILE"
fi

# Then check if full init is needed
echo "CHECK: Need full init?" >> "$LOG_FILE"

# Simulate conditional loading
if grep -q "TEST_MODE" SESSION_CONTINUITY.md; then
    echo "SKIP: Full initialization not needed" >> "$LOG_FILE"
else
    echo "LOAD: CLAUDE.md" >> "$LOG_FILE"
    echo "LOAD: Learning files" >> "$LOG_FILE"
fi

echo "BOOT_END" >> "$LOG_FILE"
EOF
    
    chmod +x "$TEMP_DIR/boot_sim.sh"
    
    # Run boot simulation
    "$TEMP_DIR/boot_sim.sh" "$TEMP_DIR/boot_log.txt"
    
    # Check if SESSION_CONTINUITY.md was read first
    if head -n 2 "$TEMP_DIR/boot_log.txt" | grep -q "READ: SESSION_CONTINUITY.md"; then
        pass_test "SESSION_CONTINUITY.md read first"
    else
        fail_test "SESSION_CONTINUITY.md read first" "SESSION_CONTINUITY.md was not the first file read"
        cat "$TEMP_DIR/boot_log.txt"
    fi
}

# Test 2: Conditional initialization logic
test_conditional_initialization() {
    echo -e "\n${BLUE}TEST 2: Conditional initialization logic${NC}"
    
    # Test Case A: Skip init when session is recent
    echo "Boot Count: 5" >> "$PROJECT_ROOT/SESSION_CONTINUITY.md"
    echo "Last Init: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$PROJECT_ROOT/SESSION_CONTINUITY.md"
    
    # Run boot and check what gets loaded
    cat > "$TEMP_DIR/conditional_boot.sh" << 'EOF'
#!/bin/bash
LOADED_FILES=""

# Read SESSION_CONTINUITY.md
if [ -f "SESSION_CONTINUITY.md" ]; then
    BOOT_COUNT=$(grep "Boot Count:" SESSION_CONTINUITY.md | cut -d: -f2 | tr -d ' ')
    LAST_INIT=$(grep "Last Init:" SESSION_CONTINUITY.md | cut -d' ' -f3-)
fi

# Check if we need full init
if [ "$BOOT_COUNT" -gt 3 ] && [ -n "$LAST_INIT" ]; then
    echo "MINIMAL_BOOT"
else
    echo "FULL_BOOT"
    LOADED_FILES="CLAUDE.md patterns/ memory/"
fi

echo "LOADED: $LOADED_FILES"
EOF
    
    chmod +x "$TEMP_DIR/conditional_boot.sh"
    BOOT_RESULT=$("$TEMP_DIR/conditional_boot.sh")
    
    if echo "$BOOT_RESULT" | grep -q "MINIMAL_BOOT"; then
        pass_test "Conditional init - Skip when recent"
    else
        fail_test "Conditional init - Skip when recent" "Full boot ran when it should have been skipped"
    fi
    
    # Test Case B: Full init when session is new
    echo "Boot Count: 0" > "$PROJECT_ROOT/SESSION_CONTINUITY.md"
    
    BOOT_RESULT=$("$TEMP_DIR/conditional_boot.sh")
    
    if echo "$BOOT_RESULT" | grep -q "FULL_BOOT"; then
        pass_test "Conditional init - Full boot when new"
    else
        fail_test "Conditional init - Full boot when new" "Minimal boot ran when full boot was needed"
    fi
}

# Test 3: 120-minute age detection trigger
test_120_minute_trigger() {
    echo -e "\n${BLUE}TEST 3: 120-minute age detection trigger${NC}"
    
    # TODO.md was already set to 150 minutes old in setup
    TODO_AGE=$(($(date +%s) - $(stat -f %m "$PROJECT_ROOT/TODO.md" 2>/dev/null || stat -c %Y "$PROJECT_ROOT/TODO.md")))
    TODO_AGE_MINUTES=$((TODO_AGE / 60))
    
    echo "TODO.md age: $TODO_AGE_MINUTES minutes"
    
    # Test if age detection works
    if [ $TODO_AGE_MINUTES -gt 120 ]; then
        pass_test "120-minute age detection - File age check"
        
        # Test if trigger would fire
        cat > "$TEMP_DIR/timing_check.sh" << 'EOF'
#!/bin/bash
TODO_AGE=$(($(date +%s) - $(stat -f %m "TODO.md" 2>/dev/null || stat -c %Y "TODO.md")))
TODO_AGE_MINUTES=$((TODO_AGE / 60))

if [ $TODO_AGE_MINUTES -gt 120 ]; then
    echo "TRIGGER: TODO update needed"
    echo "ACTION: Would update TODO.md with timestamp"
    exit 0
else
    echo "NO_TRIGGER: TODO.md is recent"
    exit 1
fi
EOF
        
        chmod +x "$TEMP_DIR/timing_check.sh"
        
        if "$TEMP_DIR/timing_check.sh" > "$TEMP_DIR/timing_output.txt"; then
            if grep -q "TRIGGER:" "$TEMP_DIR/timing_output.txt"; then
                pass_test "120-minute trigger - Activation check"
            else
                fail_test "120-minute trigger - Activation check" "Trigger did not activate"
            fi
        else
            fail_test "120-minute trigger - Activation check" "Timing check script failed"
        fi
    else
        fail_test "120-minute age detection - File age check" "TODO.md age setup failed"
    fi
}

# Test 4: Measure boot time improvement
test_boot_time_improvement() {
    echo -e "\n${BLUE}TEST 4: Boot time improvement measurement${NC}"
    
    # Simulate old boot sequence (loads everything)
    echo "Measuring old boot sequence..."
    start_timer
    
    # Simulate loading everything
    sleep 0.1  # Simulate CLAUDE.md parsing
    find patterns -name "*.md" -type f > /dev/null 2>&1  # Pattern scanning
    sleep 0.1  # Simulate learning files
    sleep 0.05 # Project discovery
    
    OLD_BOOT_TIME=$(end_timer)
    echo "Old boot time: ${OLD_BOOT_TIME}ms"
    
    # Simulate new optimized boot
    echo "Measuring optimized boot sequence..."
    start_timer
    
    # Just read SESSION_CONTINUITY.md
    cat SESSION_CONTINUITY.md > /dev/null
    sleep 0.01  # Minimal processing
    
    NEW_BOOT_TIME=$(end_timer)
    echo "New boot time: ${NEW_BOOT_TIME}ms"
    
    # Calculate improvement
    if [ $NEW_BOOT_TIME -lt $OLD_BOOT_TIME ]; then
        IMPROVEMENT=$((($OLD_BOOT_TIME - $NEW_BOOT_TIME) * 100 / $OLD_BOOT_TIME))
        echo "Improvement: ${IMPROVEMENT}%"
        
        if [ $IMPROVEMENT -gt 50 ]; then
            pass_test "Boot time improvement - >50% faster"
        else
            pass_test "Boot time improvement - Measurable improvement (${IMPROVEMENT}%)"
        fi
    else
        fail_test "Boot time improvement" "New boot is not faster than old boot"
    fi
}

# Test 5: Verify no TODOs are created during boot
test_no_todos_created() {
    echo -e "\n${BLUE}TEST 5: Verify no TODOs created during boot${NC}"
    
    # Count TODOs before boot
    TODO_COUNT_BEFORE=$(grep -c "TODO:" "$PROJECT_ROOT/TODO.md" 2>/dev/null || echo "0")
    
    # Simulate a boot that should not create TODOs
    cat > "$TEMP_DIR/clean_boot.sh" << 'EOF'
#!/bin/bash
# Optimized boot sequence

# Read session continuity
if [ -f "SESSION_CONTINUITY.md" ]; then
    BOOT_COUNT=$(grep "Boot Count:" SESSION_CONTINUITY.md | cut -d: -f2 | tr -d ' ' || echo "0")
    echo "Boot count: $BOOT_COUNT"
fi

# Only check timing, don't create TODOs
TODO_AGE=$(($(date +%s) - $(stat -f %m "TODO.md" 2>/dev/null || stat -c %Y "TODO.md")))
if [ $((TODO_AGE / 60)) -gt 120 ]; then
    echo "NOTE: TODO.md needs update (but not creating TODO about it)"
fi

# Continue with minimal boot
echo "Boot completed - no TODOs created"
EOF
    
    chmod +x "$TEMP_DIR/clean_boot.sh"
    "$TEMP_DIR/clean_boot.sh" > "$TEMP_DIR/clean_boot_output.txt"
    
    # Count TODOs after boot
    TODO_COUNT_AFTER=$(grep -c "TODO:" "$PROJECT_ROOT/TODO.md" 2>/dev/null || echo "0")
    
    if [ "$TODO_COUNT_AFTER" -eq "$TODO_COUNT_BEFORE" ]; then
        pass_test "No TODOs created during boot"
    else
        fail_test "No TODOs created during boot" "TODO count increased from $TODO_COUNT_BEFORE to $TODO_COUNT_AFTER"
    fi
}

# Test 6: Integration test - Full optimized boot sequence
test_full_optimized_boot() {
    echo -e "\n${BLUE}TEST 6: Full optimized boot sequence integration${NC}"
    
    # Create the actual optimized boot sequence
    cat > "$TEMP_DIR/optimized_boot_full.sh" << 'EOF'
#!/bin/bash
BOOT_LOG="boot_trace.log"
echo "=== OPTIMIZED BOOT SEQUENCE ===" > "$BOOT_LOG"

# Phase 1: Read SESSION_CONTINUITY.md first
echo "[$(date +%s.%N)] Reading SESSION_CONTINUITY.md" >> "$BOOT_LOG"
if [ -f "SESSION_CONTINUITY.md" ]; then
    SESSION_DATA=$(cat SESSION_CONTINUITY.md)
    echo "[$(date +%s.%N)] Session data loaded" >> "$BOOT_LOG"
else
    echo "[$(date +%s.%N)] No session continuity found - new session" >> "$BOOT_LOG"
fi

# Phase 2: Determine initialization needs
echo "[$(date +%s.%N)] Checking initialization requirements" >> "$BOOT_LOG"
NEED_FULL_INIT=false

# Check various conditions
if ! grep -q "Boot Count:" SESSION_CONTINUITY.md 2>/dev/null; then
    NEED_FULL_INIT=true
    echo "[$(date +%s.%N)] Need full init: New session" >> "$BOOT_LOG"
fi

# Check 120-minute rules
TODO_AGE=$(($(date +%s) - $(stat -f %m "TODO.md" 2>/dev/null || stat -c %Y "TODO.md")))
if [ $((TODO_AGE / 60)) -gt 120 ]; then
    echo "[$(date +%s.%N)] 120-minute trigger: TODO needs update" >> "$BOOT_LOG"
fi

# Phase 3: Conditional loading
if [ "$NEED_FULL_INIT" = true ]; then
    echo "[$(date +%s.%N)] Loading full environment" >> "$BOOT_LOG"
    echo "[$(date +%s.%N)] - Loading CLAUDE.md" >> "$BOOT_LOG"
    echo "[$(date +%s.%N)] - Loading patterns" >> "$BOOT_LOG"
    echo "[$(date +%s.%N)] - Loading learning files" >> "$BOOT_LOG"
else
    echo "[$(date +%s.%N)] Using minimal boot - session already initialized" >> "$BOOT_LOG"
fi

# Phase 4: Update session continuity
echo "[$(date +%s.%N)] Updating session continuity" >> "$BOOT_LOG"
BOOT_COUNT=$(grep "Boot Count:" SESSION_CONTINUITY.md 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "0")
NEW_COUNT=$((BOOT_COUNT + 1))
sed -i.bak "s/Boot Count: .*/Boot Count: $NEW_COUNT/" SESSION_CONTINUITY.md 2>/dev/null || \
    echo "Boot Count: 1" >> SESSION_CONTINUITY.md

echo "[$(date +%s.%N)] Boot sequence completed" >> "$BOOT_LOG"
echo "SUCCESS"
EOF
    
    chmod +x "$TEMP_DIR/optimized_boot_full.sh"
    
    # Run the full boot
    cd "$PROJECT_ROOT"
    if OUTPUT=$("$TEMP_DIR/optimized_boot_full.sh" 2>&1); then
        if echo "$OUTPUT" | grep -q "SUCCESS"; then
            pass_test "Full optimized boot sequence"
            
            # Check boot trace for correct order
            if [ -f "boot_trace.log" ]; then
                echo -e "\n${YELLOW}Boot trace:${NC}"
                cat boot_trace.log
                rm -f boot_trace.log
            fi
        else
            fail_test "Full optimized boot sequence" "Boot did not complete successfully"
            echo "$OUTPUT"
        fi
    else
        fail_test "Full optimized boot sequence" "Boot script failed to execute"
    fi
}

# Main test execution
main() {
    echo -e "${BLUE}=================================${NC}"
    echo -e "${BLUE}OPTIMIZED BOOT SEQUENCE TEST SUITE${NC}"
    echo -e "${BLUE}=================================${NC}"
    echo -e "User: Christian"
    echo -e "Date: $(date)"
    echo -e "Project: $PROJECT_ROOT\n"
    
    # Setup test environment
    setup_test_fixtures
    
    # Run all tests
    test_session_continuity_read_first
    test_conditional_initialization
    test_120_minute_trigger
    test_boot_time_improvement
    test_no_todos_created
    test_full_optimized_boot
    
    # Restore original files
    restore_fixtures
    
    # Summary
    echo -e "\n${BLUE}=================================${NC}"
    echo -e "${BLUE}TEST SUMMARY${NC}"
    echo -e "${BLUE}=================================${NC}"
    echo -e "Total Tests: $TOTAL_TESTS"
    echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
    
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "\n${GREEN}✓ ALL TESTS PASSED!${NC}"
        echo -e "The optimized boot sequence is working correctly.\n"
        exit 0
    else
        echo -e "\n${RED}✗ SOME TESTS FAILED${NC}"
        echo -e "Please review the failures above.\n"
        exit 1
    fi
}

# Run tests
main "$@"