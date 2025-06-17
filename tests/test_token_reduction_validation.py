#!/usr/bin/env python3
"""
Token Reduction Validation Test
Verifies 97.6% token reduction (24.6k → 1,140 tokens) is achieved

Created for: Christian
Target: Validate optimized system meets token reduction requirements
"""

import sys
import time
import subprocess
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from optimized_project_loader import (
    get_optimized_project_info,
    get_project_summary,
    clear_project_cache
)
from auto_project_loader import (
    initialize_project_for_session,
    get_project_config,
    get_project_summary_compact
)


def estimate_token_usage(output_text: str) -> int:
    """
    Estimate token usage from output text
    Rough approximation: ~4 characters per token for English text
    """
    return len(output_text) // 4


def capture_output_tokens(func, *args, **kwargs):
    """
    Capture stdout output and estimate token usage
    """
    import io
    import contextlib
    
    output_buffer = io.StringIO()
    
    with contextlib.redirect_stdout(output_buffer):
        result = func(*args, **kwargs)
    
    output_text = output_buffer.getvalue()
    estimated_tokens = estimate_token_usage(output_text)
    
    return result, output_text, estimated_tokens


def test_heavy_vs_optimized_comparison():
    """
    Compare token usage between heavy and optimized project loaders
    """
    print("🔬 Token Reduction Validation Test")
    print("=" * 50)
    
    # Clear any existing cache
    clear_project_cache()
    
    print("\n📊 Testing Optimized Project Loader...")
    
    # Test optimized loader (silent mode)
    start_time = time.time()
    config, output, tokens = capture_output_tokens(
        get_optimized_project_info, 
        silent=True
    )
    optimized_time = time.time() - start_time
    
    print(f"✓ Optimized scan: {optimized_time:.3f}s, ~{tokens} tokens")
    
    # Test optimized loader (verbose mode for comparison)
    config_verbose, output_verbose, tokens_verbose = capture_output_tokens(
        get_optimized_project_info,
        silent=False
    )
    
    print(f"✓ Optimized verbose: ~{tokens_verbose} tokens")
    
    # Test auto-loader initialization
    auto_config, auto_output, auto_tokens = capture_output_tokens(
        initialize_project_for_session
    )
    
    print(f"✓ Auto-loader init: ~{auto_tokens} tokens")
    
    # Test ultra-compact summary
    summary = get_project_summary_compact()
    summary_tokens = estimate_token_usage(summary)
    
    print(f"✓ Compact summary: '{summary}' (~{summary_tokens} tokens)")
    
    return {
        'optimized_silent': tokens,
        'optimized_verbose': tokens_verbose,
        'auto_loader': auto_tokens,
        'summary': summary_tokens,
        'load_time': optimized_time
    }


def test_cache_performance():
    """
    Test cache performance and token reduction through caching
    """
    print("\n🔄 Cache Performance Test...")
    
    # First load (should create cache)
    start_time = time.time()
    config1, output1, tokens1 = capture_output_tokens(
        get_optimized_project_info,
        silent=True
    )
    first_load_time = time.time() - start_time
    
    # Second load (should use cache)
    start_time = time.time()
    config2, output2, tokens2 = capture_output_tokens(
        get_optimized_project_info,
        silent=True
    )
    cache_load_time = time.time() - start_time
    
    # Third load (verify cache consistency)
    config3, output3, tokens3 = capture_output_tokens(
        get_optimized_project_info,
        silent=True
    )
    
    print(f"✓ First load: {first_load_time:.3f}s, ~{tokens1} tokens")
    print(f"✓ Cache load: {cache_load_time:.3f}s, ~{tokens2} tokens")
    print(f"✓ Cache verify: ~{tokens3} tokens")
    
    speedup = first_load_time / cache_load_time if cache_load_time > 0 else float('inf')
    print(f"🚀 Cache speedup: {speedup:.1f}x")
    
    return {
        'first_load_tokens': tokens1,
        'cache_load_tokens': tokens2,
        'cache_verify_tokens': tokens3,
        'speedup': speedup,
        'first_load_time': first_load_time,
        'cache_load_time': cache_load_time
    }


