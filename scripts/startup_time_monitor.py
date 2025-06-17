#!/usr/bin/env python3
"""
Startup Time Monitoring with Millisecond Precision
Track optimization success through precise timing measurements
User: Christian
"""

import json
import time
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable
import subprocess
import threading
import psutil
from contextlib import contextmanager

class StartupTimeMonitor:
    """Monitor startup times with millisecond precision"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.monitoring_dir = self.project_root / "monitoring"
        self.monitoring_dir.mkdir(exist_ok=True)
        
        # Timing configuration
        self.precision_ns = True  # Use nanosecond precision when available
        self.measurement_categories = {
            'boot_sequence': 'Complete system boot and initialization',
            'file_discovery': 'File system scanning and discovery',
            'pattern_loading': 'Pattern library initialization',
            'config_loading': 'Configuration file parsing',
            'session_init': 'Session state initialization',
            'cache_check': 'Cache validation and loading',
            'memory_load': 'Learning file loading',
            'dependency_check': 'Dependency validation',
        }
        
        # Performance thresholds (milliseconds)
        self.performance_thresholds = {
            'excellent': 100,   # <100ms
            'good': 500,        # <500ms
            'acceptable': 1000, # <1s
            'slow': 5000,       # <5s
            'critical': 10000,  # <10s
        }
        
        # Active measurements
        self._active_measurements = {}
        
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "CLAUDE.md").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _get_high_precision_time(self) -> float:
        """Get highest precision time available"""
        if self.precision_ns and hasattr(time, 'time_ns'):
            return time.time_ns() / 1_000_000_000  # Convert to seconds
        else:
            return time.perf_counter()
    
    def _time_to_ms(self, seconds: float) -> float:
        """Convert seconds to milliseconds with precision"""
        return seconds * 1000
    
    def start_timing_session(self, session_name: str, context: str = "") -> str:
        """Start a new timing session"""
        session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_name}"
        
        session_data = {
            'session_id': session_id,
            'session_name': session_name,
            'context': context,
            'start_time': datetime.now(timezone.utc).isoformat(),
            'start_timestamp': self._get_high_precision_time(),
            'measurements': [],
            'system_info': self._capture_system_info(),
            'totals': {
                'total_time_ms': 0,
                'operation_count': 0,
                'avg_time_ms': 0,
                'min_time_ms': float('inf'),
                'max_time_ms': 0,
            }
        }
        
        session_file = self.monitoring_dir / f"timing_{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"⏱️ Timing session started: {session_id}")
        return session_id
    
    def _capture_system_info(self) -> Dict:
        """Capture system information for timing context"""
        try:
            return {
                'cpu_count': psutil.cpu_count(),
                'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                'memory_total': psutil.virtual_memory().total,
                'memory_available': psutil.virtual_memory().available,
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None,
                'platform': sys.platform,
                'python_version': sys.version,
            }
        except Exception:
            return {'error': 'Could not capture system info'}
    
    @contextmanager
    def time_operation(self, session_id: str, operation_name: str, category: str, 
                      metadata: Dict = None):
        """Context manager for timing operations with automatic measurement"""
        
        measurement_id = f"{session_id}_{len(self._active_measurements)}"
        start_time = self._get_high_precision_time()
        
        # Track active measurement
        self._active_measurements[measurement_id] = {
            'operation': operation_name,
            'category': category,
            'start_time': start_time,
            'metadata': metadata or {},
        }
        
        try:
            yield measurement_id
        finally:
            end_time = self._get_high_precision_time()
            duration = end_time - start_time
            
            # Record measurement
            self.record_measurement(
                session_id, operation_name, category, 
                duration, metadata or {}
            )
            
            # Clean up active measurement
            if measurement_id in self._active_measurements:
                del self._active_measurements[measurement_id]
    
    def record_measurement(self, session_id: str, operation: str, category: str,
                          duration_seconds: float, metadata: Dict = None) -> Dict:
        """Record a timing measurement"""
        
        duration_ms = self._time_to_ms(duration_seconds)
        
        measurement = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'operation': operation,
            'category': category,
            'duration_seconds': duration_seconds,
            'duration_ms': duration_ms,
            'metadata': metadata or {},
            'performance_rating': self._rate_performance(duration_ms),
        }
        
        # Update session file
        session_file = self.monitoring_dir / f"timing_{session_id}.json"
        if session_file.exists():
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            session_data['measurements'].append(measurement)
            
            # Update totals
            totals = session_data['totals']
            totals['total_time_ms'] += duration_ms
            totals['operation_count'] += 1
            totals['avg_time_ms'] = totals['total_time_ms'] / totals['operation_count']
            totals['min_time_ms'] = min(totals['min_time_ms'], duration_ms)
            totals['max_time_ms'] = max(totals['max_time_ms'], duration_ms)
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
        
        rating_emoji = {
            'excellent': '🚀',
            'good': '✅',
            'acceptable': '📈',
            'slow': '⚠️',
            'critical': '❌'
        }.get(measurement['performance_rating'], '📊')
        
        print(f"{rating_emoji} {operation}: {duration_ms:.1f}ms ({measurement['performance_rating']})")
        return measurement
    
    def _rate_performance(self, duration_ms: float) -> str:
        """Rate performance based on duration thresholds"""
        if duration_ms < self.performance_thresholds['excellent']:
            return 'excellent'
        elif duration_ms < self.performance_thresholds['good']:
            return 'good'
        elif duration_ms < self.performance_thresholds['acceptable']:
            return 'acceptable'
        elif duration_ms < self.performance_thresholds['slow']:
            return 'slow'
        else:
            return 'critical'
    
    def end_timing_session(self, session_id: str) -> Dict:
        """End timing session and generate summary"""
        session_file = self.monitoring_dir / f"timing_{session_id}.json"
        
        if not session_file.exists():
            raise ValueError(f"Timing session {session_id} not found")
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        session_data['end_time'] = datetime.now(timezone.utc).isoformat()
        session_data['end_timestamp'] = self._get_high_precision_time()
        
        # Calculate session statistics
        measurements = session_data['measurements']
        totals = session_data['totals']
        
        if measurements:
            # Category breakdown
            category_stats = {}
            for measurement in measurements:
                category = measurement['category']
                if category not in category_stats:
                    category_stats[category] = {
                        'operations': 0,
                        'total_ms': 0,
                        'avg_ms': 0,
                        'min_ms': float('inf'),
                        'max_ms': 0,
                        'ratings': {'excellent': 0, 'good': 0, 'acceptable': 0, 'slow': 0, 'critical': 0}
                    }
                
                stats = category_stats[category]
                duration = measurement['duration_ms']
                rating = measurement['performance_rating']
                
                stats['operations'] += 1
                stats['total_ms'] += duration
                stats['avg_ms'] = stats['total_ms'] / stats['operations']
                stats['min_ms'] = min(stats['min_ms'], duration)
                stats['max_ms'] = max(stats['max_ms'], duration)
                stats['ratings'][rating] += 1
            
            session_data['summary'] = {
                'session_duration_seconds': session_data['end_timestamp'] - session_data['start_timestamp'],
                'total_operations': totals['operation_count'],
                'total_time_ms': totals['total_time_ms'],
                'average_time_ms': totals['avg_time_ms'],
                'fastest_operation_ms': totals['min_time_ms'],
                'slowest_operation_ms': totals['max_time_ms'],
                'category_breakdown': category_stats,
                'overall_performance': self._calculate_overall_performance(measurements),
            }
        else:
            session_data['summary'] = {'error': 'No measurements recorded'}
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        if 'error' not in session_data['summary']:
            summary = session_data['summary']
            print(f"⏱️ Timing session completed: {session_id}")
            print(f"   Total operations: {summary['total_operations']}")
            print(f"   Average time: {summary['average_time_ms']:.1f}ms")
            print(f"   Overall performance: {summary['overall_performance']}")
        
        return session_data
    
    def _calculate_overall_performance(self, measurements: List[Dict]) -> str:
        """Calculate overall performance rating for session"""
        if not measurements:
            return 'unknown'
        
        rating_scores = {'excellent': 5, 'good': 4, 'acceptable': 3, 'slow': 2, 'critical': 1}
        total_score = sum(rating_scores[m['performance_rating']] for m in measurements)
        avg_score = total_score / len(measurements)
        
        if avg_score >= 4.5:
            return 'excellent'
        elif avg_score >= 3.5:
            return 'good'
        elif avg_score >= 2.5:
            return 'acceptable'
        elif avg_score >= 1.5:
            return 'slow'
        else:
            return 'critical'
    
    def compare_timing_sessions(self, baseline_session: str, optimized_session: str) -> Dict:
        """Compare timing between two sessions"""
        
        baseline_file = self.monitoring_dir / f"timing_{baseline_session}.json"
        optimized_file = self.monitoring_dir / f"timing_{optimized_session}.json"
        
        if not baseline_file.exists() or not optimized_file.exists():
            raise ValueError("One or both timing session files not found")
        
        with open(baseline_file, 'r') as f:
            baseline_data = json.load(f)
        
        with open(optimized_file, 'r') as f:
            optimized_data = json.load(f)
        
        baseline_summary = baseline_data.get('summary', {})
        optimized_summary = optimized_data.get('summary', {})
        
        if 'error' in baseline_summary or 'error' in optimized_summary:
            raise ValueError("Cannot compare sessions with missing data")
        
        baseline_avg = baseline_summary['average_time_ms']
        optimized_avg = optimized_summary['average_time_ms']
        
        time_improvement = baseline_avg - optimized_avg
        improvement_percentage = (time_improvement / baseline_avg * 100) if baseline_avg > 0 else 0
        
        comparison = {
            'comparison_timestamp': datetime.now(timezone.utc).isoformat(),
            'baseline_session': baseline_session,
            'optimized_session': optimized_session,
            'timing_comparison': {
                'baseline_avg_ms': baseline_avg,
                'optimized_avg_ms': optimized_avg,
                'time_saved_ms': time_improvement,
                'improvement_percentage': improvement_percentage,
                'speedup_factor': baseline_avg / optimized_avg if optimized_avg > 0 else float('inf'),
            },
            'performance_comparison': {
                'baseline_rating': baseline_summary['overall_performance'],
                'optimized_rating': optimized_summary['overall_performance'],
                'performance_improved': self._performance_rank(optimized_summary['overall_performance']) > 
                                      self._performance_rank(baseline_summary['overall_performance']),
            },
            'category_comparison': {}
        }
        
        # Compare categories
        baseline_categories = baseline_summary.get('category_breakdown', {})
        optimized_categories = optimized_summary.get('category_breakdown', {})
        
        all_categories = set(baseline_categories.keys()) | set(optimized_categories.keys())
        
        for category in all_categories:
            baseline_cat = baseline_categories.get(category, {'avg_ms': 0})
            optimized_cat = optimized_categories.get(category, {'avg_ms': 0})
            
            cat_improvement = baseline_cat['avg_ms'] - optimized_cat['avg_ms']
            cat_improvement_pct = (cat_improvement / baseline_cat['avg_ms'] * 100) if baseline_cat['avg_ms'] > 0 else 0
            
            comparison['category_comparison'][category] = {
                'baseline_avg_ms': baseline_cat['avg_ms'],
                'optimized_avg_ms': optimized_cat['avg_ms'],
                'time_saved_ms': cat_improvement,
                'improvement_percentage': cat_improvement_pct,
                'speedup_factor': baseline_cat['avg_ms'] / optimized_cat['avg_ms'] if optimized_cat['avg_ms'] > 0 else float('inf'),
            }
        
        # Save comparison
        comparison_file = self.monitoring_dir / f"timing_comparison_{baseline_session}_vs_{optimized_session}.json"
        with open(comparison_file, 'w') as f:
            json.dump(comparison, f, indent=2)
        
        return comparison
    
    def _performance_rank(self, rating: str) -> int:
        """Convert performance rating to numeric rank"""
        ranks = {'critical': 1, 'slow': 2, 'acceptable': 3, 'good': 4, 'excellent': 5}
        return ranks.get(rating, 0)
    
    def generate_timing_report(self, comparison_data: Dict) -> str:
        """Generate markdown report of timing optimization results"""
        
        report_timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        report_file = self.monitoring_dir / f"timing_report_{report_timestamp}.md"
        
        timing_comp = comparison_data['timing_comparison']
        perf_comp = comparison_data['performance_comparison']
        cat_comp = comparison_data['category_comparison']
        
        report_content = f"""# Startup Time Optimization Report
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
User: Christian

