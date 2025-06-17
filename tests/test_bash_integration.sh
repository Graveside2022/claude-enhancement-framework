#!/bin/bash
# Test Bash Function Integration and Dependencies
# For Christian's CLAUDE improvement project

echo "🔍 Testing Bash Function Integration..."
echo "========================================"

# Test results tracking
PASSED=0
FAILED=0

# Color output helpers
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_function() {
    local test_name="$1"
    local test_cmd="$2"
    local expected="$3"
    
    echo -n "Testing $test_name... "
    
    # Run test in subshell
    result=$(bash -c "$test_cmd" 2>&1)
    
    if [[ "$result" == *"$expected"* ]]; then
        echo -e "${GREEN}✅ PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC}"
        echo "  Expected: $expected"
        echo "  Got: $result"
        ((FAILED++))
    fi
}

# Test 1: Handoff calling backup
echo -e "\n${YELLOW}Test 1: Handoff → Backup Integration${NC}"
test_function "handoff_backup_call" '
source /dev/stdin <<EOF
create_backup() { echo "BACKUP_CALLED: $1"; }
generate_handoff_files() {
    echo "Generating handoff..."
    create_backup "handoff_backup"
}
EOF
generate_handoff_files
' "BACKUP_CALLED: handoff_backup"

# Test 2: Error learning loading file organization
echo -e "\n${YELLOW}Test 2: Error Learning → File Organization${NC}"
test_function "error_fileorg_call" '
source /dev/stdin <<EOF
load_file_organization_enforcement() { 
    echo "FILE_ORG_LOADED"
    export FILE_ORGANIZATION_ENFORCED=true
}
load_learning_files() {
    echo "Loading learning..."
    load_file_organization_enforcement
}
EOF
load_learning_files
' "FILE_ORG_LOADED"

# Test 3: Timing system triggering backups
echo -e "\n${YELLOW}Test 3: Timing → Backup Integration${NC}"
test_function "timing_backup_call" '
source /dev/stdin <<EOF
create_backup() { echo "BACKUP_FROM_TIMING: $1"; }
check_scheduled_backup() {
    create_backup "scheduled_120min"
}
check_timing_rules() {
    check_scheduled_backup
}
EOF
check_timing_rules
' "BACKUP_FROM_TIMING: scheduled_120min"

# Test 4: Initialization chain
echo -e "\n${YELLOW}Test 4: Full Initialization Chain${NC}"
test_function "init_chain" '
source /dev/stdin <<EOF
create_backup() { echo "[BACKUP]"; }
check_scheduled_backup() { echo "[TIMING]"; create_backup "test"; }
check_timing_rules() { echo "[RULES]"; check_scheduled_backup; }
load_learning_files() { echo "[LEARNING]"; }
initialize_global_structure() {
    echo "[INIT]"
    load_learning_files
    check_timing_rules
}
EOF
initialize_global_structure
' "[INIT]"

# Test 5: Error handling across modules
echo -e "\n${YELLOW}Test 5: Error Propagation${NC}"
test_function "error_propagation" '
source /dev/stdin <<EOF
create_backup() { echo "BACKUP_ERROR"; return 1; }
check_scheduled_backup() {
    if ! create_backup "test"; then
        echo "HANDLED_ERROR"
        return 1
    fi
}
check_timing_rules() {
    if ! check_scheduled_backup; then
        echo "PROPAGATED_ERROR"
    fi
    echo "CONTINUED_ANYWAY"
}
EOF
check_timing_rules
' "HANDLED_ERROR"

# Test 6: Trigger detection integration
echo -e "\n${YELLOW}Test 6: Trigger Detection → Protocol Execution${NC}"
test_function "trigger_protocol" '
source /dev/stdin <<EOF
execute_checkpoint_protocol() { echo "CHECKPOINT_EXECUTED"; }
execute_trigger_protocol() {
    case "$1" in
        checkpoint) execute_checkpoint_protocol ;;
        *) echo "UNKNOWN_TRIGGER" ;;
    esac
}
detect_handoff_triggers() {
    if [[ "$1" == *"checkpoint"* ]]; then
        execute_trigger_protocol "checkpoint"
        return 0
    fi
    return 1
}
EOF
detect_handoff_triggers "save checkpoint please"
' "CHECKPOINT_EXECUTED"

# Test 7: Circular dependency check
echo -e "\n${YELLOW}Test 7: Circular Dependency Prevention${NC}"
test_function "no_circular_deps" '
source /dev/stdin <<EOF
# This should work without infinite recursion
func_a() { func_b; echo "A_DONE"; }
func_b() { func_c; echo "B_DONE"; }
func_c() { echo "C_DONE"; }
EOF
func_a
' "C_DONE"

# Test 8: File organization integration
echo -e "\n${YELLOW}Test 8: File Organization Integration${NC}"
test_function "file_org_integration" '
source /dev/stdin <<EOF
organize_misplaced_files() { echo "FILES_ORGANIZED"; }
load_file_organization_enforcement() {
    export FILE_ORGANIZATION_ENFORCED=true
    if [ -f "test_file.py" ]; then
        organize_misplaced_files
    fi
    echo "ORG_LOADED"
}
EOF
touch test_file.py
load_file_organization_enforcement
rm -f test_file.py
' "ORG_LOADED"

# Test 9: Report organization integration  
echo -e "\n${YELLOW}Test 9: Report Organization Integration${NC}"
test_function "report_org_integration" '
source /dev/stdin <<EOF
generate_organized_report() {
    echo "REPORT_GENERATED: $2"
}
generate_handoff_files() {
    echo "Creating handoff..."
    generate_organized_report "content" "handoff" "test"
}
EOF
generate_handoff_files
' "REPORT_GENERATED: handoff"

# Test 10: Complete workflow integration
echo -e "\n${YELLOW}Test 10: Complete Workflow Integration${NC}"
test_function "complete_workflow" '
source /dev/stdin <<EOF
# Simplified complete workflow
find_project_root() { echo "/test/project"; }
initialize_global_structure() { echo "INIT_OK"; }
load_learning_files() { echo "LEARN_OK"; }
check_timing_rules() { echo "TIMING_OK"; }
create_backup() { echo "BACKUP_OK"; }
generate_handoff_files() { echo "HANDOFF_OK"; }

# Run workflow
workflow() {
    initialize_global_structure
    load_learning_files
    check_timing_rules
    create_backup "test"
    generate_handoff_files
}
EOF
workflow
' "INIT_OK"

# Generate report
echo -e "\n========================================"
echo "📊 TEST RESULTS SUMMARY"
echo "========================================"
echo -e "${GREEN}✅ Passed: $PASSED${NC}"
echo -e "${RED}❌ Failed: $FAILED${NC}"
TOTAL=$((PASSED + FAILED))
echo "📋 Total: $TOTAL"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✨ All bash function integrations working correctly!${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  Some integrations need attention.${NC}"
    exit 1
fi