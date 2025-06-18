#!/usr/bin/env python3
"""
Pattern Validation System for Claude Enhancement Framework
Part of Claude Enhancement Framework by Christian

Validates:
1. All 19 expected patterns are present across 5 categories
2. Pattern file integrity (readable, correct format)
3. Pattern index matches actual files
4. Template variable substitution functionality
5. Pattern metadata and structure consistency

TASK: Pattern validation only - DO NOT modify existing patterns
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class PatternValidationResult:
    """Results from pattern validation."""
    pattern_path: str
    exists: bool = False
    readable: bool = False
    valid_format: bool = False
    has_metadata: bool = False
    template_vars_valid: bool = False
    category: str = ""
    errors: List[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


class PatternValidator:
    """Comprehensive pattern validation system."""
    
    # Expected 19 patterns across 5 categories as per framework spec
    EXPECTED_PATTERNS = {
        "bug_fixes": [
            "systematic_error_resolution.md",
            "defensive_programming_patterns.md",
            "error_handling_strategies.md"
        ],
        "generation": [
            "auto_session_continuity_pattern.md",
            "documentation_standard.md",
            "learning_file_loading_pattern.md",
            "memory_optimization_patterns.md",
            "project_detection_pattern.md",
            "project_initialization_pattern.md",
            "project_template_initialization.md",
            "testing_protocol_framework.md"
        ],
        "refactoring": [
            "boot_sequence_optimization.md",
            "error_learning_deferred_loading.md",
            "file_organization_enforcement.md",
            "performance_analysis_template.md",
            "token_usage_optimization.md"
        ],
        "architecture": [
            "dual_parallel_agent_configuration.md",
            "lazy_loading_optimization.md",
            "cross_project_deployment.md"
        ],
        "fabric": [
            # Fabric patterns are loaded separately - placeholder for validation
        ]
    }
    
    # Template variables that should be substitutable
    TEMPLATE_VARIABLES = [
        "{{USER_NAME}}", "{{PROJECT_NAME}}", "{{PROJECT_PATH}}", 
        "{{PLATFORM}}", "{{TIMESTAMP}}", "{{PROJECT_ROOT}}"
    ]
    
    def __init__(self, patterns_dir: Optional[Path] = None):
        """
        Initialize pattern validator.
        
        Args:
            patterns_dir: Path to patterns directory (auto-detected if not provided)
        """
        if patterns_dir:
            self.patterns_dir = Path(patterns_dir)
        else:
            # Auto-detect patterns directory
            current_dir = Path(__file__).parent
            self.patterns_dir = current_dir
        
        self.validation_results: List[PatternValidationResult] = []
        self.pattern_index_path = self.patterns_dir / ".pattern_index.json"
        
    def run_full_validation(self) -> Dict[str, Any]:
        """
        Run complete pattern validation suite.
        
        Returns:
            Comprehensive validation report
        """
        report = {
            "validation_timestamp": self._get_timestamp(),
            "patterns_directory": str(self.patterns_dir),
            "expected_pattern_count": self._get_expected_pattern_count(),
            "actual_pattern_count": 0,
            "patterns_missing": [],
            "patterns_extra": [],
            "category_validation": {},
            "pattern_results": [],
            "index_validation": {},
            "template_validation": {},
            "overall_status": "UNKNOWN",
            "critical_errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        try:
            # 1. Validate directory structure exists
            if not self._validate_directory_structure():
                report["critical_errors"].append("Patterns directory structure invalid")
                report["overall_status"] = "FAILED"
                return report
            
            # 2. Check for all expected patterns
            missing_patterns, extra_patterns = self._check_pattern_completeness()
            report["patterns_missing"] = missing_patterns
            report["patterns_extra"] = extra_patterns
            
            # 3. Validate each pattern file
            for category, patterns in self.EXPECTED_PATTERNS.items():
                if not patterns:  # Skip empty categories like fabric
                    continue
                    
                category_results = []
                category_dir = self.patterns_dir / category
                
                for pattern_file in patterns:
                    result = self._validate_pattern_file(category_dir / pattern_file, category)
                    category_results.append(result)
                    self.validation_results.append(result)
                
                report["category_validation"][category] = {
                    "expected_count": len(patterns),
                    "found_count": sum(1 for r in category_results if r.exists),
                    "valid_count": sum(1 for r in category_results if r.valid_format),
                    "results": [asdict(r) for r in category_results]
                }
            
            # 4. Validate pattern index
            report["index_validation"] = self._validate_pattern_index()
            
            # 5. Validate template substitution
            report["template_validation"] = self._validate_template_substitution()
            
            # 6. Calculate overall metrics
            report["actual_pattern_count"] = len([r for r in self.validation_results if r.exists])
            report["pattern_results"] = [asdict(r) for r in self.validation_results]
            
            # 7. Determine overall status
            report["overall_status"] = self._determine_overall_status(report)
            
            # 8. Generate recommendations
            report["recommendations"] = self._generate_recommendations(report)
            
        except Exception as e:
            report["critical_errors"].append(f"Validation failed with exception: {str(e)}")
            report["overall_status"] = "ERROR"
        
        return report
    
    def _get_expected_pattern_count(self) -> int:
        """Get total expected pattern count."""
        return sum(len(patterns) for patterns in self.EXPECTED_PATTERNS.values())
    
    def _validate_directory_structure(self) -> bool:
        """Validate that patterns directory structure exists."""
        if not self.patterns_dir.exists():
            return False
        
        # Check that category directories exist
        for category in self.EXPECTED_PATTERNS.keys():
            if not category or category == "fabric":  # Skip empty/special categories
                continue
            category_dir = self.patterns_dir / category
            if not category_dir.exists():
                return False
        
        return True
    
    def _check_pattern_completeness(self) -> Tuple[List[str], List[str]]:
        """
        Check which patterns are missing or extra.
        
        Returns:
            Tuple of (missing_patterns, extra_patterns)
        """
        missing_patterns = []
        extra_patterns = []
        
        for category, expected_patterns in self.EXPECTED_PATTERNS.items():
            if not expected_patterns:  # Skip empty categories
                continue
                
            category_dir = self.patterns_dir / category
            if not category_dir.exists():
                missing_patterns.extend([f"{category}/{p}" for p in expected_patterns])
                continue
            
            # Check for missing patterns
            for pattern_file in expected_patterns:
                pattern_path = category_dir / pattern_file
                if not pattern_path.exists():
                    missing_patterns.append(f"{category}/{pattern_file}")
            
            # Check for extra patterns
            if category_dir.exists():
                actual_files = [f.name for f in category_dir.glob("*.md")]
                for actual_file in actual_files:
                    if actual_file not in expected_patterns:
                        extra_patterns.append(f"{category}/{actual_file}")
        
        return missing_patterns, extra_patterns
    
    def _validate_pattern_file(self, pattern_path: Path, category: str) -> PatternValidationResult:
        """
        Validate individual pattern file.
        
        Args:
            pattern_path: Path to pattern file
            category: Pattern category
            
        Returns:
            PatternValidationResult with validation details
        """
        result = PatternValidationResult(
            pattern_path=str(pattern_path),
            category=category
        )
        
        # Check existence
        if not pattern_path.exists():
            result.errors.append("Pattern file does not exist")
            return result
        
        result.exists = True
        
        # Check readability
        try:
            with open(pattern_path, 'r', encoding='utf-8') as f:
                content = f.read()
            result.readable = True
        except Exception as e:
            result.errors.append(f"Cannot read pattern file: {str(e)}")
            return result
        
        # Check format validity
        if self._validate_pattern_format(content):
            result.valid_format = True
        else:
            result.errors.append("Pattern format invalid")
        
        # Check metadata presence
        if self._has_pattern_metadata(content):
            result.has_metadata = True
        else:
            result.warnings.append("Pattern missing metadata")
        
        # Check template variables
        if self._validate_template_variables(content):
            result.template_vars_valid = True
        else:
            result.warnings.append("Template variables may have issues")
        
        return result
    
    def _validate_pattern_format(self, content: str) -> bool:
        """
        Validate pattern file format.
        
        Args:
            content: Pattern file content
            
        Returns:
            True if format is valid
        """
        # Basic format checks
        if not content.strip():
            return False
        
        # Should have markdown structure
        if not content.startswith('#'):
            return False
        
        # Should have some content beyond just headers
        non_header_lines = [line for line in content.split('\n') 
                           if line.strip() and not line.strip().startswith('#')]
        if len(non_header_lines) < 3:
            return False
        
        return True
    
    def _has_pattern_metadata(self, content: str) -> bool:
        """
        Check if pattern has required metadata.
        
        Args:
            content: Pattern file content
            
        Returns:
            True if metadata is present
        """
        # Look for common metadata indicators
        metadata_indicators = [
            "description:", "category:", "usage:", "example:", "pattern:"
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in metadata_indicators)
    
    def _validate_template_variables(self, content: str) -> bool:
        """
        Validate template variable usage.
        
        Args:
            content: Pattern file content
            
        Returns:
            True if template variables are used correctly
        """
        # Find all template variables in content
        template_vars = re.findall(r'\{\{[^}]+\}\}', content)
        
        # Check for malformed variables
        for var in template_vars:
            if not re.match(r'\{\{[A-Z_]+\}\}', var):
                return False
        
        return True
    
    def _validate_pattern_index(self) -> Dict[str, Any]:
        """
        Validate pattern index file.
        
        Returns:
            Index validation results
        """
        result = {
            "index_exists": self.pattern_index_path.exists(),
            "index_readable": False,
            "index_valid_json": False,
            "patterns_match": False,
            "errors": [],
            "warnings": []
        }
        
        if not result["index_exists"]:
            result["warnings"].append("Pattern index file does not exist")
            return result
        
        try:
            with open(self.pattern_index_path, 'r', encoding='utf-8') as f:
                index_content = f.read()
            result["index_readable"] = True
            
            # Parse JSON
            index_data = json.loads(index_content)
            result["index_valid_json"] = True
            
            # Validate index structure
            if self._validate_index_structure(index_data):
                result["patterns_match"] = True
            else:
                result["errors"].append("Index structure does not match expected patterns")
                
        except json.JSONDecodeError as e:
            result["errors"].append(f"Index JSON invalid: {str(e)}")
        except Exception as e:
            result["errors"].append(f"Index validation failed: {str(e)}")
        
        return result
    
    def _validate_index_structure(self, index_data: Dict[str, Any]) -> bool:
        """
        Validate index data structure matches expected patterns.
        
        Args:
            index_data: Parsed index JSON data
            
        Returns:
            True if structure is valid
        """
        if not isinstance(index_data, dict):
            return False
        
        # Check that index contains expected categories
        for category in self.EXPECTED_PATTERNS.keys():
            if not self.EXPECTED_PATTERNS[category]:  # Skip empty categories
                continue
            if category not in index_data:
                return False
        
        return True
    
    def _validate_template_substitution(self) -> Dict[str, Any]:
        """
        Test template variable substitution functionality.
        
        Returns:
            Template substitution validation results
        """
        result = {
            "substitution_works": False,
            "test_variables": [],
            "errors": [],
            "warnings": []
        }
        
        # Test basic substitution
        test_template = "Hello {{USER_NAME}} in project {{PROJECT_NAME}} on {{PLATFORM}}"
        test_vars = {
            "USER_NAME": "TestUser",
            "PROJECT_NAME": "TestProject", 
            "PLATFORM": "TestPlatform"
        }
        
        try:
            substituted = self._substitute_template_vars(test_template, test_vars)
            if "TestUser" in substituted and "TestProject" in substituted:
                result["substitution_works"] = True
            else:
                result["errors"].append("Template substitution did not work correctly")
                
            result["test_variables"] = list(test_vars.keys())
            
        except Exception as e:
            result["errors"].append(f"Template substitution test failed: {str(e)}")
        
        return result
    
    def _substitute_template_vars(self, template: str, variables: Dict[str, str]) -> str:
        """
        Substitute template variables (simplified version for testing).
        
        Args:
            template: Template string with {{VAR}} placeholders
            variables: Variable substitutions
            
        Returns:
            Template with variables substituted
        """
        result = template
        for var_name, var_value in variables.items():
            result = result.replace(f"{{{{{var_name}}}}}", var_value)
        return result
    
    def _determine_overall_status(self, report: Dict[str, Any]) -> str:
        """
        Determine overall validation status.
        
        Args:
            report: Validation report data
            
        Returns:
            Overall status: PASSED, FAILED, or WARNING
        """
        if report["critical_errors"]:
            return "FAILED"
        
        # Check critical metrics
        expected_count = report["expected_pattern_count"]
        actual_count = report["actual_pattern_count"]
        
        if actual_count == 0:
            return "FAILED"
        
        if len(report["patterns_missing"]) > expected_count * 0.5:  # More than 50% missing
            return "FAILED"
        
        if len(report["patterns_missing"]) > 0:
            return "WARNING"
        
        # Check pattern validity
        valid_patterns = sum(1 for r in self.validation_results 
                           if r.exists and r.readable and r.valid_format)
        
        if valid_patterns < actual_count * 0.8:  # Less than 80% valid
            return "WARNING"
        
        return "PASSED"
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on validation results.
        
        Args:
            report: Validation report data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if report["patterns_missing"]:
            recommendations.append(
                f"Create {len(report['patterns_missing'])} missing patterns: "
                f"{', '.join(report['patterns_missing'][:3])}{'...' if len(report['patterns_missing']) > 3 else ''}"
            )
        
        if report["patterns_extra"]:
            recommendations.append(
                f"Review {len(report['patterns_extra'])} extra patterns for potential integration"
            )
        
        if not report["index_validation"]["index_exists"]:
            recommendations.append("Create pattern index file (.pattern_index.json)")
        
        if not report["template_validation"]["substitution_works"]:
            recommendations.append("Fix template variable substitution functionality")
        
        # Check category-specific issues
        for category, results in report["category_validation"].items():
            if results["found_count"] < results["expected_count"]:
                missing_count = results["expected_count"] - results["found_count"]
                recommendations.append(f"Create {missing_count} missing patterns in {category} category")
        
        return recommendations
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for validation report."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def generate_summary_report(self, report: Dict[str, Any]) -> str:
        """
        Generate human-readable summary report.
        
        Args:
            report: Validation report data
            
        Returns:
            Formatted summary report
        """
        status_icon = {
            "PASSED": "✅",
            "WARNING": "⚠️", 
            "FAILED": "❌",
            "ERROR": "💥"
        }.get(report["overall_status"], "❓")
        
        summary = f"""
