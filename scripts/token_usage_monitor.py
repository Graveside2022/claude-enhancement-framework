#!/usr/bin/env python3
"""
Token Usage Measurement Tools
Track optimization success through before/after comparison
User: Christian
"""

import json
import time
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import hashlib

class TokenUsageMonitor:
    """Monitor and measure token usage for optimization tracking"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.monitoring_dir = self.project_root / "monitoring"
        self.monitoring_dir.mkdir(exist_ok=True)
        
        # Token measurement configuration
        self.token_estimates = {
            'char': 0.25,  # ~4 chars per token
            'word': 0.75,  # ~1.3 words per token
            'line': 10,    # ~10 tokens per average line
        }
        
        # Operation tracking
        self.operation_categories = {
            'startup': 'System initialization and boot sequence',
            'discovery': 'File discovery and project scanning',
            'pattern_search': 'Pattern library operations',
            'memory_load': 'Learning file and memory operations',
            'config_check': 'Configuration verification',
            'session_init': 'Session state initialization',
        }
        
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "CLAUDE.md").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def start_monitoring_session(self, session_name: str, context: str = "") -> str:
        """Start a new monitoring session"""
        session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_name}"
        
        session_data = {
            'session_id': session_id,
            'session_name': session_name,
            'context': context,
            'start_time': datetime.now(timezone.utc).isoformat(),
            'measurements': [],
            'totals': {
                'token_count': 0,
                'operation_count': 0,
                'cache_hits': 0,
                'cache_misses': 0,
            }
        }
        
        session_file = self.monitoring_dir / f"session_{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"📊 Token monitoring session started: {session_id}")
        return session_id
    
    def measure_operation(self, session_id: str, operation: str, category: str, 
                         content: str = "", file_path: str = "", 
                         is_cache_hit: bool = False) -> Dict:
        """Measure token usage for a specific operation"""
        
        # Calculate token estimates
        char_count = len(content)
        word_count = len(content.split())
        line_count = content.count('\n') + 1 if content else 0
        
        estimated_tokens = {
            'by_chars': int(char_count * self.token_estimates['char']),
            'by_words': int(word_count * self.token_estimates['word']),
            'by_lines': int(line_count * self.token_estimates['line']),
        }
        
        # Use most conservative estimate
        token_estimate = max(estimated_tokens.values())
        
        measurement = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'operation': operation,
            'category': category,
            'file_path': file_path,
            'content_stats': {
                'char_count': char_count,
                'word_count': word_count,
                'line_count': line_count,
            },
            'token_estimates': estimated_tokens,
            'token_estimate': token_estimate,
            'is_cache_hit': is_cache_hit,
            'content_hash': hashlib.md5(content.encode()).hexdigest() if content else "",
        }
        
        # Update session file
        session_file = self.monitoring_dir / f"session_{session_id}.json"
        if session_file.exists():
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            session_data['measurements'].append(measurement)
            session_data['totals']['token_count'] += token_estimate
            session_data['totals']['operation_count'] += 1
            
            if is_cache_hit:
                session_data['totals']['cache_hits'] += 1
            else:
                session_data['totals']['cache_misses'] += 1
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
        
        print(f"📈 Operation measured: {operation} - {token_estimate} tokens ({'CACHE HIT' if is_cache_hit else 'FRESH'})")
        return measurement
    
    def end_monitoring_session(self, session_id: str) -> Dict:
        """End monitoring session and generate summary"""
        session_file = self.monitoring_dir / f"session_{session_id}.json"
        
        if not session_file.exists():
            raise ValueError(f"Session {session_id} not found")
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        session_data['end_time'] = datetime.now(timezone.utc).isoformat()
        
        # Calculate session statistics
        measurements = session_data['measurements']
        totals = session_data['totals']
        
        category_stats = {}
        for measurement in measurements:
            category = measurement['category']
            if category not in category_stats:
                category_stats[category] = {
                    'operations': 0,
                    'tokens': 0,
                    'cache_hits': 0,
                    'cache_misses': 0,
                }
            
            category_stats[category]['operations'] += 1
            category_stats[category]['tokens'] += measurement['token_estimate']
            
            if measurement['is_cache_hit']:
                category_stats[category]['cache_hits'] += 1
            else:
                category_stats[category]['cache_misses'] += 1
        
        session_data['summary'] = {
            'total_operations': totals['operation_count'],
            'total_tokens': totals['token_count'],
            'cache_hit_rate': totals['cache_hits'] / max(totals['operation_count'], 1) * 100,
            'category_breakdown': category_stats,
            'session_duration': self._calculate_duration(
                session_data['start_time'], 
                session_data['end_time']
            ),
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"📊 Session completed: {session_id}")
        print(f"   Total tokens: {totals['token_count']}")
        print(f"   Cache hit rate: {session_data['summary']['cache_hit_rate']:.1f}%")
        
        return session_data
    
    def compare_sessions(self, baseline_session: str, optimized_session: str) -> Dict:
        """Compare two sessions to show optimization impact"""
        
        baseline_file = self.monitoring_dir / f"session_{baseline_session}.json"
        optimized_file = self.monitoring_dir / f"session_{optimized_session}.json"
        
        if not baseline_file.exists() or not optimized_file.exists():
            raise ValueError("One or both session files not found")
        
        with open(baseline_file, 'r') as f:
            baseline_data = json.load(f)
        
        with open(optimized_file, 'r') as f:
            optimized_data = json.load(f)
        
        baseline_tokens = baseline_data['summary']['total_tokens']
        optimized_tokens = optimized_data['summary']['total_tokens']
        
        token_reduction = baseline_tokens - optimized_tokens
        reduction_percentage = (token_reduction / baseline_tokens * 100) if baseline_tokens > 0 else 0
        
        comparison = {
            'comparison_timestamp': datetime.now(timezone.utc).isoformat(),
            'baseline_session': baseline_session,
            'optimized_session': optimized_session,
            'token_comparison': {
                'baseline_tokens': baseline_tokens,
                'optimized_tokens': optimized_tokens,
                'tokens_saved': token_reduction,
                'reduction_percentage': reduction_percentage,
            },
            'cache_comparison': {
                'baseline_hit_rate': baseline_data['summary']['cache_hit_rate'],
                'optimized_hit_rate': optimized_data['summary']['cache_hit_rate'],
                'hit_rate_improvement': optimized_data['summary']['cache_hit_rate'] - baseline_data['summary']['cache_hit_rate'],
            },
            'category_comparison': {}
        }
        
        # Compare categories
        baseline_categories = baseline_data['summary']['category_breakdown']
        optimized_categories = optimized_data['summary']['category_breakdown']
        
        all_categories = set(baseline_categories.keys()) | set(optimized_categories.keys())
        
        for category in all_categories:
            baseline_cat = baseline_categories.get(category, {'tokens': 0, 'operations': 0})
            optimized_cat = optimized_categories.get(category, {'tokens': 0, 'operations': 0})
            
            cat_reduction = baseline_cat['tokens'] - optimized_cat['tokens']
            cat_reduction_pct = (cat_reduction / baseline_cat['tokens'] * 100) if baseline_cat['tokens'] > 0 else 0
            
            comparison['category_comparison'][category] = {
                'baseline_tokens': baseline_cat['tokens'],
                'optimized_tokens': optimized_cat['tokens'],
                'tokens_saved': cat_reduction,
                'reduction_percentage': cat_reduction_pct,
            }
        
        # Save comparison
        comparison_file = self.monitoring_dir / f"comparison_{baseline_session}_vs_{optimized_session}.json"
        with open(comparison_file, 'w') as f:
            json.dump(comparison, f, indent=2)
        
        return comparison
    
    def generate_optimization_report(self, comparison_data: Dict) -> str:
        """Generate a markdown report of optimization results"""
        
        report_timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        report_file = self.monitoring_dir / f"optimization_report_{report_timestamp}.md"
        
        token_comp = comparison_data['token_comparison']
        cache_comp = comparison_data['cache_comparison']
        cat_comp = comparison_data['category_comparison']
        
        report_content = f"""# Token Usage Optimization Report
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
User: Christian

