#!/usr/bin/env python3
"""
Pattern System Orchestrator - Unified Integration Hub
Connects pattern_matcher.py, pattern execution, learning capture, and context systems
with caching integration via .claude_session_state.json

This orchestrator serves as the central command center for all pattern-related operations,
providing a single interface for the entire pattern ecosystem.

Created for: Christian
Purpose: Unify pattern matching, execution, learning, and context management
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import subprocess
import logging

# Import existing components
import sys
sys.path.append(str(Path(__file__).parent))
from pattern_matcher import PatternMatcher
from session_state_manager import SessionStateManager, SmartConfigurationManager

@dataclass
class PatternExecutionResult:
    """Result of pattern execution"""
    pattern_key: str
    success: bool
    execution_time: float
    output: str
    errors: List[str]
    side_effects: List[str]
    learned_insights: List[str]
    context_updates: Dict[str, Any]

@dataclass
class LearningCapture:
    """Captured learning from pattern usage"""
    pattern_key: str
    problem_context: str
    adaptation_made: str
    effectiveness_score: float
    timestamp: float
    user_feedback: Optional[str] = None
    reusability_potential: str = "medium"

@dataclass
class ContextSnapshot:
    """Context state at point in time"""
    timestamp: float
    session_id: str
    active_patterns: List[str]
    recent_executions: List[str]
    learning_state: Dict[str, Any]
    performance_metrics: Dict[str, float]

class PatternExecutor:
    """
    Executes patterns with monitoring, error handling, and learning capture
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.execution_log = []
        
    def execute_pattern(self, pattern_key: str, context: Dict[str, Any]) -> PatternExecutionResult:
        """Execute a pattern with full monitoring and capture"""
        start_time = time.time()
        
        try:
            # Load pattern details
            pattern_file = self._get_pattern_file(pattern_key)
            if not pattern_file.exists():
                raise FileNotFoundError(f"Pattern file not found: {pattern_file}")
            
            pattern_content = pattern_file.read_text()
            
            # Extract executable components
            executable_steps = self._extract_executable_steps(pattern_content)
            
            # Execute pattern steps
            output_lines = []
            errors = []
            side_effects = []
            
            for i, step in enumerate(executable_steps):
                try:
                    step_result = self._execute_step(step, context)
                    output_lines.extend(step_result['output'])
                    side_effects.extend(step_result['side_effects'])
                except Exception as e:
                    errors.append(f"Step {i+1}: {str(e)}")
            
            # Capture learning insights
            learned_insights = self._capture_execution_insights(
                pattern_key, context, output_lines, errors
            )
            
            # Generate context updates
            context_updates = self._generate_context_updates(
                pattern_key, context, output_lines, errors
            )
            
            execution_time = time.time() - start_time
            success = len(errors) == 0
            
            result = PatternExecutionResult(
                pattern_key=pattern_key,
                success=success,
                execution_time=execution_time,
                output='\n'.join(output_lines),
                errors=errors,
                side_effects=side_effects,
                learned_insights=learned_insights,
                context_updates=context_updates
            )
            
            self.execution_log.append(result)
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            return PatternExecutionResult(
                pattern_key=pattern_key,
                success=False,
                execution_time=execution_time,
                output="",
                errors=[str(e)],
                side_effects=[],
                learned_insights=[],
                context_updates={}
            )
    
    def _get_pattern_file(self, pattern_key: str) -> Path:
        """Get pattern file path from pattern key"""
        category, name = pattern_key.split('/', 1)
        return self.project_root / "patterns" / category / f"{name}.md"
    
    def _extract_executable_steps(self, pattern_content: str) -> List[Dict[str, Any]]:
        """Extract executable steps from pattern markdown"""
        import re
        
        steps = []
        
        # Find code blocks with execution hints
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', pattern_content, re.DOTALL)
        
        for lang, code in code_blocks:
            if lang in ['bash', 'shell', 'python', 'javascript']:
                steps.append({
                    'type': 'code',
                    'language': lang,
                    'content': code.strip()
                })
        
        # Find explicit step instructions
        step_matches = re.findall(r'^\d+\.\s+(.+?)(?=\n\d+\.|\n#|\Z)', pattern_content, re.MULTILINE | re.DOTALL)
        
        for step_text in step_matches:
            steps.append({
                'type': 'instruction',
                'content': step_text.strip()
            })
        
        return steps
    
    def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single pattern step"""
        if step['type'] == 'code':
            return self._execute_code_step(step, context)
        elif step['type'] == 'instruction':
            return self._execute_instruction_step(step, context)
        else:
            return {'output': [], 'side_effects': []}
    
    def _execute_code_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code step safely"""
        output = []
        side_effects = []
        
        try:
            if step['language'] in ['bash', 'shell']:
                # Execute bash commands with safety checks
                safe_commands = self._validate_bash_safety(step['content'])
                if safe_commands:
                    result = subprocess.run(
                        step['content'], 
                        shell=True, 
                        capture_output=True, 
                        text=True,
                        cwd=self.project_root,
                        timeout=30
                    )
                    output.append(result.stdout)
                    if result.stderr:
                        output.append(f"STDERR: {result.stderr}")
                    side_effects.append(f"Executed bash: {step['content'][:50]}...")
                else:
                    output.append("SKIPPED: Unsafe bash command detected")
            
            elif step['language'] == 'python':
                # Execute Python code in controlled environment
                output.append("SIMULATED: Python code execution")
                side_effects.append(f"Would execute Python: {step['content'][:50]}...")
            
            else:
                output.append(f"UNSUPPORTED: {step['language']} execution")
                
        except subprocess.TimeoutExpired:
            output.append("ERROR: Command timed out")
        except Exception as e:
            output.append(f"ERROR: {str(e)}")
        
        return {'output': output, 'side_effects': side_effects}
    
    def _execute_instruction_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process instruction step"""
        return {
            'output': [f"INSTRUCTION: {step['content']}"],
            'side_effects': []
        }
    
    def _validate_bash_safety(self, command: str) -> bool:
        """Validate bash command safety"""
        unsafe_patterns = [
            'rm -rf', 'sudo', 'chmod 777', '> /dev/null', 'curl http',
            'wget http', 'dd if=', 'mkfs', 'fdisk', 'format'
        ]
        
        command_lower = command.lower()
        return not any(pattern in command_lower for pattern in unsafe_patterns)
    
    def _capture_execution_insights(self, pattern_key: str, context: Dict[str, Any], 
                                  output: List[str], errors: List[str]) -> List[str]:
        """Capture insights from pattern execution"""
        insights = []
        
        if errors:
            insights.append(f"Pattern {pattern_key} encountered {len(errors)} errors")
        
        if len(output) > 5:
            insights.append(f"Pattern {pattern_key} generated substantial output")
        
        # Analyze output for success indicators
        output_text = ' '.join(output).lower()
        if 'success' in output_text or 'completed' in output_text:
            insights.append(f"Pattern {pattern_key} showed success indicators")
        
        return insights
    
    def _generate_context_updates(self, pattern_key: str, context: Dict[str, Any],
                                output: List[str], errors: List[str]) -> Dict[str, Any]:
        """Generate context updates from execution"""
        return {
            'last_executed_pattern': pattern_key,
            'execution_success': len(errors) == 0,
            'output_length': len(output),
            'timestamp': time.time()
        }

class LearningCapturer:
    """
    Captures and analyzes learning from pattern usage for continuous improvement
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.learning_file = self.project_root / "memory" / "learning_archive.md"
        self.pattern_adaptations = {}
        
    def capture_learning(self, execution_result: PatternExecutionResult, 
                        problem_context: str, adaptation_made: str = "") -> LearningCapture:
        """Capture learning from pattern execution"""
        
        # Calculate effectiveness score
        effectiveness_score = self._calculate_effectiveness(execution_result)
        
        # Assess reusability potential
        reusability_potential = self._assess_reusability(execution_result, problem_context)
        
        learning = LearningCapture(
            pattern_key=execution_result.pattern_key,
            problem_context=problem_context,
            adaptation_made=adaptation_made,
            effectiveness_score=effectiveness_score,
            timestamp=time.time(),
            reusability_potential=reusability_potential
        )
        
        # Store learning
        self._store_learning(learning)
        
        return learning
    
    def _calculate_effectiveness(self, result: PatternExecutionResult) -> float:
        """Calculate pattern effectiveness score (0.0 to 1.0)"""
        base_score = 0.5
        
        # Success factor
        if result.success:
            base_score += 0.3
        else:
            base_score -= 0.2
        
        # Execution time factor (faster is better, up to a point)
        if result.execution_time < 1.0:
            base_score += 0.1
        elif result.execution_time > 10.0:
            base_score -= 0.1
        
        # Output quality factor
        if result.output and len(result.output) > 10:
            base_score += 0.1
        
        # Learning insights factor
        if result.learned_insights:
            base_score += 0.1
        
        return max(0.0, min(1.0, base_score))
    
    def _assess_reusability(self, result: PatternExecutionResult, context: str) -> str:
        """Assess reusability potential of the pattern application"""
        if result.success and result.learned_insights:
            return "high"
        elif result.success:
            return "medium"
        else:
            return "low"
    
    def _store_learning(self, learning: LearningCapture):
        """Store learning capture in archive"""
        try:
            # Ensure memory directory exists
            self.learning_file.parent.mkdir(exist_ok=True)
            
            # Append learning to archive
            timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(learning.timestamp))
            
            learning_entry = f"""
## Learning Capture - {timestamp_str}

**Pattern**: {learning.pattern_key}
**Problem Context**: {learning.problem_context}
**Adaptation Made**: {learning.adaptation_made}
**Effectiveness Score**: {learning.effectiveness_score:.2f}
**Reusability**: {learning.reusability_potential}

---
"""
            
            with open(self.learning_file, 'a') as f:
                f.write(learning_entry)
                
        except Exception as e:
            print(f"⚠️ Failed to store learning: {e}")
    
    def get_pattern_learning_history(self, pattern_key: str) -> List[LearningCapture]:
        """Get learning history for a specific pattern"""
        # Implementation would parse learning_archive.md
        # For now, return empty list
        return []
    
    def suggest_adaptations(self, pattern_key: str, current_context: str) -> List[str]:
        """Suggest adaptations based on learning history"""
        # Analyze learning history to suggest improvements
        suggestions = []
        
        # Default suggestions based on common patterns
        suggestions.append("Consider adding error handling for edge cases")
        suggestions.append("Add logging for better debugging")
        suggestions.append("Include validation steps before execution")
        
        return suggestions

