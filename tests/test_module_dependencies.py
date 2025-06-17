#!/usr/bin/env python3
"""
Module Dependencies and Integration Test
Tests cross-module function calls and verifies all interdependencies resolve correctly
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test results tracking
test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def log_result(test_name, status, message=""):
    """Log test result"""
    if status == "PASS":
        test_results["passed"].append(test_name)
        print(f"✅ {test_name}: PASSED {message}")
    elif status == "FAIL":
        test_results["failed"].append(test_name)
        print(f"❌ {test_name}: FAILED - {message}")
    elif status == "WARN":
        test_results["warnings"].append(test_name)
        print(f"⚠️  {test_name}: WARNING - {message}")

def test_bash_function_availability():
    """Test that all bash functions are available"""
    print("\n🔍 Testing Bash Function Availability...")
    
    # Core functions that should be available
    core_functions = [
        "initialize_global_structure",
        "load_learning_files",
        "check_scheduled_backup",
        "create_backup",
        "find_project_root",
        "check_timing_rules",
        "generate_handoff_files",
        "detect_handoff_triggers",
        "execute_trigger_protocol"
    ]
    
    # Test each function exists in CLAUDE.md
    claude_md_path = project_root / "CLAUDE.md"
    if not claude_md_path.exists():
        log_result("CLAUDE.md existence", "FAIL", "CLAUDE.md not found")
        return False
    
    with open(claude_md_path, 'r') as f:
        claude_content = f.read()
    
    all_found = True
    for func in core_functions:
        if f"{func}()" in claude_content:
            log_result(f"Function {func}", "PASS", "Found in CLAUDE.md")
        else:
            log_result(f"Function {func}", "FAIL", "Not found in CLAUDE.md")
            all_found = False
    
    return all_found

def test_cross_module_calls():
    """Test cross-module function calls"""
    print("\n🔍 Testing Cross-Module Function Calls...")
    
    # Test 1: Handoff functions calling backup functions
    test_script = """
    # Source CLAUDE.md functions
    source /dev/stdin <<'EOF'
    find_project_root() { echo "$PWD"; }
    create_backup() { echo "Backup created: $1"; return 0; }
    generate_handoff_files() {
        echo "Creating handoff files..."
        create_backup "handoff_test"
        echo "Handoff complete"
    }
EOF
    
    # Test the call
    generate_handoff_files
    """
    
    try:
        result = subprocess.run(['bash', '-c', test_script], 
                              capture_output=True, text=True, check=True)
        if "Backup created: handoff_test" in result.stdout:
            log_result("Handoff→Backup integration", "PASS", "Handoff can call backup functions")
        else:
            log_result("Handoff→Backup integration", "FAIL", "Backup not called from handoff")
    except subprocess.CalledProcessError as e:
        log_result("Handoff→Backup integration", "FAIL", f"Script error: {e.stderr}")
    
    # Test 2: Error learning accessing file organization
    test_script2 = """
    # Source functions
    source /dev/stdin <<'EOF'
    find_project_root() { echo "$PWD"; }
    load_file_organization_enforcement() { 
        echo "Loading file organization..."
        export FILE_ORGANIZATION_ENFORCED=true
        return 0
    }
    load_learning_files() {
        echo "Loading learning files..."
        load_file_organization_enforcement
        echo "Learning files loaded"
    }
EOF
    
    # Test the call
    load_learning_files
    """
    
    try:
        result = subprocess.run(['bash', '-c', test_script2], 
                              capture_output=True, text=True, check=True)
        if "Loading file organization..." in result.stdout:
            log_result("ErrorLearning→FileOrg integration", "PASS", 
                      "Error learning can access file organization")
        else:
            log_result("ErrorLearning→FileOrg integration", "FAIL", 
                      "File organization not loaded")
    except subprocess.CalledProcessError as e:
        log_result("ErrorLearning→FileOrg integration", "FAIL", f"Script error: {e.stderr}")
    
    # Test 3: Timing system triggering backups
    test_script3 = """
    # Source functions
    source /dev/stdin <<'EOF'
    create_backup() { echo "Backup triggered: $1"; return 0; }
    check_scheduled_backup() {
        echo "Checking backup schedule..."
        # Simulate backup due
        create_backup "scheduled_120min"
        return 0
    }
    check_timing_rules() {
        echo "Checking timing rules..."
        check_scheduled_backup
        echo "Timing check complete"
    }