## Executive Summary

### 🎯 Optimization Results
- **Baseline tokens**: {token_comp['baseline_tokens']:,}
- **Optimized tokens**: {token_comp['optimized_tokens']:,}
- **Tokens saved**: {token_comp['tokens_saved']:,}
- **Reduction**: {token_comp['reduction_percentage']:.1f}%

### 📊 Cache Performance
- **Baseline cache hit rate**: {cache_comp['baseline_hit_rate']:.1f}%
- **Optimized cache hit rate**: {cache_comp['optimized_hit_rate']:.1f}%
- **Cache improvement**: {cache_comp['hit_rate_improvement']:+.1f}%

## Detailed Analysis

### Token Usage by Category
"""
        
        for category, stats in cat_comp.items():
            if stats['baseline_tokens'] > 0 or stats['optimized_tokens'] > 0:
                report_content += f"""
#### {category.replace('_', ' ').title()}
- **Before**: {stats['baseline_tokens']:,} tokens
- **After**: {stats['optimized_tokens']:,} tokens
- **Saved**: {stats['tokens_saved']:,} tokens ({stats['reduction_percentage']:.1f}% reduction)
"""
        
        # Assessment
        if token_comp['reduction_percentage'] >= 90:
            assessment = "🚀 **EXCELLENT** - Outstanding optimization results"
        elif token_comp['reduction_percentage'] >= 75:
            assessment = "✅ **VERY GOOD** - Significant token reduction achieved"
        elif token_comp['reduction_percentage'] >= 50:
            assessment = "👍 **GOOD** - Meaningful optimization improvements"
        elif token_comp['reduction_percentage'] >= 25:
            assessment = "📈 **MODERATE** - Some optimization benefits realized"
        else:
            assessment = "⚠️ **LIMITED** - Minor optimization impact"
        
        report_content += f"""
## Optimization Assessment

{assessment}

