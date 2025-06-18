#!/usr/bin/env python3
"""
Context Engine - Project-Aware Suggestion System
Analyzes project history, session patterns, and provides predictive suggestions.
Connects to SESSION_CONTINUITY.md and existing project state.
"""

import os
import json
import re
import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict, Counter
import hashlib


@dataclass
class ContextPattern:
    """Represents a detected usage pattern in the project."""
    pattern_type: str
    frequency: int
    last_used: datetime.datetime
    confidence: float
    context_data: Dict[str, Any]
    suggested_actions: List[str]


@dataclass
class ProjectState:
    """Current state of the project."""
    session_count: int
    last_session: datetime.datetime
    active_patterns: List[str]
    completion_rates: Dict[str, float]
    common_workflows: List[str]
    performance_metrics: Dict[str, float]


class ProjectHistoryAnalyzer:
    """Analyzes project history from SESSION_CONTINUITY.md and session logs."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.session_continuity_path = self.project_root / "SESSION_CONTINUITY.md"
        self.memory_path = self.project_root / "memory"
        self.logs_path = self.project_root / "logs"
        self.patterns_path = self.project_root / "patterns"
        # Add caching infrastructure
        self._cache = {}
        self._mtimes = {}
    
    def _get_empty_history_data(self) -> Dict[str, Any]:
        """Get empty history data structure."""
        return {
            'total_sessions': 0,
            'cleanup_operations': 0,
            'optimization_cycles': 0,
            'performance_improvements': [],
            'common_tasks': Counter(),
            'success_patterns': [],
            'time_patterns': defaultdict(list)
        }
    
    def analyze_session_history(self) -> Dict[str, Any]:
        """Analyze session continuity and extract patterns, with caching."""
        path = self.session_continuity_path
        cache_key = 'session_history'
        
        # Check if file exists and if it has been modified since last read
        if not path.exists():
            return self._cache.get(cache_key, self._get_empty_history_data())
        
        current_mtime = path.stat().st_mtime
        last_mtime = self._mtimes.get(str(path))
        
        if self._cache.get(cache_key) and last_mtime == current_mtime:
            return self._cache[cache_key]
        
        # Cache miss or file modified - perform analysis
        history_data = self._get_empty_history_data()
        
        if not path.exists():
            return history_data
        
        try:
            with open(self.session_continuity_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract session timestamps
            timestamp_pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?)'
            timestamps = re.findall(timestamp_pattern, content)
            history_data['total_sessions'] = len(timestamps)
            
            # Extract cleanup operations
            cleanup_pattern = r'cleanup|optimization|Performance|reduction'
            cleanup_matches = re.findall(cleanup_pattern, content, re.IGNORECASE)
            history_data['cleanup_operations'] = len(cleanup_matches)
            
            # Extract performance metrics
            perf_pattern = r'(\d+(?:\.\d+)?%|\d+x faster|\d+(?:\.\d+)?s|\d+(?:\.\d+)?MB)'
            performance_metrics = re.findall(perf_pattern, content)
            history_data['performance_improvements'] = performance_metrics
            
            # Extract common task patterns (optimized single-pass regex)
            task_patterns = [
                'file reduction', 'token reduction', 'boot optimization',
                'memory management', 'pattern creation', 'session continuity',
                'backup system', 'performance monitoring'
            ]
            
            # Combine patterns into single regex for efficiency
            combined_pattern = '|'.join(f'({pattern})' for pattern in task_patterns)
            all_matches = re.findall(combined_pattern, content, re.IGNORECASE)
            
            if all_matches:
                # Count occurrences from the single list of matches
                for match_groups in all_matches:
                    for i, match in enumerate(match_groups):
                        if match:  # Non-empty match
                            pattern_name = task_patterns[i]
                            history_data['common_tasks'][pattern_name] += 1
            
            # Extract success indicators
            success_indicators = re.findall(r'✅|SUCCESS|COMPLETE|accomplished', content, re.IGNORECASE)
            history_data['success_patterns'] = success_indicators
            
        except Exception as e:
            print(f"Warning: Error analyzing session history: {e}")
        
        # Update cache
        self._cache[cache_key] = history_data
        self._mtimes[str(path)] = current_mtime
        
        return history_data
    
    def analyze_project_patterns(self) -> Dict[str, Any]:
        """Analyze patterns directory for usage frequency."""
        pattern_data = {
            'total_patterns': 0,
            'pattern_categories': Counter(),
            'recent_patterns': [],
            'pattern_complexity': {},
            'usage_frequency': Counter()
        }
        
        if not self.patterns_path.exists():
            return pattern_data
        
        try:
            for category_dir in self.patterns_path.iterdir():
                if category_dir.is_dir():
                    category_name = category_dir.name
                    pattern_data['pattern_categories'][category_name] = 0
                    
                    for pattern_file in category_dir.glob('*.md'):
                        pattern_data['total_patterns'] += 1
                        pattern_data['pattern_categories'][category_name] += 1
                        
                        # Analyze pattern complexity and usage
                        with open(pattern_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Extract complexity indicators
                        complexity_score = self._calculate_pattern_complexity(content)
                        pattern_data['pattern_complexity'][pattern_file.name] = complexity_score
                        
                        # Extract usage frequency hints
                        usage_matches = re.findall(r'uses?:\s*(\d+)', content, re.IGNORECASE)
                        if usage_matches:
                            pattern_data['usage_frequency'][pattern_file.name] = int(usage_matches[0])
                        
                        # Check if pattern is recent (modified in last 7 days)
                        if (datetime.datetime.now() - datetime.datetime.fromtimestamp(pattern_file.stat().st_mtime)).days <= 7:
                            pattern_data['recent_patterns'].append(pattern_file.name)
        
        except Exception as e:
            print(f"Warning: Error analyzing project patterns: {e}")
        
        return pattern_data
    
    def _calculate_pattern_complexity(self, content: str) -> int:
        """Calculate pattern complexity based on content analysis."""
        complexity_score = 0
        
        # Code blocks indicate higher complexity
        code_blocks = len(re.findall(r'```', content))
        complexity_score += code_blocks // 2
        
        # Multiple sections indicate structured complexity
        sections = len(re.findall(r'^##?\s', content, re.MULTILINE))
        complexity_score += sections
        
        # Decision points indicate logical complexity
        decision_words = ['if', 'while', 'for', 'switch', 'case', 'when']
        for word in decision_words:
            complexity_score += len(re.findall(rf'\b{word}\b', content, re.IGNORECASE))
        
        return min(complexity_score, 10)  # Cap at 10


class SessionPatternTracker:
    """Tracks patterns within and across sessions."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.session_logs_path = self.project_root / "logs" / "session_continuity"
        
    def analyze_session_patterns(self) -> Dict[str, Any]:
        """Analyze patterns across multiple sessions."""
        session_data = {
            'session_frequency': {},
            'typical_session_duration': {},
            'common_workflows': Counter(),
            'handoff_patterns': [],
            'productivity_metrics': {},
            'context_switching': []
        }
        
        if not self.session_logs_path.exists():
            return session_data
        
        try:
            # Analyze session frequency by date
            for session_file in self.session_logs_path.glob('**/*.md'):
                date_match = re.match(r'session_(\d{4}-\d{2}-\d{2})', session_file.name)
                if date_match:
                    date = date_match.group(1)
                    session_data['session_frequency'][date] = session_data['session_frequency'].get(date, 0) + 1
            
            # Analyze workflows from session content
            workflow_patterns = [
                'boot sequence', 'pattern matching', 'file cleanup',
                'performance optimization', 'memory management',
                'backup creation', 'session handoff', 'context restoration'
            ]
            
            for session_file in self.session_logs_path.glob('**/*.md'):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for workflow in workflow_patterns:
                        if re.search(workflow, content, re.IGNORECASE):
                            session_data['common_workflows'][workflow] += 1
                
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"Warning: Error analyzing session patterns: {e}")
        
        return session_data
    
    def detect_usage_trends(self) -> Dict[str, Any]:
        """Detect trends in tool and pattern usage."""
        trends = {
            'increasing_patterns': [],
            'decreasing_patterns': [],
            'stable_patterns': [],
            'emerging_patterns': [],
            'obsolete_patterns': []
        }
        
        try:
            # Simple trend detection based on file modification times
            patterns_dir = self.project_root / "patterns"
            if patterns_dir.exists():
                now = datetime.datetime.now()
                
                for pattern_file in patterns_dir.glob('**/*.md'):
                    mod_time = datetime.datetime.fromtimestamp(pattern_file.stat().st_mtime)
                    days_since_mod = (now - mod_time).days
                    
                    if days_since_mod <= 1:
                        trends['emerging_patterns'].append(pattern_file.name)
                    elif days_since_mod <= 7:
                        trends['increasing_patterns'].append(pattern_file.name)
                    elif days_since_mod <= 30:
                        trends['stable_patterns'].append(pattern_file.name)
                    else:
                        trends['decreasing_patterns'].append(pattern_file.name)
        
        except Exception as e:
            print(f"Warning: Error detecting usage trends: {e}")
        
        return trends


