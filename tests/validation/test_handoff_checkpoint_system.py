#!/usr/bin/env python3
"""
Handoff and Checkpoint System Testing Script
User: Christian
Project: CLAUDE Improvement

Comprehensive test suite for validating the handoff and checkpoint scripts work correctly.
Tests all major functionality including:
- Script executability
- Argument handling
- SESSION_CONTINUITY.md updates
- File creation and content validation
- Integration between components
"""

import subprocess
import json
import os
from pathlib import Path
import datetime
import tempfile
import shutil
from typing import Dict, List, Tuple

class HandoffCheckpointTester:
    """Comprehensive tester for handoff and checkpoint scripts"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.scripts_dir = self.project_root / "scripts"
        self.test_results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": "Christian",
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "test_details": []
        }
        
    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test and record results"""
        self.test_results["total_tests"] += 1
        
        try:
            print(f"🧪 Testing: {test_name}")
            result = test_func()
            
            if result:
                self.test_results["passed"] += 1
                print(f"✅ PASS: {test_name}")
            else:
                self.test_results["failed"] += 1
                print(f"❌ FAIL: {test_name}")
                
            self.test_results["test_details"].append({
                "test_name": test_name,
                "passed": result,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            self.test_results["failed"] += 1
            print(f"❌ ERROR in {test_name}: {str(e)}")
            
            self.test_results["test_details"].append({
                "test_name": test_name,
                "passed": False,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            return False
    
    def test_script_executable(self) -> bool:
        """Test that all scripts are executable"""
        scripts = [
            "project_handoff.py",
            "handoff_trigger_detection.py", 
            "archive_session_continuity.py"
        ]
        
        for script in scripts:
            script_path = self.scripts_dir / script
            if not script_path.exists():
                print(f"   ❌ Script not found: {script}")
                return False
            if not os.access(script_path, os.X_OK):
                print(f"   ❌ Script not executable: {script}")
                return False
            print(f"   ✓ Script executable: {script}")
        
        return True
    
    def test_project_handoff_help(self) -> bool:
        """Test project_handoff.py --help command"""
        try:
            result = subprocess.run(
                ["python3", str(self.scripts_dir / "project_handoff.py"), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"   ❌ Help command failed with return code: {result.returncode}")
                return False
                
            if "CLAUDE Project Handoff System" not in result.stdout:
                print(f"   ❌ Help output missing expected content")
                return False
                
            print(f"   ✓ Help command works properly")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"   ❌ Help command timed out")
            return False
        except Exception as e:
            print(f"   ❌ Help command error: {e}")
            return False
    
    def test_project_handoff_status(self) -> bool:
        """Test project_handoff.py --status command"""
        try:
            result = subprocess.run(
                ["python3", str(self.scripts_dir / "project_handoff.py"), "--status"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"   ❌ Status command failed with return code: {result.returncode}")
                print(f"   Error output: {result.stderr}")
                return False
                
            # Parse JSON output
            try:
                status_data = json.loads(result.stdout)
                required_keys = ["timestamp", "user", "backup_system", "timing_requirements"]
                
                for key in required_keys:
                    if key not in status_data:
                        print(f"   ❌ Status output missing required key: {key}")
                        return False
                
                if status_data["user"] != "Christian":
                    print(f"   ❌ Status shows wrong user: {status_data['user']}")
                    return False
                    
                print(f"   ✓ Status command returns valid JSON with correct data")
                return True
                
            except json.JSONDecodeError:
                print(f"   ❌ Status output is not valid JSON")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ Status command timed out")
            return False
        except Exception as e:
            print(f"   ❌ Status command error: {e}")
            return False
    
    def test_project_handoff_timing_check(self) -> bool:
        """Test project_handoff.py --check-timing command"""
        try:
            result = subprocess.run(
                ["python3", str(self.scripts_dir / "project_handoff.py"), "--check-timing"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"   ❌ Timing check failed with return code: {result.returncode}")
                return False
                
            # Parse JSON output
            try:
                timing_data = json.loads(result.stdout)
                required_keys = ["backup_due", "todo_update_due", "session_continuity_stale"]
                
                for key in required_keys:
                    if key not in timing_data:
                        print(f"   ❌ Timing output missing required key: {key}")
                        return False
                        
                print(f"   ✓ Timing check returns valid data")
                return True
                
            except json.JSONDecodeError:
                print(f"   ❌ Timing output is not valid JSON")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ Timing check timed out")
            return False
        except Exception as e:
            print(f"   ❌ Timing check error: {e}")
            return False
    
    def test_session_continuity_update(self) -> bool:
        """Test that SESSION_CONTINUITY.md gets updated by handoff system"""
        session_file = self.project_root / "SESSION_CONTINUITY.md"
        
        if not session_file.exists():
            print(f"   ❌ SESSION_CONTINUITY.md does not exist")
            return False
            
        # Get initial modification time
        initial_mtime = session_file.stat().st_mtime
        
        # Run execute-updates to trigger SESSION_CONTINUITY update
        try:
            result = subprocess.run(
                ["python3", str(self.scripts_dir / "project_handoff.py"), "--execute-updates"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"   ❌ Execute updates failed with return code: {result.returncode}")
                print(f"   Error: {result.stderr}")
                return False
            
            # Check if file was modified
            final_mtime = session_file.stat().st_mtime
            
            if final_mtime <= initial_mtime:
                print(f"   ❌ SESSION_CONTINUITY.md was not updated")
                return False
                
            # Verify the update contains handoff system content
            content = session_file.read_text()
            if "Handoff System:" not in content:
                print(f"   ❌ SESSION_CONTINUITY.md missing handoff system content")
                return False
                
            print(f"   ✓ SESSION_CONTINUITY.md successfully updated")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"   ❌ Execute updates timed out")
            return False
        except Exception as e:
            print(f"   ❌ Execute updates error: {e}")
            return False
    
    def test_handoff_trigger_detection(self) -> bool:
        """Test handoff trigger detection script"""
        try:
            result = subprocess.run(
                ["python3", str(self.scripts_dir / "handoff_trigger_detection.py")],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"   ❌ Trigger detection failed with return code: {result.returncode}")
                return False
                
            # Check for successful test completion
            output = result.stdout
            if "Success rate: 100.0%" not in output:
                print(f"   ❌ Trigger detection tests did not achieve 100% success rate")
                return False
                
            if "✅ Handoff trigger detection system fully implemented and tested" not in output:
                print(f"   ❌ Trigger detection system completion message missing")
                return False
                
            # Check if test results file was created
            test_results_file = self.project_root / "handoff_trigger_test_results.json"
            if not test_results_file.exists():
                print(f"   ❌ Test results file not created")
                return False
                
            print(f"   ✓ Handoff trigger detection works with 100% test success")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"   ❌ Trigger detection timed out")
            return False
        except Exception as e:
            print(f"   ❌ Trigger detection error: {e}")
            return False
    
    def test_archive_session_continuity_dry_run(self) -> bool:
        """Test archive session continuity script in dry-run mode"""
        try:
            result = subprocess.run(
                ["python3", str(self.scripts_dir / "archive_session_continuity.py"), "--dry-run"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"   ❌ Archive dry-run failed with return code: {result.returncode}")
                return False
                
            # Check for successful dry run
            output = result.stdout
            if "DRY RUN MODE" not in output:
                print(f"   ❌ Dry run mode not indicated")
                return False
                
            if "Archival Summary:" not in output:
                print(f"   ❌ Archival summary not provided")
                return False
                
            print(f"   ✓ Archive session continuity dry-run works correctly")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"   ❌ Archive dry-run timed out")
            return False
        except Exception as e:
            print(f"   ❌ Archive dry-run error: {e}")
            return False
    
    def test_context_usage_monitoring(self) -> bool:
        """Test context usage monitoring functionality"""
        try:
            # Test normal context usage (should not trigger handoff)
            result = subprocess.run(
                ["python3", str(self.scripts_dir / "project_handoff.py"), "--context-usage", "75"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"   ❌ Context monitoring (75%) failed")
                return False
                
            if "Context usage 75%: Monitoring" not in result.stdout:
                print(f"   ❌ Context monitoring message incorrect for 75%")
                return False
                
            print(f"   ✓ Context usage monitoring (75%) works correctly")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"   ❌ Context monitoring timed out")
            return False
        except Exception as e:
            print(f"   ❌ Context monitoring error: {e}")
            return False
    
    def test_handoff_file_creation(self) -> bool:
        """Test that handoff files are created when context limit reached"""
        handoff_summary = self.project_root / "HANDOFF_SUMMARY.md"
        next_session_prompt = self.project_root / "NEXT_SESSION_HANDOFF_PROMPT.md"
        
        # Check if handoff files already exist from previous tests
        files_exist = handoff_summary.exists() and next_session_prompt.exists()
        
        if not files_exist:
            print(f"   ❌ Handoff files not found (may not have been created in previous tests)")
            return False
            
        # Verify file contents
        try:
            handoff_content = handoff_summary.read_text()
            if "HANDOFF SUMMARY - SESSION END" not in handoff_content:
                print(f"   ❌ HANDOFF_SUMMARY.md missing expected header")
                return False
                
            if "User: Christian" not in handoff_content:
                print(f"   ❌ HANDOFF_SUMMARY.md missing user identification")
                return False
                
            prompt_content = next_session_prompt.read_text()
            if "SESSION HANDOFF - CONTEXT PRESERVATION" not in prompt_content:
                print(f"   ❌ NEXT_SESSION_HANDOFF_PROMPT.md missing expected header")
                return False
                
            print(f"   ✓ Handoff files created with correct content")
            return True
            
        except Exception as e:
            print(f"   ❌ Error reading handoff files: {e}")
            return False
    
    def run_all_tests(self) -> Dict:
        """Run all tests and return comprehensive results"""
        print("🚀 Starting Handoff and Checkpoint System Testing for Christian")
        print("=" * 70)
        
        # Run all tests
        self.run_test("Script Executability", self.test_script_executable)
        self.run_test("Project Handoff Help Command", self.test_project_handoff_help)
        self.run_test("Project Handoff Status Command", self.test_project_handoff_status)
        self.run_test("Project Handoff Timing Check", self.test_project_handoff_timing_check)
        self.run_test("SESSION_CONTINUITY.md Update", self.test_session_continuity_update)
        self.run_test("Handoff Trigger Detection", self.test_handoff_trigger_detection)
        self.run_test("Archive Session Continuity Dry Run", self.test_archive_session_continuity_dry_run)
        self.run_test("Context Usage Monitoring", self.test_context_usage_monitoring)
        self.run_test("Handoff File Creation", self.test_handoff_file_creation)
        
        # Calculate results
        self.test_results["success_rate"] = (
            self.test_results["passed"] / self.test_results["total_tests"] * 100
            if self.test_results["total_tests"] > 0 else 0
        )
        
        print("\n" + "=" * 70)
        print("📊 Test Results Summary:")
        print(f"Total tests: {self.test_results['total_tests']}")
        print(f"Passed: {self.test_results['passed']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Success rate: {self.test_results['success_rate']:.1f}%")
        
        if self.test_results["success_rate"] >= 90:
            print("✅ SYSTEM STATUS: EXCELLENT - Handoff and checkpoint scripts fully operational")
        elif self.test_results["success_rate"] >= 75:
            print("⚠️ SYSTEM STATUS: GOOD - Handoff and checkpoint scripts mostly operational")
        else:
            print("❌ SYSTEM STATUS: NEEDS ATTENTION - Significant issues found")
        
        return self.test_results
    
    def save_test_report(self, filename: str = "handoff_checkpoint_test_report.json") -> str:
        """Save test results to JSON file"""
        report_path = self.project_root / filename
        
        with open(report_path, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"📄 Test report saved to: {report_path}")
        return str(report_path)


def main():
    """Main testing function"""
    tester = HandoffCheckpointTester()
    results = tester.run_all_tests()
    report_path = tester.save_test_report()
    
    print(f"\n🎯 TESTING COMPLETE")
    print(f"📋 Report: {report_path}")
    print(f"🔄 System ready for handoff and checkpoint operations")
    
    # Return appropriate exit code
    exit_code = 0 if results["success_rate"] >= 90 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()