#!/usr/bin/env python3
"""
Cache Hit Rate and Session State Monitoring
Track optimization success through cache performance and session metrics
User: Christian
"""

import json
import time
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import hashlib
import sqlite3
import threading
from contextlib import contextmanager

class CacheSessionMonitor:
    """Monitor cache performance and session state for optimization tracking"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.monitoring_dir = self.project_root / "monitoring"
        self.monitoring_dir.mkdir(exist_ok=True)
        
        # Initialize cache tracking database
        self.db_path = self.monitoring_dir / "cache_session_tracking.db"
        self._init_database()
        
        # Cache configuration
        self.cache_types = {
            'session_state': 'Session continuity and state caching',
            'file_discovery': 'Project file discovery results',
            'pattern_index': 'Pattern library indexing',
            'config_cache': 'Configuration file parsing',
            'learning_files': 'Learning file content caching',
            'dependency_check': 'Dependency validation results',
        }
        
        # Session tracking
        self.session_states = {
            'initializing': 'System starting up',
            'active': 'Session is active and working',
            'idle': 'Session idle but responsive',
            'cached': 'Running from cached state',
            'refreshing': 'Cache refresh in progress',
            'error': 'Session in error state',
        }
        
        # Performance thresholds
        self.cache_performance_thresholds = {
            'excellent': 95.0,  # >95% hit rate
            'good': 85.0,       # >85% hit rate
            'acceptable': 70.0, # >70% hit rate
            'poor': 50.0,       # >50% hit rate
            'critical': 0.0,    # Any hit rate
        }
        
        # Session state tracking
        self._current_session = None
        self._lock = threading.Lock()
        
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "CLAUDE.md").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _init_database(self):
        """Initialize SQLite database for cache tracking"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    cache_type TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    cache_key TEXT NOT NULL,
                    hit BOOLEAN NOT NULL,
                    response_time_ms REAL,
                    content_size INTEGER,
                    metadata TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS session_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    state TEXT NOT NULL,
                    duration_ms REAL,
                    metadata TEXT
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_cache_session_type 
                ON cache_events(session_id, cache_type)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_session_events_session 
                ON session_events(session_id, timestamp)
            ''')
    
    def start_session_monitoring(self, session_name: str, context: str = "") -> str:
        """Start monitoring a new session"""
        session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_name}"
        
        with self._lock:
            self._current_session = {
                'session_id': session_id,
                'session_name': session_name,
                'context': context,
                'start_time': datetime.now(timezone.utc),
                'state': 'initializing',
                'cache_stats': {cache_type: {'hits': 0, 'misses': 0, 'total_time_ms': 0} 
                               for cache_type in self.cache_types},
            }
        
        # Record session start
        self._record_session_event(session_id, 'session_start', 'initializing')
        
        print(f"📊 Cache/Session monitoring started: {session_id}")
        return session_id
    
    def record_cache_access(self, session_id: str, cache_type: str, operation: str,
                           cache_key: str, is_hit: bool, response_time_ms: float = 0,
                           content_size: int = 0, metadata: Dict = None) -> Dict:
        """Record a cache access event"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO cache_events 
                (timestamp, session_id, cache_type, operation, cache_key, hit, 
                 response_time_ms, content_size, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, session_id, cache_type, operation, cache_key, is_hit,
                  response_time_ms, content_size, json.dumps(metadata or {})))
        
        # Update session stats
        with self._lock:
            if self._current_session and self._current_session['session_id'] == session_id:
                cache_stats = self._current_session['cache_stats'][cache_type]
                if is_hit:
                    cache_stats['hits'] += 1
                else:
                    cache_stats['misses'] += 1
                cache_stats['total_time_ms'] += response_time_ms
        
        # Log cache event
        hit_status = "HIT" if is_hit else "MISS"
        time_info = f"{response_time_ms:.1f}ms" if response_time_ms > 0 else ""
        size_info = f"({content_size} bytes)" if content_size > 0 else ""
        
        cache_emoji = "💾" if is_hit else "🔍"
        print(f"{cache_emoji} {cache_type}.{operation}: {hit_status} {time_info} {size_info}")
        
        return {
            'timestamp': timestamp,
            'session_id': session_id,
            'cache_type': cache_type,
            'operation': operation,
            'cache_key': cache_key,
            'is_hit': is_hit,
            'response_time_ms': response_time_ms,
            'content_size': content_size,
        }
    
    def update_session_state(self, session_id: str, new_state: str, metadata: Dict = None):
        """Update the current session state"""
        
        with self._lock:
            if self._current_session and self._current_session['session_id'] == session_id:
                old_state = self._current_session['state']
                if old_state != new_state:
                    state_duration = (datetime.now(timezone.utc) - 
                                    self._current_session.get('state_start_time', 
                                                            self._current_session['start_time'])).total_seconds() * 1000
                    
                    self._current_session['state'] = new_state
                    self._current_session['state_start_time'] = datetime.now(timezone.utc)
                    
                    # Record state change
                    self._record_session_event(session_id, 'state_change', new_state, 
                                             state_duration, metadata)
                    
                    print(f"🔄 Session state: {old_state} → {new_state}")
    
    def _record_session_event(self, session_id: str, event_type: str, state: str,
                             duration_ms: float = 0, metadata: Dict = None):
        """Record a session event in the database"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO session_events 
                (timestamp, session_id, event_type, state, duration_ms, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp, session_id, event_type, state, duration_ms, 
                  json.dumps(metadata or {})))
    
    @contextmanager
    def track_cache_operation(self, session_id: str, cache_type: str, operation: str,
                             cache_key: str, check_cache_func: callable = None):
        """Context manager for tracking cache operations with timing"""
        
        start_time = time.perf_counter()
        cache_hit = False
        content_size = 0
        
        try:
            # Check cache if function provided
            if check_cache_func:
                cached_result = check_cache_func(cache_key)
                if cached_result is not None:
                    cache_hit = True
                    if isinstance(cached_result, (str, bytes)):
                        content_size = len(cached_result)
                    elif isinstance(cached_result, dict):
                        content_size = len(json.dumps(cached_result))
                    
                    # Record cache hit
                    end_time = time.perf_counter()
                    response_time = (end_time - start_time) * 1000
                    
                    self.record_cache_access(session_id, cache_type, operation, cache_key,
                                           True, response_time, content_size)
                    
                    yield cached_result
                    return
            
            # Cache miss - yield for operation execution
            yield None
            
        finally:
            # Record cache miss if we got here
            if not cache_hit:
                end_time = time.perf_counter()
                response_time = (end_time - start_time) * 1000
                
                self.record_cache_access(session_id, cache_type, operation, cache_key,
                                       False, response_time, content_size)
    
    def get_cache_statistics(self, session_id: str, time_window_minutes: int = None) -> Dict:
        """Get cache statistics for a session"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Base query
            query = '''
                SELECT cache_type, operation, hit, response_time_ms, content_size
                FROM cache_events 
                WHERE session_id = ?
            '''
            params = [session_id]
            
            # Add time window filter if specified
            if time_window_minutes:
                window_start = (datetime.now(timezone.utc) - 
                              timedelta(minutes=time_window_minutes)).isoformat()
                query += ' AND timestamp >= ?'
                params.append(window_start)
            
            query += ' ORDER BY timestamp'
            
            cursor = conn.execute(query, params)
            events = cursor.fetchall()
        
        if not events:
            return {'error': 'No cache events found for session'}
        
        # Calculate statistics
        total_hits = sum(1 for event in events if event[2])  # hit column
        total_requests = len(events)
        total_misses = total_requests - total_hits
        
        overall_hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0
        
        # Statistics by cache type
        type_stats = {}
        for cache_type in self.cache_types:
            type_events = [e for e in events if e[0] == cache_type]
            if type_events:
                type_hits = sum(1 for e in type_events if e[2])
                type_total = len(type_events)
                type_hit_rate = (type_hits / type_total * 100) if type_total > 0 else 0
                avg_response_time = sum(e[3] for e in type_events if e[3]) / len([e for e in type_events if e[3]]) if any(e[3] for e in type_events) else 0
                
                type_stats[cache_type] = {
                    'requests': type_total,
                    'hits': type_hits,
                    'misses': type_total - type_hits,
                    'hit_rate': type_hit_rate,
                    'avg_response_time_ms': avg_response_time,
                    'performance_rating': self._rate_cache_performance(type_hit_rate),
                }
        
        return {
            'session_id': session_id,
            'time_window_minutes': time_window_minutes,
            'overall_statistics': {
                'total_requests': total_requests,
                'total_hits': total_hits,
                'total_misses': total_misses,
                'hit_rate': overall_hit_rate,
                'performance_rating': self._rate_cache_performance(overall_hit_rate),
            },
            'cache_type_statistics': type_stats,
        }
    
    def _rate_cache_performance(self, hit_rate: float) -> str:
        """Rate cache performance based on hit rate"""
        if hit_rate >= self.cache_performance_thresholds['excellent']:
            return 'excellent'
        elif hit_rate >= self.cache_performance_thresholds['good']:
            return 'good'
        elif hit_rate >= self.cache_performance_thresholds['acceptable']:
            return 'acceptable'
        elif hit_rate >= self.cache_performance_thresholds['poor']:
            return 'poor'
        else:
            return 'critical'
    
    def get_session_timeline(self, session_id: str) -> Dict:
        """Get session state timeline and events"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT timestamp, event_type, state, duration_ms, metadata
                FROM session_events 
                WHERE session_id = ?
                ORDER BY timestamp
            ''', [session_id])
            
            events = cursor.fetchall()
        
        if not events:
            return {'error': 'No session events found'}
        
        timeline = []
        state_durations = {}
        current_state = None
        
        for event in events:
            timestamp, event_type, state, duration_ms, metadata_json = event
            metadata = json.loads(metadata_json) if metadata_json else {}
            
            timeline_entry = {
                'timestamp': timestamp,
                'event_type': event_type,
                'state': state,
                'duration_ms': duration_ms,
                'metadata': metadata,
            }
            timeline.append(timeline_entry)
            
            # Track state durations
            if event_type == 'state_change' and duration_ms > 0:
                prev_state = current_state
                if prev_state:
                    if prev_state not in state_durations:
                        state_durations[prev_state] = 0
                    state_durations[prev_state] += duration_ms
            
            current_state = state
        
        return {
            'session_id': session_id,
            'timeline': timeline,
            'state_durations': state_durations,
            'total_events': len(events),
            'session_summary': self._analyze_session_timeline(timeline),
        }
    
    def _analyze_session_timeline(self, timeline: List[Dict]) -> Dict:
        """Analyze session timeline for insights"""
        
        if not timeline:
            return {'error': 'No timeline data'}
        
        start_time = datetime.fromisoformat(timeline[0]['timestamp'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(timeline[-1]['timestamp'].replace('Z', '+00:00'))
        total_duration = (end_time - start_time).total_seconds()
        
        state_counts = {}
        error_events = []
        
        for event in timeline:
            state = event['state']
            state_counts[state] = state_counts.get(state, 0) + 1
            
            if state == 'error' or event['event_type'] == 'error':
                error_events.append(event)
        
        # Determine session health
        if error_events:
            health = 'error'
        elif 'cached' in state_counts and state_counts.get('cached', 0) > state_counts.get('active', 0):
            health = 'optimized'
        elif 'active' in state_counts:
            health = 'healthy'
        else:
            health = 'unknown'
        
        return {
            'total_duration_seconds': total_duration,
            'state_distribution': state_counts,
            'error_count': len(error_events),
            'session_health': health,
            'optimization_indicator': 'cached' in state_counts and state_counts.get('cached', 0) > 0,
        }
    
    def end_session_monitoring(self, session_id: str) -> Dict:
        """End session monitoring and generate final statistics"""
        
        # Record session end
        self._record_session_event(session_id, 'session_end', 'completed')
        
        # Get final statistics
        cache_stats = self.get_cache_statistics(session_id)
        session_timeline = self.get_session_timeline(session_id)
        
        # Generate summary report
        summary = {
            'session_id': session_id,
            'end_time': datetime.now(timezone.utc).isoformat(),
            'cache_performance': cache_stats,
            'session_timeline': session_timeline,
        }
        
        # Save summary to file
        summary_file = self.monitoring_dir / f"session_summary_{session_id}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        with self._lock:
            if self._current_session and self._current_session['session_id'] == session_id:
                self._current_session = None
        
        if 'error' not in cache_stats:
            overall_hit_rate = cache_stats['overall_statistics']['hit_rate']
            session_health = session_timeline['session_summary']['session_health']
            
            print(f"📊 Session monitoring completed: {session_id}")
            print(f"   Cache hit rate: {overall_hit_rate:.1f}%")
            print(f"   Session health: {session_health}")
        
        return summary
    
    def compare_cache_sessions(self, baseline_session: str, optimized_session: str) -> Dict:
        """Compare cache performance between two sessions"""
        
        baseline_stats = self.get_cache_statistics(baseline_session)
        optimized_stats = self.get_cache_statistics(optimized_session)
        
        if 'error' in baseline_stats or 'error' in optimized_stats:
            raise ValueError("Cannot compare sessions with missing data")
        
        baseline_hit_rate = baseline_stats['overall_statistics']['hit_rate']
        optimized_hit_rate = optimized_stats['overall_statistics']['hit_rate']
        
        hit_rate_improvement = optimized_hit_rate - baseline_hit_rate
        
        comparison = {
            'comparison_timestamp': datetime.now(timezone.utc).isoformat(),
            'baseline_session': baseline_session,
            'optimized_session': optimized_session,
            'cache_comparison': {
                'baseline_hit_rate': baseline_hit_rate,
                'optimized_hit_rate': optimized_hit_rate,
                'hit_rate_improvement': hit_rate_improvement,
                'baseline_rating': baseline_stats['overall_statistics']['performance_rating'],
                'optimized_rating': optimized_stats['overall_statistics']['performance_rating'],
            },
            'cache_type_comparison': {}
        }
        
        # Compare by cache type
        baseline_types = baseline_stats['cache_type_statistics']
        optimized_types = optimized_stats['cache_type_statistics']
        
        all_types = set(baseline_types.keys()) | set(optimized_types.keys())
        
        for cache_type in all_types:
            baseline_type = baseline_types.get(cache_type, {'hit_rate': 0})
            optimized_type = optimized_types.get(cache_type, {'hit_rate': 0})
            
            type_improvement = optimized_type['hit_rate'] - baseline_type['hit_rate']
            
            comparison['cache_type_comparison'][cache_type] = {
                'baseline_hit_rate': baseline_type['hit_rate'],
                'optimized_hit_rate': optimized_type['hit_rate'],
                'hit_rate_improvement': type_improvement,
            }
        
        # Save comparison
        comparison_file = self.monitoring_dir / f"cache_comparison_{baseline_session}_vs_{optimized_session}.json"
        with open(comparison_file, 'w') as f:
            json.dump(comparison, f, indent=2)
        
        return comparison
    
    def generate_cache_report(self, comparison_data: Dict) -> str:
        """Generate markdown report of cache optimization results"""
        
        report_timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        report_file = self.monitoring_dir / f"cache_report_{report_timestamp}.md"
        
        cache_comp = comparison_data['cache_comparison']
        type_comp = comparison_data['cache_type_comparison']
        
        report_content = f"""# Cache Performance Optimization Report
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
User: Christian

## Executive Summary

### 💾 Cache Performance Results
- **Baseline hit rate**: {cache_comp['baseline_hit_rate']:.1f}%
- **Optimized hit rate**: {cache_comp['optimized_hit_rate']:.1f}%
- **Hit rate improvement**: {cache_comp['hit_rate_improvement']:+.1f}%
- **Performance rating**: {cache_comp['baseline_rating'].title()} → {cache_comp['optimized_rating'].title()}

### 📊 Cache Performance Assessment
"""
        
        if cache_comp['optimized_hit_rate'] >= 95:
            assessment = "🚀 **EXCELLENT** - Outstanding cache performance"
        elif cache_comp['optimized_hit_rate'] >= 85:
            assessment = "✅ **VERY GOOD** - Strong cache efficiency"
        elif cache_comp['optimized_hit_rate'] >= 70:
            assessment = "📈 **ACCEPTABLE** - Adequate cache performance"
        elif cache_comp['optimized_hit_rate'] >= 50:
            assessment = "⚠️ **POOR** - Cache needs improvement"
        else:
            assessment = "❌ **CRITICAL** - Cache performance is problematic"
        
        report_content += f"{assessment}\n\n"
        
        report_content += """## Detailed Cache Analysis

### Performance by Cache Type
"""
        
        for cache_type, stats in type_comp.items():
            report_content += f"""
#### {cache_type.replace('_', ' ').title()}
- **Before**: {stats['baseline_hit_rate']:.1f}% hit rate
- **After**: {stats['optimized_hit_rate']:.1f}% hit rate
- **Improvement**: {stats['hit_rate_improvement']:+.1f}%
"""
        
        report_content += f"""
## Cache Optimization Impact

### Performance Metrics
- **Overall Hit Rate**: {cache_comp['optimized_hit_rate']:.1f}% ({'Excellent' if cache_comp['optimized_hit_rate'] >= 95 else 'Good' if cache_comp['optimized_hit_rate'] >= 85 else 'Needs Improvement'})
- **Hit Rate Improvement**: {cache_comp['hit_rate_improvement']:+.1f}% ({'Significant' if abs(cache_comp['hit_rate_improvement']) >= 10 else 'Moderate' if abs(cache_comp['hit_rate_improvement']) >= 5 else 'Minimal'})
- **Performance Rating**: {cache_comp['optimized_rating'].title()}

### Cache Effectiveness Targets
- ✅ Excellent (>95%): {'✅ ACHIEVED' if cache_comp['optimized_hit_rate'] >= 95 else '❌ NOT ACHIEVED'}
- ✅ Good (>85%): {'✅ ACHIEVED' if cache_comp['optimized_hit_rate'] >= 85 else '❌ NOT ACHIEVED'}
- ✅ Acceptable (>70%): {'✅ ACHIEVED' if cache_comp['optimized_hit_rate'] >= 70 else '❌ NOT ACHIEVED'}

## Recommendations

### Immediate Actions
"""
        
        if cache_comp['optimized_hit_rate'] < 70:
            report_content += "- **CRITICAL**: Implement better caching strategies immediately\n"
        elif cache_comp['optimized_hit_rate'] < 85:
            report_content += "- **HIGH PRIORITY**: Optimize cache algorithms and policies\n"
        elif cache_comp['optimized_hit_rate'] < 95:
            report_content += "- **MEDIUM PRIORITY**: Fine-tune cache for excellent performance\n"
        else:
            report_content += "- **MAINTAIN**: Current cache performance is excellent\n"
        
        if cache_comp['hit_rate_improvement'] < 5:
            report_content += "- Investigate additional cache optimization opportunities\n"
        
        report_content += """
### Future Optimizations
- Monitor cache hit rate trends over time
- Implement predictive caching strategies
- Optimize cache eviction policies

### Monitoring Strategy
- Continuous cache performance monitoring
- Alert on cache hit rate degradation
- Regular cache policy reviews

---
*Report generated by Cache Session Monitor for CLAUDE Optimization Project*
"""
        
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        print(f"📋 Cache report generated: {report_file}")
        return str(report_file)

def main():
    """Command line interface for cache and session monitoring"""
    if len(sys.argv) < 2:
        print("Usage: python cache_session_monitor.py <command> [args...]")
        print("Commands:")
        print("  start <session_name> [context]                      - Start session monitoring")
        print("  cache <session_id> <type> <operation> <key> <hit>   - Record cache access")
        print("  state <session_id> <new_state>                      - Update session state")
        print("  stats <session_id>                                  - Get cache statistics")
        print("  timeline <session_id>                               - Get session timeline")
        print("  end <session_id>                                    - End session monitoring")
        print("  compare <baseline> <optimized>                      - Compare cache sessions")
        print("  report <baseline> <optimized>                       - Generate cache report")
        return
    
    monitor = CacheSessionMonitor()
    command = sys.argv[1]
    
    if command == "start":
        session_name = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        session_id = monitor.start_session_monitoring(session_name, context)
        print(f"Session ID: {session_id}")
    
    elif command == "cache":
        session_id = sys.argv[2]
        cache_type = sys.argv[3]
        operation = sys.argv[4]
        cache_key = sys.argv[5]
        is_hit = sys.argv[6].lower() in ('true', '1', 'yes', 'hit')
        response_time = float(sys.argv[7]) if len(sys.argv) > 7 else 0
        
        monitor.record_cache_access(session_id, cache_type, operation, cache_key, is_hit, response_time)
    
    elif command == "state":
        session_id = sys.argv[2]
        new_state = sys.argv[3]
        monitor.update_session_state(session_id, new_state)
    
    elif command == "stats":
        session_id = sys.argv[2]
        time_window = int(sys.argv[3]) if len(sys.argv) > 3 else None
        stats = monitor.get_cache_statistics(session_id, time_window)
        print(json.dumps(stats, indent=2))
    
    elif command == "timeline":
        session_id = sys.argv[2]
        timeline = monitor.get_session_timeline(session_id)
        print(json.dumps(timeline, indent=2))
    
    elif command == "end":
        session_id = sys.argv[2]
        summary = monitor.end_session_monitoring(session_id)
        print(f"Session summary saved")
    
    elif command == "compare":
        baseline = sys.argv[2]
        optimized = sys.argv[3]
        comparison = monitor.compare_cache_sessions(baseline, optimized)
        print(f"Comparison saved: cache_comparison_{baseline}_vs_{optimized}.json")
    
    elif command == "report":
        baseline = sys.argv[2]
        optimized = sys.argv[3]
        comparison = monitor.compare_cache_sessions(baseline, optimized)
        report_file = monitor.generate_cache_report(comparison)
        print(f"Report generated: {report_file}")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()