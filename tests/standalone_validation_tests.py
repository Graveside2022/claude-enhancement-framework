#!/usr/bin/env python3
"""
Standalone Test Suite for Configuration Validation Optimizer
TDD tests without external dependencies

Tests the 4 validation checks and optimization performance
Created for: Christian
"""

import time
import tempfile
import shutil
from pathlib import Path

# Import the system under test
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "scripts"))

try:
    from config_validation_optimizer import ConfigurationValidationCache, ValidationAdapter
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Python path: {sys.path}")
    print(f"Looking for: {project_root / 'scripts' / 'config_validation_optimizer.py'}")
    raise


class StandaloneTestRunner:
    """Standalone test runner for validation optimizer"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def assert_equal(self, actual, expected, message=""):
        """Simple assertion helper"""
        if actual == expected:
            return True
        else:
            raise AssertionError(f"Expected {expected}, got {actual}. {message}")
    
    def assert_true(self, condition, message=""):
        """Assert condition is true"""
        if condition:
            return True
        else:
            raise AssertionError(f"Expected True, got {condition}. {message}")
    
    def assert_in(self, item, container, message=""):
        """Assert item is in container"""
        if item in container:
            return True
        else:
            raise AssertionError(f"Expected {item} in {container}. {message}")
    
    def assert_less(self, a, b, message=""):
        """Assert a < b"""
        if a < b:
            return True
        else:
            raise AssertionError(f"Expected {a} < {b}. {message}")
    
    def assert_greater(self, a, b, message=""):
        """Assert a > b"""
        if a > b:
            return True
        else:
            raise AssertionError(f"Expected {a} > {b}. {message}")
    
    def run_test(self, test_func, test_name):
        """Run a single test"""
        try:
            print(f"  🧪 {test_name}...", end="")
            test_func()
            print(" ✅ PASSED")
            self.passed += 1
            return True
        except Exception as e:
            print(f" ❌ FAILED: {e}")
            self.failed += 1
            return False
    
    def create_temp_project(self):
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
        
        return temp_dir
    
    def test_single_load_configuration_caching(self):
        """Test that configuration is loaded once and cached"""
        temp_project = self.create_temp_project()
        try:
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
            self.assert_true(cache.cache_loaded)
            self.assert_equal(config1, config2)
            self.assert_less(second_load_time, first_load_time * 0.1)
            self.assert_in('claude_md_config', config1)
            self.assert_in('tdd_config', config1)
            self.assert_in('agent_config', config1)
            self.assert_in('pattern_config', config1)
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_tdd_protocol_validation(self):
        """Test TDD protocol validation - Query 1"""
        temp_project = self.create_temp_project()
        try:
            cache = ConfigurationValidationCache(str(temp_project))
            result = cache.validate_tdd_protocol()
            
            # Assertions
            self.assert_true(result['cached'])
            self.assert_equal(result['check_type'], 'tdd_protocol')
            self.assert_true(result['valid'])
            self.assert_true(result['seven_step_active'])
            self.assert_equal(result['complexity_threshold'], 7)
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_agent_configuration_validation(self):
        """Test agent configuration validation - Query 2"""
        temp_project = self.create_temp_project()
        try:
            cache = ConfigurationValidationCache(str(temp_project))
            result = cache.validate_agent_configuration()
            
            # Assertions
            self.assert_true(result['cached'])
            self.assert_equal(result['check_type'], 'agent_configuration')
            self.assert_true(result['valid'])
            self.assert_in(result['default_count'], [5, 7])
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_pattern_first_validation(self):
        """Test pattern-first validation - Query 3"""
        temp_project = self.create_temp_project()
        try:
            cache = ConfigurationValidationCache(str(temp_project))
            result = cache.validate_pattern_first()
            
            # Assertions
            self.assert_true(result['cached'])
            self.assert_equal(result['check_type'], 'pattern_first')
            self.assert_true(result['valid'])
            self.assert_true(result['patterns_available'])
            self.assert_greater(result['matching_threshold'], 50)
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_config_file_validation(self):
        """Test config file validation - Query 4"""
        temp_project = self.create_temp_project()
        try:
            cache = ConfigurationValidationCache(str(temp_project))
            result = cache.validate_config_file()
            
            # Assertions
            self.assert_true(result['cached'])
            self.assert_equal(result['check_type'], 'config_file')
            self.assert_true(result['valid'])
            self.assert_true(result['has_binding_statements'])
            self.assert_true(result['has_enforcement_protocol'])
            self.assert_equal(len(result['security_issues']), 0)
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_all_validations_performance(self):
        """Test that all 4 validations use cached data efficiently"""
        temp_project = self.create_temp_project()
        try:
            cache = ConfigurationValidationCache(str(temp_project))
            
            start_time = time.time()
            results = cache.run_all_validations()
            total_time = time.time() - start_time
            
            # Assertions
            self.assert_in('tdd_protocol', results)
            self.assert_in('agent_configuration', results)
            self.assert_in('pattern_first', results)
            self.assert_in('config_file', results)
            self.assert_in('optimization_stats', results)
            
            # Performance assertions
            stats = results['optimization_stats']
            self.assert_equal(stats['processes_spawned'], 0)  # KEY: No processes spawned
            self.assert_equal(stats['queries_executed'], 4)
            self.assert_true(stats['cache_used'])
            self.assert_less(total_time, 0.1)  # Should be very fast
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_validation_adapter_backward_compatibility(self):
        """Test that adapter provides backward compatibility"""
        temp_project = self.create_temp_project()
        try:
            adapter = ValidationAdapter(str(temp_project))
            
            # Test legacy interfaces
            tdd_result = adapter.check_tdd_protocol()
            agent_result = adapter.check_agent_config()
            pattern_result = adapter.check_pattern_first()
            config_result = adapter.validate_config_file()
            
            # Assertions
            self.assert_true(isinstance(tdd_result, bool))
            self.assert_true(isinstance(agent_result, int))
            self.assert_true(isinstance(pattern_result, bool))
            self.assert_true(isinstance(config_result, bool))
            
            # Values should match optimization
            self.assert_true(tdd_result)
            self.assert_in(agent_result, [5, 7])
            self.assert_true(pattern_result)
            self.assert_true(config_result)
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_security_pattern_detection(self):
        """Test security pattern detection in config validation"""
        temp_project = self.create_temp_project()
        try:
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
            self.assert_equal(result['valid'], False)
            self.assert_greater(len(result['security_issues']), 0)
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_optimization_eliminates_redundant_loading(self):
        """Test that optimization eliminates redundant configuration loading"""
        temp_project = self.create_temp_project()
        try:
            cache = ConfigurationValidationCache(str(temp_project))
            
            # Track configuration loading calls
            load_calls = []
            original_load = cache._load_claude_md_config
            
            def track_load():
                load_calls.append(time.time())
                return original_load()
            
            cache._load_claude_md_config = track_load
            
            # First, load configuration once
            cache.load_configuration_once()
            
            # Clear the load calls from initial loading
            load_calls.clear()
            
            # Run multiple validations - these should use cached data
            cache.validate_tdd_protocol()
            cache.validate_agent_configuration()
            cache.validate_pattern_first()
            cache.validate_config_file()
            
            # Assertions - no additional loading should occur
            self.assert_equal(len(load_calls), 0)  # No additional loading after cache
            self.assert_true(cache.cache_loaded)
            
        finally:
            shutil.rmtree(temp_project)
    
    def test_performance_comparison_simulation(self):
        """Simulate performance comparison between old and new approaches"""
        temp_project = self.create_temp_project()
        try:
            adapter = ValidationAdapter(str(temp_project))
            
            # Measure optimized approach
            start_time = time.time()
            results = adapter.get_all_validations()
            optimized_time = time.time() - start_time
            
            # Simulate old approach timing (would spawn 4 Python processes)
            simulated_old_time = 4 * 0.075  # 75ms per process spawn
            
            # Assertions
            self.assert_less(optimized_time, simulated_old_time * 0.1)
            self.assert_equal(results['optimization_stats']['processes_spawned'], 0)
            
            # Performance metrics
            speedup_factor = simulated_old_time / optimized_time if optimized_time > 0 else 100
            self.assert_greater(speedup_factor, 5)  # Should be much faster
            
        finally:
            shutil.rmtree(temp_project)
    
    def run_all_tests(self):
        """Run all validation tests"""
        print("🧪 Running TDD Validation Tests for Configuration Optimizer")
        print("=" * 70)
        print()
        
        # Define test methods
        test_methods = [
            (self.test_single_load_configuration_caching, "Single Load Configuration Caching"),
            (self.test_tdd_protocol_validation, "TDD Protocol Validation"),
            (self.test_agent_configuration_validation, "Agent Configuration Validation"),
            (self.test_pattern_first_validation, "Pattern-First Validation"),
            (self.test_config_file_validation, "Config File Validation"),
            (self.test_all_validations_performance, "All Validations Performance"),
            (self.test_validation_adapter_backward_compatibility, "Validation Adapter Backward Compatibility"),
            (self.test_security_pattern_detection, "Security Pattern Detection"),
            (self.test_optimization_eliminates_redundant_loading, "Optimization Eliminates Redundant Loading"),
            (self.test_performance_comparison_simulation, "Performance Comparison Simulation")
        ]
        
        # Run tests
        for test_func, test_name in test_methods:
            self.run_test(test_func, test_name)
        
        # Summary
        print()
        print("📊 Test Results Summary:")
        print(f"   ✅ Passed: {self.passed}")
        print(f"   ❌ Failed: {self.failed}")
        print(f"   📈 Success Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 All TDD validation tests passed!")
            print("✅ Configuration validation optimizer verified:")
            print("   • Single-load, multi-query pattern works")
            print("   • All 4 validation checks function correctly")
            print("   • Zero redundant Python process spawns")
            print("   • Backward compatibility maintained")
            print("   • Performance optimization achieved")
        else:
            print(f"\n⚠️ {self.failed} test(s) failed!")
            print("🔧 Review the failures above")
        
        return self.failed == 0


def main():
    """Main test execution"""
    runner = StandaloneTestRunner()
    success = runner.run_all_tests()
    return success


if __name__ == "__main__":
    main()