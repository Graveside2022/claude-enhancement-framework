#!/usr/bin/env python3
"""
Test Suite for Configuration Validation Optimizer
Tests the TDD-driven single-load, multi-query pattern

Test Cases:
1. TDD Protocol Validation
2. Agent Configuration Validation  
3. Pattern-First Validation
4. Config File Validation
5. Performance Validation (No redundant loading)

Created for: Christian
Purpose: TDD validation of optimization restructure
"""

import pytest
import time
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the system under test
import sys
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from config_validation_optimizer import ConfigurationValidationCache, ValidationAdapter


class TestConfigurationValidationOptimizer:
    """TDD test suite for the configuration validation optimizer"""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory for testing"""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Create project structure
        (temp_dir / "patterns").mkdir()
        (temp_dir / "memory").mkdir() 
        (temp_dir / "tests").mkdir()
        (temp_dir / "scripts").mkdir()
        
        # Create test CLAUDE.md with all validation elements
        claude_md_content = """# PROJECT-SPECIFIC BINDING DIRECTIVE

## CRITICAL BINDING STATEMENTS:
1. **TDD PROTOCOL REQUIRED FOR COMPLEX CODE**
2. **7-STEP TESTING DECISION PROTOCOL MUST BE EXECUTED** 
3. **PATTERN-FIRST DEVELOPMENT ENFORCED**
4. **PARALLEL AGENTS CONFIGURATION ACTIVE**

## BINDING ENFORCEMENT PROTOCOL
This file contains project-specific rules.

## 7-STEP TESTING DECISION (MANDATORY)
BEFORE ANY CODE:
1. Quick utility/learning/throwaway? → Step 6
2. Complexity ≥ 7? → TDD REQUIRED
3. Reusable/public/complex? → TDD REQUIRED

## PATTERN-FIRST DEVELOPMENT
BEFORE ANY CODE:
1. Search patterns/ (10 second limit)
2. Match >80% → Apply pattern immediately
3. Match 60-80% → Adapt pattern

