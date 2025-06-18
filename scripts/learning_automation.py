#!/usr/bin/env python3
"""
Learning Archive Automation - Automatic Pattern Detection & Success Tracking
Lightweight integration with existing session_state_manager and context_engine.

Features:
1. Direct code pattern detection from git diffs
2. Automatic success metric capture from operations
3. Auto-learning from Christian's coding style and preferences
4. Pattern candidate generation and promotion tracking

Created for: Christian
Integration: Hooks into existing session management (minimal overhead)
"""

import os
import re
import json
import time
import hashlib
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict

@dataclass
class CodePattern:
    """Detected code pattern with metrics."""
    pattern_id: str
    pattern_type: str  # function, class, config, workflow
    pattern_signature: str  # Key identifying characteristics
    usage_count: int
    success_rate: float
    complexity_score: int  # 1-10
    context_tags: List[str]
    first_seen: str
    last_used: str
    quality_metrics: Dict[str, float]

@dataclass
class LearningSession:
    """Session learning data."""
    session_id: str
    timestamp: str
    patterns_detected: List[str]
    patterns_applied: List[str]
    success_indicators: List[str]
    code_style_observations: Dict[str, Any]
    performance_metrics: Dict[str, float]
    user_feedback_signals: List[str]

class AutoLearningEngine:
    """Lightweight learning engine that integrates with existing systems."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.learning_archive = self.project_root / "memory" / "learning_archive.md"
        self.learning_cache = self.project_root / ".claude_learning_cache.json"
        self.session_patterns = {}
        self.style_profile = {}
        
        # Load existing learning data
        self._load_learning_cache()
        
    def _load_learning_cache(self):
        """Load cached learning data for fast access."""
        try:
            if self.learning_cache.exists():
                with open(self.learning_cache, 'r') as f:
                    cache_data = json.load(f)
                    self.session_patterns = cache_data.get('patterns', {})
                    self.style_profile = cache_data.get('style_profile', {})
        except Exception:
            self.session_patterns = {}
            self.style_profile = {}
    
    def _save_learning_cache(self):
        """Save learning cache for persistence."""
        try:
            cache_data = {
                'patterns': self.session_patterns,
                'style_profile': self.style_profile,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.learning_cache, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            pass  # Silent fail to avoid disrupting main operations
    
    def detect_code_patterns_from_git(self) -> List[CodePattern]:
        """Detect code patterns from recent git changes."""
        patterns = []
        
        try:
            # Get recent git diff (last 5 commits)
            result = subprocess.run(
                ['git', 'diff', 'HEAD~5..HEAD', '--unified=0'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return patterns
                
            diff_content = result.stdout
            
            # Pattern detection rules
            detected = self._analyze_diff_patterns(diff_content)
            
            for pattern_data in detected:
                pattern = CodePattern(
                    pattern_id=self._generate_pattern_id(pattern_data['signature']),
                    pattern_type=pattern_data['type'],
                    pattern_signature=pattern_data['signature'],
                    usage_count=1,
                    success_rate=1.0,  # Assume success until proven otherwise
                    complexity_score=pattern_data['complexity'],
                    context_tags=pattern_data['tags'],
                    first_seen=datetime.now().isoformat(),
                    last_used=datetime.now().isoformat(),
                    quality_metrics=self._assess_pattern_quality(pattern_data)
                )
                patterns.append(pattern)
                
        except Exception as e:
            # Silent fail - don't disrupt main operations
            pass
            
        return patterns
    
    def _analyze_diff_patterns(self, diff_content: str) -> List[Dict[str, Any]]:
        """Analyze git diff for code patterns."""
        patterns = []
        
        # Function definition patterns
        function_matches = re.findall(r'\+\s*def\s+(\w+)\s*\([^)]*\):', diff_content)
        for func_name in function_matches:
            patterns.append({
                'type': 'function',
                'signature': f'def {func_name}',
                'complexity': self._estimate_function_complexity(diff_content, func_name),
                'tags': ['function', 'python', 'implementation']
            })
        
        # Class definition patterns
        class_matches = re.findall(r'\+\s*class\s+(\w+)', diff_content)
        for class_name in class_matches:
            patterns.append({
                'type': 'class',
                'signature': f'class {class_name}',
                'complexity': 6,  # Classes are inherently more complex
                'tags': ['class', 'python', 'architecture']
            })
        
        # Configuration patterns
        config_matches = re.findall(r'\+\s*(\w+)\s*=\s*([^;\n]+)', diff_content)
        for var_name, value in config_matches:
            if any(keyword in var_name.lower() for keyword in ['config', 'setting', 'param', 'option']):
                patterns.append({
                    'type': 'config',
                    'signature': f'{var_name} = {value[:50]}',
                    'complexity': 3,
                    'tags': ['config', 'setting', 'parameter']
                })
        
        # Error handling patterns
        if '+' in diff_content and any(keyword in diff_content for keyword in ['try:', 'except:', 'catch']):
            patterns.append({
                'type': 'error_handling',
                'signature': 'try_except_pattern',
                'complexity': 4,
                'tags': ['error_handling', 'robustness', 'quality']
            })
        
        # Optimization patterns
        if any(keyword in diff_content.lower() for keyword in ['optimization', 'performance', 'cache', 'speed']):
            patterns.append({
                'type': 'optimization',
                'signature': 'performance_optimization',
                'complexity': 7,
                'tags': ['optimization', 'performance', 'improvement']
            })
        
        return patterns
    
    def _estimate_function_complexity(self, diff_content: str, func_name: str) -> int:
        """Estimate function complexity based on diff content."""
        # Simple heuristic based on content
        func_context = re.search(rf'def\s+{func_name}.*?(?=\ndef|\Z)', diff_content, re.DOTALL)
        if not func_context:
            return 3
        
        content = func_context.group(0)
        complexity = 1
        
        # Add complexity for control structures
        complexity += len(re.findall(r'\b(if|while|for|with)\b', content))
        complexity += len(re.findall(r'\b(try|except|finally)\b', content)) * 2
        complexity += len(re.findall(r'\breturn\b', content))
        
        return min(complexity, 10)
    
    def _assess_pattern_quality(self, pattern_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess pattern quality metrics."""
        return {
            'readability': 8.0,  # Default assumption
            'maintainability': 7.5,
            'performance': 8.0,
            'reliability': 7.5,
            'documentation': 6.0
        }
    
    def _generate_pattern_id(self, signature: str) -> str:
        """Generate unique pattern ID."""
        return hashlib.md5(signature.encode()).hexdigest()[:8]
    
    def capture_success_metrics(self, operation_type: str, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Capture success metrics from operations."""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'operation_type': operation_type,
            'success_indicators': [],
            'performance_metrics': {},
            'quality_signals': []
        }
        
        # Pattern application success
        if operation_type == 'pattern_application':
            if operation_data.get('errors_encountered', 0) == 0:
                metrics['success_indicators'].append('error_free_execution')
            if operation_data.get('execution_time', 0) < 5:
                metrics['success_indicators'].append('fast_execution')
                
        # Code generation success
        elif operation_type == 'code_generation':
            if 'syntax_error' not in operation_data.get('output', ''):
                metrics['success_indicators'].append('valid_syntax')
            if operation_data.get('lines_generated', 0) > 0:
                metrics['performance_metrics']['productivity'] = operation_data['lines_generated']
                
        # Optimization success
        elif operation_type == 'optimization':
            if operation_data.get('performance_improvement', 0) > 0:
                metrics['success_indicators'].append('performance_gain')
                metrics['performance_metrics']['improvement_factor'] = operation_data['performance_improvement']
        
        return metrics
    
    def learn_coding_style(self, session_data: Dict[str, Any]):
        """Learn from Christian's coding style and preferences."""
        style_observations = {}
        
        # Analyze preferences from git history
        try:
            # Get recent commit messages for preference signals
            result = subprocess.run(
                ['git', 'log', '--oneline', '-10', '--pretty=format:%s'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                commit_messages = result.stdout.split('\n')
                
                # Detect style preferences
                if any('optimization' in msg.lower() for msg in commit_messages):
                    style_observations['prefers_optimization'] = True
                if any('cleanup' in msg.lower() for msg in commit_messages):
                    style_observations['values_clean_code'] = True
                if any('test' in msg.lower() for msg in commit_messages):
                    style_observations['emphasizes_testing'] = True
                    
        except Exception:
            pass
        
        # Update style profile
        for observation, value in style_observations.items():
            if observation not in self.style_profile:
                self.style_profile[observation] = []
            self.style_profile[observation].append({
                'value': value,
                'timestamp': datetime.now().isoformat()
            })
    
    def update_learning_archive(self, patterns: List[CodePattern], session_metrics: Dict[str, Any]):
        """Update learning_archive.md with new patterns and metrics."""
        try:
            if not self.learning_archive.exists():
                return
                
            # Read current content
            with open(self.learning_archive, 'r') as f:
                content = f.read()
            
            # Update metrics section
            content = self._update_metrics_section(content, patterns, session_metrics)
            
            # Add new patterns
            content = self._add_detected_patterns(content, patterns)
            
            # Write updated content
            with open(self.learning_archive, 'w') as f:
                f.write(content)
                
        except Exception as e:
            # Silent fail to avoid disrupting operations
            pass
    
    def _update_metrics_section(self, content: str, patterns: List[CodePattern], session_metrics: Dict[str, Any]) -> str:
        """Update the metrics section of learning_archive.md."""
        # Update solution count
        pattern_count = len(patterns)
        if pattern_count > 0:
            content = re.sub(
                r'- \*\*Total Solutions\*\*: \d+',
                f'- **Total Solutions**: {session_metrics.get("total_solutions", pattern_count)}',
                content
            )
            
            # Update last updated timestamp
            content = re.sub(
                r'Last Updated: [^\n]+',
                f'Last Updated: {datetime.now().isoformat()}',
                content
            )
        
        return content
    
    def _add_detected_patterns(self, content: str, patterns: List[CodePattern]) -> str:
        """Add newly detected patterns to the archive."""
        if not patterns:
            return content
            
        # Find insertion point (end of file)
        new_entries = f"\n\n### Auto-Detected Patterns - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for pattern in patterns:
            new_entries += f"#### Pattern: {pattern.pattern_type.title()}\n"
            new_entries += f"- **Signature**: `{pattern.pattern_signature}`\n"
            new_entries += f"- **Complexity**: {pattern.complexity_score}/10\n"
            new_entries += f"- **Tags**: {', '.join(pattern.context_tags)}\n"
            new_entries += f"- **Quality Score**: {pattern.quality_metrics.get('readability', 8.0):.1f}/10\n"
            new_entries += f"- **First Detected**: {pattern.first_seen}\n\n"
        
        return content + new_entries

class LearningIntegration:
    """Integration layer with existing session management."""
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.engine = AutoLearningEngine(project_root)
        
    def hook_into_session_manager(self):
        """Hook learning into session state manager operations."""
        # This would be called from session_state_manager.py
        pass
    
    def process_session_end(self, session_data: Dict[str, Any]):
        """Process learning at session end."""
        # Detect patterns from git changes
        patterns = self.engine.detect_code_patterns_from_git()
        
        # Capture success metrics
        session_metrics = self.engine.capture_success_metrics('session_completion', session_data)
        
        # Learn coding style
        self.engine.learn_coding_style(session_data)
        
        # Update learning archive
        self.engine.update_learning_archive(patterns, session_metrics)
        
        # Save cache
        self.engine._save_learning_cache()
    
    def lightweight_pattern_check(self, operation_type: str, operation_data: Dict[str, Any]):
        """Lightweight pattern checking during operations (minimal overhead)."""
        # Only run if operation took longer than 1 second (avoid overhead on quick ops)
        if operation_data.get('execution_time', 0) > 1:
            metrics = self.engine.capture_success_metrics(operation_type, operation_data)
            
            # Store in session cache for batch processing
            if 'session_learning' not in operation_data:
                operation_data['session_learning'] = []
            operation_data['session_learning'].append(metrics)

def integrate_with_session_manager():
    """Integration hook for session_state_manager.py"""
    try:
        learning = LearningIntegration("/Users/scarmatrix/Project/CLAUDE_improvement")
        
        # Example usage in session operations
        session_data = {
            'execution_time': 2.5,
            'patterns_used': ['optimization', 'cleanup'],
            'success_indicators': ['error_free', 'performance_gain']
        }
        
        learning.process_session_end(session_data)
        
    except Exception:
        # Silent fail - never disrupt main operations
        pass

if __name__ == "__main__":
    # Test the learning system
    print("🧠 Testing Auto-Learning Engine...")
    
    learning = LearningIntegration("/Users/scarmatrix/Project/CLAUDE_improvement")
    
    # Simulate session data
    test_session = {
        'execution_time': 3.2,
        'patterns_used': ['session_optimization', 'cleanup'],
        'success_indicators': ['performance_improvement', 'clean_code']
    }
    
    learning.process_session_end(test_session)
    print("✅ Learning integration test complete")