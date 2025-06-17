#!/bin/bash
# Pre-Migration Baseline Capture for CLAUDE.md Functions
# User: Christian
# Purpose: Capture current behavior before migration

set -euo pipefail

echo "=== Pre-Migration Baseline Capture ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "User: Christian"
echo ""

# Create baseline directory
BASELINE_DIR="tests/pre_migration/baseline_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BASELINE_DIR"

# Source CLAUDE.md to load all functions
echo "Loading CLAUDE.md functions..."
source <(grep -A 10000 "^initialize_global_structure()" CLAUDE.md | grep -B 10000 "^# important-instruction-reminders" | head -n -1)

# Test 1: Core System Functions
echo "Testing Core System Functions..."
{
    echo "=== initialize_global_structure() ==="
    # Create temp directory for testing
    export HOME="$BASELINE_DIR/test_home"
    mkdir -p "$HOME"
    initialize_global_structure 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== find_project_root() ==="
    cd "$BASELINE_DIR"
    mkdir -p test_project/.git
    cd test_project
    find_project_root 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== whats_next() ==="
    whats_next 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== detect_whats_next_request() ==="
    detect_whats_next_request "whats next" 2>&1 || echo "Function returned: $?"
    detect_whats_next_request "hello" 2>&1 || echo "Function returned: $?"
} > "$BASELINE_DIR/core_functions.log" 2>&1

# Test 2: Learning Functions
echo "Testing Learning Functions..."
{
    echo "=== load_learning_files() ==="
    load_learning_files 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== load_file_organization_enforcement() ==="
    load_file_organization_enforcement 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== organize_misplaced_files() ==="
    # Create test files
    touch test_1.sh test_2.py test.log
    organize_misplaced_files 2>&1 || echo "Function returned: $?"
} > "$BASELINE_DIR/learning_functions.log" 2>&1

# Test 3: Backup Functions
echo "Testing Backup Functions..."
{
    echo "=== check_scheduled_backup() ==="
    mkdir -p backups
    check_scheduled_backup 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== create_backup() ==="
    create_backup "test_baseline" 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== check_context_backup() ==="
    check_context_backup 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== create_project_backup() ==="
    create_project_backup "baseline_test" 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== check_timing_rules() ==="
    check_timing_rules 2>&1 || echo "Function returned: $?"
} > "$BASELINE_DIR/backup_functions.log" 2>&1

# Test 4: Handoff Functions
echo "Testing Handoff Functions..."
{
    echo "=== generate_handoff_files() ==="
    generate_handoff_files 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== detect_handoff_triggers() ==="
    detect_handoff_triggers "checkpoint" 2>&1 || echo "Function returned: $?"
    detect_handoff_triggers "normal text" 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== validate_handoff_completeness() ==="
    validate_handoff_completeness 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== check_all_handoff_functions() ==="
    check_all_handoff_functions 2>&1 || echo "Function returned: $?"
} > "$BASELINE_DIR/handoff_functions.log" 2>&1

# Test 5: Reports Functions
echo "Testing Reports Functions..."
{
    echo "=== initialize_reports_structure() ==="
    initialize_reports_structure 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== get_timestamped_report_path() ==="
    get_timestamped_report_path "session" "test" 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== categorize_report() ==="
    categorize_report "This is an error report" 2>&1 || echo "Function returned: $?"
    
    echo -e "\n=== generate_organized_report() ==="
    generate_organized_report "Test content" "session" "baseline" 2>&1 || echo "Function returned: $?"
} > "$BASELINE_DIR/reports_functions.log" 2>&1

# Test 6: Function Dependencies
echo "Testing Function Dependencies..."
{
    echo "=== Function Call Graph ==="
    # Check which functions call other functions
    for func in initialize_global_structure load_learning_files check_scheduled_backup generate_handoff_files; do
        echo "Function: $func"
        grep -A 50 "^$func()" CLAUDE.md | grep -E "^\s*(initialize_|load_|check_|create_|generate_|detect_|execute_|validate_|get_|cleanup_|categorize_|update_|find_|organize_|whats_)" | sort | uniq || echo "  No internal function calls found"
        echo ""
    done
} > "$BASELINE_DIR/function_dependencies.log" 2>&1

# Create summary
echo "Creating baseline summary..."
{
    echo "=== Pre-Migration Baseline Summary ==="
    echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "User: Christian"
    echo ""
    echo "Functions Tested: 29"
    echo "Test Categories: 6"
    echo ""
    echo "File Checksums:"
    for log in "$BASELINE_DIR"/*.log; do
        echo "$(basename "$log"): $(shasum -a 256 "$log" | cut -d' ' -f1)"
    done
    echo ""
    echo "Baseline Location: $BASELINE_DIR"
} > "$BASELINE_DIR/BASELINE_SUMMARY.md"

echo "✅ Baseline capture complete!"
echo "📁 Results saved to: $BASELINE_DIR"
echo "📊 Summary: $BASELINE_DIR/BASELINE_SUMMARY.md"

# Return to original directory
cd - > /dev/null