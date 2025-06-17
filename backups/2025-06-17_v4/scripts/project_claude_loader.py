#!/usr/bin/env python3
"""
Automatic Project CLAUDE.md Loading and Parsing System
Implements Section 5 procedures exactly as documented in CLAUDE.md

Created for: Christian
Following: Section 5 - PROJECT HIERARCHY AND CONTEXT MANAGEMENT SYSTEM
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ProjectCLAUDELoader:
    """
    Implements project hierarchy rules and automatic CLAUDE.md loading
    Following documented procedures in Section 5
    """
    
    def __init__(self, start_directory: str = "."):
        self.start_directory = Path(start_directory).resolve()
        self.project_root = None
        self.project_claude_path = None
        self.project_config = {}
        self.validation_results = {}
        self.pattern_library = {}
        
    def find_project_root(self) -> Optional[str]:
        """
        Step 5.1.2: Project Root Detection Function
        Implements the exact bash function from CLAUDE.md
        """
        current_dir = self.start_directory
        max_depth = 20
        depth = 0
        
        print("🔍 Searching for project root...")
        
        # Search up directory tree for project markers
        while str(current_dir) != "/" and depth < max_depth:
            print(f"   Checking: {current_dir}")
            
            # Primary markers (highest confidence)
            claude_md_path = current_dir / "CLAUDE.md"
            if claude_md_path.exists():
                print(f"✓ Found CLAUDE.md at: {current_dir}")
                self.project_root = str(current_dir)
                self.project_claude_path = str(claude_md_path)
                return str(current_dir)
            
            # Secondary markers with Claude memory structure
            memory_dir = current_dir / "memory"
            learning_archive = memory_dir / "learning_archive.md"
            if memory_dir.exists() and learning_archive.exists():
                print(f"✓ Found memory structure at: {current_dir}")
                self.project_root = str(current_dir)
                return str(current_dir)
            
            # Tertiary markers - common project indicators with Claude structure
            has_package_json = (current_dir / "package.json").exists()
            has_requirements = (current_dir / "requirements.txt").exists()
            has_git = (current_dir / ".git").exists()
            
            if has_package_json or has_requirements or has_git:
                # Verify it also has Claude learning structure
                session_continuity = current_dir / "SESSION_CONTINUITY.md"
                if memory_dir.exists() or session_continuity.exists():
                    print(f"✓ Found project indicators with Claude structure at: {current_dir}")
                    self.project_root = str(current_dir)
                    return str(current_dir)
            
            # Move up one directory
            current_dir = current_dir.parent
            depth += 1
        
        # No project root found - use current directory
        print(f"ℹ️ No project root found - using current directory: {self.start_directory}")
        self.project_root = str(self.start_directory)
        return str(self.start_directory)
    
    def execute_project_discovery(self) -> Dict:
        """
        Step 5.1.3: Project Discovery Protocol Implementation
        Implements the exact discovery protocol from CLAUDE.md
        """
        print("=== Project Discovery Scan ===")
        print("User: Christian")
        print("")
        
        # Detect project root using documented function
        project_root = self.find_project_root()
        print(f"📁 Project root detected: {project_root}")
        
        discovery_results = {
            "project_root": project_root,
            "claude_md_found": False,
            "project_type": [],
            "configuration_files": [],
            "project_structure": [],
            "git_info": {}
        }
        
        # Check for project CLAUDE.md in project root
        print("Checking for project CLAUDE.md…")
        claude_md_path = Path(project_root) / "CLAUDE.md"
        
        if claude_md_path.exists():
            print("✓ Project CLAUDE.md found - will follow project rules")
            print("  - Project patterns available")
            print("  - Project testing protocol active")
            discovery_results["claude_md_found"] = True
            self.project_claude_path = str(claude_md_path)
        else:
            print("✗ No project CLAUDE.md - using global defaults")
            discovery_results["claude_md_found"] = False
        
        # Detect project type using project root
        print("")
        print("Detecting project type:")
        
        project_root_path = Path(project_root)
        
        # Check for Python project
        requirements_txt = project_root_path / "requirements.txt"
        if requirements_txt.exists():
            print("✓ Python project detected")
            discovery_results["project_type"].append("Python")
            discovery_results["configuration_files"].append(str(requirements_txt))
        
        # Check for Node.js project
        package_json = project_root_path / "package.json"
        if package_json.exists():
            print("✓ Node.js project detected")
            discovery_results["project_type"].append("Node.js")
            discovery_results["configuration_files"].append(str(package_json))
        
        # Check for other project types
        cargo_toml = project_root_path / "Cargo.toml"
        if cargo_toml.exists():
            print("✓ Rust project detected")
            discovery_results["project_type"].append("Rust")
            discovery_results["configuration_files"].append(str(cargo_toml))
        
        go_mod = project_root_path / "go.mod"
        if go_mod.exists():
            print("✓ Go project detected")
            discovery_results["project_type"].append("Go")
            discovery_results["configuration_files"].append(str(go_mod))
        
        composer_json = project_root_path / "composer.json"
        if composer_json.exists():
            print("✓ PHP project detected")
            discovery_results["project_type"].append("PHP")
            discovery_results["configuration_files"].append(str(composer_json))
        
        gemfile = project_root_path / "Gemfile"
        if gemfile.exists():
            print("✓ Ruby project detected")
            discovery_results["project_type"].append("Ruby")
            discovery_results["configuration_files"].append(str(gemfile))
        
        # Check for key configuration files
        print("")
        print("Configuration files:")
        
        env_file = project_root_path / ".env"
        if env_file.exists():
            print("✓ .env (Environment config present - DO NOT DISPLAY CONTENTS)")
            discovery_results["configuration_files"].append(".env")
        
        dockerfile = project_root_path / "Dockerfile"
        if dockerfile.exists():
            print("✓ Dockerfile (Docker configuration)")
            discovery_results["configuration_files"].append("Dockerfile")
        
        docker_compose = project_root_path / "docker-compose.yml"
        if docker_compose.exists():
            print("✓ docker-compose.yml (Docker Compose setup)")
            discovery_results["configuration_files"].append("docker-compose.yml")
        
        # Check project structure (first 20 files)
        print("")
        print("Project structure:")
        
        code_extensions = [".py", ".js", ".ts", ".jsx", ".tsx"]
        code_files = []
        
        for ext in code_extensions:
            files = list(project_root_path.rglob(f"*{ext}"))
            code_files.extend(files[:20])  # Limit to first 20 per extension
        
        for file_path in code_files[:20]:  # Overall limit of 20 files
            relative_path = file_path.relative_to(project_root_path)
            print(f"  {relative_path}")
            discovery_results["project_structure"].append(str(relative_path))
        
        # Check git status
        git_dir = project_root_path / ".git"
        if git_dir.exists():
            print("")
            print("Git repository detected:")
            discovery_results["git_info"]["is_git_repo"] = True
            
            # Try to get git status
            try:
                import subprocess
                os.chdir(project_root)
                
                # Get git status
                result = subprocess.run(['git', 'status', '--short'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    status_lines = result.stdout.strip().split('\n')
                    for line in status_lines:
                        if line.strip():
                            print(f"  {line}")
                    discovery_results["git_info"]["status"] = status_lines
                
                # Get current branch
                result = subprocess.run(['git', 'branch', '--show-current'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    branch = result.stdout.strip()
                    print(f"Current branch: {branch}")
                    discovery_results["git_info"]["current_branch"] = branch
                    
            except Exception as e:
                print(f"Git status unavailable: {e}")
        
        # Create project context if needed
        project_context_path = project_root_path / ".project_context"
        if not project_context_path.exists():
            print("")
            print("Creating initial project context…")
            
            context_content = f"""# Project Context - {Path().cwd().name}