## Executive Summary

### ⚡ Performance Results
- **Baseline time**: {timing_comp['baseline_avg_ms']:.1f}ms
- **Optimized time**: {timing_comp['optimized_avg_ms']:.1f}ms
- **Time saved**: {timing_comp['time_saved_ms']:.1f}ms
- **Performance improvement**: {timing_comp['improvement_percentage']:.1f}%
- **Speedup factor**: {timing_comp['speedup_factor']:.2f}x

### 📊 Performance Rating
- **Baseline rating**: {perf_comp['baseline_rating'].title()}
- **Optimized rating**: {perf_comp['optimized_rating'].title()}
- **Performance improved**: {'✅ Yes' if perf_comp['performance_improved'] else '❌ No'}

## Detailed Timing Analysis

### Performance by Category
"""
        
        for category, stats in cat_comp.items():
            if stats['baseline_avg_ms'] > 0 or stats['optimized_avg_ms'] > 0:
                report_content += f"""
#### {category.replace('_', ' ').title()}
- **Before**: {stats['baseline_avg_ms']:.1f}ms
- **After**: {stats['optimized_avg_ms']:.1f}ms
- **Improvement**: {stats['time_saved_ms']:.1f}ms ({stats['improvement_percentage']:.1f}%)
- **Speedup**: {stats['speedup_factor']:.2f}x
"""
        
        # Performance assessment
        if timing_comp['improvement_percentage'] >= 80:
            assessment = "🚀 **OUTSTANDING** - Exceptional performance improvement"
        elif timing_comp['improvement_percentage'] >= 60:
            assessment = "⚡ **EXCELLENT** - Significant performance gains"
        elif timing_comp['improvement_percentage'] >= 40:
            assessment = "✅ **VERY GOOD** - Notable performance improvement"
        elif timing_comp['improvement_percentage'] >= 20:
            assessment = "📈 **GOOD** - Meaningful performance gains"
        elif timing_comp['improvement_percentage'] >= 0:
            assessment = "👍 **MODERATE** - Some performance improvement"
        else:
            assessment = "⚠️ **REGRESSION** - Performance has decreased"
        
        # Performance category assessment
        optimized_rating = perf_comp['optimized_rating']
        if optimized_rating == 'excellent':
            rating_assessment = "🚀 **EXCELLENT** - Sub-100ms response times"
        elif optimized_rating == 'good':
            rating_assessment = "✅ **GOOD** - Sub-500ms response times"
        elif optimized_rating == 'acceptable':
            rating_assessment = "📈 **ACCEPTABLE** - Sub-1s response times"
        elif optimized_rating == 'slow':
            rating_assessment = "⚠️ **SLOW** - Response times need improvement"
        else:
            rating_assessment = "❌ **CRITICAL** - Response times are problematic"
        
        report_content += f"""
