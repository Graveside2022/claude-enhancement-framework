#!/usr/bin/env python3
"""
Manual Backup System Validation Test
Tests the manual backup system to ensure:
1. "backup" command creates standard backup in /backups
2. "full backup" command creates comprehensive backup in /backups  
3. Automatic backup processes are completely removed
4. No 120-minute automatic triggers remain active

User: Christian
"""

import os
import subprocess
import time
import json
from pathlib import Path

class ManualBackupSystemValidator:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backup_dir = self.project_root / "backups"
        self.results = {}
        
    def test_manual_backup_commands(self):
        """Test that manual backup commands work correctly"""
        print("🧪 Testing Manual Backup Commands...")
        
        # Test 1: Standard backup command
        try:
            result = subprocess.run([
                "bash", "scripts/manual_backup.sh", "backup", "validation_test"
            ], capture_output=True, text=True, timeout=30)
            
            standard_backup_success = result.returncode == 0 and "Standard backup created successfully" in result.stdout
            self.results["standard_backup_command"] = {
                "success": standard_backup_success,
                "output": result.stdout,
                "error": result.stderr
            }
            print(f"  ✓ Standard backup command: {'PASS' if standard_backup_success else 'FAIL'}")
            
        except Exception as e:
            self.results["standard_backup_command"] = {"success": False, "error": str(e)}
            print(f"  ✗ Standard backup command: FAIL - {e}")
        
        # Test 2: Full backup command  
        try:
            result = subprocess.run([
                "bash", "scripts/manual_backup.sh", "full", "backup", "validation_full_test"
            ], capture_output=True, text=True, timeout=30)
            
            full_backup_success = result.returncode == 0 and "Comprehensive full backup created successfully" in result.stdout
            self.results["full_backup_command"] = {
                "success": full_backup_success,
                "output": result.stdout,
                "error": result.stderr
            }
            print(f"  ✓ Full backup command: {'PASS' if full_backup_success else 'FAIL'}")
            
        except Exception as e:
            self.results["full_backup_command"] = {"success": False, "error": str(e)}
            print(f"  ✗ Full backup command: FAIL - {e}")
    
    def test_backup_contents(self):
        """Verify backup contents are correct"""
        print("🔍 Testing Backup Contents...")
        
        # Find the most recent standard and full backups
        backup_dirs = sorted([d for d in self.backup_dir.iterdir() if d.is_dir() and d.name.startswith("2025-")])
        
        if len(backup_dirs) >= 2:
            # Check standard backup (should have basic files)
            standard_backup = None
            full_backup = None
            
            for backup in reversed(backup_dirs):
                backup_info = backup / "backup_info.txt"
                if backup_info.exists():
                    content = backup_info.read_text()
                    if "Standard Manual Backup" in content and "validation_test" in content:
                        standard_backup = backup
                    elif "Comprehensive Full Backup" in content and "validation_full_test" in content:
                        full_backup = backup
            
            # Validate standard backup
            if standard_backup:
                standard_files = set(f.name for f in standard_backup.iterdir())
                expected_standard = {"TODO.md", "CLAUDE.md", ".project_context", "backup_info.txt"}
                standard_valid = expected_standard.issubset(standard_files)
                self.results["standard_backup_contents"] = {
                    "success": standard_valid,
                    "found_files": list(standard_files),
                    "expected_files": list(expected_standard)
                }
                print(f"  ✓ Standard backup contents: {'PASS' if standard_valid else 'FAIL'}")
            else:
                self.results["standard_backup_contents"] = {"success": False, "error": "Standard backup not found"}
                print("  ✗ Standard backup contents: FAIL - backup not found")
            
            # Validate full backup  
            if full_backup:
                full_files = set(f.name for f in full_backup.iterdir())
                expected_full = {"TODO.md", "CLAUDE.md", ".project_context", "backup_info.txt", 
                               "SESSION_CONTINUITY.md", "patterns", "memory", "scripts"}
                full_valid = expected_full.issubset(full_files)
                self.results["full_backup_contents"] = {
                    "success": full_valid,
                    "found_files": list(full_files),
                    "expected_files": list(expected_full)
                }
                print(f"  ✓ Full backup contents: {'PASS' if full_valid else 'FAIL'}")
            else:
                self.results["full_backup_contents"] = {"success": False, "error": "Full backup not found"}
                print("  ✗ Full backup contents: FAIL - backup not found")
        else:
            print("  ✗ Backup contents: FAIL - insufficient backups found")
            self.results["backup_contents"] = {"success": False, "error": "Insufficient backups"}
    
    def test_automatic_processes_removed(self):
        """Verify automatic backup processes are completely removed"""
        print("🚫 Testing Automatic Process Removal...")
        
        # Check for running backup processes using ps
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            backup_processes = []
            for line in result.stdout.split('\n'):
                if 'backup_daemon.py' in line or 'timing_enforcement.sh' in line:
                    backup_processes.append(line.strip())
            
            no_backup_processes = len(backup_processes) == 0
            self.results["no_automatic_processes"] = {
                "success": no_backup_processes,
                "found_processes": backup_processes
            }
            print(f"  ✓ No automatic backup processes: {'PASS' if no_backup_processes else 'FAIL'}")
        except Exception as e:
            self.results["no_automatic_processes"] = {"success": False, "error": str(e)}
            print(f"  ✗ Process check failed: {e}")
        
        # Check for disabled scripts
        disabled_scripts = [
            "scripts/timing_enforcement.sh.disabled",
            "scripts/session_start_handler.sh.disabled"
        ]
        
        scripts_disabled = all(Path(script).exists() for script in disabled_scripts)
        self.results["timing_scripts_disabled"] = {
            "success": scripts_disabled,
            "checked_scripts": disabled_scripts
        }
        print(f"  ✓ Timing scripts disabled: {'PASS' if scripts_disabled else 'FAIL'}")
        
        # Check daemon executability
        daemon_scripts = [
            "scripts/backup_daemon.py",
            "scripts/install_backup_daemon.sh", 
            "scripts/start_backup_daemon.sh"
        ]
        
        daemons_disabled = all(not os.access(script, os.X_OK) for script in daemon_scripts if Path(script).exists())
        self.results["daemon_scripts_disabled"] = {
            "success": daemons_disabled,
            "checked_scripts": daemon_scripts
        }
        print(f"  ✓ Daemon scripts disabled: {'PASS' if daemons_disabled else 'FAIL'}")
    
    def test_120_minute_triggers_removed(self):
        """Verify no 120-minute automatic triggers remain active"""
        print("⏰ Testing 120-minute Trigger Removal...")
        
        # Check crontab
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            has_cron_backup = '120' in result.stdout and 'backup' in result.stdout.lower()
        except subprocess.CalledProcessError:
            has_cron_backup = False  # No crontab
        
        no_cron_triggers = not has_cron_backup
        self.results["no_cron_triggers"] = {
            "success": no_cron_triggers,
            "crontab_checked": True
        }
        print(f"  ✓ No cron backup triggers: {'PASS' if no_cron_triggers else 'FAIL'}")
        
        # Check launchctl services
        try:
            result = subprocess.run(['launchctl', 'list'], capture_output=True, text=True)
            has_launch_backup = 'backup' in result.stdout.lower() and 'claude' in result.stdout.lower()
        except subprocess.CalledProcessError:
            has_launch_backup = False
        
        no_launch_triggers = not has_launch_backup
        self.results["no_launch_triggers"] = {
            "success": no_launch_triggers,
            "launchctl_checked": True
        }
        print(f"  ✓ No launch daemon triggers: {'PASS' if no_launch_triggers else 'FAIL'}")
        
        # Check for timing cache files (should not auto-refresh)
        timing_cache_files = [
            ".claude_timing_cache.json",
            ".claude_timing_daemon.json"
        ]
        
        cache_files_exist = [Path(f).exists() for f in timing_cache_files]
        self.results["timing_cache_status"] = {
            "files_found": cache_files_exist,
            "cache_files": timing_cache_files
        }
        print(f"  ℹ️ Timing cache files: {sum(cache_files_exist)}/{len(timing_cache_files)} found (informational)")
    
    def test_backup_directory_structure(self):
        """Verify backup directory structure is correct"""
        print("📁 Testing Backup Directory Structure...")
        
        # Check backup directory exists
        backup_dir_exists = self.backup_dir.exists() and self.backup_dir.is_dir()
        
        # Check backup log exists
        backup_log_exists = (self.backup_dir / "backup_log.txt").exists()
        
        # Count backups
        backup_count = len([d for d in self.backup_dir.iterdir() if d.is_dir() and d.name.startswith("2025-")])
        
        structure_valid = backup_dir_exists and backup_log_exists and backup_count > 0
        self.results["backup_directory_structure"] = {
            "success": structure_valid,
            "backup_dir_exists": backup_dir_exists,
            "backup_log_exists": backup_log_exists,
            "backup_count": backup_count
        }
        print(f"  ✓ Backup directory structure: {'PASS' if structure_valid else 'FAIL'}")
        print(f"    - Backup directory exists: {backup_dir_exists}")
        print(f"    - Backup log exists: {backup_log_exists}")
        print(f"    - Backup count: {backup_count}")
    
    def run_validation(self):
        """Run complete validation suite"""
        print("=== MANUAL BACKUP SYSTEM VALIDATION ===")
        print("User: Christian")
        print("Test Suite: Manual backup system validation")
        print("")
        
        start_time = time.time()
        
        # Run all tests
        self.test_manual_backup_commands()
        self.test_backup_contents()
        self.test_automatic_processes_removed()
        self.test_120_minute_triggers_removed()
        self.test_backup_directory_structure()
        
        end_time = time.time()
        
        # Calculate results
        total_tests = 0
        passed_tests = 0
        
        for test_name, test_result in self.results.items():
            if isinstance(test_result, dict) and 'success' in test_result:
                total_tests += 1
                if test_result['success']:
                    passed_tests += 1
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("")
        print("=== VALIDATION RESULTS ===")
        print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"⏱️ Test Duration: {end_time - start_time:.2f} seconds")
        
        # Overall status
        if success_rate >= 90:
            print("🎉 VALIDATION RESULT: PASS - Manual backup system is working correctly")
            overall_status = "PASS"
        elif success_rate >= 70:
            print("⚠️ VALIDATION RESULT: PARTIAL - Some issues detected")
            overall_status = "PARTIAL"
        else:
            print("❌ VALIDATION RESULT: FAIL - Major issues detected")
            overall_status = "FAIL"
        
        # Save detailed results
        validation_results = {
            "timestamp": time.time(),
            "overall_status": overall_status,
            "success_rate": success_rate,
            "tests_passed": passed_tests,
            "total_tests": total_tests,
            "test_duration": end_time - start_time,
            "detailed_results": self.results
        }
        
        with open("manual_backup_validation_results.json", "w") as f:
            json.dump(validation_results, f, indent=2)
        
        print(f"📋 Detailed results saved to: manual_backup_validation_results.json")
        
        return overall_status == "PASS"

if __name__ == "__main__":
    validator = ManualBackupSystemValidator()
    success = validator.run_validation()
    exit(0 if success else 1)