User: Christian
Type: {', '.join(discovery_results['project_type']) if discovery_results['project_type'] else '[To be determined]'}
Main Language: {discovery_results['project_type'][0] if discovery_results['project_type'] else '[Inferred from file extensions]'}
Dependencies: [Listed from package files]
"""
            
            with open(project_context_path, 'w') as f:
                f.write(context_content)
        
        print("")
        return discovery_results
    
    def validate_project_configuration(self) -> Dict:
        """
        Step 5.2: Validate Project Configuration Files
        Implements comprehensive validation as documented
        """
        if not self.project_claude_path:
            return {"valid": True, "message": "No project CLAUDE.md to validate"}
        
        print("🔍 Validating project CLAUDE.md...")
        validation_results = {
            "valid": True,
            "issues": [],
            "warnings": [],
            "file_readable": False,
            "markdown_valid": False,
            "structure_valid": False,
            "security_safe": False
        }
        
        try:
            # Step 5.2.1: Verify File Integrity
            claude_path = Path(self.project_claude_path)
            
            # Check if file is readable
            with open(claude_path, 'r', encoding='utf-8') as f:
                content = f.read()
                validation_results["file_readable"] = True
                print("✓ File is readable")
            
            # Check for basic markdown structure
            if content.strip():
                validation_results["markdown_valid"] = True
                print("✓ File contains content")
                
                # Basic markdown structure check
                if re.search(r'^#\s+', content, re.MULTILINE):
                    print("✓ Contains markdown headers")
                else:
                    validation_results["warnings"].append("No markdown headers found")
            
            # Check for structural integrity
            required_sections = [
                "BINDING ENFORCEMENT PROTOCOL",
                "CRITICAL BINDING STATEMENTS",
                "ENFORCEMENT MECHANISMS"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if not missing_sections:
                validation_results["structure_valid"] = True
                print("✓ Required sections present")
            else:
                validation_results["issues"].extend(missing_sections)
                print(f"⚠️ Missing sections: {', '.join(missing_sections)}")
            
            # Basic security check - look for obviously dangerous patterns
            dangerous_patterns = [
                r'rm\s+-rf\s+/',
                r'sudo\s+rm',
                r'eval\s*\(',
                r'exec\s*\(',
                r'__import__\s*\(',
                r'subprocess\.call\s*\([^)]*shell\s*=\s*True'
            ]
            
            security_issues = []
            for pattern in dangerous_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    security_issues.append(f"Potentially dangerous pattern: {pattern}")
            
            if not security_issues:
                validation_results["security_safe"] = True
                print("✓ No obvious security issues detected")
            else:
                validation_results["issues"].extend(security_issues)
                validation_results["valid"] = False
                print(f"🚨 Security concerns: {len(security_issues)} issues found")
            
        except Exception as e:
            validation_results["valid"] = False
            validation_results["issues"].append(f"Validation error: {str(e)}")
            print(f"❌ Validation failed: {e}")
        
        self.validation_results = validation_results
        return validation_results
    
    def parse_project_configuration(self) -> Dict:
        """
        Step 5.3: Apply Project-Specific Configurations
        Parse and overlay project rules on global defaults
        """
        if not self.project_claude_path or not self.validation_results.get("valid", False):
            print("ℹ️ No valid project configuration to parse")
            return {}
        
        print("⚙️ Parsing project-specific configurations...")
        
        try:
            with open(self.project_claude_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            config = {
                "testing_protocol": self._extract_testing_protocol(content),
                "parallel_execution": self._extract_parallel_config(content),
                "pattern_library": self._extract_pattern_config(content),
                "coding_standards": self._extract_coding_standards(content),
                "project_specific_rules": self._extract_project_rules(content)
            }
            
            self.project_config = config
            print("✓ Project configuration parsed successfully")
            return config
            
        except Exception as e:
            print(f"❌ Failed to parse project configuration: {e}")
            return {}
    
    def _extract_testing_protocol(self, content: str) -> Dict:
        """Extract testing protocol from CLAUDE.md content"""
        testing_config = {}
        
        # Look for testing decision protocol
        if "TESTING DECISION PROTOCOL" in content:
            testing_config["protocol_defined"] = True
            # Extract 7-step protocol if present
            if "STEP 1:" in content and "STEP 7:" in content:
                testing_config["seven_step_protocol"] = True
        
        # Look for TDD requirements
        if "test-first development" in content.lower() or "tdd" in content.lower():
            testing_config["tdd_preferred"] = True
        
        return testing_config
    
    def _extract_parallel_config(self, content: str) -> Dict:
        """Extract parallel execution configuration"""
        parallel_config = {}
        
        # Look for agent configurations
        agent_patterns = [
            r"(\d+)\s*agents?",
            r"Deploy\s+(\d+)",
            r"(\d+)-agent"
        ]
        
        for pattern in agent_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                agent_counts = [int(m) for m in matches if m.isdigit()]
                if agent_counts:
                    parallel_config["default_agents"] = max(agent_counts)
                    break
        
        # Look for execution mode preferences
        if "parallel" in content.lower():
            parallel_config["parallel_preferred"] = True
        if "sequential" in content.lower():
            parallel_config["sequential_required"] = True
        
        return parallel_config
    
    def _extract_pattern_config(self, content: str) -> Dict:
        """Extract pattern library configuration"""
        pattern_config = {}
        
        # Look for pattern directory references
        if "patterns/" in content:
            pattern_config["pattern_dir"] = "patterns/"
        
        # Look for pattern application rules
        if "pattern" in content.lower() and "before" in content.lower():
            pattern_config["check_patterns_first"] = True
        
        return pattern_config
    
    def _extract_coding_standards(self, content: str) -> Dict:
        """Extract coding standards and directives"""
        standards = {}
        
        # Look for coding directives
        directive_matches = re.findall(r"Directive\s+(\d+)", content, re.IGNORECASE)
        if directive_matches:
            standards["directive_count"] = len(directive_matches)
        
        # Look for specific standards
        if "clean code" in content.lower():
            standards["clean_code_required"] = True
        
        if "test coverage" in content.lower():
            standards["test_coverage_required"] = True
        
        return standards
    
    def _extract_project_rules(self, content: str) -> List[str]:
        """Extract project-specific rules and requirements"""
        rules = []
        
        # Look for binding statements
        binding_section = re.search(
            r"CRITICAL BINDING STATEMENTS:(.*?)(?=###|$)", 
            content, 
            re.DOTALL | re.IGNORECASE
        )
        
        if binding_section:
            binding_text = binding_section.group(1)
            # Extract numbered rules
            rule_matches = re.findall(r"\d+\.\s*\*\*(.*?)\*\*", binding_text)
            rules.extend(rule_matches)
        
        return rules
    
    def load_pattern_library(self) -> Dict:
        """
        Step 5.4: Load Project Pattern Libraries
        Scan and index available patterns
        """
        if not self.project_root:
            return {}
        
        print("📚 Loading pattern library...")
        pattern_library = {}
        
        patterns_dir = Path(self.project_root) / "patterns"
        if not patterns_dir.exists():
            print("ℹ️ No patterns directory found")
            return {}
        
        # Step 5.4.1: Detect Pattern Files
        categories = ["bug_fixes", "generation", "refactoring", "architecture"]
        
        for category in categories:
            category_dir = patterns_dir / category
            if category_dir.exists():
                pattern_files = list(category_dir.glob("*.md"))
                if pattern_files:
                    print(f"✓ Found {len(pattern_files)} patterns in {category}/")
                    pattern_library[category] = [str(f) for f in pattern_files]
        
        # Skip fabric patterns - use on-demand loading instead
        fabric_dir = patterns_dir / "fabric"
        if fabric_dir.exists():
            print(f"⚠️ Skipping fabric patterns (use scripts/fabric_on_demand.sh for on-demand access)")
            # Do not load fabric patterns - they are available via scripts/fabric_on_demand.sh
        
        self.pattern_library = pattern_library
        return pattern_library
    
    def generate_loading_report(self) -> str:
        """Generate a comprehensive loading report"""
        report = f"""# Project CLAUDE.md Loading Report
