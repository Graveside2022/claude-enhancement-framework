#!/usr/bin/env python3
"""
Pattern Executor for CLAUDE Improvement System
Applies pattern templates to solve problems with guided execution and validation.

Created for: Christian
"""

import os
import re
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import tempfile
import shutil

# Import the existing pattern matcher
try:
    from pattern_matcher import PatternMatcher
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from pattern_matcher import PatternMatcher

class PatternExecutor:
    """
    Pattern execution engine that applies pattern templates to solve problems.
    Provides template variable substitution, step-by-step execution guidance,
    and progress tracking with validation checkpoints.
    """
    
    def __init__(self, project_root: str = ".", interactive: bool = True):
        self.project_root = Path(project_root).resolve()
        self.patterns_dir = self.project_root / "patterns"
        self.interactive = interactive
        self.pattern_matcher = PatternMatcher(project_root)
        
        # Execution tracking
        self.execution_log = []
        self.current_execution = None
        self.validation_checkpoints = []
        
        # Template variable cache
        self.template_variables = {}
        
        # Initialize logging
        self.log_dir = self.project_root / "logs" / "pattern_execution"
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def find_and_execute_pattern(self, problem_description: str, pattern_key: str = None) -> Dict:
        """
        Find the best pattern for a problem and execute it.
        
        Args:
            problem_description: Description of the problem to solve
            pattern_key: Specific pattern to use (optional, will search if not provided)
            
        Returns:
            Execution result with status, steps, and outputs
        """
        print(f"🚀 CLAUDE Pattern Executor - User: Christian")
        print(f"Problem: {problem_description}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # Initialize execution tracking
        execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_execution = {
            'id': execution_id,
            'problem': problem_description,
            'pattern_key': pattern_key,
            'start_time': datetime.now().isoformat(),
            'status': 'started',
            'steps': [],
            'variables': {},
            'outputs': [],
            'validation_results': []
        }
        
        try:
            # Step 1: Pattern Selection
            if pattern_key is None:
                pattern_key = self._select_pattern(problem_description)
                if not pattern_key:
                    return self._finalize_execution('failed', "No suitable pattern found")
            
            print(f"📋 Selected Pattern: {pattern_key}")
            
            # Step 2: Load Pattern Details
            pattern_details = self.pattern_matcher.get_pattern_details(pattern_key)
            if not pattern_details:
                return self._finalize_execution('failed', f"Pattern not found: {pattern_key}")
            
            # Step 3: Variable Substitution
            print("\n🔧 Template Variable Substitution")
            variables = self._collect_template_variables(pattern_details, problem_description)
            self.current_execution['variables'] = variables
            
            # Step 4: Execute Pattern Steps
            print("\n⚙️ Executing Pattern Steps")
            execution_result = self._execute_pattern_template(pattern_details, variables)
            
            if execution_result['success']:
                return self._finalize_execution('completed', "Pattern executed successfully", execution_result)
            else:
                return self._finalize_execution('failed', execution_result.get('error', 'Unknown error'))
        
        except Exception as e:
            return self._finalize_execution('error', f"Execution error: {str(e)}")
    
    def _select_pattern(self, problem_description: str) -> Optional[str]:
        """Select the best pattern for the given problem"""
        print("🔍 Finding best pattern match...")
        
        matches = self.pattern_matcher.match_patterns(problem_description, max_results=5)
        
        if not matches:
            print("❌ No patterns found for this problem")
            return None
        
        # Display top matches
        print(f"Found {len(matches)} potential patterns:")
        for i, match in enumerate(matches, 1):
            print(f"  {i}. {match['title']} ({match['category']})")
            print(f"     Confidence: {match['confidence']:.1f}% | Complexity: {match['complexity']}")
        
        # Auto-select highest confidence if > 80%, otherwise ask user
        best_match = matches[0]
        if best_match['confidence'] >= 80 and not self.interactive:
            print(f"✅ Auto-selecting: {best_match['title']} (confidence: {best_match['confidence']:.1f}%)")
            return best_match['pattern_key']
        
        if self.interactive:
            while True:
                try:
                    choice = input(f"\nSelect pattern (1-{len(matches)}, or 'q' to quit): ").strip()
                    if choice.lower() == 'q':
                        return None
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(matches):
                        selected = matches[choice_idx]
                        print(f"✅ Selected: {selected['title']}")
                        return selected['pattern_key']
                    else:
                        print("Invalid choice. Please try again.")
                except (ValueError, KeyboardInterrupt):
                    print("Invalid input or cancelled.")
                    return None
        else:
            # Non-interactive mode: use best match
            return best_match['pattern_key']
    
    def _collect_template_variables(self, pattern_details: Dict, problem_description: str) -> Dict:
        """Collect and substitute template variables from pattern"""
        variables = {
            'TIMESTAMP': datetime.now().isoformat(),
            'USER': 'Christian',
            'PROBLEM_DESCRIPTION': problem_description,
            'PATTERN_NAME': pattern_details['title'],
            'CATEGORY': pattern_details['category']
        }
        
        # Load pattern content to find template variables
        pattern_content = self._load_pattern_content(pattern_details['file_path'])
        
        # Extract template variables from pattern content
        template_vars = re.findall(r'\[([A-Z_][A-Z0-9_]*)\]', pattern_content)
        
        print(f"Found {len(template_vars)} template variables to substitute:")
        
        for var in set(template_vars):
            if var not in variables:
                # Try to auto-generate common variables
                auto_value = self._auto_generate_variable(var, problem_description, pattern_details)
                
                if auto_value:
                    variables[var] = auto_value
                    print(f"  ✅ {var}: {auto_value}")
                elif self.interactive:
                    # Ask user for variable value
                    prompt = f"  Enter value for {var}: "
                    user_value = input(prompt).strip()
                    variables[var] = user_value if user_value else f"[{var}]"
                    print(f"  ✅ {var}: {variables[var]}")
                else:
                    # Use placeholder in non-interactive mode
                    variables[var] = f"[{var}]"
                    print(f"  ⚠️ {var}: {variables[var]} (placeholder)")
        
        return variables
    
    def _auto_generate_variable(self, var: str, problem_description: str, pattern_details: Dict) -> Optional[str]:
        """Auto-generate common template variables"""
        var_generators = {
            'ERROR_DESCRIPTION': lambda: problem_description,
            'ERROR_CATEGORY': lambda: self._infer_error_category(problem_description),
            'URGENCY': lambda: self._infer_urgency(problem_description),
            'COMPONENT_NAME': lambda: self._extract_component_name(problem_description),
            'TEST_NAME': lambda: f"{pattern_details['title'].replace(' ', '_')}_test",
            'OUTPUT_DIR': lambda: "output",
            'DOC_TYPE': lambda: pattern_details['category'],
            'TEST_SCOPE': lambda: self._infer_test_scope(problem_description),
            'TEST_ENV': lambda: "development",
            'LOG_LEVEL': lambda: "info",
            'BACKUP_TYPE': lambda: "manual",
            'CONFIG_KEY': lambda: self._extract_config_key(problem_description),
            'FEATURE_NAME': lambda: self._extract_feature_name(problem_description)
        }
        
        if var in var_generators:
            try:
                return var_generators[var]()
            except:
                return None
        
        return None
    
    def _infer_error_category(self, description: str) -> str:
        """Infer error category from description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['config', 'configuration', 'setup']):
            return 'config'
        elif any(word in description_lower for word in ['behavior', 'rule', 'enforcement']):
            return 'behavior'
        elif any(word in description_lower for word in ['integration', 'component', 'system']):
            return 'integration'
        elif any(word in description_lower for word in ['performance', 'slow', 'speed', 'optimization']):
            return 'performance'
        else:
            return 'general'
    
    def _infer_urgency(self, description: str) -> str:
        """Infer urgency level from description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['critical', 'urgent', 'emergency', 'blocking']):
            return 'critical'
        elif any(word in description_lower for word in ['important', 'high', 'priority']):
            return 'high'
        elif any(word in description_lower for word in ['minor', 'low', 'optional']):
            return 'low'
        else:
            return 'medium'
    
    def _infer_test_scope(self, description: str) -> str:
        """Infer test scope from description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['system', 'full', 'complete', 'end-to-end']):
            return 'system'
        elif any(word in description_lower for word in ['integration', 'component', 'interaction']):
            return 'integration'
        elif any(word in description_lower for word in ['regression', 'after', 'change']):
            return 'regression'
        else:
            return 'unit'
    
    def _extract_component_name(self, description: str) -> str:
        """Extract component name from description"""
        # Simple heuristics to extract component names
        words = description.split()
        
        # Look for common component patterns
        for i, word in enumerate(words):
            if word.lower() in ['system', 'module', 'component', 'service']:
                if i > 0:
                    return words[i-1].lower()
        
        # Fallback to first meaningful word
        for word in words:
            if len(word) > 3 and word.isalpha():
                return word.lower()
        
        return 'component'
    
    def _extract_config_key(self, description: str) -> str:
        """Extract configuration key from description"""
        # Look for config-related words
        words = description.lower().split()
        config_words = ['timeout', 'retry', 'limit', 'size', 'count', 'interval', 'mode', 'level']
        
        for word in words:
            if word in config_words:
                return word.upper()
        
        return 'CONFIG_VALUE'
    
    def _extract_feature_name(self, description: str) -> str:
        """Extract feature name from description"""
        # Simple feature name extraction
        words = description.split()
        
        for i, word in enumerate(words):
            if word.lower() in ['feature', 'capability', 'function']:
                if i > 0:
                    return '_'.join(words[max(0, i-2):i]).lower()
        
        # Use first few meaningful words
        meaningful_words = [w for w in words[:3] if len(w) > 2 and w.isalpha()]
        return '_'.join(meaningful_words).lower() if meaningful_words else 'new_feature'
    
    def _load_pattern_content(self, file_path: str) -> str:
        """Load pattern file content"""
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return ""
    
    def _execute_pattern_template(self, pattern_details: Dict, variables: Dict) -> Dict:
        """Execute the pattern template with substituted variables"""
        pattern_content = self._load_pattern_content(pattern_details['file_path'])
        
        if not pattern_content:
            return {'success': False, 'error': 'Could not load pattern content'}
        
        # Extract code template section
        code_template = self._extract_code_template(pattern_content)
        
        if not code_template:
            return {'success': False, 'error': 'No code template found in pattern'}
        
        # Substitute variables in template
        substituted_template = self._substitute_variables(code_template, variables)
        
        # Extract execution steps from pattern
        execution_steps = self._extract_execution_steps(pattern_content, substituted_template)
        
        # Execute steps with validation checkpoints
        return self._execute_steps_with_validation(execution_steps, substituted_template)
    
    def _extract_code_template(self, pattern_content: str) -> str:
        """Extract code template section from pattern"""
        # Look for code template section
        template_match = re.search(r'## Code Template\s*\n```(?:bash|python|sh)?\s*\n(.*?)\n```', 
                                 pattern_content, re.DOTALL)
        
        if template_match:
            return template_match.group(1)
        
        # Fallback: look for any code block
        code_blocks = re.findall(r'```(?:bash|python|sh)?\s*\n(.*?)\n```', pattern_content, re.DOTALL)
        
        if code_blocks:
            # Use the largest code block
            return max(code_blocks, key=len)
        
        return ""
    
    def _substitute_variables(self, template: str, variables: Dict) -> str:
        """Substitute template variables with actual values"""
        result = template
        
        for var, value in variables.items():
            placeholder = f"[{var}]"
            result = result.replace(placeholder, str(value))
        
        return result
    
    def _extract_execution_steps(self, pattern_content: str, substituted_template: str) -> List[Dict]:
        """Extract execution steps from pattern content"""
        steps = []
        
        # Look for step-by-step sections in the pattern
        step_patterns = [
            r'(\d+)\.\s*\*\*([^*]+)\*\*[:\s]*(.+?)(?=\n(?:\d+\.\s*\*\*|\n##|\Z))',
            r'(STEP \d+):\s*([^-\n]+)(.+?)(?=\nSTEP|\n##|\Z)',
            r'(Phase \d+):\s*([^-\n]+)(.+?)(?=\nPhase|\n##|\Z)'
        ]
        
        for pattern in step_patterns:
            matches = re.findall(pattern, pattern_content, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                step_num = match[0]
                step_title = match[1].strip()
                step_content = match[2].strip()
                
                steps.append({
                    'number': step_num,
                    'title': step_title,
                    'description': step_content,
                    'type': 'manual',
                    'validation': None
                })
        
        # If no explicit steps found, create steps from template functions
        if not steps:
            steps = self._extract_steps_from_template(substituted_template)
        
        return steps
    
    def _extract_steps_from_template(self, template: str) -> List[Dict]:
        """Extract execution steps from template functions"""
        steps = []
        
        # Look for function calls or main execution blocks
        function_calls = re.findall(r'^\s*#\s*(STEP|Phase)\s*(\d+)[:\s]*(.+)', template, re.MULTILINE)
        
        for match in function_calls:
            step_type = match[0]
            step_num = match[1]
            step_desc = match[2].strip()
            
            steps.append({
                'number': f"{step_type} {step_num}",
                'title': step_desc,
                'description': f"Execute {step_desc}",
                'type': 'automated',
                'validation': None
            })
        
        # If still no steps, create a single execution step
        if not steps:
            steps.append({
                'number': '1',
                'title': 'Execute Pattern Template',
                'description': 'Run the complete pattern template',
                'type': 'automated',
                'validation': None
            })
        
        return steps
    
    def _execute_steps_with_validation(self, steps: List[Dict], template: str) -> Dict:
        """Execute steps with validation checkpoints"""
        print(f"📋 Executing {len(steps)} steps with validation checkpoints")
        
        results = {
            'success': True,
            'steps_completed': 0,
            'steps_total': len(steps),
            'step_results': [],
            'template_output': None,
            'validation_summary': []
        }
        
        # Create execution script
        script_path = self._create_execution_script(template)
        
        try:
            for i, step in enumerate(steps, 1):
                print(f"\n📌 Step {i}: {step['title']}")
                print(f"   {step['description']}")
                
                # Add step to execution log
                step_result = {
                    'step_number': step['number'],
                    'title': step['title'],
                    'start_time': datetime.now().isoformat(),
                    'status': 'started'
                }
                
                if self.interactive:
                    # Ask user if they want to proceed with this step
                    proceed = input(f"   Execute this step? (y/n/skip): ").strip().lower()
                    
                    if proceed == 'n':
                        step_result.update({
                            'status': 'cancelled',
                            'end_time': datetime.now().isoformat()
                        })
                        results['step_results'].append(step_result)
                        results['success'] = False
                        break
                    elif proceed == 'skip':
                        step_result.update({
                            'status': 'skipped',
                            'end_time': datetime.now().isoformat()
                        })
                        results['step_results'].append(step_result)
                        continue
                
                # Execute step
                try:
                    if step['type'] == 'automated' and script_path:
                        # Execute the template script
                        exec_result = self._execute_script(script_path)
                        step_result.update({
                            'status': 'completed' if exec_result['success'] else 'failed',
                            'output': exec_result.get('output', ''),
                            'error': exec_result.get('error', ''),
                            'end_time': datetime.now().isoformat()
                        })
                        
                        if not exec_result['success']:
                            results['success'] = False
                            
                    else:
                        # Manual step - just mark as completed
                        print("   ✅ Manual step - marked as completed")
                        step_result.update({
                            'status': 'completed',
                            'end_time': datetime.now().isoformat()
                        })
                    
                    results['steps_completed'] += 1
                    
                except Exception as e:
                    step_result.update({
                        'status': 'error',
                        'error': str(e),
                        'end_time': datetime.now().isoformat()
                    })
                    results['success'] = False
                
                results['step_results'].append(step_result)
                
                # Validation checkpoint
                if step_result['status'] == 'completed':
                    validation_result = self._validate_step_completion(step, step_result)
                    results['validation_summary'].append(validation_result)
                    
                    if not validation_result['passed']:
                        print(f"   ⚠️ Validation failed: {validation_result['message']}")
                        if self.interactive:
                            continue_anyway = input("   Continue anyway? (y/n): ").strip().lower()
                            if continue_anyway != 'y':
                                results['success'] = False
                                break
        
        finally:
            # Cleanup temporary script
            if script_path and script_path.exists():
                script_path.unlink()
        
        return results
    
    def _create_execution_script(self, template: str) -> Optional[Path]:
        """Create executable script from template"""
        try:
            # Create temporary script file
            script_file = tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False)
            
            # Add shebang and make executable
            script_content = f"#!/bin/bash\n# Generated execution script\n# User: Christian\n\n{template}"
            
            script_file.write(script_content)
            script_file.close()
            
            script_path = Path(script_file.name)
            script_path.chmod(0o755)
            
            return script_path
            
        except Exception as e:
            print(f"Failed to create execution script: {e}")
            return None
    
    def _execute_script(self, script_path: Path) -> Dict:
        """Execute the pattern script"""
        try:
            # Change to project root for execution
            original_cwd = os.getcwd()
            os.chdir(self.project_root)
            
            # Execute script
            result = subprocess.run(
                [str(script_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                'success': result.returncode == 0,
                'return_code': result.returncode,
                'output': result.stdout,
                'error': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Script execution timed out (5 minutes)'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Script execution failed: {str(e)}'
            }
        finally:
            os.chdir(original_cwd)
    
    def _validate_step_completion(self, step: Dict, step_result: Dict) -> Dict:
        """Validate step completion"""
        validation = {
            'step_number': step['number'],
            'passed': True,
            'message': 'Step completed successfully',
            'checks': []
        }
        
        # Basic validation checks
        if step_result['status'] == 'completed':
            validation['checks'].append({'check': 'Status', 'passed': True, 'message': 'Step marked as completed'})
        else:
            validation['passed'] = False
            validation['message'] = f"Step failed with status: {step_result['status']}"
            validation['checks'].append({'check': 'Status', 'passed': False, 'message': validation['message']})
        
        # Check for errors
        if step_result.get('error'):
            validation['passed'] = False
            validation['message'] = f"Step completed with errors: {step_result['error']}"
            validation['checks'].append({'check': 'Errors', 'passed': False, 'message': step_result['error']})
        else:
            validation['checks'].append({'check': 'Errors', 'passed': True, 'message': 'No errors detected'})
        
        return validation
    
    def _finalize_execution(self, status: str, message: str, additional_data: Dict = None) -> Dict:
        """Finalize execution and save results"""
        self.current_execution['status'] = status
        self.current_execution['end_time'] = datetime.now().isoformat()
        self.current_execution['message'] = message
        
        if additional_data:
            self.current_execution.update(additional_data)
        
        # Save execution log
        self._save_execution_log()
        
        # Display summary
        self._display_execution_summary()
        
        return self.current_execution
    
    def _save_execution_log(self):
        """Save execution log to file"""
        if not self.current_execution:
            return
        
        log_file = self.log_dir / f"{self.current_execution['id']}.json"
        
        try:
            with open(log_file, 'w') as f:
                json.dump(self.current_execution, f, indent=2)
            
            print(f"\n📋 Execution log saved: {log_file}")
            
        except Exception as e:
            print(f"Failed to save execution log: {e}")
    
    def _display_execution_summary(self):
        """Display execution summary"""
        if not self.current_execution:
            return
        
        print("\n" + "=" * 60)
        print("📊 EXECUTION SUMMARY")
        print("=" * 60)
        
        print(f"Execution ID: {self.current_execution['id']}")
        print(f"Status: {self.current_execution['status'].upper()}")
        print(f"Pattern: {self.current_execution.get('pattern_key', 'N/A')}")
        print(f"Message: {self.current_execution['message']}")
        
        # Show step results if available
        if 'step_results' in self.current_execution:
            step_results = self.current_execution['step_results']
            total_steps = len(step_results)
            completed_steps = len([s for s in step_results if s['status'] == 'completed'])
            
            print(f"Steps: {completed_steps}/{total_steps} completed")
            
            for step in step_results:
                status_icon = {
                    'completed': '✅',
                    'failed': '❌',
                    'error': '💥',
                    'skipped': '⏭️',
                    'cancelled': '🚫'
                }.get(step['status'], '❓')
                
                print(f"  {status_icon} {step['title']} ({step['status']})")
        
        # Show validation summary
        if 'validation_summary' in self.current_execution:
            validation_results = self.current_execution['validation_summary']
            passed_validations = len([v for v in validation_results if v['passed']])
            total_validations = len(validation_results)
            
            print(f"Validations: {passed_validations}/{total_validations} passed")
        
        print("=" * 60)

def main():
    """Interactive pattern executor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CLAUDE Pattern Executor')
    parser.add_argument('problem', nargs='?', help='Problem description')
    parser.add_argument('--pattern', '-p', help='Specific pattern to use')
    parser.add_argument('--non-interactive', '-n', action='store_true', help='Non-interactive mode')
    parser.add_argument('--project-root', '-r', default='.', help='Project root directory')
    
    args = parser.parse_args()
    
    # Interactive mode if no problem provided
    if not args.problem:
        print("🚀 CLAUDE Pattern Executor - Interactive Mode")
        print("User: Christian")
        print("=" * 50)
        
        while True:
            try:
                problem = input("\nDescribe the problem you want to solve (or 'quit' to exit): ").strip()
                
                if problem.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not problem:
                    print("Please provide a problem description.")
                    continue
                
                # Execute pattern
                executor = PatternExecutor(args.project_root, interactive=not args.non_interactive)
                result = executor.find_and_execute_pattern(problem, args.pattern)
                
                if result['status'] == 'completed':
                    print("\n🎉 Pattern execution completed successfully!")
                else:
                    print(f"\n❌ Pattern execution failed: {result['message']}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    else:
        # Command line mode
        executor = PatternExecutor(args.project_root, interactive=not args.non_interactive)
        result = executor.find_and_execute_pattern(args.problem, args.pattern)
        
        # Exit with appropriate code
        if result['status'] == 'completed':
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()