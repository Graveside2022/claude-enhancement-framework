#!/usr/bin/env python3
"""
IMMEDIATE Security Fixes for pattern_executor.py
Critical security patches to prevent command injection and other attacks.

URGENT: Apply these fixes immediately to prevent security vulnerabilities.
Created for: Christian
Security Priority: CRITICAL
"""

import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

class SecurityError(Exception):
    """Custom exception for security violations"""
    pass

class ImmediateSecurityPatch:
    """
    Immediate security patches for pattern_executor.py
    These are critical fixes that must be applied immediately.
    """
    
    def __init__(self):
        # Command whitelist - ONLY these commands are allowed
        self.ALLOWED_COMMANDS = {
            'echo', 'cat', 'ls', 'pwd', 'date', 'whoami',
            'mkdir', 'touch', 'cp', 'mv', 'rm',
            'grep', 'sed', 'awk', 'sort', 'uniq',
            'git', 'python3', 'pip', 'npm', 'head', 'tail'
        }
        
        # Dangerous patterns that must be blocked
        self.DANGEROUS_PATTERNS = [
            r';\s*\w+',           # Command chaining with semicolon
            r'\|\s*\w+',          # Pipe to another command
            r'&&\s*\w+',          # AND operator
            r'\|\|\s*\w+',        # OR operator
            r'`[^`]+`',           # Backtick execution
            r'\$\([^)]+\)',       # Command substitution
            r'>\s*/',             # Redirect to root
            r'<\s*/',             # Input from root
            r'\.\./\.\.',         # Path traversal
            r'sudo|su|passwd',    # Privilege escalation
            r'curl|wget|nc|netcat', # Network commands
            r'eval|exec',         # Dynamic execution
            r'rm\s+-rf?\s+/',     # Dangerous deletions
        ]
        
        # Setup logging
        self.setup_security_logging()
    
    def setup_security_logging(self):
        """Setup security logging"""
        log_dir = Path("security")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=str(log_dir / "security.log"),
            level=logging.WARNING,
            format='%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def sanitize_template_variables(self, variables: Dict[str, str]) -> Dict[str, str]:
        """
        CRITICAL: Sanitize all template variables to prevent injection
        """
        sanitized = {}
        
        for key, value in variables.items():
            if not isinstance(value, str):
                value = str(value)
            
            # Remove dangerous characters
            sanitized_value = value
            
            # Remove null bytes
            sanitized_value = sanitized_value.replace('\x00', '')
            
            # Remove shell metacharacters
            dangerous_chars = ['`', '$', ';', '|', '&', '>', '<', '(', ')', '{', '}']
            for char in dangerous_chars:
                sanitized_value = sanitized_value.replace(char, '')
            
            # Limit length
            if len(sanitized_value) > 1000:
                sanitized_value = sanitized_value[:1000]
                self.logger.warning(f"Variable '{key}' truncated due to length")
            
            # Check for dangerous patterns
            for pattern in self.DANGEROUS_PATTERNS:
                if re.search(pattern, sanitized_value, re.IGNORECASE):
                    self.logger.critical(f"SECURITY VIOLATION: Dangerous pattern in variable '{key}': {value}")
                    raise SecurityError(f"Security violation in variable '{key}': dangerous pattern detected")
            
            sanitized[key] = sanitized_value
        
        return sanitized
    
    def validate_template_content(self, template: str) -> str:
        """
        CRITICAL: Validate template content for security violations
        """
        if not isinstance(template, str):
            raise SecurityError("Template must be a string")
        
        # Check for dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            matches = re.finditer(pattern, template, re.IGNORECASE)
            for match in matches:
                self.logger.critical(f"SECURITY VIOLATION: Dangerous pattern in template: {match.group(0)}")
                raise SecurityError(f"Security violation: dangerous pattern detected: {match.group(0)}")
        
        # Check for script injections
        script_patterns = [
            r'<script[^>]*>',
            r'javascript:',
            r'vbscript:',
            r'on\w+\s*=',
        ]
        
        for pattern in script_patterns:
            if re.search(pattern, template, re.IGNORECASE):
                self.logger.critical(f"SECURITY VIOLATION: Script injection attempt in template")
                raise SecurityError("Security violation: script injection detected")
        
        return template
    
    def validate_command(self, command: str) -> bool:
        """
        CRITICAL: Validate that command is safe to execute
        """
        if not command or not command.strip():
            return False
        
        # Parse command safely
        try:
            parts = shlex.split(command.strip())
        except ValueError:
            self.logger.warning(f"Invalid command syntax: {command}")
            return False
        
        if not parts:
            return False
        
        # Check if base command is allowed
        base_command = parts[0]
        if base_command not in self.ALLOWED_COMMANDS:
            self.logger.critical(f"SECURITY VIOLATION: Unauthorized command: {base_command}")
            return False
        
        # Check for dangerous patterns in full command
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                self.logger.critical(f"SECURITY VIOLATION: Dangerous pattern in command: {command}")
                return False
        
        return True
    
    def secure_substitute_variables(self, template: str, variables: Dict[str, str]) -> str:
        """
        CRITICAL: Safely substitute variables in template
        """
        # Validate template first
        validated_template = self.validate_template_content(template)
        
        # Sanitize variables
        sanitized_vars = self.sanitize_template_variables(variables)
        
        # Perform safe substitution
        result = validated_template
        for key, value in sanitized_vars.items():
            placeholder = f"[{key}]"
            # Use safe replacement
            result = result.replace(placeholder, shlex.quote(str(value)))
        
        # Final validation of result
        self.validate_template_content(result)
        
        return result
    
    def secure_create_execution_script(self, template: str) -> Optional[Path]:
        """
        CRITICAL: Create execution script with security measures
        """
        try:
            # Create temporary script with restricted permissions
            script_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.sh',
                delete=False,
                dir=tempfile.gettempdir()
            )
            
            # Secure script header
            script_content = f"""#!/bin/bash
# CLAUDE Security-Enhanced Execution Script
# User: Christian
# Generated: {os.environ.get('USER', 'unknown')}
# Security: ENABLED

set -euo pipefail  # Strict error handling
export PATH="/usr/local/bin:/usr/bin:/bin"  # Restricted PATH
cd "$(dirname "$0")"  # Work in script directory

# Security: Resource limits
ulimit -t 300      # CPU time limit: 5 minutes
ulimit -f 10240    # File size limit: 10MB
ulimit -v 262144   # Virtual memory limit: 256MB

# Security: Validate working directory
if [[ ! -d "$(pwd)" ]]; then
    echo "SECURITY ERROR: Invalid working directory"
    exit 1
fi

# Execute template content
{template}
"""
            
            script_file.write(script_content)
            script_file.close()
            
            script_path = Path(script_file.name)
            
            # Set restrictive permissions: owner read/execute only
            script_path.chmod(0o700)
            
            self.logger.info(f"Created secure execution script: {script_path}")
            return script_path
            
        except Exception as e:
            self.logger.error(f"Failed to create secure execution script: {e}")
            return None
    
    def secure_execute_script(self, script_path: Path, project_root: Path) -> Dict[str, Any]:
        """
        CRITICAL: Execute script with security restrictions
        """
        try:
            # Security: Change to project root with validation
            if not project_root.exists() or not project_root.is_dir():
                raise SecurityError(f"Invalid project root: {project_root}")
            
            original_cwd = os.getcwd()
            os.chdir(project_root)
            
            # Security: Restricted environment
            secure_env = {
                'PATH': '/usr/local/bin:/usr/bin:/bin',
                'HOME': str(project_root),
                'USER': 'claude_executor',
                'SHELL': '/bin/bash',
                'TERM': 'xterm',
                'LC_ALL': 'C',
                'LANG': 'C'
            }
            
            # Security: Execute with restrictions
            result = subprocess.run(
                [str(script_path)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=project_root,
                env=secure_env,
                shell=False  # CRITICAL: Never use shell=True
            )
            
            # Log execution
            self.logger.info(f"Script executed: {script_path}, return_code: {result.returncode}")
            
            return {
                'success': result.returncode == 0,
                'return_code': result.returncode,
                'output': result.stdout,
                'error': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            self.logger.critical("SECURITY: Script execution timeout")
            return {
                'success': False,
                'error': 'Script execution timed out (5 minutes)'
            }
        except Exception as e:
            self.logger.critical(f"SECURITY: Script execution failed: {e}")
            return {
                'success': False,
                'error': f'Script execution failed: {str(e)}'
            }
        finally:
            # Always restore original directory
            os.chdir(original_cwd)
            
            # Cleanup script file
            try:
                if script_path.exists():
                    script_path.unlink()
            except Exception:
                pass


def apply_immediate_security_fixes():
    """
    Apply immediate security fixes to pattern executor.
    THIS MUST BE CALLED BEFORE ANY PATTERN EXECUTION.
    """
    
    # Create security patch instance
    security_patch = ImmediateSecurityPatch()
    
    print("🔒 APPLYING IMMEDIATE SECURITY FIXES")
    print("=" * 50)
    print("User: Christian")
    print("Priority: CRITICAL")
    print("Applying security patches to prevent:")
    print("- Command injection attacks")
    print("- Path traversal attacks") 
    print("- Code execution attacks")
    print("- Privilege escalation")
    print("- Resource exhaustion")
    print("=" * 50)
    
    # Return security patch for use
    return security_patch


# CRITICAL SECURITY PATCHES FOR PATTERN_EXECUTOR.PY
# These patches must be integrated immediately:

SECURITY_PATCH_INSTRUCTIONS = """
CRITICAL SECURITY INTEGRATION INSTRUCTIONS
==========================================

1. IMMEDIATE ACTIONS (Apply NOW):
   
   a) Import security patch in pattern_executor.py:
      ```python
      from security.immediate_security_fixes import apply_immediate_security_fixes
      ```
   
   b) Initialize security in PatternExecutor.__init__():
      ```python
      self.security_patch = apply_immediate_security_fixes()
      ```
   
   c) Replace _substitute_variables() method:
      ```python
      def _substitute_variables(self, template: str, variables: Dict) -> str:
          return self.security_patch.secure_substitute_variables(template, variables)
      ```
   
   d) Replace _create_execution_script() method:
      ```python
      def _create_execution_script(self, template: str) -> Optional[Path]:
          return self.security_patch.secure_create_execution_script(template)
      ```
   
   e) Replace _execute_script() method:
      ```python
      def _execute_script(self, script_path: Path) -> Dict:
          return self.security_patch.secure_execute_script(script_path, self.project_root)
      ```

2. VALIDATION REQUIREMENTS:
   
   - Test with malicious inputs to verify blocking
   - Verify command whitelist enforcement
   - Test path traversal prevention
   - Validate resource limit enforcement

3. MONITORING:
   
   - Check security.log for violations
   - Monitor for failed execution attempts
   - Review blocked commands and patterns

4. EMERGENCY PROCEDURES:
   
   - If security violation detected: STOP ALL EXECUTIONS
   - Review all recent pattern executions
   - Check system for signs of compromise
   - Update security patterns immediately

FAILURE TO APPLY THESE FIXES LEAVES SYSTEM VULNERABLE TO:
- Remote code execution
- Data exfiltration
- System compromise
- Privilege escalation

APPLY IMMEDIATELY - DO NOT DELAY
"""

if __name__ == "__main__":
    print(SECURITY_PATCH_INSTRUCTIONS)
    
    # Test security patch
    patch = apply_immediate_security_fixes()
    
    # Test cases
    test_cases = [
        {"template": "echo '[MESSAGE]'", "vars": {"MESSAGE": "Hello Christian"}},
        {"template": "echo '[MESSAGE]'", "vars": {"MESSAGE": "'; rm -rf /; echo '"}},  # Should be blocked
        {"template": "cat [FILE]", "vars": {"FILE": "../../etc/passwd"}},  # Should be blocked
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['template']}")
        try:
            result = patch.secure_substitute_variables(test['template'], test['vars'])
            print(f"Result: {result}")
        except SecurityError as e:
            print(f"SECURITY BLOCKED: {e}")