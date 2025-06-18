#!/usr/bin/env python3
"""
Test Context Restoration Scripts
Tests the read.sh and continue.sh scripts to ensure they:
1. Properly read SESSION_CONTINUITY.md
2. Display relevant context information
3. Format output clearly for context restoration
4. Work as intended for post-/clear usage
"""

import subprocess
import os
import json
import re
from datetime import datetime
from pathlib import Path

class ContextRestorationTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.scripts_dir = self.project_root / "scripts"
        self.read_script = self.scripts_dir / "read.sh"
        self.continue_script = self.scripts_dir / "continue.sh"
        self.session_continuity = self.project_root / "SESSION_CONTINUITY.md"
        self.test_results = []
        
    def run_command(self, command, timeout=30):
        """Run a shell command and return result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_root
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -2
            }
    
    def test_script_existence(self):
        """Test 1: Verify both scripts exist and are executable"""
        test_name = "Script Existence and Executability"
        
        read_exists = self.read_script.exists()
        continue_exists = self.continue_script.exists()
        read_executable = os.access(self.read_script, os.X_OK) if read_exists else False
        continue_executable = os.access(self.continue_script, os.X_OK) if continue_exists else False
        
        success = read_exists and continue_exists and read_executable and continue_executable
        
        details = {
            'read_script_exists': read_exists,
            'continue_script_exists': continue_exists,
            'read_script_executable': read_executable,
            'continue_script_executable': continue_executable
        }
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'score': 100 if success else 0
        })
        
        return success
    
    def test_session_continuity_reading(self):
        """Test 2: Verify scripts can read SESSION_CONTINUITY.md"""
        test_name = "SESSION_CONTINUITY.md Reading"
        
        # Test read script
        read_result = self.run_command("./scripts/read.sh recent")
        continue_result = self.run_command("./scripts/continue.sh")
        
        read_success = read_result['success'] and self.session_continuity.exists()
        continue_success = continue_result['success']
        
        # Check if SESSION_CONTINUITY content appears in output
        session_content_in_read = "SESSION_CONTINUITY" in read_result['stdout'] or "Recent Completed Work" in read_result['stdout']
        session_content_in_continue = "Recent Major Completions" in continue_result['stdout']
        
        success = read_success and continue_success and session_content_in_read and session_content_in_continue
        
        details = {
            'read_script_success': read_success,
            'continue_script_success': continue_success,
            'session_content_in_read': session_content_in_read,
            'session_content_in_continue': session_content_in_continue,
            'session_file_exists': self.session_continuity.exists(),
            'read_output_length': len(read_result['stdout']),
            'continue_output_length': len(continue_result['stdout'])
        }
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'score': 95 if success else 40 if read_success and continue_success else 0
        })
        
        return success
    
    def test_context_information_display(self):
        """Test 3: Verify relevant context information is displayed"""
        test_name = "Context Information Display"
        
        # Test different options for read script
        read_quick = self.run_command("./scripts/read.sh quick")
        read_recent = self.run_command("./scripts/read.sh recent")
        read_system = self.run_command("./scripts/read.sh system")
        
        # Test continue script with focus
        continue_coding = self.run_command("./scripts/continue.sh coding")
        continue_default = self.run_command("./scripts/continue.sh")
        
        # Check for key context elements
        context_elements = [
            "Christian",  # User identification
            "CLAUDE Improvement",  # Project name
            "Agent",  # Agent configuration info
            "parallel",  # Execution preference
            "patterns",  # Pattern-first development
            "optimization",  # System optimization status
        ]
        
        results = []
        outputs = [
            ("read_quick", read_quick['stdout']),
            ("read_recent", read_recent['stdout']),
            ("read_system", read_system['stdout']),
            ("continue_coding", continue_coding['stdout']),
            ("continue_default", continue_default['stdout'])
        ]
        
        for name, output in outputs:
            elements_found = sum(1 for element in context_elements if element.lower() in output.lower())
            results.append({
                'command': name,
                'elements_found': elements_found,
                'total_elements': len(context_elements),
                'coverage': elements_found / len(context_elements) * 100
            })
        
        average_coverage = sum(r['coverage'] for r in results) / len(results)
        success = average_coverage >= 70  # At least 70% context coverage
        
        details = {
            'context_elements': context_elements,
            'command_results': results,
            'average_coverage': average_coverage
        }
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'score': int(average_coverage)
        })
        
        return success
    
    def test_output_formatting(self):
        """Test 4: Verify output is clearly formatted"""
        test_name = "Output Formatting Quality"
        
        read_output = self.run_command("./scripts/read.sh")['stdout']
        continue_output = self.run_command("./scripts/continue.sh")['stdout']
        
        # Check for formatting elements
        formatting_checks = {
            'headers_present': bool(re.search(r'=+', read_output + continue_output)),
            'sections_organized': bool(re.search(r'[🔄🔧⚡🧠📖]', read_output + continue_output)),
            'colored_output': bool(re.search(r'\[\d+;\d+m', read_output + continue_output)),
            'bullet_points': bool(re.search(r'[→✅❌⚠️]', read_output + continue_output)),
            'clear_structure': len(re.findall(r'\n\s*\n', read_output + continue_output)) >= 5,
            'usage_info_present': 'Usage:' in read_output or 'Usage:' in continue_output
        }
        
        formatting_score = sum(formatting_checks.values()) / len(formatting_checks) * 100
        success = formatting_score >= 80
        
        details = {
            'formatting_checks': formatting_checks,
            'formatting_score': formatting_score,
            'read_output_lines': len(read_output.split('\n')),
            'continue_output_lines': len(continue_output.split('\n'))
        }
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'score': int(formatting_score)
        })
        
        return success
    
    def test_command_options(self):
        """Test 5: Verify command options work correctly"""
        test_name = "Command Options Functionality"
        
        # Test read script options
        read_commands = [
            ("quick", "./scripts/read.sh quick"),
            ("recent", "./scripts/read.sh recent"),
            ("system", "./scripts/read.sh system"),
            ("all", "./scripts/read.sh all"),
            ("default", "./scripts/read.sh")
        ]
        
        # Test continue script options
        continue_commands = [
            ("coding", "./scripts/continue.sh coding"),
            ("testing", "./scripts/continue.sh testing"),
            ("optimization", "./scripts/continue.sh optimization"),
            ("backup", "./scripts/continue.sh backup"),
            ("default", "./scripts/continue.sh")
        ]
        
        results = []
        
        for name, command in read_commands + continue_commands:
            result = self.run_command(command)
            results.append({
                'command': name,
                'success': result['success'],
                'has_output': len(result['stdout']) > 100,
                'no_errors': len(result['stderr']) == 0
            })
        
        successful_commands = sum(1 for r in results if r['success'] and r['has_output'])
        total_commands = len(results)
        success_rate = successful_commands / total_commands * 100
        success = success_rate >= 90
        
        details = {
            'command_results': results,
            'successful_commands': successful_commands,
            'total_commands': total_commands,
            'success_rate': success_rate
        }
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'score': int(success_rate)
        })
        
        return success
    
    def test_post_clear_readiness(self):
        """Test 6: Verify scripts are suitable for post-/clear usage"""
        test_name = "Post-/clear Usage Readiness"
        
        # Run both scripts and check for essential post-clear information
        read_output = self.run_command("./scripts/read.sh")['stdout']
        continue_output = self.run_command("./scripts/continue.sh")['stdout']
        
        combined_output = read_output + continue_output
        
        # Essential information for post-/clear context restoration
        essential_info = {
            'user_identification': 'Christian' in combined_output,
            'project_identification': 'CLAUDE Improvement' in combined_output,
            'agent_preferences': 'parallel' in combined_output.lower() and '5 agents' in combined_output,
            'current_status': any(word in combined_output.lower() for word in ['complete', 'operational', 'active']),
            'next_steps': any(phrase in combined_output for phrase in ['Next Steps', 'Recommended', 'Ready to continue']),
            'system_rules': 'pattern' in combined_output.lower() and 'backup' in combined_output.lower(),
            'performance_metrics': any(metric in combined_output for metric in ['97.8%', '88%', 'optimization']),
            'welcome_message': 'Welcome back' in combined_output
        }
        
        essential_score = sum(essential_info.values()) / len(essential_info) * 100
        success = essential_score >= 85  # High bar for post-/clear readiness
        
        details = {
            'essential_info_checks': essential_info,
            'essential_score': essential_score,
            'output_comprehensive': len(combined_output) > 2000,
            'ready_for_immediate_use': success and len(combined_output) > 2000
        }
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'score': int(essential_score)
        })
        
        return success
    
    def run_all_tests(self):
        """Run all tests and return comprehensive results"""
        print("🧪 Testing Context Restoration Scripts")
        print("=" * 50)
        
        tests = [
            self.test_script_existence,
            self.test_session_continuity_reading,
            self.test_context_information_display,
            self.test_output_formatting,
            self.test_command_options,
            self.test_post_clear_readiness
        ]
        
        all_passed = True
        for i, test in enumerate(tests, 1):
            print(f"Running Test {i}/6: {test.__name__}...")
            try:
                result = test()
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {status}")
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"  ❌ ERROR: {e}")
                all_passed = False
        
        return self.generate_report(all_passed)
    
    def generate_report(self, all_passed):
        """Generate comprehensive test report"""
        total_score = sum(test['score'] for test in self.test_results) / len(self.test_results)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_success': all_passed,
            'total_score': total_score,
            'grade': self.get_grade(total_score),
            'tests_passed': sum(1 for test in self.test_results if test['success']),
            'total_tests': len(self.test_results),
            'test_results': self.test_results,
            'summary': {
                'scripts_functional': all(test['success'] for test in self.test_results[:2]),
                'context_restoration_quality': total_score,
                'post_clear_readiness': self.test_results[-1]['success'] if self.test_results else False,
                'recommendation': self.get_recommendation(total_score, all_passed)
            }
        }
        
        return report
    
    def get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "B+"
        elif score >= 80:
            return "B"
        elif score >= 75:
            return "C+"
        elif score >= 70:
            return "C"
        else:
            return "F"
    
    def get_recommendation(self, score, all_passed):
        """Get recommendation based on test results"""
        if all_passed and score >= 90:
            return "EXCELLENT: Scripts are production-ready for context restoration"
        elif all_passed and score >= 80:
            return "GOOD: Scripts work well for context restoration with minor improvements possible"
        elif score >= 70:
            return "FAIR: Scripts function but need improvements for optimal context restoration"
        else:
            return "POOR: Scripts need significant work before being suitable for context restoration"

def main():
    """Main test execution"""
    tester = ContextRestorationTester()
    report = tester.run_all_tests()
    
    print("\n" + "=" * 50)
    print("📊 CONTEXT RESTORATION SCRIPTS TEST REPORT")
    print("=" * 50)
    print(f"Overall Success: {'✅ PASS' if report['overall_success'] else '❌ FAIL'}")
    print(f"Total Score: {report['total_score']:.1f}/100 (Grade: {report['grade']})")
    print(f"Tests Passed: {report['tests_passed']}/{report['total_tests']}")
    print(f"Post-/clear Ready: {'✅ YES' if report['summary']['post_clear_readiness'] else '❌ NO'}")
    print(f"\nRecommendation: {report['summary']['recommendation']}")
    
    # Save detailed report
    report_file = Path(__file__).parent / "context_restoration_test_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    return report['overall_success']

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)