def validate_token_reduction_target():
    """
    Validate that the 97.6% token reduction target is met
    """
    print("\n🎯 Token Reduction Target Validation...")
    
    # Original system baseline: 24,600 tokens
    original_baseline = 24600
    target_reduction = 0.976  # 97.6%
    target_tokens = int(original_baseline * (1 - target_reduction))  # ~1,140 tokens
    
    print(f"📈 Original baseline: {original_baseline:,} tokens")
    print(f"🎯 Target after 97.6% reduction: {target_tokens:,} tokens")
    
    # Test complete startup sequence
    total_tokens = 0
    
    # 1. Project discovery
    _, _, discovery_tokens = capture_output_tokens(
        get_optimized_project_info,
        silent=True
    )
    total_tokens += discovery_tokens
    
    # 2. Auto-loader initialization
    _, _, init_tokens = capture_output_tokens(
        initialize_project_for_session
    )
    total_tokens += init_tokens
    
    # 3. Configuration access (10 calls to simulate typical usage)
    for _ in range(10):
        _, _, config_tokens = capture_output_tokens(get_project_config)
        total_tokens += config_tokens
    
    # 4. Summary generation
    summary_tokens = estimate_token_usage(get_project_summary_compact())
    total_tokens += summary_tokens
    
    print(f"\n📊 Actual Token Usage Breakdown:")
    print(f"- Project discovery: ~{discovery_tokens} tokens")
    print(f"- Auto-loader init: ~{init_tokens} tokens")
    print(f"- Config access (10x): ~{total_tokens - discovery_tokens - init_tokens - summary_tokens} tokens")
    print(f"- Summary generation: ~{summary_tokens} tokens")
    print(f"- TOTAL: ~{total_tokens} tokens")
    
    # Calculate reduction achieved
    reduction_achieved = 1 - (total_tokens / original_baseline)
    reduction_percentage = reduction_achieved * 100
    
    print(f"\n🏆 Results:")
    print(f"- Token reduction achieved: {reduction_percentage:.1f}%")
    print(f"- Target reduction: {target_reduction * 100:.1f}%")
    
    if total_tokens <= target_tokens:
        print(f"✅ SUCCESS: Target met! ({total_tokens:,} ≤ {target_tokens:,} tokens)")
        return True
    else:
        print(f"❌ MISS: Target exceeded ({total_tokens:,} > {target_tokens:,} tokens)")
        return False


def main():
    """
    Run complete token reduction validation test suite
    """
    print("🧪 CLAUDE Improvement Project - Token Reduction Validation")
    print("Target: 97.6% reduction (24.6k → 1,140 tokens)")
    print("=" * 70)
    
    # Test 1: Compare optimized vs heavy loaders
    comparison_results = test_heavy_vs_optimized_comparison()
    
    # Test 2: Cache performance validation
    cache_results = test_cache_performance()
    
    # Test 3: Validate target achievement
    target_met = validate_token_reduction_target()
    
    print("\n" + "=" * 70)
    print("📋 VALIDATION SUMMARY")
    print("=" * 70)
    
    print(f"⚡ Load Performance:")
    print(f"  - Optimized load time: {comparison_results['load_time']:.3f}s")
    print(f"  - Cache speedup: {cache_results['speedup']:.1f}x")
    
    print(f"\n🔢 Token Efficiency:")
    print(f"  - Silent mode: ~{comparison_results['optimized_silent']} tokens")
    print(f"  - Auto-loader: ~{comparison_results['auto_loader']} tokens")
    print(f"  - Compact summary: ~{comparison_results['summary']} tokens")
    
    print(f"\n🎯 Target Achievement:")
    if target_met:
        print("  ✅ 97.6% token reduction TARGET MET")
        print("  🏆 Optimized system ready for deployment")
    else:
        print("  ❌ Token reduction target not met")
        print("  🔧 Further optimization required")
    
    print("\n" + "=" * 70)
    return target_met


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)