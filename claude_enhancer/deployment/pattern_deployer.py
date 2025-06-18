"""
PatternDeployer: Pattern deployment system for Claude Enhancement Framework
Part of Claude Enhancement Framework by Christian

Provides pattern deployment capabilities:
- Template variable substitution during deployment
- Selective pattern deployment (by category or individual)
- Pattern integrity preservation
- Integration with ClaudeEnhancer API
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Set
from ..core.path_manager import PathManager


class PatternDeployer:
    """
    Handles deployment of patterns from framework to target projects.
    
    Features:
    - Template variable substitution
    - Selective deployment by category/pattern
    - Pattern integrity preservation
    - Deployment validation and rollback
    """
    
    def __init__(self, path_manager: PathManager):
        """
        Initialize PatternDeployer.
        
        Args:
            path_manager: PathManager instance for path resolution
        """
        self.path_manager = path_manager
        self.framework_patterns_dir = self._get_framework_patterns_dir()
        
        # Pattern categories supported by framework
        self.pattern_categories = {
            "architecture": "Architectural patterns and system design",
            "refactoring": "Code refactoring and optimization patterns", 
            "bug_fixes": "Bug resolution and prevention patterns",
            "generation": "Code generation and template patterns",
            "testing": "Testing strategies and patterns"
        }
        
        # Template variables that should NOT be substituted in pattern content
        self.protected_variables = {
            "{{USER_INPUT}}", "{{PATTERN_CONTENT}}", "{{CODE_BLOCK}}",
            "{{IMPLEMENTATION}}", "{{CUSTOM_LOGIC}}", "{{PROJECT_SPECIFIC}}"
        }
    
    def _get_framework_patterns_dir(self) -> Path:
        """Get framework patterns directory."""
        current_dir = Path(__file__).parent.parent
        patterns_dir = current_dir / "patterns"
        return patterns_dir
    
    def deploy_patterns(self, target_project: Union[str, Path], 
                       categories: Optional[List[str]] = None,
                       specific_patterns: Optional[List[str]] = None,
                       force: bool = False) -> Dict[str, Any]:
        """
        Deploy patterns to target project.
        
        Args:
            target_project: Target project directory path
            categories: List of pattern categories to deploy (defaults to all)
            specific_patterns: List of specific pattern files to deploy
            force: Force overwrite existing patterns
            
        Returns:
            Deployment results dictionary
        """
        results = {
            "success": False,
            "target_project": str(target_project),
            "patterns_deployed": [],
            "patterns_updated": [],
            "patterns_skipped": [],
            "directories_created": [],
            "errors": [],
            "deployment_summary": {}
        }
        
        try:
            target_path = Path(target_project).resolve()
            
            # Validate target project
            if not target_path.exists():
                results["errors"].append(f"Target project does not exist: {target_path}")
                return results
            
            # Create patterns directory in target project
            target_patterns_dir = target_path / "patterns"
            if not target_patterns_dir.exists():
                target_patterns_dir.mkdir(parents=True, exist_ok=True)
                results["directories_created"].append(str(target_patterns_dir))
            
            # Determine patterns to deploy
            patterns_to_deploy = self._get_patterns_to_deploy(categories, specific_patterns)
            
            if not patterns_to_deploy:
                results["errors"].append("No patterns found matching deployment criteria")
                return results
            
            # Deploy each pattern
            for pattern_info in patterns_to_deploy:
                deploy_result = self._deploy_single_pattern(
                    pattern_info, target_patterns_dir, target_path, force
                )
                
                if deploy_result["success"]:
                    if deploy_result["action"] == "created":
                        results["patterns_deployed"].append(deploy_result["pattern_path"])
                    elif deploy_result["action"] == "updated":
                        results["patterns_updated"].append(deploy_result["pattern_path"])
                else:
                    if deploy_result["action"] == "skipped":
                        results["patterns_skipped"].append(deploy_result["pattern_path"])
                    else:
                        results["errors"].extend(deploy_result["errors"])
            
            # Create deployment summary
            results["deployment_summary"] = {
                "total_patterns": len(patterns_to_deploy),
                "deployed": len(results["patterns_deployed"]),
                "updated": len(results["patterns_updated"]),
                "skipped": len(results["patterns_skipped"]),
                "errors": len(results["errors"])
            }
            
            # Create pattern index
            self._create_pattern_index(target_patterns_dir, results)
            
            results["success"] = len(results["errors"]) == 0
            
        except Exception as e:
            results["errors"].append(f"Pattern deployment failed: {str(e)}")
        
        return results
    
    def _get_patterns_to_deploy(self, categories: Optional[List[str]] = None,
                               specific_patterns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get list of patterns to deploy based on criteria.
        
        Args:
            categories: Pattern categories to include
            specific_patterns: Specific pattern files to include
            
        Returns:
            List of pattern information dictionaries
        """
        patterns_to_deploy = []
        
        if not self.framework_patterns_dir.exists():
            return patterns_to_deploy
        
        # If specific patterns requested, find those
        if specific_patterns:
            for pattern_name in specific_patterns:
                pattern_file = self._find_pattern_file(pattern_name)
                if pattern_file:
                    patterns_to_deploy.append({
                        "source_path": pattern_file,
                        "category": pattern_file.parent.name,
                        "name": pattern_file.stem,
                        "relative_path": pattern_file.relative_to(self.framework_patterns_dir)
                    })
            return patterns_to_deploy
        
        # Otherwise, deploy by categories
        target_categories = categories or list(self.pattern_categories.keys())
        
        for category in target_categories:
            category_dir = self.framework_patterns_dir / category
            if category_dir.exists() and category_dir.is_dir():
                for pattern_file in category_dir.glob("*.md"):
                    patterns_to_deploy.append({
                        "source_path": pattern_file,
                        "category": category,
                        "name": pattern_file.stem,
                        "relative_path": pattern_file.relative_to(self.framework_patterns_dir)
                    })
        
        return patterns_to_deploy
    
    def _find_pattern_file(self, pattern_name: str) -> Optional[Path]:
        """Find pattern file by name across all categories."""
        if not self.framework_patterns_dir.exists():
            return None
            
        # Search all category directories
        for category_dir in self.framework_patterns_dir.iterdir():
            if category_dir.is_dir():
                pattern_file = category_dir / f"{pattern_name}.md"
                if pattern_file.exists():
                    return pattern_file
        
        return None
    
    def _deploy_single_pattern(self, pattern_info: Dict[str, Any], 
                              target_patterns_dir: Path,
                              target_project_path: Path, 
                              force: bool) -> Dict[str, Any]:
        """
        Deploy a single pattern to target project.
        
        Args:
            pattern_info: Pattern information dictionary
            target_patterns_dir: Target patterns directory
            target_project_path: Target project root path
            force: Force overwrite existing pattern
            
        Returns:
            Single pattern deployment result
        """
        result = {
            "success": False,
            "action": "none",
            "pattern_path": "",
            "errors": []
        }
        
        try:
            source_path = pattern_info["source_path"]
            relative_path = pattern_info["relative_path"]
            target_path = target_patterns_dir / relative_path
            
            result["pattern_path"] = str(relative_path)
            
            # Create category directory if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if not target_path.parent in [target_patterns_dir]:
                # Only log if we created a new category directory
                pass
            
            # Check if pattern already exists
            file_existed = target_path.exists()
            if file_existed and not force:
                result["action"] = "skipped"
                result["success"] = True
                return result
            
            # Read source pattern content
            with open(source_path, 'r', encoding='utf-8') as f:
                pattern_content = f.read()
            
            # Apply template substitution while preserving pattern integrity
            processed_content = self._process_pattern_content(
                pattern_content, target_project_path
            )
            
            # Write to target location
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            result["action"] = "updated" if file_existed else "created"
            result["success"] = True
            
        except Exception as e:
            result["errors"].append(f"Failed to deploy pattern {pattern_info['name']}: {str(e)}")
        
        return result
    
    def _process_pattern_content(self, content: str, target_project_path: Path) -> str:
        """
        Process pattern content with template substitution while preserving integrity.
        
        Args:
            content: Original pattern content
            target_project_path: Target project path for context
            
        Returns:
            Processed content with appropriate substitutions
        """
        # Extract project-specific variables
        project_name = target_project_path.name
        extra_vars = {
            "PROJECT_NAME": project_name,
            "PROJECT_PATH": str(target_project_path)
        }
        
        # Temporarily protect pattern-specific variables
        protected_content = content
        protection_map = {}
        
        for i, protected_var in enumerate(self.protected_variables):
            if protected_var in content:
                placeholder = f"__PROTECTED_VAR_{i}__"
                protection_map[placeholder] = protected_var
                protected_content = protected_content.replace(protected_var, placeholder)
        
        # Apply standard template substitution
        processed_content = self.path_manager.substitute_template_variables(
            protected_content, extra_vars
        )
        
        # Restore protected variables
        for placeholder, original_var in protection_map.items():
            processed_content = processed_content.replace(placeholder, original_var)
        
        return processed_content
    
    def _create_pattern_index(self, target_patterns_dir: Path, deployment_results: Dict[str, Any]):
        """
        Create pattern index file for deployed patterns.
        
        Args:
            target_patterns_dir: Target patterns directory
            deployment_results: Deployment results for indexing
        """
        try:
            index_data = {
                "framework_version": "1.0.0",
                "deployment_timestamp": self._get_timestamp(),
                "categories": {},
                "patterns": []
            }
            
            # Build category information
            for category, description in self.pattern_categories.items():
                category_dir = target_patterns_dir / category
                if category_dir.exists():
                    pattern_files = list(category_dir.glob("*.md"))
                    index_data["categories"][category] = {
                        "description": description,
                        "pattern_count": len(pattern_files),
                        "patterns": [p.stem for p in pattern_files]
                    }
            
            # Build pattern list
            for deployed_pattern in deployment_results["patterns_deployed"] + deployment_results["patterns_updated"]:
                pattern_path = Path(deployed_pattern)
                index_data["patterns"].append({
                    "name": pattern_path.stem,
                    "category": pattern_path.parent.name,
                    "path": str(pattern_path),
                    "status": "active"
                })
            
            # Write index file
            index_file = target_patterns_dir / ".pattern_index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, sort_keys=True)
                
        except Exception as e:
            # Non-critical error - don't fail deployment
            deployment_results.setdefault("warnings", []).append(
                f"Failed to create pattern index: {str(e)}"
            )
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for indexing."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def validate_deployment(self, target_project: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate pattern deployment in target project.
        
        Args:
            target_project: Target project directory path
            
        Returns:
            Validation results dictionary
        """
        results = {
            "valid": False,
            "target_project": str(target_project),
            "patterns_found": [],
            "missing_categories": [],
            "invalid_patterns": [],
            "index_valid": False,
            "errors": []
        }
        
        try:
            target_path = Path(target_project).resolve()
            patterns_dir = target_path / "patterns"
            
            if not patterns_dir.exists():
                results["errors"].append("Patterns directory not found")
                return results
            
            # Check pattern index
            index_file = patterns_dir / ".pattern_index.json"
            if index_file.exists():
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        index_data = json.load(f)
                    results["index_valid"] = True
                    results["index_data"] = index_data
                except Exception as e:
                    results["errors"].append(f"Invalid pattern index: {str(e)}")
            
            # Validate pattern files
            for category in self.pattern_categories.keys():
                category_dir = patterns_dir / category
                if category_dir.exists():
                    pattern_files = list(category_dir.glob("*.md"))
                    for pattern_file in pattern_files:
                        if self._validate_pattern_file(pattern_file):
                            results["patterns_found"].append(str(pattern_file.relative_to(patterns_dir)))
                        else:
                            results["invalid_patterns"].append(str(pattern_file.relative_to(patterns_dir)))
                else:
                    results["missing_categories"].append(category)
            
            results["valid"] = (
                len(results["patterns_found"]) > 0 and 
                len(results["invalid_patterns"]) == 0 and
                len(results["errors"]) == 0
            )
            
        except Exception as e:
            results["errors"].append(f"Validation failed: {str(e)}")
        
        return results
    
    def _validate_pattern_file(self, pattern_file: Path) -> bool:
        """
        Validate individual pattern file.
        
        Args:
            pattern_file: Path to pattern file
            
        Returns:
            True if pattern file is valid
        """
        try:
            # Basic validation - file exists and is readable
            if not pattern_file.exists() or not pattern_file.is_file():
                return False
            
            # Check file is readable and not empty
            with open(pattern_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return len(content) > 0
                
        except Exception:
            return False
    
    def get_available_patterns(self) -> Dict[str, Any]:
        """
        Get information about available patterns in framework.
        
        Returns:
            Dictionary of available patterns by category
        """
        patterns_info = {
            "framework_patterns_dir": str(self.framework_patterns_dir),
            "categories": {},
            "total_patterns": 0
        }
        
        if not self.framework_patterns_dir.exists():
            return patterns_info
        
        for category, description in self.pattern_categories.items():
            category_dir = self.framework_patterns_dir / category
            if category_dir.exists() and category_dir.is_dir():
                pattern_files = list(category_dir.glob("*.md"))
                patterns_info["categories"][category] = {
                    "description": description,
                    "pattern_count": len(pattern_files),
                    "patterns": [
                        {
                            "name": p.stem,
                            "file": p.name,
                            "size": p.stat().st_size if p.exists() else 0
                        }
                        for p in pattern_files
                    ]
                }
                patterns_info["total_patterns"] += len(pattern_files)
        
        return patterns_info
    
    def rollback_deployment(self, target_project: Union[str, Path],
                          backup_patterns: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Rollback pattern deployment.
        
        Args:
            target_project: Target project directory path
            backup_patterns: Optional backup patterns to restore
            
        Returns:
            Rollback results dictionary
        """
        results = {
            "success": False,
            "target_project": str(target_project),
            "patterns_removed": [],
            "patterns_restored": [],
            "errors": []
        }
        
        try:
            target_path = Path(target_project).resolve()
            patterns_dir = target_path / "patterns"
            
            if not patterns_dir.exists():
                results["errors"].append("No patterns directory to rollback")
                return results
            
            # Remove deployed patterns (keep project-specific ones)
            index_file = patterns_dir / ".pattern_index.json"
            if index_file.exists():
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        index_data = json.load(f)
                    
                    # Remove framework-deployed patterns
                    for pattern_info in index_data.get("patterns", []):
                        pattern_path = patterns_dir / pattern_info["path"]
                        if pattern_path.exists():
                            pattern_path.unlink()
                            results["patterns_removed"].append(pattern_info["path"])
                    
                    # Remove index file
                    index_file.unlink()
                    
                except Exception as e:
                    results["errors"].append(f"Failed to process pattern index: {str(e)}")
            
            # Restore backup patterns if provided
            if backup_patterns:
                for pattern_path, content in backup_patterns.items():
                    full_path = patterns_dir / pattern_path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    results["patterns_restored"].append(pattern_path)
            
            results["success"] = len(results["errors"]) == 0
            
        except Exception as e:
            results["errors"].append(f"Rollback failed: {str(e)}")
        
        return results