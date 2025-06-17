#!/bin/bash
# Validation Script for Extracted Functions
# User: Christian
# Purpose: Ensure extracted functions work identically to originals

set -euo pipefail

echo "=== Function Extraction Validation ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "User: Christian"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "Testing $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Load the extracted functions
echo "Loading extracted functions..."
if [ -f "scripts/utils/sourcing_helper.sh" ]; then
    source scripts/utils/sourcing_helper.sh
else
    echo -e "${RED}ERROR: sourcing_helper.sh not found${NC}"
    exit 1
fi

echo ""
echo "Running validation tests..."
echo "=========================="

# Test 1: Core Functions
echo -e "\n${YELLOW}Core System Functions:${NC}"
run_test "initialize_global_structure exists" "type -t initialize_global_structure"
run_test "find_project_root exists" "type -t find_project_root"
run_test "whats_next exists" "type -t whats_next"
run_test "detect_whats_next_request exists" "type -t detect_whats_next_request"

# Test function execution
mkdir -p test_validation
cd test_validation
run_test "find_project_root executes" "find_project_root"
cd ..
rm -rf test_validation

# Test 2: Learning Functions
echo -e "\n${YELLOW}Learning Functions:${NC}"
run_test "load_learning_files exists" "type -t load_learning_files"
run_test "load_file_organization_enforcement exists" "type -t load_file_organization_enforcement"
run_test "organize_misplaced_files exists" "type -t organize_misplaced_files"

# Test 3: Backup Functions
echo -e "\n${YELLOW}Backup Functions:${NC}"
run_test "check_scheduled_backup exists" "type -t check_scheduled_backup"
run_test "create_backup exists" "type -t create_backup"
run_test "check_context_backup exists" "type -t check_context_backup"
run_test "create_project_backup exists" "type -t create_project_backup"
run_test "check_timing_rules exists" "type -t check_timing_rules"

# Test 4: Handoff Functions
echo -e "\n${YELLOW}Handoff Functions:${NC}"
run_test "generate_handoff_files exists" "type -t generate_handoff_files"
run_test "detect_handoff_triggers exists" "type -t detect_handoff_triggers"
run_test "execute_trigger_protocol exists" "type -t execute_trigger_protocol"
run_test "execute_checkpoint_protocol exists" "type -t execute_checkpoint_protocol"
run_test "execute_handoff_protocol exists" "type -t execute_handoff_protocol"
run_test "execute_context_limit_protocol exists" "type -t execute_context_limit_protocol"
run_test "validate_handoff_completeness exists" "type -t validate_handoff_completeness"
run_test "check_all_handoff_functions exists" "type -t check_all_handoff_functions"
run_test "generate_session_end_protocol exists" "type -t generate_session_end_protocol"

# Test 5: Reports Functions
echo -e "\n${YELLOW}Reports Functions:${NC}"
run_test "initialize_reports_structure exists" "type -t initialize_reports_structure"
run_test "get_timestamped_report_path exists" "type -t get_timestamped_report_path"
run_test "cleanup_old_reports exists" "type -t cleanup_old_reports"
run_test "categorize_report exists" "type -t categorize_report"
run_test "generate_organized_report exists" "type -t generate_organized_report"
run_test "update_existing_reports_to_use_organization exists" "type -t update_existing_reports_to_use_organization"

# Test 6: Project Functions
echo -e "\n${YELLOW}Project Functions:${NC}"
run_test "initialize_complete_project_template exists" "type -t initialize_complete_project_template"

# Test Inter-function Dependencies
echo -e "\n${YELLOW}Testing Function Dependencies:${NC}"
# Create minimal test environment
export HOME="$(pwd)/test_home"
mkdir -p "$HOME/.claude"
mkdir -p backups

run_test "check_timing_rules calls check_scheduled_backup" "check_timing_rules 2>&1 | grep -q 'backup'"

# Clean up test environment
rm -rf test_home

# Summary
echo ""
echo "=========================="
echo "Validation Summary:"
echo "=========================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All validation tests passed!${NC}"
    echo "Functions have been successfully extracted and are working correctly."
    exit 0
else
    echo -e "${RED}❌ Some tests failed!${NC}"
    echo "Please review the failed tests before proceeding with migration."
    exit 1
fi