## Performance Assessment

### Optimization Impact
{assessment}

### Current Performance Level
{rating_assessment}

### Performance Metrics Summary
- **Response Time**: {timing_comp['optimized_avg_ms']:.1f}ms ({'Sub-second' if timing_comp['optimized_avg_ms'] < 1000 else 'Over 1 second'})
- **Improvement Factor**: {timing_comp['speedup_factor']:.2f}x faster
- **Performance Category**: {optimized_rating.title()}

### Optimization Targets
- ✅ Sub-100ms (Excellent): {'✅ ACHIEVED' if timing_comp['optimized_avg_ms'] < 100 else '❌ NOT ACHIEVED'}
- ✅ Sub-500ms (Good): {'✅ ACHIEVED' if timing_comp['optimized_avg_ms'] < 500 else '❌ NOT ACHIEVED'}
- ✅ Sub-1000ms (Acceptable): {'✅ ACHIEVED' if timing_comp['optimized_avg_ms'] < 1000 else '❌ NOT ACHIEVED'}

## Recommendations

### Immediate Actions
"""
        
        if timing_comp['optimized_avg_ms'] > 1000:
            report_content += "- **CRITICAL**: Response times exceed 1 second - immediate optimization required\n"
        elif timing_comp['optimized_avg_ms'] > 500:
            report_content += "- **HIGH PRIORITY**: Target sub-500ms response times for better user experience\n"
        elif timing_comp['optimized_avg_ms'] > 100:
            report_content += "- **MEDIUM PRIORITY**: Optimize further to achieve sub-100ms excellence threshold\n"
        else:
            report_content += "- **MAINTAIN**: Current performance is excellent, focus on stability\n"
        
        if timing_comp['improvement_percentage'] < 50:
            report_content += "- Investigate additional optimization opportunities\n"
        
        report_content += """