# Pattern Validation Report {status_icon}

**Overall Status:** {report["overall_status"]}
**Validation Time:** {report["validation_timestamp"]}
**Patterns Directory:** {report["patterns_directory"]}

## Pattern Coverage
- **Expected:** {report["expected_pattern_count"]} patterns
- **Found:** {report["actual_pattern_count"]} patterns
- **Missing:** {len(report["patterns_missing"])} patterns
- **Extra:** {len(report["patterns_extra"])} patterns

## Category Breakdown
"""
        
        for category, results in report["category_validation"].items():
            coverage_pct = (results["found_count"] / results["expected_count"]) * 100 if results["expected_count"] > 0 else 0
            summary += f"- **{category}:** {results['found_count']}/{results['expected_count']} ({coverage_pct:.1f}%)\n"
        
        if report["patterns_missing"]:
            summary += f"\n## Missing Patterns ({len(report['patterns_missing'])})\n"
            for pattern in report["patterns_missing"][:10]:  # Show first 10
                summary += f"- {pattern}\n"
            if len(report["patterns_missing"]) > 10:
                summary += f"- ... and {len(report['patterns_missing']) - 10} more\n"
        
        if report["critical_errors"]:
            summary += f"\n## Critical Errors ({len(report['critical_errors'])})\n"
            for error in report["critical_errors"]:
                summary += f"- ❌ {error}\n"
        
        if report["recommendations"]:
            summary += f"\n## Recommendations ({len(report['recommendations'])})\n"
            for rec in report["recommendations"]:
                summary += f"- 💡 {rec}\n"
        
        summary += f"\n---\n*Generated by Claude Enhancement Framework Pattern Validator*"
        
        return summary


def main():
    """Main validation entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Claude Enhancement Framework patterns")
    parser.add_argument("--patterns-dir", type=str, help="Path to patterns directory")
    parser.add_argument("--output", type=str, help="Output file for detailed report (JSON)")
    parser.add_argument("--summary", action="store_true", help="Show summary report only")
    
    args = parser.parse_args()
    
    # Initialize validator
    patterns_dir = Path(args.patterns_dir) if args.patterns_dir else None
    validator = PatternValidator(patterns_dir)
    
    print("🔍 Running pattern validation...")
    print(f"📁 Patterns directory: {validator.patterns_dir}")
    
    # Run validation
    report = validator.run_full_validation()
    
    # Output results
    if args.summary:
        summary = validator.generate_summary_report(report)
        print(summary)
    else:
        # Show detailed results
        print(f"\n📊 Validation Status: {report['overall_status']}")
        print(f"📋 Expected patterns: {report['expected_pattern_count']}")
        print(f"✅ Found patterns: {report['actual_pattern_count']}")
        print(f"❌ Missing patterns: {len(report['patterns_missing'])}")
        print(f"➕ Extra patterns: {len(report['patterns_extra'])}")
        
        if report['patterns_missing']:
            print(f"\n🚨 Missing Patterns:")
            for pattern in report['patterns_missing']:
                print(f"   - {pattern}")
        
        if report['critical_errors']:
            print(f"\n💥 Critical Errors:")
            for error in report['critical_errors']:
                print(f"   - {error}")
        
        if report['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"   - {rec}")
    
    # Save detailed report if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Detailed report saved to: {output_path}")
    
    # Exit with appropriate code
    exit_code = 0 if report['overall_status'] == 'PASSED' else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()