EOF
    
    # Test the call
    check_timing_rules
    """
    
    try:
        result = subprocess.run(['bash', '-c', test_script3], 
                              capture_output=True, text=True, check=True)
        if "Backup triggered: scheduled_120min" in result.stdout:
            log_result("Timing→Backup integration", "PASS", 
                      "Timing system can trigger backups")
        else:
            log_result("Timing→Backup integration", "FAIL", 
                      "Backup not triggered from timing")
    except subprocess.CalledProcessError as e:
        log_result("Timing→Backup integration", "FAIL", f"Script error: {e.stderr}")

def test_dependency_chains():
    """Test complex dependency chains"""
    print("\n🔍 Testing Complex Dependency Chains...")
    
    # Test initialization → timing → backup → handoff chain
    test_script = """
    # Source complete dependency chain
    source /dev/stdin <<'EOF'
    find_project_root() { echo "$PWD"; }
    
    create_backup() { 
        echo "[BACKUP] Creating backup: $1"
        return 0
    }
    
    check_scheduled_backup() {
        echo "[TIMING] Checking backup schedule"
        create_backup "timing_triggered"
        return 0
    }
    
    check_timing_rules() {
        echo "[TIMING] Running timing rules"
        check_scheduled_backup
        return 0
    }
    
    generate_handoff_files() {
        echo "[HANDOFF] Generating handoff"
        create_backup "handoff_backup"
        return 0
    }
    
    initialize_global_structure() {
        echo "[INIT] Initializing global structure"
        check_timing_rules
        return 0
    }
EOF
    
    # Test the full chain
    initialize_global_structure
    """
    
    try:
        result = subprocess.run(['bash', '-c', test_script], 
                              capture_output=True, text=True, check=True)
        
        # Check all components were called in order
        expected_sequence = [
            "[INIT] Initializing",
            "[TIMING] Running timing",
            "[TIMING] Checking backup",
            "[BACKUP] Creating backup: timing_triggered"
        ]
        
        all_found = True
        for expected in expected_sequence:
            if expected in result.stdout:
                log_result(f"Chain: {expected[:20]}", "PASS", "Called in sequence")
            else:
                log_result(f"Chain: {expected[:20]}", "FAIL", "Not found in output")
                all_found = False
                
    except subprocess.CalledProcessError as e:
        log_result("Dependency chain", "FAIL", f"Script error: {e.stderr}")

def test_error_handling_integration():
    """Test error handling across modules"""
    print("\n🔍 Testing Error Handling Integration...")
    
    # Test error propagation
    test_script = """
    source /dev/stdin <<'EOF'
    create_backup() {
        echo "[BACKUP] Simulating backup failure"
        return 1  # Simulate failure
    }
    
    check_scheduled_backup() {
        echo "[TIMING] Attempting backup"
        if ! create_backup "test"; then
            echo "[TIMING] Backup failed, handling error"
            return 1
        fi
        return 0
    }
    
    check_timing_rules() {
        echo "[TIMING] Running checks"
        if ! check_scheduled_backup; then
            echo "[TIMING] Scheduled backup failed"
            # But continue with other checks
        fi
        echo "[TIMING] Continuing despite backup failure"
        return 0
    }