class PredictiveSuggestionSystem:
    """Provides intelligent suggestions based on project context and history."""
    
    def __init__(self, history_analyzer: ProjectHistoryAnalyzer, pattern_tracker: SessionPatternTracker):
        self.history_analyzer = history_analyzer
        self.pattern_tracker = pattern_tracker
        self.suggestion_cache = {}
    
    def generate_context_suggestions(self, current_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate suggestions based on current context and historical patterns."""
        suggestions = []
        
        # Analyze current context
        context_type = self._determine_context_type(current_context)
        history_data = self.history_analyzer.analyze_session_history()
        pattern_data = self.history_analyzer.analyze_project_patterns()
        session_patterns = self.pattern_tracker.analyze_session_patterns()
        
        # Generate suggestions based on context type
        if context_type == "startup":
            suggestions.extend(self._generate_startup_suggestions(history_data, pattern_data))
        elif context_type == "development":
            suggestions.extend(self._generate_development_suggestions(history_data, pattern_data))
        elif context_type == "optimization":
            suggestions.extend(self._generate_optimization_suggestions(history_data, session_patterns))
        elif context_type == "maintenance":
            suggestions.extend(self._generate_maintenance_suggestions(history_data, pattern_data))
        
        # Add pattern-based suggestions
        suggestions.extend(self._generate_pattern_suggestions(pattern_data))
        
        # Score and rank suggestions
        scored_suggestions = self._score_suggestions(suggestions, current_context)
        
        return sorted(scored_suggestions, key=lambda x: x['confidence'], reverse=True)[:10]
    
    def _determine_context_type(self, context: Dict[str, Any]) -> str:
        """Determine the type of current context."""
        indicators = {
            'startup': ['boot', 'init', 'setup', 'start'],
            'development': ['implement', 'create', 'build', 'code'],
            'optimization': ['optimize', 'performance', 'improve', 'speed'],
            'maintenance': ['cleanup', 'organize', 'backup', 'archive']
        }
        
        context_text = ' '.join(str(v).lower() for v in context.values())
        
        for context_type, keywords in indicators.items():
            if any(keyword in context_text for keyword in keywords):
                return context_type
        
        return "general"
    
    def _generate_startup_suggestions(self, history_data: Dict, pattern_data: Dict) -> List[Dict[str, Any]]:
        """Generate suggestions for startup context."""
        suggestions = []
        
        # Based on historical startup patterns
        if history_data.get('cleanup_operations', 0) > 2:
            suggestions.append({
                'type': 'optimization',
                'title': 'Consider running cleanup optimization',
                'description': 'Historical data shows frequent cleanup operations. Consider automated cleanup.',
                'action': 'scripts/cleanup',
                'confidence': 0.8,
                'estimated_time': '5-10 minutes'
            })
        
        # Based on pattern usage
        if pattern_data.get('recent_patterns'):
            suggestions.append({
                'type': 'pattern_usage',
                'title': 'Apply recent patterns',
                'description': f"Recently updated patterns available: {', '.join(pattern_data['recent_patterns'][:3])}",
                'action': 'check_patterns',
                'confidence': 0.7,
                'estimated_time': '2-5 minutes'
            })
        
        return suggestions
    
    def _generate_development_suggestions(self, history_data: Dict, pattern_data: Dict) -> List[Dict[str, Any]]:
        """Generate suggestions for development context."""
        suggestions = []
        
        # Suggest most used patterns
        if pattern_data.get('usage_frequency'):
            top_patterns = pattern_data['usage_frequency'].most_common(3)
            for pattern, count in top_patterns:
                suggestions.append({
                    'type': 'pattern_reuse',
                    'title': f'Consider reusing {pattern}',
                    'description': f'This pattern has been used {count} times successfully',
                    'action': f'apply_pattern:{pattern}',
                    'confidence': 0.6 + (count * 0.1),
                    'estimated_time': '3-8 minutes'
                })
        
        return suggestions
    
    def _generate_optimization_suggestions(self, history_data: Dict, session_patterns: Dict) -> List[Dict[str, Any]]:
        """Generate suggestions for optimization context."""
        suggestions = []
        
        # Based on performance improvements history
        if history_data.get('performance_improvements'):
            suggestions.append({
                'type': 'performance',
                'title': 'Apply proven optimization techniques',
                'description': 'Historical data shows successful performance improvements',
                'action': 'review_optimization_history',
                'confidence': 0.9,
                'estimated_time': '10-20 minutes'
            })
        
        # Based on common workflows
        common_workflows = session_patterns.get('common_workflows', Counter())
        if common_workflows:
            most_common = common_workflows.most_common(1)[0]
            suggestions.append({
                'type': 'workflow',
                'title': f'Optimize {most_common[0]} workflow',
                'description': f'This workflow appears {most_common[1]} times in session history',
                'action': f'optimize_workflow:{most_common[0]}',
                'confidence': 0.7,
                'estimated_time': '15-30 minutes'
            })
        
        return suggestions
    
    def _generate_maintenance_suggestions(self, history_data: Dict, pattern_data: Dict) -> List[Dict[str, Any]]:
        """Generate suggestions for maintenance context."""
        suggestions = []
        
        # Session continuity maintenance
        suggestions.append({
            'type': 'maintenance',
            'title': 'Update session continuity',
            'description': 'Regular maintenance of session continuity files',
            'action': 'scripts/session_update.sh',
            'confidence': 0.6,
            'estimated_time': '2-5 minutes'
        })
        
        # Pattern organization
        if pattern_data.get('total_patterns', 0) > 10:
            suggestions.append({
                'type': 'organization',
                'title': 'Organize pattern library',
                'description': f'{pattern_data["total_patterns"]} patterns available for organization',
                'action': 'organize_patterns',
                'confidence': 0.5,
                'estimated_time': '10-15 minutes'
            })
        
        return suggestions
    
    def _generate_pattern_suggestions(self, pattern_data: Dict) -> List[Dict[str, Any]]:
        """Generate suggestions based on available patterns."""
        suggestions = []
        
        # Suggest based on pattern categories
        categories = pattern_data.get('pattern_categories', Counter())
        for category, count in categories.most_common(3):
            suggestions.append({
                'type': 'pattern_category',
                'title': f'Explore {category} patterns',
                'description': f'{count} patterns available in {category} category',
                'action': f'explore_patterns:{category}',
                'confidence': 0.4 + (count * 0.1),
                'estimated_time': '5-10 minutes'
            })
        
        return suggestions
    
    def _score_suggestions(self, suggestions: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Score suggestions based on relevance and context."""
        for suggestion in suggestions:
            # Base confidence
            base_confidence = suggestion.get('confidence', 0.5)
            
            # Context relevance boost
            context_text = ' '.join(str(v).lower() for v in context.values())
            suggestion_text = (suggestion.get('title', '') + ' ' + suggestion.get('description', '')).lower()
            
            # Simple relevance scoring
            common_words = set(context_text.split()) & set(suggestion_text.split())
            relevance_boost = len(common_words) * 0.05
            
            # Time-based scoring (prefer quicker suggestions)
            time_text = suggestion.get('estimated_time', '10 minutes')
            time_minutes = self._extract_time_minutes(time_text)
            time_penalty = min(time_minutes * 0.01, 0.2)
            
            # Final confidence score
            suggestion['confidence'] = min(base_confidence + relevance_boost - time_penalty, 1.0)
        
        return suggestions
    
    def _extract_time_minutes(self, time_text: str) -> int:
        """Extract estimated minutes from time text."""
        match = re.search(r'(\d+)', time_text)
        return int(match.group(1)) if match else 10


class ContextEngine:
    """Main context engine orchestrating all components."""
    
    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = self._find_project_root()
        
        self.project_root = Path(project_root)
        self.history_analyzer = ProjectHistoryAnalyzer(str(self.project_root))
        self.pattern_tracker = SessionPatternTracker(str(self.project_root))
        self.suggestion_system = PredictiveSuggestionSystem(self.history_analyzer, self.pattern_tracker)
        self.context_cache = {}
        
    def _find_project_root(self) -> str:
        """Find project root using the established pattern."""
        current_dir = Path.cwd()
        max_depth = 20
        depth = 0
        
        while current_dir != current_dir.parent and depth < max_depth:
            # Primary markers
            if (current_dir / "CLAUDE.md").exists():
                return str(current_dir)
            
            # Secondary markers
            if ((current_dir / "memory").exists() and 
                (current_dir / "memory" / "learning_archive.md").exists()):
                return str(current_dir)
            
            # Tertiary markers
            project_files = ["package.json", "requirements.txt", ".git"]
            if any((current_dir / pf).exists() for pf in project_files):
                if ((current_dir / "memory").exists() or 
                    (current_dir / "SESSION_CONTINUITY.md").exists()):
                    return str(current_dir)
            
            current_dir = current_dir.parent
            depth += 1
        
        return str(Path.cwd())
    
    def analyze_current_context(self, user_input: str = "", additional_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze current context and return comprehensive analysis."""
        context = {
            'timestamp': datetime.datetime.now().isoformat(),
            'user_input': user_input,
            'project_root': str(self.project_root),
            'additional_context': additional_context or {}
        }
        
        # Add project state analysis
        context['project_state'] = self._analyze_current_project_state()
        
        # Add historical context
        context['history_analysis'] = self.history_analyzer.analyze_session_history()
        context['pattern_analysis'] = self.history_analyzer.analyze_project_patterns()
        context['session_patterns'] = self.pattern_tracker.analyze_session_patterns()
        
        return context
    
    def get_suggestions(self, user_input: str = "", context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get intelligent suggestions based on current context."""
        if context is None:
            context = self.analyze_current_context(user_input)
        
        suggestions = self.suggestion_system.generate_context_suggestions(context)
        
        # Add metadata
        for suggestion in suggestions:
            suggestion['generated_at'] = datetime.datetime.now().isoformat()
            suggestion['context_hash'] = self._hash_context(context)
        
        return suggestions
    
    def _analyze_current_project_state(self) -> Dict[str, Any]:
        """Analyze current state of the project."""
        state = {
            'session_continuity_exists': (self.project_root / "SESSION_CONTINUITY.md").exists(),
            'patterns_count': 0,
            'memory_files_count': 0,
            'scripts_count': 0,
            'last_activity': None
        }
        
        # Count patterns
        patterns_dir = self.project_root / "patterns"
        if patterns_dir.exists():
            state['patterns_count'] = len(list(patterns_dir.glob('**/*.md')))
        
        # Count memory files
        memory_dir = self.project_root / "memory"
        if memory_dir.exists():
            state['memory_files_count'] = len(list(memory_dir.glob('*.md')))
        
        # Count scripts
        scripts_dir = self.project_root / "scripts"
        if scripts_dir.exists():
            state['scripts_count'] = len(list(scripts_dir.glob('*')))
        
        # Find last activity
        session_file = self.project_root / "SESSION_CONTINUITY.md"
        if session_file.exists():
            mod_time = datetime.datetime.fromtimestamp(session_file.stat().st_mtime)
            state['last_activity'] = mod_time.isoformat()
        
        return state
    
    def _hash_context(self, context: Dict[str, Any]) -> str:
        """Create a hash of the context for caching purposes."""
        context_str = json.dumps(context, sort_keys=True, default=str)
        return hashlib.md5(context_str.encode()).hexdigest()[:8]
    
    def generate_context_report(self) -> Dict[str, Any]:
        """Generate comprehensive context report."""
        context = self.analyze_current_context()
        suggestions = self.get_suggestions(context=context)
        
        report = {
            'generated_at': datetime.datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'context_analysis': context,
            'suggestions': suggestions,
            'summary': {
                'total_patterns': context['pattern_analysis'].get('total_patterns', 0),
                'total_sessions': context['history_analysis'].get('total_sessions', 0),
                'suggestion_count': len(suggestions),
                'high_confidence_suggestions': len([s for s in suggestions if s.get('confidence', 0) > 0.7])
            }
        }
        
        return report


def main():
    """Main function for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Context Engine - Project-Aware Suggestions')
    parser.add_argument('--project-root', help='Project root directory')
    parser.add_argument('--input', help='User input for context analysis')
    parser.add_argument('--report', action='store_true', help='Generate full context report')
    parser.add_argument('--suggestions-only', action='store_true', help='Show only suggestions')
    
    args = parser.parse_args()
    
    # Initialize context engine
    engine = ContextEngine(args.project_root)
    
    if args.report:
        # Generate full report
        report = engine.generate_context_report()
        print(json.dumps(report, indent=2))
    elif args.suggestions_only:
        # Show only suggestions
        suggestions = engine.get_suggestions(args.input or "")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion['title']} (confidence: {suggestion['confidence']:.2f})")
            print(f"   {suggestion['description']}")
            print(f"   Action: {suggestion['action']}")
            print(f"   Time: {suggestion['estimated_time']}")
            print()
    else:
        # Default: show context analysis and top suggestions
        context = engine.analyze_current_context(args.input or "")
        suggestions = engine.get_suggestions(context=context)
        
        print("=== Context Analysis ===")
        print(f"Project: {context['project_state']}")
        print(f"Patterns: {context['pattern_analysis'].get('total_patterns', 0)}")
        print(f"Sessions: {context['history_analysis'].get('total_sessions', 0)}")
        print()
        
        print("=== Top Suggestions ===")
        for i, suggestion in enumerate(suggestions[:5], 1):
            print(f"{i}. {suggestion['title']} (confidence: {suggestion['confidence']:.2f})")
            print(f"   {suggestion['description']}")
            print()


if __name__ == "__main__":
    main()