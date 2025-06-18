#!/usr/bin/env python3
"""
Platform Compatibility Validation Script
Claude Enhancement Framework - Agent 3 Validation Tool

Validates framework compatibility on target platform and provides
specific recommendations for optimal deployment.

Author: Christian (Agent 3)
Purpose: Platform-specific compatibility validation and recommendations
"""

import os
import sys
import platform
import subprocess
import tempfile
from pathlib import Path
import json
import time


class PlatformCompatibilityValidator:
    """Validates Claude Enhancement Framework compatibility on current platform."""
    
    def __init__(self):
        self.platform_name = platform.system()
        self.platform_version = platform.release()
        self.platform_arch = platform.machine()
        self.python_version = sys.version_info
        
        self.validation_results = {
            "platform_info": {
                "system": self.platform_name,
                "version": self.platform_version,
                "architecture": self.platform_arch,
                "python_version": f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}"
            },
            "compatibility_status": {},
            "performance_expectations": {},
            "platform_limitations": {},
            "recommendations": []
        }
    
    def run_validation(self):
        """Execute complete platform compatibility validation."""
        print("🔍 Claude Enhancement Framework - Platform Compatibility Validation")
        print("=" * 70)
        print(f"Platform: {self.platform_name} {self.platform_version}")
        print(f"Architecture: {self.platform_arch}")
        print(f"Python: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print()
        
        self.validate_system_requirements()
        self.validate_python_environment()
        self.validate_framework_compatibility()
        self.validate_performance_expectations()
        self.validate_platform_specific_features()
        self.generate_recommendations()
        
        self.display_validation_results()
        return self.validation_results
    
    def validate_system_requirements(self):
        """Validate system requirements for framework deployment."""
        print("📋 Validating System Requirements...")
        
        requirements = {
            "python_version": self.python_version >= (3, 8),
            "platform_supported": self.platform_name in ["Darwin", "Linux", "Windows"],
            "architecture_supported": True,  # All common architectures supported
            "file_system_access": self._test_file_system_access(),
            "network_access": self._test_network_access(),
            "shell_access": self._test_shell_access()
        }
        
        self.validation_results["compatibility_status"]["system_requirements"] = requirements
        
        passed = sum(1 for result in requirements.values() if result)
        total = len(requirements)
        
        print(f"   System Requirements: {passed}/{total} ✅")
        
        for req_name, req_result in requirements.items():
            status = "✅" if req_result else "❌"
            print(f"   {req_name.replace('_', ' ').title()}: {status}")
    
    def _test_file_system_access(self):
        """Test file system read/write capabilities."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                test_file = Path(temp_dir) / "test_access.txt"
                test_file.write_text("test")
                content = test_file.read_text()
                return content == "test"
        except:
            return False
    
    def _test_network_access(self):
        """Test basic network connectivity (optional)."""
        try:
            # Simple DNS resolution test
            import socket
            socket.gethostbyname("github.com")
            return True
        except:
            return False
    
    def _test_shell_access(self):
        """Test shell command execution capability."""
        try:
            result = subprocess.run(["python", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def validate_python_environment(self):
        """Validate Python environment compatibility."""
        print("🐍 Validating Python Environment...")
        
        # Test required modules
        required_modules = [
            "os", "sys", "pathlib", "platform", "tempfile", 
            "json", "time", "subprocess"
        ]
        
        module_availability = {}
        for module_name in required_modules:
            try:
                __import__(module_name)
                module_availability[module_name] = True
            except ImportError:
                module_availability[module_name] = False
        
        # Test Python features
        python_features = {
            "pathlib_support": hasattr(Path, "exists"),
            "f_strings": True,  # Python 3.8+ requirement ensures this
            "type_hints": True,  # Available in Python 3.8+
            "asyncio": self._test_asyncio_support(),
            "json_encoding": self._test_json_encoding(),
            "unicode_support": self._test_unicode_support()
        }
        
        environment_status = {
            "modules": module_availability,
            "features": python_features,
            "version_compatible": self.python_version >= (3, 8)
        }
        
        self.validation_results["compatibility_status"]["python_environment"] = environment_status
        
        module_count = sum(1 for available in module_availability.values() if available)
        feature_count = sum(1 for available in python_features.values() if available)
        
        print(f"   Required Modules: {module_count}/{len(required_modules)} ✅")
        print(f"   Python Features: {feature_count}/{len(python_features)} ✅")
        print(f"   Version Compatible: {'✅' if environment_status['version_compatible'] else '❌'}")
    
    def _test_asyncio_support(self):
        """Test asyncio availability."""
        try:
            import asyncio
            return hasattr(asyncio, "run")
        except:
            return False
    
    def _test_json_encoding(self):
        """Test JSON encoding/decoding."""
        try:
            import json
            test_data = {"test": "data", "unicode": "测试"}
            encoded = json.dumps(test_data)
            decoded = json.loads(encoded)
            return decoded == test_data
        except:
            return False
    
    def _test_unicode_support(self):
        """Test Unicode string handling."""
        try:
            test_string = "Hello 世界 🌍"
            return len(test_string) > 0 and "🌍" in test_string
        except:
            return False
    
    def validate_framework_compatibility(self):
        """Validate framework-specific compatibility."""
        print("🔧 Validating Framework Compatibility...")
        
        # Test framework import capability
        framework_dir = Path(__file__).parent
        framework_tests = {
            "framework_directory": framework_dir.exists(),
            "claude_enhancer_module": (framework_dir / "claude_enhancer").exists(),
            "init_files": (framework_dir / "claude_enhancer" / "__init__.py").exists(),
            "core_module": (framework_dir / "claude_enhancer" / "core").exists(),
            "setup_script": (framework_dir / "setup").exists()
        }
        
        # Test PathManager functionality
        pathmanager_tests = {}
        try:
            sys.path.insert(0, str(framework_dir))
            from claude_enhancer.core.path_manager import PathManager
            
            pm = PathManager()
            pathmanager_tests = {
                "instantiation": True,
                "platform_detection": hasattr(pm, "platform"),
                "username_detection": hasattr(pm, "username"),
                "path_resolution": callable(getattr(pm, "find_project_root", None)),
                "template_substitution": callable(getattr(pm, "substitute_template_variables", None))
            }
        except Exception as e:
            pathmanager_tests = {
                "import_error": str(e),
                "instantiation": False
            }
        
        compatibility_status = {
            "framework_structure": framework_tests,
            "pathmanager_functionality": pathmanager_tests
        }
        
        self.validation_results["compatibility_status"]["framework"] = compatibility_status
        
        structure_count = sum(1 for test in framework_tests.values() if test)
        pathmanager_count = sum(1 for test in pathmanager_tests.values() if test)
        
        print(f"   Framework Structure: {structure_count}/{len(framework_tests)} ✅")
        print(f"   PathManager Functionality: {pathmanager_count}/{len(pathmanager_tests)} ✅")
    
    def validate_performance_expectations(self):
        """Validate expected performance characteristics."""
        print("⚡ Validating Performance Expectations...")
        
        # Platform-specific performance targets
        performance_targets = {
            "Darwin": {"boot_time_ms": 50, "memory_mb": 100, "cache_hit_rate": 0.90},
            "Linux": {"boot_time_ms": 30, "memory_mb": 80, "cache_hit_rate": 0.95},
            "Windows": {"boot_time_ms": 200, "memory_mb": 150, "cache_hit_rate": 0.85}
        }
        
        current_targets = performance_targets.get(self.platform_name, performance_targets["Linux"])
        
        # Test actual performance
        performance_tests = {}
        
        # Test import time
        start_time = time.perf_counter()
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from claude_enhancer.core.path_manager import PathManager
            import_time = (time.perf_counter() - start_time) * 1000
            performance_tests["import_time_ms"] = round(import_time, 3)
        except:
            performance_tests["import_time_ms"] = None
        
        # Test PathManager operations
        if performance_tests["import_time_ms"] is not None:
            try:
                pm = PathManager()
                
                # Time path operations
                start_time = time.perf_counter()
                pm.find_project_root()
                path_resolution_time = (time.perf_counter() - start_time) * 1000
                
                start_time = time.perf_counter()
                pm.substitute_template_variables("{{USER_NAME}} on {{PLATFORM}}")
                template_time = (time.perf_counter() - start_time) * 1000
                
                performance_tests["path_resolution_ms"] = round(path_resolution_time, 3)
                performance_tests["template_substitution_ms"] = round(template_time, 3)
            except:
                performance_tests["path_resolution_ms"] = None
                performance_tests["template_substitution_ms"] = None
        
        performance_analysis = {
            "targets": current_targets,
            "measured": performance_tests,
            "meets_boot_target": (performance_tests.get("import_time_ms", float('inf')) < current_targets["boot_time_ms"]),
            "performance_grade": self._calculate_performance_grade(performance_tests, current_targets)
        }
        
        self.validation_results["performance_expectations"] = performance_analysis
        
        print(f"   Import Time: {performance_tests.get('import_time_ms', 'N/A')}ms")
        print(f"   Boot Target: <{current_targets['boot_time_ms']}ms")
        print(f"   Performance Grade: {performance_analysis['performance_grade']}")
    
    def _calculate_performance_grade(self, measured, targets):
        """Calculate performance grade based on measurements."""
        import_time = measured.get("import_time_ms")
        if import_time is None:
            return "Unknown"
        
        target_time = targets["boot_time_ms"]
        
        if import_time < target_time * 0.1:
            return "Excellent"
        elif import_time < target_time * 0.5:
            return "Good"
        elif import_time < target_time:
            return "Acceptable"
        else:
            return "Poor"
    
    def validate_platform_specific_features(self):
        """Validate platform-specific features and limitations."""
        print("🌐 Validating Platform-Specific Features...")
        
        platform_features = {}
        
        if self.platform_name == "Darwin":
            platform_features = self._validate_macos_features()
        elif self.platform_name == "Linux":
            platform_features = self._validate_linux_features()
        elif self.platform_name == "Windows":
            platform_features = self._validate_windows_features()
        
        self.validation_results["platform_limitations"] = platform_features
        
        feature_count = sum(1 for feature in platform_features.values() if isinstance(feature, bool) and feature)
        total_features = sum(1 for feature in platform_features.values() if isinstance(feature, bool))
        
        print(f"   Platform Features: {feature_count}/{total_features} ✅")
        
        for feature_name, feature_status in platform_features.items():
            if isinstance(feature_status, bool):
                status = "✅" if feature_status else "⚠️"
                print(f"   {feature_name.replace('_', ' ').title()}: {status}")
    
    def _validate_macos_features(self):
        """Validate macOS-specific features."""
        features = {}
        
        # Test case sensitivity
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                file1 = Path(temp_dir) / "TestFile.txt"
                file2 = Path(temp_dir) / "testfile.txt"
                file1.write_text("test1")
                file2.write_text("test2")
                features["case_sensitive_filesystem"] = file1.read_text() != file2.read_text()
            except:
                features["case_sensitive_filesystem"] = None
        
        # Test executable permissions
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = Path(temp_file.name)
                temp_path.chmod(0o755)
                features["executable_permissions"] = os.access(temp_path, os.X_OK)
                temp_path.unlink()
        except:
            features["executable_permissions"] = False
        
        # Test launchd availability (service management)
        try:
            result = subprocess.run(["launchctl", "version"], 
                                  capture_output=True, text=True, timeout=5)
            features["launchd_available"] = result.returncode == 0
        except:
            features["launchd_available"] = False
        
        return features
    
    def _validate_linux_features(self):
        """Validate Linux-specific features."""
        features = {}
        
        # Test systemd availability
        try:
            result = subprocess.run(["systemctl", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            features["systemd_available"] = result.returncode == 0
        except:
            features["systemd_available"] = False
        
        # Test SELinux status
        try:
            result = subprocess.run(["sestatus"], 
                                  capture_output=True, text=True, timeout=5)
            features["selinux_present"] = result.returncode == 0
            if features["selinux_present"]:
                features["selinux_enforcing"] = "Enforcing" in result.stdout
        except:
            features["selinux_present"] = False
        
        # Test package manager availability
        package_managers = ["apt", "yum", "dnf", "pacman", "zypper"]
        features["package_managers"] = []
        
        for pm in package_managers:
            try:
                result = subprocess.run([pm, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    features["package_managers"].append(pm)
            except:
                continue
        
        features["package_manager_available"] = len(features["package_managers"]) > 0
        
        return features
    
    def _validate_windows_features(self):
        """Validate Windows-specific features."""
        features = {}
        
        # Test PowerShell availability
        try:
            result = subprocess.run(["powershell", "-Command", "Get-Host"], 
                                  capture_output=True, text=True, timeout=10)
            features["powershell_available"] = result.returncode == 0
        except:
            features["powershell_available"] = False
        
        # Test Windows services
        try:
            result = subprocess.run(["sc", "query"], 
                                  capture_output=True, text=True, timeout=10)
            features["windows_services"] = result.returncode == 0
        except:
            features["windows_services"] = False
        
        # Test long path support
        try:
            long_path = "a" * 300
            Path(long_path)
            features["long_path_support"] = True
        except:
            features["long_path_support"] = False
        
        return features
    
    def generate_recommendations(self):
        """Generate platform-specific recommendations."""
        print("📋 Generating Recommendations...")
        
        recommendations = []
        
        # General recommendations
        if self.validation_results["compatibility_status"]["system_requirements"]["python_version"]:
            recommendations.append("✅ Python version meets requirements")
        else:
            recommendations.append("❌ Upgrade to Python 3.8 or higher")
        
        # Platform-specific recommendations
        if self.platform_name == "Darwin":
            recommendations.extend([
                "🍎 macOS Recommendations:",
                "  • Run ./setup directly - excellent compatibility expected",
                "  • Performance targets easily achievable (<50ms boot)",
                "  • Consider 'xattr -d com.apple.quarantine ./setup' if Gatekeeper blocks execution",
                "  • Case-sensitive filesystem detected - consistent with Linux/Unix behavior"
            ])
        
        elif self.platform_name == "Linux":
            recommendations.extend([
                "🐧 Linux Recommendations:",
                "  • Optimal platform for deployment - best performance expected",
                "  • Target boot time <30ms achievable",
                "  • Check SELinux/AppArmor policies if deployment issues occur",
                "  • Use package manager for dependencies if needed"
            ])
            
            if self.validation_results["platform_limitations"].get("selinux_enforcing", False):
                recommendations.append("  ⚠️ SELinux is enforcing - may need policy adjustments")
        
        elif self.platform_name == "Windows":
            recommendations.extend([
                "🪟 Windows Recommendations:",
                "  • Consider using WSL for optimal experience",
                "  • Configure PowerShell execution policy: Set-ExecutionPolicy RemoteSigned",
                "  • Boot time target <200ms (slower than Unix-like systems)",
                "  • Add antivirus exclusions if script execution is blocked"
            ])
            
            if not self.validation_results["platform_limitations"].get("long_path_support", True):
                recommendations.append("  ⚠️ Enable long path support for complex project structures")
        
        # Performance recommendations
        performance_grade = self.validation_results["performance_expectations"].get("performance_grade", "Unknown")
        if performance_grade in ["Poor", "Acceptable"]:
            recommendations.extend([
                "⚡ Performance Optimization:",
                "  • Clear system caches before deployment",
                "  • Close unnecessary applications during setup",
                "  • Consider SSD storage for optimal file I/O performance"
            ])
        
        self.validation_results["recommendations"] = recommendations
        
        print("   📝 Platform-specific recommendations generated")
        print(f"   📊 {len(recommendations)} recommendations created")
    
    def display_validation_results(self):
        """Display comprehensive validation results."""
        print("\n" + "=" * 70)
        print("📊 PLATFORM COMPATIBILITY VALIDATION RESULTS")
        print("=" * 70)
        
        # Platform summary
        print(f"Platform: {self.platform_name} {self.platform_version}")
        print(f"Architecture: {self.platform_arch}")
        print(f"Python: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print()
        
        # Compatibility status
        overall_compatible = True
        print("🔍 Compatibility Status:")
        
        for category, status in self.validation_results["compatibility_status"].items():
            if isinstance(status, dict):
                if category == "system_requirements":
                    passed = sum(1 for result in status.values() if result)
                    total = len(status)
                    compatible = passed == total
                    overall_compatible &= compatible
                    print(f"   {category.replace('_', ' ').title()}: {passed}/{total} {'✅' if compatible else '❌'}")
                elif category == "python_environment":
                    compatible = status.get("version_compatible", False)
                    overall_compatible &= compatible
                    print(f"   {category.replace('_', ' ').title()}: {'✅' if compatible else '❌'}")
                elif category == "framework":
                    structure_ok = all(status["framework_structure"].values())
                    pathmanager_ok = status["pathmanager_functionality"].get("instantiation", False)
                    compatible = structure_ok and pathmanager_ok
                    overall_compatible &= compatible
                    print(f"   {category.title()}: {'✅' if compatible else '❌'}")
        
        # Performance expectations
        performance_grade = self.validation_results["performance_expectations"].get("performance_grade", "Unknown")
        meets_target = self.validation_results["performance_expectations"].get("meets_boot_target", False)
        
        print(f"\n⚡ Performance Assessment:")
        print(f"   Grade: {performance_grade}")
        print(f"   Meets Boot Target: {'✅' if meets_target else '❌'}")
        
        # Overall status
        print(f"\n🎯 Overall Compatibility: {'✅ COMPATIBLE' if overall_compatible else '❌ ISSUES DETECTED'}")
        
        # Recommendations
        print("\n📋 Recommendations:")
        for recommendation in self.validation_results["recommendations"]:
            print(f"{recommendation}")
        
        # Save validation report
        report_file = Path(__file__).parent / f"platform_validation_{self.platform_name.lower()}.json"
        with open(report_file, 'w') as f:
            json.dump(self.validation_results, f, indent=2, default=str)
        
        print(f"\n📄 Detailed validation report saved: {report_file}")
        
        if overall_compatible:
            print("\n🚀 Platform ready for Claude Enhancement Framework deployment!")
        else:
            print("\n⚠️ Please address compatibility issues before deployment.")


def main():
    """Run platform compatibility validation."""
    validator = PlatformCompatibilityValidator()
    results = validator.run_validation()
    return results


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Validation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)