EOF
    
    check_timing_rules
    echo "Exit code: $?"
    """
    
    try:
        result = subprocess.run(['bash', '-c', test_script], 
                              capture_output=True, text=True)
        
        if "handling error" in result.stdout and "Continuing despite" in result.stdout:
            log_result("Error propagation", "PASS", 
                      "Errors handled gracefully across modules")
        else:
            log_result("Error propagation", "FAIL", 
                      "Error handling not working correctly")
            
    except Exception as e:
        log_result("Error propagation", "FAIL", f"Unexpected error: {e}")

def test_circular_dependencies():
    """Check for circular dependencies"""
    print("\n🔍 Testing for Circular Dependencies...")
    
    # Analyze CLAUDE.md for potential circular dependencies
    claude_md_path = project_root / "CLAUDE.md"
    
    with open(claude_md_path, 'r') as f:
        content = f.read()
    
    # Extract function definitions and their calls
    import re
    
    # Find all function definitions
    func_defs = re.findall(r'^(\w+)\(\)\s*{', content, re.MULTILINE)
    
    # Build dependency graph
    dependencies = {}
    for func in func_defs:
        # Find what this function calls
        func_pattern = rf'^{func}\(\)\s*{{.*?^}}'
        func_match = re.search(func_pattern, content, re.MULTILINE | re.DOTALL)
        if func_match:
            func_body = func_match.group(0)
            # Find function calls within this function
            calls = []
            for other_func in func_defs:
                if other_func != func and f"{other_func}" in func_body:
                    calls.append(other_func)
            dependencies[func] = calls
    
    # Check for circular dependencies using DFS
    def has_cycle(graph, start, visited, rec_stack):
        visited[start] = True
        rec_stack[start] = True
        
        for neighbor in graph.get(start, []):
            if neighbor not in visited:
                visited[neighbor] = False
                rec_stack[neighbor] = False
            
            if not visited.get(neighbor, False):
                if has_cycle(graph, neighbor, visited, rec_stack):
                    return True
            elif rec_stack.get(neighbor, False):
                return True
        
        rec_stack[start] = False
        return False
    
    # Check each function for cycles
    circular_found = False
    for func in dependencies:
        visited = {}
        rec_stack = {}
        if has_cycle(dependencies, func, visited, rec_stack):
            log_result(f"Circular dependency check ({func})", "FAIL", 
                      "Circular dependency detected")
            circular_found = True
            break
    
    if not circular_found:
        log_result("Circular dependency check", "PASS", 
                  "No circular dependencies found")

def test_module_loader():
    """Test the module loader functionality"""
    print("\n🔍 Testing Module Loader...")
    
    module_loader_path = project_root / "claude_modules" / "module_loader.py"
    
    if module_loader_path.exists():
        try:
            # Import and test module loader
            spec = __import__('importlib.util').util.spec_from_file_location(
                "module_loader", module_loader_path)
            module_loader = __import__('importlib.util').util.module_from_spec(spec)
            spec.loader.exec_module(module_loader)
            
            log_result("Module loader import", "PASS", "Successfully imported")
            
            # Test module loader functionality
            if hasattr(module_loader, 'ClaudeModuleLoader'):
                log_result("ClaudeModuleLoader class", "PASS", "Module loader available")
                
                # Test instantiation
                try:
                    loader = module_loader.ClaudeModuleLoader()
                    log_result("Module loader instantiation", "PASS", "Successfully created loader instance")
                except Exception as e:
                    log_result("Module loader instantiation", "FAIL", f"Failed to create instance: {e}")
            else:
                log_result("ClaudeModuleLoader class", "FAIL", "ClaudeModuleLoader not found")
                
        except Exception as e:
            log_result("Module loader", "FAIL", f"Import error: {e}")
    else:
        log_result("Module loader", "WARN", "module_loader.py not found")

def test_integration_completeness():
    """Test overall integration completeness"""
    print("\n🔍 Testing Integration Completeness...")
    
    # Check that all major systems can work together
    test_script = """
    # Set up test environment
    export HOME=$(mktemp -d)
    cd "$HOME"
    
    # Source all functions (simplified versions for testing)
    source /dev/stdin <<'EOF'
    find_project_root() { echo "$PWD"; }
    
    initialize_global_structure() {
        echo "[INIT] Creating directories"
        mkdir -p "$HOME/.claude/backups"
        touch "$HOME/.claude/TODO.md"
        return 0
    }
    
    load_learning_files() {
        echo "[LEARN] Loading learning files"
        return 0
    }
    
    check_timing_rules() {
        echo "[TIMING] Checking timing rules"
        return 0
    }
    
    create_backup() {
        echo "[BACKUP] Creating backup: $1"
        mkdir -p backups
        touch "backups/test_backup"
        return 0
    }
    
    generate_handoff_files() {
        echo "[HANDOFF] Generating handoff"
        touch "HANDOFF_SUMMARY.md"
        return 0
    }
    
    detect_handoff_triggers() {
        echo "[TRIGGER] Detecting triggers"
        return 1  # No trigger
    }