### Future Optimizations
- Monitor response time trends over time
- Identify new bottlenecks as system scales
- Benchmark against industry standards

### Monitoring Strategy
- Continuous monitoring of startup times
- Alerting for performance regressions
- Regular optimization reviews

---
*Report generated by Startup Time Monitor for CLAUDE Optimization Project*
"""
        
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        print(f"📋 Timing report generated: {report_file}")
        return str(report_file)

    def benchmark_common_operations(self, session_id: str) -> Dict:
        """Benchmark common CLAUDE operations for baseline measurements"""
        
        print("🔬 Running benchmark of common operations...")
        
        operations = [
            ('session_check', 'session_init', lambda: self._simulate_session_check()),
            ('todo_read', 'memory_load', lambda: self._simulate_todo_read()),
            ('config_check', 'config_loading', lambda: self._simulate_config_check()),
            ('pattern_search', 'pattern_loading', lambda: self._simulate_pattern_search()),
            ('file_discovery', 'file_discovery', lambda: self._simulate_file_discovery()),
        ]
        
        results = {}
        
        for operation_name, category, operation_func in operations:
            with self.time_operation(session_id, operation_name, category):
                try:
                    operation_func()
                    results[operation_name] = 'success'
                except Exception as e:
                    results[operation_name] = f'error: {str(e)}'
        
        return results
    
    def _simulate_session_check(self):
        """Simulate session state check"""
        session_file = self.project_root / "SESSION_CONTINUITY.md"
        if session_file.exists():
            with open(session_file, 'r') as f:
                content = f.read()
        time.sleep(0.01)  # Simulate processing time
    
    def _simulate_todo_read(self):
        """Simulate TODO.md reading"""
        todo_file = self.project_root / "TODO.md"
        if todo_file.exists():
            with open(todo_file, 'r') as f:
                content = f.read()
        time.sleep(0.005)  # Simulate processing time
    
    def _simulate_config_check(self):
        """Simulate CLAUDE.md configuration check"""
        claude_file = self.project_root / "CLAUDE.md"
        if claude_file.exists():
            with open(claude_file, 'r') as f:
                lines = f.readlines()[:50]  # Read first 50 lines
        time.sleep(0.02)  # Simulate processing time
    
    def _simulate_pattern_search(self):
        """Simulate pattern library search"""
        patterns_dir = self.project_root / "patterns"
        if patterns_dir.exists():
            pattern_files = list(patterns_dir.glob("**/*.md"))[:10]
        time.sleep(0.015)  # Simulate search time
    
    def _simulate_file_discovery(self):
        """Simulate project file discovery"""
        for root, dirs, files in os.walk(self.project_root):
            if len(files) > 100:  # Limit to prevent long scans
                break
        time.sleep(0.03)  # Simulate discovery time

def main():
    """Command line interface for startup time monitoring"""
    if len(sys.argv) < 2:
        print("Usage: python startup_time_monitor.py <command> [args...]")
        print("Commands:")
        print("  start <session_name> [context]           - Start timing session")
        print("  record <session_id> <operation> <category> <duration_ms> - Record measurement")
        print("  end <session_id>                         - End timing session")
        print("  compare <baseline> <optimized>           - Compare two sessions")
        print("  report <baseline> <optimized>            - Generate timing report")
        print("  benchmark <session_id>                   - Benchmark common operations")
        return
    
    monitor = StartupTimeMonitor()
    command = sys.argv[1]
    
    if command == "start":
        session_name = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        session_id = monitor.start_timing_session(session_name, context)
        print(f"Session ID: {session_id}")
    
    elif command == "record":
        session_id = sys.argv[2]
        operation = sys.argv[3]
        category = sys.argv[4]
        duration_ms = float(sys.argv[5])
        duration_seconds = duration_ms / 1000
        monitor.record_measurement(session_id, operation, category, duration_seconds)
    
    elif command == "end":
        session_id = sys.argv[2]
        monitor.end_timing_session(session_id)
    
    elif command == "compare":
        baseline = sys.argv[2]
        optimized = sys.argv[3]
        comparison = monitor.compare_timing_sessions(baseline, optimized)
        print(f"Comparison saved: timing_comparison_{baseline}_vs_{optimized}.json")
    
    elif command == "report":
        baseline = sys.argv[2]
        optimized = sys.argv[3]
        comparison = monitor.compare_timing_sessions(baseline, optimized)
        report_file = monitor.generate_timing_report(comparison)
        print(f"Report generated: {report_file}")
    
    elif command == "benchmark":
        session_id = sys.argv[2]
        results = monitor.benchmark_common_operations(session_id)
        print("Benchmark results:", results)
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()