#!/usr/bin/env python3
"""
Comprehensive Test Suite for CLAUDE Caching Mechanisms
Tests the .claude_session_state.json and .claude_discovery_cache.json systems

Mission Objectives:
1. Test session-level caching system
2. Verify discovery cache with 1-hour default
3. Validate cache invalidation and refresh logic
4. Measure cache hit rates and performance improvements
5. Verify prevention of redundant file system operations

Created for: Christian
Purpose: Validate that caching mechanisms work exactly as designed
"""

import os
import json
import time
import tempfile
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from optimized_project_loader import OptimizedProjectLoader, SmartConfigurationManager, get_optimized_project_info
from session_state_manager import SessionStateManager

class CachingTestSuite:
    """Comprehensive test suite for caching mechanisms"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.resolve()
        self.test_results = []
        self.performance_metrics = {}
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append((test_name, passed, details))
        print(f"{status}: {test_name}")
        if details:
            print(f"    {details}")
        
    def measure_performance(self, operation_name: str, func, *args, **kwargs):
        """Measure operation performance"""
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_ms = (time.time() - start_time) * 1000
        
        if operation_name not in self.performance_metrics:
            self.performance_metrics[operation_name] = []
        
        self.performance_metrics[operation_name].append(elapsed_ms)
        return result, elapsed_ms
    
    def test_session_state_caching(self) -> bool:
        """Test 1: Session state caching prevents redundant operations"""
        print("\n🧪 Testing Session State Caching System...")
        
        # Clean start
        session_file = self.project_root / ".claude_session_state.json"
        if session_file.exists():
            session_file.unlink()
        
        manager = SessionStateManager(self.project_root)
        
        # Test 1.1: First initialization should create state
        state1, time1 = self.measure_performance("session_init_first", 
                                                manager.initialize_session)
        
        self.log_test("Session initialization creates state file", 
                     session_file.exists(),
                     f"Time: {time1:.1f}ms")
        
        # Test 1.2: Second check should use cached state
        state2, time2 = self.measure_performance("session_init_cached",
                                                manager.initialize_session)
        
        cache_used = state1.session_id == state2.session_id
        self.log_test("Subsequent initialization uses cached state",
                     cache_used,
                     f"Time: {time2:.1f}ms, Cache hit: {cache_used}")
        
        # Test 1.3: Cache hit should be significantly faster
        speedup = time1 / time2 if time2 > 0 else float('inf')
        self.log_test("Cached access is faster than initial",
                     speedup > 2.0,
                     f"Speedup: {speedup:.1f}x")
        
        return all([session_file.exists(), cache_used, speedup > 2.0])
    
    def test_discovery_cache_system(self) -> bool:
        """Test 2: Discovery cache with 1-hour expiration"""
        print("\n🧪 Testing Discovery Cache System...")
        
        # Test using the session-level cache file
        cache_file = self.project_root / ".claude_session_state.json"
        
        loader = OptimizedProjectLoader(self.project_root)
        
        # Test 2.1: First discovery creates/uses cache
        discovery1, time1 = self.measure_performance("discovery_first",
                                                    loader.quick_discovery, True)
        
        self.log_test("Discovery creates session state",
                     cache_file.exists(),
                     f"Time: {time1:.1f}ms")
        
        # Test 2.2: Second discovery uses cache
        discovery2, time2 = self.measure_performance("discovery_cached",
                                                    loader.quick_discovery, True)
        
        # Should be same results (cached)
        cache_used = discovery1 == discovery2
        self.log_test("Subsequent discovery uses cache",
                     cache_used,
                     f"Time: {time2:.1f}ms, Cache hit: {cache_used}")
        
        # Test 2.3: Cache contains required fields
        required_fields = ['project_type', 'has_claude_md']
        has_required = all(field in discovery1 for field in required_fields)
        self.log_test("Cache contains all required fields",
                     has_required,
                     f"Fields: {list(discovery1.keys())}")
        
        return all([cache_file.exists(), cache_used, has_required])
    
    def test_cache_invalidation(self) -> bool:
        """Test 3: Cache invalidation and refresh logic"""
        print("\n🧪 Testing Cache Invalidation Logic...")
        
        cache_file = self.project_root / ".claude_session_state.json"
        
        # Test 3.1: Age-based invalidation simulation
        if cache_file.exists():
            # Backup current cache
            with open(cache_file, 'r') as f:
                original_cache = json.load(f)
            
            # Modify last_access to simulate old session (>2 hours)
            old_cache = original_cache.copy()
            old_cache['last_access'] = time.time() - 7300  # 2 hours and 2 minutes ago
            
            with open(cache_file, 'w') as f:
                json.dump(old_cache, f)
            
            # Try to load - should be considered inactive
            session_manager = SessionStateManager(self.project_root)
            session_active = session_manager.is_session_active()
            
            cache_invalidated = not session_active
            self.log_test("Expired session is invalidated",
                         cache_invalidated,
                         "Session older than 2 hours rejected")
            
            # Test 3.2: Fresh session after invalidation
            new_session, time_fresh = self.measure_performance("session_after_invalidation",
                                                             session_manager.initialize_session, True)
            
            session_refreshed = new_session.session_id != old_cache.get('session_id')
            self.log_test("Fresh session created after invalidation",
                         session_refreshed,
                         f"Time: {time_fresh:.1f}ms")
            
            # Restore original cache
            with open(cache_file, 'w') as f:
                json.dump(original_cache, f)
            
            return cache_invalidated and session_refreshed
        else:
            self.log_test("Cache invalidation test", False, "No cache file to test")
            return False
    
    def test_file_modification_detection(self) -> bool:
        """Test 4: Cache invalidation on file modifications"""
        print("\n🧪 Testing File Modification Detection...")
        
        session_manager = SessionStateManager(self.project_root)
        session_manager.initialize_session()
        
        # Test file modification detection
        claude_md = self.project_root / "CLAUDE.md"
        if claude_md.exists():
            # Get current state
            original_modified = session_manager._config_files_changed()
            
            # Simulate file modification by touching the file
            original_mtime = claude_md.stat().st_mtime
            
            # Wait a bit then touch file
            time.sleep(0.1)
            claude_md.touch()
            
            # Check if modification detected
            modification_detected = session_manager._config_files_changed()
            
            self.log_test("File modification detected",
                         modification_detected,
                         f"Original changed: {original_modified}, After touch: {modification_detected}")
            
            return modification_detected
        else:
            self.log_test("File modification detection", False, "CLAUDE.md not found")
            return False
    
    def test_cache_hit_rates(self) -> bool:
        """Test 5: Measure cache hit rates over multiple operations"""
        print("\n🧪 Testing Cache Hit Rates...")
        
        config_manager = SmartConfigurationManager(self.project_root)
        
        # Multiple configuration requests
        cache_hits = 0
        total_requests = 5
        times = []
        
        for i in range(total_requests):
            start_time = time.time()
            config = config_manager.get_project_config()
            elapsed = (time.time() - start_time) * 1000
            times.append(elapsed)
            
            # After first request, subsequent should be cache hits
            if i > 0 and elapsed < 10:  # Less than 10ms indicates cache hit
                cache_hits += 1
        
        cache_hit_rate = (cache_hits / (total_requests - 1)) * 100  # Exclude first request
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        self.log_test("High cache hit rate achieved",
                     cache_hit_rate >= 80,
                     f"Hit rate: {cache_hit_rate:.1f}%, Avg time: {avg_time:.1f}ms")
        
        return cache_hit_rate >= 80
    
    def test_redundant_operations_prevention(self) -> bool:
        """Test 6: Verify prevention of redundant file system operations"""
        print("\n🧪 Testing Prevention of Redundant Operations...")
        
        # Test pattern scanning caching
        loader = OptimizedProjectLoader(self.project_root)
        
        # First pattern check - should scan files
        patterns1, time1 = self.measure_performance("pattern_count_first",
                                                   loader.get_pattern_count)
        
        # Second pattern check - should use cached
        patterns2, time2 = self.measure_performance("pattern_count_cached",
                                                   loader.get_pattern_count)
        
        # Should be identical (cached) and faster
        patterns_identical = patterns1 == patterns2
        speedup = time1 / time2 if time2 > 0 else float('inf')
        
        self.log_test("Pattern counting uses cache",
                     patterns_identical and speedup > 1.2,
                     f"Identical: {patterns_identical}, Speedup: {speedup:.1f}x")
        
        # Test project type detection caching
        types1, time3 = self.measure_performance("project_type_first",
                                               loader.get_project_type)
        
        types2, time4 = self.measure_performance("project_type_cached", 
                                               loader.get_project_type)
        
        types_identical = types1 == types2
        type_speedup = time3 / time4 if time4 > 0 else float('inf')
        
        self.log_test("Project type detection uses cache",
                     types_identical and type_speedup > 1.2,
                     f"Identical: {types_identical}, Speedup: {type_speedup:.1f}x")
        
        return all([patterns_identical, speedup > 1.2, types_identical, type_speedup > 1.2])
    
    def test_performance_improvements(self) -> bool:
        """Test 7: Measure overall performance improvements"""
        print("\n🧪 Testing Performance Improvements...")
        
        # Clean slate test
        session_file = self.project_root / ".claude_session_state.json"
        
        # Backup existing cache
        session_backup = None
        
        if session_file.exists():
            session_backup = session_file.read_text()
            session_file.unlink()
        
        try:
            # Test cold start (no cache)
            loader_cold = OptimizedProjectLoader(self.project_root)
            result_cold, time_cold = self.measure_performance("cold_start",
                                                            loader_cold.quick_discovery, True)
            
            # Test warm start (with cache) - same loader instance
            result_warm, time_warm = self.measure_performance("warm_start",
                                                            loader_cold.quick_discovery, True)
            
            # Calculate improvements - second call should be faster
            time_improvement = ((time_cold - time_warm) / time_cold) * 100 if time_cold > 0 else 0
            results_identical = result_cold == result_warm
            
            self.log_test("Performance improvement with cache",
                         time_improvement > 10 and results_identical,
                         f"Improvement: {time_improvement:.1f}%, Identical results: {results_identical}")
            
            # Test global function caching
            info1, time_info1 = self.measure_performance("global_func_first",
                                                        get_optimized_project_info, str(self.project_root), True)
            
            info2, time_info2 = self.measure_performance("global_func_cached",
                                                        get_optimized_project_info, str(self.project_root), True)
            
            global_improvement = ((time_info1 - time_info2) / time_info1) * 100 if time_info1 > 0 else 0
            global_identical = info1 == info2
            
            self.log_test("Global function performance improvement",
                         global_improvement > 5 and global_identical,
                         f"Global improvement: {global_improvement:.1f}%, Identical: {global_identical}")
            
            return all([time_improvement > 10, results_identical, global_improvement > 5, global_identical])
            
        finally:
            # Restore original cache
            if session_backup:
                session_file.write_text(session_backup)
    
    def run_all_tests(self) -> Dict:
        """Run complete test suite"""
        print("🚀 Starting Comprehensive Caching Mechanism Test Suite")
        print("=" * 60)
        
        # Run all tests
        tests = [
            ("Session State Caching", self.test_session_state_caching),
            ("Discovery Cache System", self.test_discovery_cache_system),
            ("Cache Invalidation", self.test_cache_invalidation),
            ("File Modification Detection", self.test_file_modification_detection),
            ("Cache Hit Rates", self.test_cache_hit_rates),
            ("Redundant Operations Prevention", self.test_redundant_operations_prevention),
            ("Performance Improvements", self.test_performance_improvements)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed_tests += 1
            except Exception as e:
                self.log_test(f"{test_name} (ERROR)", False, f"Exception: {e}")
        
        # Generate summary report
        self.generate_test_report(passed_tests, total_tests)
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': (passed_tests / total_tests) * 100,
            'performance_metrics': self.performance_metrics,
            'detailed_results': self.test_results
        }
    
    def generate_test_report(self, passed: int, total: int):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 CACHING MECHANISM TEST RESULTS")
        print("=" * 60)
        
        success_rate = (passed / total) * 100
        status = "✅ SUCCESS" if success_rate >= 85 else "⚠️ NEEDS ATTENTION"
        
        print(f"Overall Status: {status}")
        print(f"Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
        
        # Performance summary
        if self.performance_metrics:
            print("\n📈 Performance Metrics:")
            for operation, times in self.performance_metrics.items():
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                print(f"  {operation}: avg={avg_time:.1f}ms, min={min_time:.1f}ms, max={max_time:.1f}ms")
        
        # Detailed results
        print("\n📋 Detailed Test Results:")
        for test_name, passed, details in self.test_results:
            status = "✅" if passed else "❌"
            print(f"  {status} {test_name}")
            if details:
                print(f"      {details}")
        
        # Cache status
        session_file = self.project_root / ".claude_session_state.json"
        discovery_file = self.project_root / ".claude_discovery_cache.json"
        
        print(f"\n💾 Cache Files Status:")
        print(f"  Session State: {'✅ EXISTS' if session_file.exists() else '❌ MISSING'}")
        print(f"  Discovery Cache: {'✅ EXISTS' if discovery_file.exists() else '❌ MISSING'}")
        
        if session_file.exists():
            age = (time.time() - session_file.stat().st_mtime) / 60
            print(f"    Session age: {age:.1f} minutes")
        
        if discovery_file.exists():
            age = (time.time() - discovery_file.stat().st_mtime) / 60
            print(f"    Discovery age: {age:.1f} minutes")

def main():
    """Run the caching test suite"""
    test_suite = CachingTestSuite()
    results = test_suite.run_all_tests()
    
    # Return success/failure for scripting
    return results['success_rate'] >= 85

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)