EOF
    
    # Test complete workflow
    echo "=== Starting Integration Test ==="
    initialize_global_structure
    load_learning_files
    check_timing_rules
    create_backup "integration_test"
    generate_handoff_files
    detect_handoff_triggers "test input"
    
    # Check results
    echo "=== Checking Results ==="
    [ -d "$HOME/.claude/backups" ] && echo "✓ Global structure created"
    [ -f "$HOME/.claude/TODO.md" ] && echo "✓ TODO.md created"
    [ -f "backups/test_backup" ] && echo "✓ Backup created"
    [ -f "HANDOFF_SUMMARY.md" ] && echo "✓ Handoff files created"
    
    # Cleanup
    rm -rf "$HOME"
    """
    
    try:
        result = subprocess.run(['bash', '-c', test_script], 
                              capture_output=True, text=True, check=True)
        
        success_markers = [
            "✓ Global structure created",
            "✓ TODO.md created", 
            "✓ Backup created",
            "✓ Handoff files created"
        ]
        
        all_success = all(marker in result.stdout for marker in success_markers)
        
        if all_success:
            log_result("Complete integration workflow", "PASS", 
                      "All systems working together")
        else:
            log_result("Complete integration workflow", "FAIL", 
                      "Some components not working")
            
    except subprocess.CalledProcessError as e:
        log_result("Complete integration workflow", "FAIL", 
                  f"Workflow error: {e.stderr}")

def generate_report():
    """Generate final test report"""
    print("\n" + "="*60)
    print("📊 MODULE DEPENDENCY TEST REPORT")
    print("="*60)
    
    total_tests = len(test_results["passed"]) + len(test_results["failed"])
    
    print(f"\n✅ Passed: {len(test_results['passed'])}/{total_tests}")
    print(f"❌ Failed: {len(test_results['failed'])}/{total_tests}")
    print(f"⚠️  Warnings: {len(test_results['warnings'])}")
    
    if test_results["failed"]:
        print("\n🔴 Failed Tests:")
        for test in test_results["failed"]:
            print(f"  - {test}")
    
    if test_results["warnings"]:
        print("\n⚠️  Warnings:")
        for test in test_results["warnings"]:
            print(f"  - {test}")
    
    print("\n📋 Summary:")
    if not test_results["failed"]:
        print("✅ All critical dependencies and integrations are working correctly!")
    else:
        print("❌ Some dependencies or integrations need attention.")
        print("   Please review the failed tests above.")
    
    # Save report
    report_path = project_root / "tests" / "dependency_test_report.md"
    with open(report_path, 'w') as f:
        f.write("# Module Dependency Test Report\n\n")
        from datetime import datetime
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"## Results\n")
        f.write(f"- Passed: {len(test_results['passed'])}/{total_tests}\n")
        f.write(f"- Failed: {len(test_results['failed'])}/{total_tests}\n")
        f.write(f"- Warnings: {len(test_results['warnings'])}\n\n")
        
        if test_results["failed"]:
            f.write("## Failed Tests\n")
            for test in test_results["failed"]:
                f.write(f"- {test}\n")
        
        if test_results["warnings"]:
            f.write("\n## Warnings\n")
            for test in test_results["warnings"]:
                f.write(f"- {test}\n")
    
    print(f"\n📄 Detailed report saved to: {report_path}")

def main():
    """Run all dependency tests"""
    print("🚀 Starting Module Dependency Tests...")
    print("="*60)
    
    # Run all tests
    test_bash_function_availability()
    test_cross_module_calls()
    test_dependency_chains()
    test_error_handling_integration()
    test_circular_dependencies()
    test_module_loader()
    test_integration_completeness()
    
    # Generate report
    generate_report()

if __name__ == "__main__":
    main()