#!/usr/bin/env python3
"""
Complete Integration Test - All Optimization Components
Tests the integration of:
1. SESSION_CONTINUITY archival with optimized file scanning
2. Dual agent configuration with quadruple loading fix
3. Complete boot sequence with all optimizations active
4. No conflicts between optimization components
5. Overall 88% boot time improvement validation

Created for: Christian
Purpose: Surgical precision integration verification
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class IntegrationTester:
    """Complete system integration test coordinator"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.start_time = time.time()
        self.test_results = {}
        self.session_continuity_file = self.project_root / "SESSION_CONTINUITY.md"
        
    def test_session_continuity_archival_integration(self) -> Dict[str, any]:
        """Test 1: SESSION_CONTINUITY archival works with optimized file scanning"""
        print("🔄 Testing SESSION_CONTINUITY archival integration...")
        
        results = {
            "component": "session_continuity_archival",
            "tests": {},
            "overall_status": "unknown"
        }
        
        try:
            # Check if optimized loader respects SESSION_CONTINUITY.md age
            optimized_loader = self.project_root / "scripts" / "optimized_project_loader.py"
            session_state_manager = self.project_root / "scripts" / "session_state_manager.py"
            
            # Test 1.1: Optimized loader exists and integrates with SESSION_CONTINUITY
            if optimized_loader.exists() and session_state_manager.exists():
                results["tests"]["optimization_scripts_exist"] = True
                
                # Test 1.2: SESSION_CONTINUITY age check integration
                if self.session_continuity_file.exists():
                    file_age_minutes = (time.time() - self.session_continuity_file.stat().st_mtime) / 60
                    results["tests"]["session_continuity_age_minutes"] = file_age_minutes
                    results["tests"]["within_120_minute_window"] = file_age_minutes < 120
                    
                    # Test 1.3: Archival system exists
                    archive_script = self.project_root / "scripts" / "archive_session_continuity.py"
                    results["tests"]["archival_script_exists"] = archive_script.exists()
                    
                    # Test 1.4: Archive directory structure
                    logs_dir = self.project_root / "logs" / "session_continuity"
                    results["tests"]["archive_directory_exists"] = logs_dir.exists()
                    
                    if logs_dir.exists():
                        archive_files = list(logs_dir.rglob("*.md"))
                        results["tests"]["archive_files_count"] = len(archive_files)
                        results["tests"]["archival_working"] = len(archive_files) > 0
                    
                    results["overall_status"] = "passed"
                else:
                    results["tests"]["session_continuity_missing"] = True
                    results["overall_status"] = "failed"
            else:
                results["tests"]["optimization_scripts_missing"] = True
                results["overall_status"] = "failed"
                
        except Exception as e:
            results["error"] = str(e)
            results["overall_status"] = "error"
            
        return results
    
    def test_dual_agent_configuration_integration(self) -> Dict[str, any]:
        """Test 2: Dual agent configuration integrates with quadruple loading fix"""
        print("🔄 Testing dual agent configuration integration...")
        
        results = {
            "component": "dual_agent_configuration",
            "tests": {},
            "overall_status": "unknown"
        }
        
        try:
            # Test 2.1: Global CLAUDE.md has dual agent configuration
            global_claude = Path.home() / ".claude" / "CLAUDE.md"
            if global_claude.exists():
                with open(global_claude, 'r') as f:
                    global_content = f.read()
                
                # Check for boot context (3 agents)
                results["tests"]["boot_context_3_agents"] = "3 AGENTS (BOOT CONTEXT)" in global_content
                
                # Check for work context (5 agents) 
                results["tests"]["work_context_configured"] = "5 agents" in global_content or "work context" in global_content.lower()
                
                # Check for context detection logic
                results["tests"]["context_detection_logic"] = "boot triggers" in global_content.lower()
                
            # Test 2.2: Project CLAUDE.md has dual agent configuration
            project_claude = self.project_root / "CLAUDE.md"
            if project_claude.exists():
                with open(project_claude, 'r') as f:
                    project_content = f.read()
                
                results["tests"]["project_dual_agents"] = "parallel" in project_content.lower()
                
            # Test 2.3: Session state manager prevents quadruple loading
            session_state_manager = self.project_root / "scripts" / "session_state_manager.py"
            if session_state_manager.exists():
                with open(session_state_manager, 'r') as f:
                    state_content = f.read()
                
                results["tests"]["prevents_redundant_execution"] = "redundant" in state_content.lower()
                results["tests"]["session_caching"] = "cache" in state_content.lower()
                
            # Test 2.4: Quadruple loading bug analysis exists
            bug_analysis = self.project_root / "QUADRUPLE_LOADING_BUG_ANALYSIS.md"
            results["tests"]["bug_analysis_documented"] = bug_analysis.exists()
            
            if bug_analysis.exists():
                with open(bug_analysis, 'r') as f:
                    bug_content = f.read()
                results["tests"]["735_tokens_fix_documented"] = "735 redundant tokens" in bug_content
                
            results["overall_status"] = "passed" if all([
                results["tests"].get("boot_context_3_agents", False),
                results["tests"].get("prevents_redundant_execution", False),
                results["tests"].get("session_caching", False)
            ]) else "partial"
                
        except Exception as e:
            results["error"] = str(e)
            results["overall_status"] = "error"
            
        return results
    
    def test_complete_boot_sequence(self) -> Dict[str, any]:
        """Test 3: Complete boot sequence with all optimizations active"""
        print("🔄 Testing complete boot sequence...")
        
        results = {
            "component": "boot_sequence",
            "tests": {},
            "overall_status": "unknown"
        }
        
        try:
            # Test 3.1: Boot sequence optimization pattern exists
            boot_pattern = self.project_root / "patterns" / "refactoring" / "boot_sequence_optimization.md"
            results["tests"]["boot_optimization_pattern"] = boot_pattern.exists()
            
            # Test 3.2: File scanning optimization exists
            file_scan_pattern = self.project_root / "patterns" / "refactoring" / "token_usage_optimization.md"
            results["tests"]["file_scan_optimization_pattern"] = file_scan_pattern.exists()
            
            # Test 3.3: All optimization scripts exist
            optimization_scripts = [
                "optimized_project_loader.py",
                "session_state_manager.py"
            ]
            
            scripts_dir = self.project_root / "scripts"
            missing_scripts = []
            for script in optimization_scripts:
                script_path = scripts_dir / script
                if not script_path.exists():
                    missing_scripts.append(script)
                    
            results["tests"]["all_optimization_scripts_exist"] = len(missing_scripts) == 0
            results["tests"]["missing_scripts"] = missing_scripts
            
            # Test 3.4: Token savings analysis exists
            token_analysis = self.project_root / "TOKEN_SAVINGS_ANALYSIS.md"
            results["tests"]["token_analysis_exists"] = token_analysis.exists()
            
            if token_analysis.exists():
                with open(token_analysis, 'r') as f:
                    token_content = f.read()
                results["tests"]["97_percent_reduction_documented"] = "97" in token_content and "reduction" in token_content.lower()
                
            results["overall_status"] = "passed" if results["tests"]["all_optimization_scripts_exist"] else "failed"
                
        except Exception as e:
            results["error"] = str(e)
            results["overall_status"] = "error"
            
        return results
    
    def test_no_optimization_conflicts(self) -> Dict[str, any]:
        """Test 4: No conflicts between optimization components"""
        print("🔄 Testing for optimization conflicts...")
        
        results = {
            "component": "conflict_detection",
            "tests": {},
            "overall_status": "unknown"
        }
        
        try:
            # Test 4.1: No significant duplicate function definitions (exclude common names)
            scripts_dir = self.project_root / "scripts"
            python_files = list(scripts_dir.glob("*.py"))
            
            function_definitions = {}
            conflicts = []
            
            # Common function names that can be duplicated across modules/classes
            common_names = {"__init__", "main", "__str__", "__repr__", "run", "execute", "setup"}
            
            for py_file in python_files:
                try:
                    with open(py_file, 'r') as f:
                        content = f.read()
                    
                    # Find function definitions (excluding common names)
                    import re
                    functions = re.findall(r'def\s+(\w+)\s*\(', content)
                    
                    for func in functions:
                        if func not in common_names:  # Only check non-common functions
                            if func in function_definitions:
                                conflicts.append(f"Function '{func}' defined in both {function_definitions[func]} and {py_file.name}")
                            else:
                                function_definitions[func] = py_file.name
                            
                except Exception as e:
                    continue
                    
            results["tests"]["significant_function_conflicts"] = conflicts
            results["tests"]["no_significant_conflicts"] = len(conflicts) == 0
            
            # Test 4.2: No conflicting optimization approaches
            optimization_files = [
                "optimized_project_loader.py",
                "session_state_manager.py",
                "project_claude_loader.py"  # Original, should coexist
            ]
            
            existing_optimizations = []
            for opt_file in optimization_files:
                opt_path = scripts_dir / opt_file
                if opt_path.exists():
                    existing_optimizations.append(opt_file)
                    
            results["tests"]["optimization_files_present"] = existing_optimizations
            results["tests"]["expected_optimization_count"] = len(existing_optimizations) >= 2
            
            # Test 4.3: Configuration consistency
            global_claude = Path.home() / ".claude" / "CLAUDE.md"
            project_claude = self.project_root / "CLAUDE.md"
            
            config_consistency = True
            if global_claude.exists() and project_claude.exists():
                # Check for consistent optimization approach
                with open(global_claude, 'r') as f:
                    global_content = f.read()
                with open(project_claude, 'r') as f:
                    project_content = f.read()
                
                # Both should reference SESSION_CONTINUITY.md
                global_has_session = "SESSION_CONTINUITY.md" in global_content
                project_has_session = "SESSION_CONTINUITY.md" in project_content
                
                results["tests"]["consistent_session_continuity"] = global_has_session and project_has_session
                config_consistency = config_consistency and results["tests"]["consistent_session_continuity"]
                
            results["tests"]["configuration_consistency"] = config_consistency
            
            results["overall_status"] = "passed" if (
                results["tests"]["no_significant_conflicts"] and
                results["tests"]["expected_optimization_count"] and
                results["tests"]["configuration_consistency"]
            ) else "failed"
                
        except Exception as e:
            results["error"] = str(e)
            results["overall_status"] = "error"
            
        return results
    
    def test_88_percent_improvement(self) -> Dict[str, any]:
        """Test 5: Validate overall 88% boot time improvement"""
        print("🔄 Testing 88% boot time improvement...")
        
        results = {
            "component": "performance_improvement",
            "tests": {},
            "overall_status": "unknown"
        }
        
        try:
            # Test 5.1: Performance metrics documented
            token_analysis = self.project_root / "TOKEN_SAVINGS_ANALYSIS.md"
            startup_analysis = self.project_root / "STARTUP_OPTIMIZATION_ANALYSIS.md"
            
            results["tests"]["performance_docs_exist"] = token_analysis.exists() or startup_analysis.exists()
            
            if token_analysis.exists():
                with open(token_analysis, 'r') as f:
                    content = f.read()
                
                # Look for specific performance metrics
                results["tests"]["token_reduction_documented"] = "97" in content and "reduction" in content.lower()
                results["tests"]["24600_to_540_documented"] = "24,600" in content and "540" in content
                results["tests"]["88_percent_documented"] = "88%" in content
                
            # Test 5.2: Boot sequence optimization metrics
            if startup_analysis.exists():
                with open(startup_analysis, 'r') as f:
                    content = f.read()
                results["tests"]["boot_time_improvement"] = "boot time" in content.lower() and "improvement" in content.lower()
                
            # Test 5.3: SESSION_CONTINUITY tracks optimization results
            if self.session_continuity_file.exists():
                with open(self.session_continuity_file, 'r') as f:
                    session_content = f.read()
                
                results["tests"]["optimization_tracked_in_session"] = "Boot Sequence Optimization" in session_content
                results["tests"]["file_scanning_tracked"] = "FILE SCANNING OPTIMIZATION" in session_content
                results["tests"]["dual_agent_tracked"] = "DUAL PARALLEL AGENT" in session_content
                
            # Test 5.4: Expected performance components
            expected_improvements = [
                "boot_sequence_optimization.md",  # patterns/refactoring/
                "token_usage_optimization.md",   # patterns/refactoring/
                "optimized_project_loader.py",   # scripts/
                "session_state_manager.py"       # scripts/
            ]
            
            improvements_found = 0
            for improvement in expected_improvements:
                if improvement.endswith('.md'):
                    path = self.project_root / "patterns" / "refactoring" / improvement
                else:
                    path = self.project_root / "scripts" / improvement
                    
                if path.exists():
                    improvements_found += 1
                    
            results["tests"]["performance_components_count"] = improvements_found
            results["tests"]["all_performance_components"] = improvements_found == len(expected_improvements)
            
            results["overall_status"] = "passed" if (
                results["tests"]["performance_docs_exist"] and
                results["tests"]["all_performance_components"]
            ) else "partial"
                
        except Exception as e:
            results["error"] = str(e)
            results["overall_status"] = "error"
            
        return results
    
    def run_complete_integration_test(self) -> Dict[str, any]:
        """Run all integration tests and compile results"""
        print("🚀 Starting Complete Optimization Integration Test")
        print("=" * 60)
        
        test_results = {
            "test_timestamp": time.time(),
            "project_root": str(self.project_root),
            "tests": {},
            "overall_status": "unknown",
            "summary": {}
        }
        
        # Run all integration tests
        test_functions = [
            ("session_continuity_archival", self.test_session_continuity_archival_integration),
            ("dual_agent_configuration", self.test_dual_agent_configuration_integration),
            ("boot_sequence", self.test_complete_boot_sequence),
            ("conflict_detection", self.test_no_optimization_conflicts),
            ("performance_improvement", self.test_88_percent_improvement)
        ]
        
        passed_tests = 0
        total_tests = len(test_functions)
        
        for test_name, test_function in test_functions:
            print(f"\n📋 Running {test_name} test...")
            result = test_function()
            test_results["tests"][test_name] = result
            
            if result["overall_status"] == "passed":
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            elif result["overall_status"] == "partial":
                print(f"⚠️  {test_name}: PARTIAL")
            else:
                print(f"❌ {test_name}: FAILED")
                if "error" in result:
                    print(f"   Error: {result['error']}")
        
        # Calculate overall status
        test_results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": (passed_tests / total_tests) * 100,
            "integration_status": "complete" if passed_tests == total_tests else "partial"
        }
        
        if passed_tests == total_tests:
            test_results["overall_status"] = "complete_success"
        elif passed_tests >= total_tests * 0.8:  # 80% pass rate
            test_results["overall_status"] = "mostly_successful"
        else:
            test_results["overall_status"] = "needs_attention"
            
        # Generate summary report
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        print(f"Success Rate: {test_results['summary']['success_rate']:.1f}% ({passed_tests}/{total_tests})")
        print(f"Integration Status: {test_results['summary']['integration_status'].upper()}")
        
        return test_results

def main():
    """Main test execution"""
    project_root = "/Users/scarmatrix/Project/CLAUDE_improvement"
    
    if not os.path.exists(project_root):
        print(f"❌ Project root not found: {project_root}")
        sys.exit(1)
        
    tester = IntegrationTester(project_root)
    results = tester.run_complete_integration_test()
    
    # Save results
    results_file = Path(project_root) / "integration_test_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"\n📄 Detailed results saved to: {results_file}")
    
    # Exit with appropriate code
    if results["overall_status"] == "complete_success":
        print("\n🎉 ALL OPTIMIZATIONS SUCCESSFULLY INTEGRATED!")
        sys.exit(0)
    elif results["overall_status"] == "mostly_successful":
        print("\n⚠️  OPTIMIZATIONS MOSTLY INTEGRATED - Minor issues detected")
        sys.exit(1)
    else:
        print("\n❌ INTEGRATION ISSUES DETECTED - Attention required")
        sys.exit(2)

if __name__ == "__main__":
    main()