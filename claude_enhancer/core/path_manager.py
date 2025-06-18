"""
PathManager: Dynamic path resolution for cross-platform deployment
Part of Claude Enhancement Framework by Christian

Handles dynamic path resolution for:
- Project root detection (from any subdirectory within 20 levels)
- Global configuration (~/.claude/)
- Template variable substitution
- Cross-platform path normalization
"""

import os
import platform
from pathlib import Path
from typing import Dict, Optional, Union


class PathManager:
    """Manages dynamic path resolution for Claude Enhancement Framework."""
    
    def __init__(self, username: Optional[str] = None, project_name: Optional[str] = None):
        """
        Initialize PathManager with optional customization.
        
        Args:
            username: Override detected username
            project_name: Override detected project name
        """
        self.username = username or self._detect_username()
        self.project_name = project_name
        self.platform = platform.system().lower()
        
        # Cache for expensive operations
        self._project_root_cache = None
        self._global_claude_dir_cache = None
    
    def _detect_username(self) -> str:
        """Detect current username across platforms."""
        return os.getenv("USER") or os.getenv("USERNAME") or "user"
    
    def find_project_root(self, start_path: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """
        Find project root by searching for CLAUDE.md marker file.
        
        Searches up to 20 directory levels from start_path for CLAUDE.md.
        Caches result for performance.
        
        Args:
            start_path: Starting directory (defaults to current working directory)
            
        Returns:
            Path to project root directory or None if not found
        """
        if self._project_root_cache:
            return self._project_root_cache
            
        current_path = Path(start_path or os.getcwd()).resolve()
        max_levels = 20
        
        for _ in range(max_levels):
            claude_md_path = current_path / "CLAUDE.md"
            if claude_md_path.exists():
                self._project_root_cache = current_path
                return current_path
            
            parent = current_path.parent
            if parent == current_path:  # Reached filesystem root
                break
            current_path = parent
        
        return None
    
    def get_global_claude_dir(self) -> Path:
        """
        Get global Claude configuration directory.
        
        Returns:
            Path to ~/.claude/ directory
        """
        if self._global_claude_dir_cache:
            return self._global_claude_dir_cache
            
        home_dir = Path.home()
        claude_dir = home_dir / ".claude"
        
        # Ensure directory exists
        claude_dir.mkdir(exist_ok=True)
        
        self._global_claude_dir_cache = claude_dir
        return claude_dir
    
    def get_project_memory_dir(self, project_root: Optional[Path] = None) -> Optional[Path]:
        """
        Get project memory directory.
        
        Args:
            project_root: Project root path (auto-detected if not provided)
            
        Returns:
            Path to project/memory/ directory or None if project root not found
        """
        root = project_root or self.find_project_root()
        if not root:
            return None
            
        memory_dir = root / "memory"
        memory_dir.mkdir(exist_ok=True)
        return memory_dir
    
    def get_project_patterns_dir(self, project_root: Optional[Path] = None) -> Optional[Path]:
        """
        Get project patterns directory.
        
        Args:
            project_root: Project root path (auto-detected if not provided)
            
        Returns:
            Path to project/patterns/ directory or None if project root not found
        """
        root = project_root or self.find_project_root()
        if not root:
            return None
            
        patterns_dir = root / "patterns"
        patterns_dir.mkdir(exist_ok=True)
        return patterns_dir
    
    def substitute_template_variables(self, content: str, extra_vars: Optional[Dict[str, str]] = None) -> str:
        """
        Substitute template variables in content.
        
        Available variables:
        - {{USER_NAME}}: Current username
        - {{PROJECT_NAME}}: Project name (if detected)
        - {{GLOBAL_CLAUDE_DIR}}: ~/.claude/ path
        - {{PROJECT_ROOT}}: Project root path
        - Any additional variables from extra_vars
        
        Args:
            content: Template content with variables
            extra_vars: Additional variables to substitute
            
        Returns:
            Content with variables substituted
        """
        variables = {
            "USER_NAME": self.username,
            "PROJECT_NAME": self.project_name or "{{PROJECT_NAME}}",
            "GLOBAL_CLAUDE_DIR": str(self.get_global_claude_dir()),
            "PROJECT_ROOT": str(self.find_project_root() or "{{PROJECT_ROOT}}"),
            "PLATFORM": self.platform,
        }
        
        if extra_vars:
            variables.update(extra_vars)
        
        result = content
        for var_name, var_value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            result = result.replace(placeholder, str(var_value))
        
        return result
    
    def is_project_directory(self, path: Union[str, Path]) -> bool:
        """
        Check if directory is a Claude-enhanced project.
        
        Args:
            path: Directory path to check
            
        Returns:
            True if directory contains CLAUDE.md marker file
        """
        claude_md_path = Path(path) / "CLAUDE.md"
        return claude_md_path.exists()
    
    def get_cross_platform_script_path(self, script_name: str) -> str:
        """
        Get platform-appropriate script path.
        
        Args:
            script_name: Base script name (e.g., "setup")
            
        Returns:
            Platform-appropriate script name
        """
        if self.platform == "windows":
            return f"{script_name}.bat"
        else:
            return script_name
    
    def normalize_path(self, path: Union[str, Path]) -> Path:
        """
        Normalize path for current platform.
        
        Args:
            path: Path to normalize
            
        Returns:
            Normalized Path object
        """
        return Path(path).resolve()
    
    def clear_cache(self):
        """Clear internal path caches (useful for testing)."""
        self._project_root_cache = None
        self._global_claude_dir_cache = None