### Performance Metrics Achieved
- **Token Efficiency**: {token_comp['reduction_percentage']:.1f}% reduction
- **Cache Effectiveness**: {cache_comp['optimized_hit_rate']:.1f}% hit rate
- **System Responsiveness**: {'High' if cache_comp['optimized_hit_rate'] > 80 else 'Moderate' if cache_comp['optimized_hit_rate'] > 50 else 'Low'}

### Success Criteria
- ✅ Token usage reduction: **{token_comp['reduction_percentage']:.1f}%** ({'EXCEEDED TARGET' if token_comp['reduction_percentage'] >= 90 else 'MET TARGET' if token_comp['reduction_percentage'] >= 75 else 'BELOW TARGET'})
- ✅ Cache hit rate: **{cache_comp['optimized_hit_rate']:.1f}%** ({'EXCELLENT' if cache_comp['optimized_hit_rate'] >= 90 else 'GOOD' if cache_comp['optimized_hit_rate'] >= 70 else 'NEEDS IMPROVEMENT'})

## Recommendations

### Immediate Actions
"""
        
        if token_comp['reduction_percentage'] < 75:
            report_content += "- Investigate additional optimization opportunities\n"
        if cache_comp['optimized_hit_rate'] < 80:
            report_content += "- Improve cache hit rate through better caching strategies\n"
        
        report_content += """
### Future Optimizations
- Monitor token usage trends over time
- Identify new optimization opportunities
- Benchmark against future improvements

---
*Report generated by Token Usage Monitor for CLAUDE Optimization Project*
"""
        
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        print(f"📋 Optimization report generated: {report_file}")
        return str(report_file)
    
    def _calculate_duration(self, start_time: str, end_time: str) -> float:
        """Calculate duration between timestamps in seconds"""
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        return (end - start).total_seconds()
    
    def track_optimization_scenario(self, scenario_name: str) -> str:
        """Track a complete optimization scenario (before/after)"""
        
        print(f"🎯 Starting optimization scenario tracking: {scenario_name}")
        
        # Start baseline session
        baseline_session = self.start_monitoring_session(f"{scenario_name}_baseline", "Pre-optimization baseline")
        
        print("📊 Baseline session started. Please run your operations and then call track_optimization_impact()")
        return baseline_session
    
    def track_optimization_impact(self, baseline_session: str, optimized_name: str) -> Dict:
        """Complete optimization tracking with comparison"""
        
        # End baseline session
        baseline_data = self.end_monitoring_session(baseline_session)
        
        # Start optimized session
        optimized_session = self.start_monitoring_session(f"{optimized_name}_optimized", "Post-optimization measurement")
        
        print("📈 Optimized session started. Run your optimized operations and then call finalize_optimization_tracking()")
        return {
            'baseline_session': baseline_session,
            'optimized_session': optimized_session,
        }
    
    def finalize_optimization_tracking(self, baseline_session: str, optimized_session: str) -> str:
        """Finalize optimization tracking with complete analysis"""
        
        # End optimized session
        optimized_data = self.end_monitoring_session(optimized_session)
        
        # Generate comparison
        comparison = self.compare_sessions(baseline_session, optimized_session)
        
        # Generate report
        report_file = self.generate_optimization_report(comparison)
        
        print(f"🎉 Optimization tracking completed!")
        print(f"   Report: {report_file}")
        
        return report_file

def main():
    """Command line interface for token usage monitoring"""
    if len(sys.argv) < 2:
        print("Usage: python token_usage_monitor.py <command> [args...]")
        print("Commands:")
        print("  start <session_name> [context]  - Start monitoring session")
        print("  measure <session_id> <operation> <category> [file_path] - Measure operation")
        print("  end <session_id>                 - End monitoring session")
        print("  compare <baseline> <optimized>   - Compare two sessions")
        print("  report <baseline> <optimized>    - Generate optimization report")
        return
    
    monitor = TokenUsageMonitor()
    command = sys.argv[1]
    
    if command == "start":
        session_name = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        session_id = monitor.start_monitoring_session(session_name, context)
        print(f"Session ID: {session_id}")
    
    elif command == "measure":
        session_id = sys.argv[2]
        operation = sys.argv[3]
        category = sys.argv[4]
        file_path = sys.argv[5] if len(sys.argv) > 5 else ""
        
        # Read content from stdin or file
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
        else:
            content = sys.stdin.read()
        
        monitor.measure_operation(session_id, operation, category, content, file_path)
    
    elif command == "end":
        session_id = sys.argv[2]
        monitor.end_monitoring_session(session_id)
    
    elif command == "compare":
        baseline = sys.argv[2]
        optimized = sys.argv[3]
        comparison = monitor.compare_sessions(baseline, optimized)
        print(f"Comparison saved: comparison_{baseline}_vs_{optimized}.json")
    
    elif command == "report":
        baseline = sys.argv[2]
        optimized = sys.argv[3]
        comparison = monitor.compare_sessions(baseline, optimized)
        report_file = monitor.generate_optimization_report(comparison)
        print(f"Report generated: {report_file}")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()