class ContextEngine:
    """
    Manages context state, history, and intelligent context switching
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.context_file = self.project_root / ".claude_context_state.json"
        self.current_context = {}
        self.context_history = []
        
    def capture_context_snapshot(self, session_id: str, active_patterns: List[str],
                               recent_executions: List[str]) -> ContextSnapshot:
        """Capture current context state"""
        snapshot = ContextSnapshot(
            timestamp=time.time(),
            session_id=session_id,
            active_patterns=active_patterns,
            recent_executions=recent_executions,
            learning_state=self._get_learning_state(),
            performance_metrics=self._get_performance_metrics()
        )
        
        self.context_history.append(snapshot)
        self._save_context_state()
        
        return snapshot
    
    def restore_context(self, timestamp: float) -> Optional[ContextSnapshot]:
        """Restore context from specific timestamp"""
        for snapshot in reversed(self.context_history):
            if snapshot.timestamp <= timestamp:
                self.current_context = asdict(snapshot)
                return snapshot
        return None
    
    def _get_learning_state(self) -> Dict[str, Any]:
        """Get current learning state summary"""
        return {
            'total_patterns_used': len(set(self.current_context.get('recent_patterns', []))),
            'success_rate': self.current_context.get('success_rate', 0.0),
            'last_learning_update': time.time()
        }
    
    def _get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        return {
            'avg_execution_time': self.current_context.get('avg_execution_time', 0.0),
            'cache_hit_rate': self.current_context.get('cache_hit_rate', 0.0),
            'error_rate': self.current_context.get('error_rate', 0.0)
        }
    
    def _save_context_state(self):
        """Save context state to disk"""
        try:
            context_data = {
                'current_context': self.current_context,
                'history_count': len(self.context_history),
                'last_update': time.time()
            }
            
            with open(self.context_file, 'w') as f:
                json.dump(context_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save context state: {e}")
    
    def update_context(self, updates: Dict[str, Any]):
        """Update current context with new information"""
        self.current_context.update(updates)
        self._save_context_state()

class PatternSystemOrchestrator:
    """
    Central orchestrator that coordinates all pattern system components
    Provides unified interface for pattern operations with caching integration
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        
        # Initialize components
        self.pattern_matcher = PatternMatcher(project_root)
        self.pattern_executor = PatternExecutor(project_root)
        self.learning_capturer = LearningCapturer(project_root)
        self.context_engine = ContextEngine(project_root)
        
        # Session and caching integration
        self.session_manager = SessionStateManager(project_root)
        self.config_manager = SmartConfigurationManager(project_root)
        
        # Performance tracking
        self.operation_metrics = {
            'patterns_matched': 0,
            'patterns_executed': 0,
            'learning_captures': 0,
            'cache_hits': 0,
            'total_execution_time': 0.0
        }
        
        # Setup logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for orchestrator operations"""
        log_file = self.project_root / "logs" / "pattern_orchestrator.log"
        log_file.parent.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('PatternOrchestrator')
    
    def solve_problem(self, problem_description: str, max_patterns: int = 3, 
                     execute_best: bool = False) -> Dict[str, Any]:
        """
        Main problem-solving interface that coordinates all pattern operations
        
        Args:
            problem_description: Description of the problem to solve
            max_patterns: Maximum number of patterns to consider
            execute_best: Whether to execute the best matching pattern
            
        Returns:
            Complete solution report with patterns, execution results, and learning
        """
        start_time = time.time()
        
        self.logger.info(f"Solving problem: {problem_description[:100]}...")
        
        try:
            # Step 1: Pattern Matching (with caching)
            patterns = self._match_patterns_cached(problem_description, max_patterns)
            
            if not patterns:
                return {
                    'success': False,
                    'message': 'No matching patterns found',
                    'patterns': [],
                    'execution_results': [],
                    'learning_captures': [],
                    'total_time': time.time() - start_time
                }
            
            # Step 2: Pattern Execution (if requested)
            execution_results = []
            learning_captures = []
            
            if execute_best and patterns:
                best_pattern = patterns[0]
                
                # Prepare execution context
                context = self._prepare_execution_context(problem_description, best_pattern)
                
                # Execute pattern
                exec_result = self.pattern_executor.execute_pattern(
                    best_pattern['pattern_key'], context
                )
                execution_results.append(exec_result)
                
                # Capture learning
                learning = self.learning_capturer.capture_learning(
                    exec_result, problem_description, ""
                )
                learning_captures.append(learning)
                
                # Update context
                self.context_engine.update_context(exec_result.context_updates)
                
                self.operation_metrics['patterns_executed'] += 1
                self.operation_metrics['learning_captures'] += 1
            
            # Step 3: Update performance metrics
            total_time = time.time() - start_time
            self.operation_metrics['total_execution_time'] += total_time
            
            # Step 4: Update session cache
            self._update_session_cache({
                'last_problem': problem_description,
                'patterns_found': len(patterns),
                'execution_success': execution_results and execution_results[0].success,
                'timestamp': time.time()
            })
            
            return {
                'success': True,
                'patterns': patterns,
                'execution_results': [asdict(r) for r in execution_results],
                'learning_captures': [asdict(l) for l in learning_captures],
                'total_time': total_time,
                'metrics': self.operation_metrics.copy(),
                'suggestions': self._generate_suggestions(patterns, execution_results)
            }
            
        except Exception as e:
            self.logger.error(f"Error solving problem: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'patterns': [],
                'execution_results': [],
                'learning_captures': [],
                'total_time': time.time() - start_time
            }
    
    def _match_patterns_cached(self, problem_description: str, max_patterns: int) -> List[Dict[str, Any]]:
        """Match patterns with caching optimization"""
        
        # Check cache for similar problems
        cache_key = hashlib.md5(problem_description.encode()).hexdigest()[:12]
        
        # Use session cache to store recent pattern matches
        cached_config = self.session_manager.get_cached_config()
        if cached_config and 'recent_pattern_matches' in cached_config:
            if cache_key in cached_config['recent_pattern_matches']:
                self.operation_metrics['cache_hits'] += 1
                self.logger.info("Using cached pattern matches")
                return cached_config['recent_pattern_matches'][cache_key]
        
        # Perform fresh pattern matching
        patterns = self.pattern_matcher.match_patterns(problem_description, max_patterns)
        self.operation_metrics['patterns_matched'] += len(patterns)
        
        # Cache the results
        self._cache_pattern_matches(cache_key, patterns)
        
        return patterns
    
    def _cache_pattern_matches(self, cache_key: str, patterns: List[Dict[str, Any]]):
        """Cache pattern matching results"""
        try:
            # Update session cache with pattern matches
            session_file = self.project_root / ".claude_session_state.json"
            
            if session_file.exists():
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                if 'recent_pattern_matches' not in session_data:
                    session_data['recent_pattern_matches'] = {}
                
                # Keep only last 10 cached matches
                if len(session_data['recent_pattern_matches']) >= 10:
                    oldest_key = min(session_data['recent_pattern_matches'].keys())
                    del session_data['recent_pattern_matches'][oldest_key]
                
                session_data['recent_pattern_matches'][cache_key] = patterns
                session_data['last_cache_update'] = time.time()
                
                with open(session_file, 'w') as f:
                    json.dump(session_data, f, indent=2)
                    
        except Exception as e:
            self.logger.warning(f"Failed to cache pattern matches: {e}")
    
    def _prepare_execution_context(self, problem_description: str, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context for pattern execution"""
        return {
            'problem_description': problem_description,
            'pattern_confidence': pattern.get('confidence', 0),
            'project_root': str(self.project_root),
            'session_id': self.session_manager.session_id,
            'execution_timestamp': time.time()
        }
    
    def _update_session_cache(self, updates: Dict[str, Any]):
        """Update session cache with operation results"""
        try:
            session_file = self.project_root / ".claude_session_state.json"
            
            if session_file.exists():
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                if 'orchestrator_state' not in session_data:
                    session_data['orchestrator_state'] = {}
                
                session_data['orchestrator_state'].update(updates)
                
                with open(session_file, 'w') as f:
                    json.dump(session_data, f, indent=2)
                    
        except Exception as e:
            self.logger.warning(f"Failed to update session cache: {e}")
    
    def _generate_suggestions(self, patterns: List[Dict[str, Any]], 
                            execution_results: List[PatternExecutionResult]) -> List[str]:
        """Generate suggestions based on patterns and execution results"""
        suggestions = []
        
        if patterns:
            if len(patterns) > 1:
                suggestions.append(f"Consider trying alternative pattern: {patterns[1]['title']}")
            
            if execution_results and not execution_results[0].success:
                suggestions.append("Pattern execution encountered errors - consider manual review")
                suggestions.extend(
                    self.learning_capturer.suggest_adaptations(
                        patterns[0]['pattern_key'], 
                        execution_results[0].output
                    )
                )
        
        return suggestions
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        pattern_stats = self.pattern_matcher.get_statistics()
        session_summary = self.config_manager.get_session_summary()
        
        return {
            'pattern_library': pattern_stats,
            'session_state': session_summary,
            'operation_metrics': self.operation_metrics,
            'components_loaded': {
                'pattern_matcher': True,
                'pattern_executor': True,
                'learning_capturer': True,
                'context_engine': True,
                'session_manager': self.session_manager.is_session_active()
            },
            'cache_status': {
                'session_file_exists': (self.project_root / ".claude_session_state.json").exists(),
                'context_file_exists': (self.project_root / ".claude_context_state.json").exists(),
                'learning_archive_exists': (self.project_root / "memory" / "learning_archive.md").exists()
            },
            'timestamp': time.time()
        }
    
    def cleanup_caches(self, max_age_hours: int = 24):
        """Cleanup old cache entries"""
        try:
            # Cleanup session cache
            self.session_manager.cleanup_old_sessions()
            
            # Cleanup pattern match cache
            session_file = self.project_root / ".claude_session_state.json"
            if session_file.exists():
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                if 'recent_pattern_matches' in session_data:
                    # Remove old cached matches
                    current_time = time.time()
                    max_age_seconds = max_age_hours * 3600
                    
                    # For simplicity, clear all if any are old
                    last_update = session_data.get('last_cache_update', 0)
                    if current_time - last_update > max_age_seconds:
                        session_data['recent_pattern_matches'] = {}
                        session_data['last_cache_update'] = current_time
                        
                        with open(session_file, 'w') as f:
                            json.dump(session_data, f, indent=2)
                
            self.logger.info("Cache cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Cache cleanup failed: {e}")

# Convenience functions for integration with existing CLAUDE.md
def quick_pattern_solve(problem_description: str, execute: bool = False) -> Dict[str, Any]:
    """
    Quick pattern-based problem solving
    Use this as the primary interface for pattern operations
    """
    orchestrator = PatternSystemOrchestrator()
    return orchestrator.solve_problem(problem_description, execute_best=execute)

def get_pattern_system_status() -> Dict[str, Any]:
    """
    Get pattern system status
    Use this for health checks and debugging
    """
    orchestrator = PatternSystemOrchestrator()
    return orchestrator.get_system_status()

def cleanup_pattern_caches():
    """
    Cleanup pattern system caches
    Use this for maintenance operations
    """
    orchestrator = PatternSystemOrchestrator()
    orchestrator.cleanup_caches()

@contextmanager
def pattern_operation_context(problem_description: str):
    """
    Context manager for pattern operations with automatic cleanup
    """
    orchestrator = PatternSystemOrchestrator()
    
    # Capture initial context
    session_id = orchestrator.session_manager.session_id
    snapshot = orchestrator.context_engine.capture_context_snapshot(
        session_id, [], []
    )
    
    try:
        yield orchestrator
    finally:
        # Cleanup and update context
        orchestrator.context_engine.update_context({
            'operation_completed': time.time(),
            'problem_description': problem_description
        })

def main():
    """Test the pattern system orchestrator"""
    print("🎭 Pattern System Orchestrator Test")
    print("=" * 60)
    
    orchestrator = PatternSystemOrchestrator()
    
    # Display system status
    print("📊 System Status")
    print("-" * 30)
    status = orchestrator.get_system_status()
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for subkey, subvalue in value.items():
                print(f"    {subkey}: {subvalue}")
        else:
            print(f"  {key}: {value}")
    print()
    
    # Test problem solving
    test_problems = [
        "I need to optimize boot sequence performance",
        "How do I fix session continuity errors?",
        "Want to implement automated backup system",
    ]
    
    for i, problem in enumerate(test_problems, 1):
        print(f"🔍 Test {i}: {problem}")
        print("-" * 50)
        
        result = orchestrator.solve_problem(problem, max_patterns=2, execute_best=False)
        
        if result['success']:
            print(f"  ✅ Found {len(result['patterns'])} patterns")
            for pattern in result['patterns']:
                print(f"     • {pattern['title']} ({pattern['confidence']:.1f}%)")
            print(f"  ⚡ Total time: {result['total_time']*1000:.1f}ms")
        else:
            print(f"  ❌ Failed: {result.get('error', 'No patterns found')}")
        print()
    
    # Test with execution
    print("🚀 Test with Pattern Execution")
    print("-" * 40)
    
    if test_problems:
        result = orchestrator.solve_problem(
            test_problems[0], 
            max_patterns=1, 
            execute_best=True
        )
        
        if result['success'] and result['execution_results']:
            exec_result = result['execution_results'][0]
            print(f"  Pattern: {exec_result['pattern_key']}")
            print(f"  Success: {exec_result['success']}")
            print(f"  Execution time: {exec_result['execution_time']*1000:.1f}ms")
            print(f"  Learning insights: {len(exec_result['learned_insights'])}")
        else:
            print("  No execution results available")
    
    print("\n🧹 Running cleanup...")
    orchestrator.cleanup_caches()
    
    print("\n✅ Pattern System Orchestrator test completed!")

if __name__ == "__main__":
    main()