Generated: {Path().cwd()}
User: Christian
Timestamp: {os.popen('date -u +%Y-%m-%dT%H:%M:%SZ').read().strip()}

## Project Discovery Results
- Project Root: {self.project_root}
- CLAUDE.md Found: {bool(self.project_claude_path)}
- Validation Status: {self.validation_results.get('valid', 'Not validated')}

## Configuration Loading
"""
        
        if self.project_config:
            report += "✓ Project configuration loaded successfully\n\n"
            report += "### Parsed Configuration:\n"
            for key, value in self.project_config.items():
                report += f"- {key}: {value}\n"
        else:
            report += "ℹ️ No project configuration loaded (using global defaults)\n"
        
        report += f"\n## Pattern Library Status\n"
        if self.pattern_library:
            report += "✓ Pattern library loaded\n"
            for category, patterns in self.pattern_library.items():
                report += f"- {category}: {len(patterns)} patterns\n"
        else:
            report += "ℹ️ No pattern library found\n"
        
        if self.validation_results:
            report += f"\n## Validation Details\n"
            if self.validation_results.get("issues"):
                report += "### Issues Found:\n"
                for issue in self.validation_results["issues"]:
                    report += f"- ❌ {issue}\n"
            
            if self.validation_results.get("warnings"):
                report += "### Warnings:\n"
                for warning in self.validation_results["warnings"]:
                    report += f"- ⚠️ {warning}\n"
        
        return report
    
    def execute_complete_loading_sequence(self) -> Dict:
        """
        Execute the complete project CLAUDE.md loading sequence
        Following all documented procedures in Section 5
        """
        print("🚀 Executing complete project CLAUDE.md loading sequence for Christian")
        print("Following Section 5: PROJECT HIERARCHY AND CONTEXT MANAGEMENT SYSTEM")
        print("=" * 80)
        
        results = {}
        
        # Step 5.1: Execute Project Context Discovery
        discovery_results = self.execute_project_discovery()
        results["discovery"] = discovery_results
        
        # Step 5.2: Validate Project Configuration Files
        validation_results = self.validate_project_configuration()
        results["validation"] = validation_results
        
        # Step 5.3: Apply Project-Specific Configurations
        if validation_results.get("valid", False):
            config_results = self.parse_project_configuration()
            results["configuration"] = config_results
        else:
            print("⚠️ Skipping configuration parsing due to validation issues")
            results["configuration"] = {}
        
        # Step 5.4: Load Project Pattern Libraries
        pattern_results = self.load_pattern_library()
        results["patterns"] = pattern_results
        
        # Generate comprehensive report
        loading_report = self.generate_loading_report()
        results["report"] = loading_report
        
        print("=" * 80)
        print("✅ Project CLAUDE.md loading sequence completed")
        print(f"📊 Results: {len(results)} components processed")
        
        return results

def main():
    """Main execution function for testing the loader"""
    loader = ProjectCLAUDELoader()
    results = loader.execute_complete_loading_sequence()
    
    # Save results to file
    results_file = Path("project_claude_loading_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to: {results_file}")
    
    # Save loading report
    report_file = Path("PROJECT_CLAUDE_LOADING_REPORT.md")
    with open(report_file, 'w') as f:
        f.write(results["report"])
    
    print(f"📋 Report saved to: {report_file}")

if __name__ == "__main__":
    main()