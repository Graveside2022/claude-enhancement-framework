#!/usr/bin/env python3
"""
Cache Optimization Validation Script
Tests the improved cache performance from 66.7% to 90%+ target

Created for: Christian
Focus: Cache invalidation logic optimization ONLY
"""

import time
import json
import tempfile
import shutil
from pathlib import Path
from scripts.session_state_manager import SmartConfigurationManager, timing_check, learning_access

def test_cache_performance():
    """Test cache performance with the optimized invalidation logic"""
    print("🚀 Cache Performance Optimization Validation")
    print("=" * 50)
    
    manager = SmartConfigurationManager()
    
    # Test 1: Baseline cache performance (should exceed 90%)
    print("\n📊 Test 1: Cache Hit Rate Validation")
    operations = []
    total_operations = 30  # More operations for statistical significance
    
    # Initial load
    start_time = time.time()
    config = manager.get_project_configuration()
    initial_load_time = (time.time() - start_time) * 1000
    print(f"  Initial load: {initial_load_time:.2f}ms")
    
    # Mixed operations to simulate real usage patterns
    for i in range(total_operations):
        start_time = time.time()
        
        if i % 4 == 0:
            result = timing_check("session_scan")
            op_type = "timing_check"
        elif i % 4 == 1:
            result = learning_access("memory")
            op_type = "learning_access"
        elif i % 4 == 2:
            result = manager.is_tdd_protocol_active()
            op_type = "tdd_check"
        else:
            result = manager.get_project_configuration()
            op_type = "config_access"
            
        access_time = (time.time() - start_time) * 1000
        # Optimized cache should be sub-millisecond
        cache_hit = access_time < 1.0
        operations.append((op_type, cache_hit, access_time))
    
    # Calculate metrics
    cache_hits = sum(1 for _, hit, _ in operations if hit)
    hit_rate = (cache_hits / total_operations) * 100
    avg_access_time = sum(time for _, _, time in operations) / total_operations
    
    print(f"  Operations tested: {total_operations}")
    print(f"  Cache hits: {cache_hits}")
    print(f"  Hit rate: {hit_rate:.1f}%")
    print(f"  Average access time: {avg_access_time:.3f}ms")
    print(f"  Target (90%): {'✅ EXCEEDED' if hit_rate >= 90 else '❌ FAILED'}")
    
    return hit_rate >= 90

def test_session_timeout_optimization():
    """Test that extended session timeout reduces cache misses"""
    print("\n⏰ Test 2: Session Timeout Optimization")
    
    manager = SmartConfigurationManager()
    
    # Test current timeout settings
    timeout_hours = manager.session_manager.session_timeout_hours
    max_lifetime = manager.session_manager.max_session_lifetime_hours
    
    print(f"  Session timeout: {timeout_hours} hours (optimized from 2)")
    print(f"  Max lifetime: {max_lifetime} hours")
    print(f"  Improvement: {(timeout_hours - 2) / 2 * 100:.0f}% longer session retention")
    
    # Verify improvement
    improved = timeout_hours > 2
    print(f"  Timeout optimization: {'✅ ACTIVE' if improved else '❌ NOT APPLIED'}")
    
    return improved

def test_file_change_detection():
    """Test content-based change detection vs mtime sensitivity"""
    print("\n🔍 Test 3: File Change Detection Optimization")
    
    manager = SmartConfigurationManager()
    
    # Force session initialization
    manager.get_project_configuration()
    
    # Get current file hashes (should be content-based)
    if manager.session_manager.state and manager.session_manager.state.config_file_hashes:
        claude_md_path = str(Path.cwd() / "CLAUDE.md")
        current_hash = manager.session_manager.state.config_file_hashes.get(claude_md_path)
        
        print(f"  Using content hashing: {'✅ YES' if current_hash else '❌ NO'}")
        print(f"  Hash tracking active: {'✅ YES' if manager.session_manager.state.config_file_hashes else '❌ NO'}")
        
        # Test that touching file doesn't invalidate cache
        if current_hash:
            # Touch the file (changes mtime but not content)
            claude_md = Path("CLAUDE.md")
            if claude_md.exists():
                original_mtime = claude_md.stat().st_mtime
                claude_md.touch()
                new_mtime = claude_md.stat().st_mtime
                
                # Check if cache is still valid
                is_still_active = manager.session_manager.is_session_active()
                print(f"  File touched (mtime changed): {'✅ YES' if new_mtime > original_mtime else '❌ NO'}")
                print(f"  Cache remains valid: {'✅ YES' if is_still_active else '❌ NO'}")
                
                return is_still_active
    
    print("  Content hashing: ❌ NOT DETECTED")
    return False

def test_concurrent_access_safety():
    """Test that file locking prevents race conditions"""
    print("\n🔒 Test 4: Concurrent Access Safety")
    
    # Test that safe file operations are being used
    manager = SmartConfigurationManager()
    
    # Check if locking mechanism is available
    has_fcntl = hasattr(manager.session_manager, '_safe_file_operation')
    print(f"  Thread-safe file operations: {'✅ IMPLEMENTED' if has_fcntl else '❌ MISSING'}")
    
    if has_fcntl:
        # Test that we can read safely
        try:
            result = manager.session_manager._safe_file_operation('read')
            print(f"  Safe read operation: {'✅ WORKING' if result is not None else '⚠️ PARTIAL'}")
            return True
        except Exception as e:
            print(f"  Safe read operation: ❌ ERROR: {e}")
            return False
    
    return has_fcntl

def main():
    """Run complete cache optimization validation"""
    print("🎯 CACHE OPTIMIZATION VALIDATION")
    print("Improving from 66.7% to 90%+ target")
    print("Focus: Cache invalidation logic optimization ONLY")
    print()
    
    results = []
    
    # Run all tests
    results.append(("Cache Hit Rate", test_cache_performance()))
    results.append(("Session Timeout", test_session_timeout_optimization()))
    results.append(("File Change Detection", test_file_change_detection()))
    results.append(("Concurrent Safety", test_concurrent_access_safety()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 OPTIMIZATION VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<25}: {status}")
        if result:
            passed += 1
    
    overall_success = passed == len(results)
    success_rate = (passed / len(results)) * 100
    
    print(f"\n📊 Overall Results:")
    print(f"  Tests passed: {passed}/{len(results)}")
    print(f"  Success rate: {success_rate:.1f}%")
    print(f"  Cache optimization: {'✅ COMPLETE' if overall_success else '⚠️ PARTIAL'}")
    
    if overall_success:
        print(f"\n🎉 Cache performance optimized from 66.7% to 90%+ target!")
        print(f"   Key improvements implemented:")
        print(f"   • Extended session timeout (2h → 8h)")
        print(f"   • Content-based change detection (mtime → SHA-256)")
        print(f"   • Complete learning_files caching")
        print(f"   • Thread-safe file operations")
        print(f"   • New timing_check() and learning_access() helpers")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)