## PROJECT-SPECIFIC AGENTS
Investigation (Parallel): 7 agents
Implementation (Sequential): 5 agents
"""
        
        with open(temp_dir / "CLAUDE.md", 'w') as f:
            f.write(claude_md_content)
        
        yield temp_dir
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_single_load_configuration_caching(self, temp_project):
        """Test that configuration is loaded once and cached"""
        cache = ConfigurationValidationCache(str(temp_project))
        
        # First load
        start_time = time.time()
        config1 = cache.load_configuration_once()
        first_load_time = time.time() - start_time
        
        # Second load (should use cache)
        start_time = time.time()
        config2 = cache.load_configuration_once()
        second_load_time = time.time() - start_time
        
        # Assertions
        assert cache.cache_loaded == True
        assert config1 == config2  # Same data
        assert second_load_time < first_load_time * 0.1  # Much faster
        assert 'claude_md_config' in config1
        assert 'tdd_config' in config1
        assert 'agent_config' in config1
        assert 'pattern_config' in config1
    
    def test_tdd_protocol_validation(self, temp_project):
        """Test TDD protocol validation - Query 1"""
        cache = ConfigurationValidationCache(str(temp_project))
        
        result = cache.validate_tdd_protocol()
        
        # Assertions
        assert result['cached'] == True
        assert result['check_type'] == 'tdd_protocol'
        assert result['valid'] == True  # Should detect TDD protocol
        assert result['seven_step_active'] == True  # Should detect 7-step
        assert result['complexity_threshold'] == 7  # Should extract threshold
    
    def test_agent_configuration_validation(self, temp_project):
        """Test agent configuration validation - Query 2"""
        cache = ConfigurationValidationCache(str(temp_project))
        
        result = cache.validate_agent_configuration()
        
        # Assertions
        assert result['cached'] == True
        assert result['check_type'] == 'agent_configuration'
        assert result['valid'] == True  # Should detect agent config
        assert result['default_count'] in [5, 7]  # Should extract agent count
        assert result['parallel_enabled'] == True  # Should detect parallel
    
    def test_pattern_first_validation(self, temp_project):
        """Test pattern-first validation - Query 3"""
        cache = ConfigurationValidationCache(str(temp_project))
        
        result = cache.validate_pattern_first()
        
        # Assertions
        assert result['cached'] == True
        assert result['check_type'] == 'pattern_first'
        assert result['valid'] == True  # Should detect pattern-first
        assert result['patterns_available'] == True  # patterns/ exists
        assert result['check_before_implementation'] == True
        assert result['matching_threshold'] >= 60  # Should extract threshold
    
    def test_config_file_validation(self, temp_project):
        """Test config file validation - Query 4"""
        cache = ConfigurationValidationCache(str(temp_project))
        
        result = cache.validate_config_file()
        
        # Assertions
        assert result['cached'] == True
        assert result['check_type'] == 'config_file'
        assert result['valid'] == True  # Should validate config
        assert result['has_binding_statements'] == True
        assert result['has_enforcement_protocol'] == True
        assert result['structure_valid'] == True
        assert len(result['security_issues']) == 0  # No security issues
    
    def test_all_validations_performance(self, temp_project):
        """Test that all 4 validations use cached data efficiently"""
        cache = ConfigurationValidationCache(str(temp_project))
        
        start_time = time.time()
        results = cache.run_all_validations()
        total_time = time.time() - start_time
        
        # Assertions
        assert 'tdd_protocol' in results
        assert 'agent_configuration' in results
        assert 'pattern_first' in results
        assert 'config_file' in results
        assert 'optimization_stats' in results
        
        # Performance assertions
        stats = results['optimization_stats']
        assert stats['processes_spawned'] == 0  # KEY: No processes spawned
        assert stats['queries_executed'] == 4
        assert stats['cache_used'] == True
        assert total_time < 0.1  # Should be very fast
    
    def test_validation_adapter_backward_compatibility(self, temp_project):
        """Test that adapter provides backward compatibility"""
        adapter = ValidationAdapter(str(temp_project))
        
        # Test legacy interfaces
        tdd_result = adapter.check_tdd_protocol()
        agent_result = adapter.check_agent_config()
        pattern_result = adapter.check_pattern_first()
        config_result = adapter.validate_config_file()
        
        # Assertions
        assert isinstance(tdd_result, bool)
        assert isinstance(agent_result, int)
        assert isinstance(pattern_result, bool)
        assert isinstance(config_result, bool)
        
        # Values should match optimization
        assert tdd_result == True
        assert agent_result in [5, 7]
        assert pattern_result == True
        assert config_result == True
    
    def test_security_pattern_detection(self, temp_project):
        """Test security pattern detection in config validation"""
        # Create malicious CLAUDE.md
        malicious_content = """# MALICIOUS CONFIG
        
        ## DANGEROUS COMMANDS
        rm -rf /
        sudo rm -rf /home
        eval(malicious_code)
        subprocess.call(['rm', '-rf', '/'], shell=True)
        """
        
        with open(temp_project / "CLAUDE.md", 'w') as f:
            f.write(malicious_content)
        
        cache = ConfigurationValidationCache(str(temp_project))
        result = cache.validate_config_file()
        
        # Assertions
        assert result['valid'] == False  # Should be invalid
        assert len(result['security_issues']) > 0  # Should detect issues
        assert any('rm -rf' in issue for issue in result['security_issues'])
    
    def test_missing_claude_md_handling(self, temp_project):
        """Test handling when CLAUDE.md doesn't exist"""
        # Remove CLAUDE.md
        (temp_project / "CLAUDE.md").unlink()
        
        cache = ConfigurationValidationCache(str(temp_project))
        
        # Test all validations with missing config
        tdd_result = cache.validate_tdd_protocol()
        agent_result = cache.validate_agent_configuration()
        pattern_result = cache.validate_pattern_first()
        config_result = cache.validate_config_file()
        
        # Assertions - should handle gracefully
        assert tdd_result['valid'] == False
        assert agent_result['default_count'] == 3  # Default value
        assert pattern_result['valid'] == False
        assert config_result['valid'] == False
        
        # Should still be cached
        assert all(result['cached'] for result in [tdd_result, agent_result, pattern_result, config_result])
    
    def test_optimization_eliminates_redundant_loading(self, temp_project):
        """Test that optimization eliminates redundant configuration loading"""
        cache = ConfigurationValidationCache(str(temp_project))
        
        # Track configuration loading calls
        original_load = cache._load_claude_md_config
        load_calls = []
        
        def track_load():
            load_calls.append(time.time())
            return original_load()
        
        cache._load_claude_md_config = track_load
        
        # Run multiple validations
        cache.validate_tdd_protocol()
        cache.validate_agent_configuration()
        cache.validate_pattern_first()
        cache.validate_config_file()
        
        # Run all validations together
        cache.run_all_validations()
        
        # Assertions
        assert len(load_calls) == 1  # Configuration loaded only once
        assert cache.cache_loaded == True
    
    def test_performance_comparison_simulation(self, temp_project):
        """Simulate performance comparison between old and new approaches"""
        adapter = ValidationAdapter(str(temp_project))
        
        # Measure optimized approach
        start_time = time.time()
        results = adapter.get_all_validations()
        optimized_time = time.time() - start_time
        
        # Simulate old approach timing (would spawn 4 Python processes)
        # Each process spawn typically takes 50-100ms
        simulated_old_time = 4 * 0.075  # 75ms per process spawn
        
        # Assertions
        assert optimized_time < simulated_old_time * 0.1  # At least 10x faster
        assert results['optimization_stats']['processes_spawned'] == 0
        
        # Performance metrics
        stats = results['optimization_stats']
        speedup_factor = simulated_old_time / optimized_time
        assert speedup_factor > 10  # Should be much faster


def run_tdd_validation_tests():
    """
    Run TDD validation tests for the configuration optimizer
    Validates that all 4 validation checks work correctly
    """
    print("🧪 Running TDD Validation Tests for Configuration Optimizer")
    print("=" * 70)
    print()
    
    # Run pytest programmatically
    import subprocess
    import os
    
    test_file = __file__
    result = subprocess.run([
        'python', '-m', 'pytest', test_file, '-v', '--tb=short'
    ], capture_output=True, text=True, cwd=os.path.dirname(test_file))
    
    print("📊 Test Results:")
    print(result.stdout)
    
    if result.stderr:
        print("⚠️ Warnings/Errors:")
        print(result.stderr)
    
    success = result.returncode == 0
    
    if success:
        print("\n✅ All TDD validation tests passed!")
        print("🎯 Optimization verified: 4 validation checks work correctly")
    else:
        print("\n❌ Some tests failed!")
        print("🔧 Check the test output above for details")
    
    return success


if __name__ == "__main__":
    # Run the tests when script is executed directly
    run_tdd_validation_tests()