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
import stat
import re
from pathlib import Path
from typing import Dict, Optional, Union, List, Tuple


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
    
    def validate_path(self, path: Union[str, Path], 
                     check_exists: bool = True,
                     check_writable: bool = True,
                     create_if_missing: bool = False,
                     require_confirmation: bool = True) -> Tuple[bool, List[str], Optional[Path]]:
        """
        Comprehensive path validation for user-specified installation directories.
        
        Args:
            path: Path to validate
            check_exists: Whether to check if path exists
            check_writable: Whether to check write permissions
            create_if_missing: Whether to create directory if it doesn't exist
            require_confirmation: Whether to ask user confirmation before creating
            
        Returns:
            Tuple of (is_valid, error_messages, normalized_path)
        """
        errors = []
        
        try:
            # Normalize path
            if isinstance(path, str):
                path_obj = Path(path).expanduser().resolve()
            else:
                path_obj = path.expanduser().resolve()
                
        except (OSError, ValueError) as e:
            errors.append(f"Invalid path format: {e}")
            return False, errors, None
        
        # Validate path format and detect invalid characters
        if not self._is_valid_path_format(str(path_obj)):
            errors.append("Path contains invalid characters or format")
            return False, errors, None
        
        # Check if path exists
        if check_exists and not path_obj.exists():
            if create_if_missing:
                if require_confirmation:
                    response = input(f"Directory '{path_obj}' does not exist. Create it? [y/N]: ").strip().lower()
                    if response not in ['y', 'yes']:
                        errors.append("Directory does not exist and creation declined")
                        return False, errors, None
                
                try:
                    path_obj.mkdir(parents=True, exist_ok=True)
                    print(f"✅ Created directory: {path_obj}")
                except (OSError, PermissionError) as e:
                    errors.append(f"Cannot create directory: {e}")
                    return False, errors, None
            else:
                errors.append(f"Directory '{path_obj}' does not exist")
                return False, errors, None
        
        # Check if it's a directory (not a file)
        if path_obj.exists() and not path_obj.is_dir():
            errors.append("Path exists but is not a directory")
            return False, errors, None
        
        # Check write permissions
        if check_writable and path_obj.exists():
            if not self._check_write_permission(path_obj):
                errors.append("Directory is not writable")
                return False, errors, None
        
        # Additional platform-specific validations
        platform_errors = self._validate_platform_specific(path_obj)
        if platform_errors:
            errors.extend(platform_errors)
        
        # If no errors, path is valid
        if not errors:
            return True, [], path_obj
        else:
            return False, errors, None
    
    def _is_valid_path_format(self, path_str: str) -> bool:
        """
        Validate path format and detect invalid characters.
        
        Args:
            path_str: Path string to validate
            
        Returns:
            True if path format is valid
        """
        # Check for null bytes or other dangerous characters
        if '\x00' in path_str:
            return False
        
        # Platform-specific invalid characters
        if self.platform == "windows":
            # Windows invalid characters: < > : " | ? * and control characters
            invalid_chars = r'[<>:"|?*\x00-\x1f]'
            if re.search(invalid_chars, path_str):
                return False
            
            # Windows reserved names
            reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                             'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                             'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
            path_parts = Path(path_str).parts
            for part in path_parts:
                if part.upper().split('.')[0] in reserved_names:
                    return False
        
        # Check path length limits
        if len(path_str) > 4096:  # Most systems have limits around this range
            return False
        
        return True
    
    def _check_write_permission(self, path: Path) -> bool:
        """
        Check if directory has write permissions.
        
        Args:
            path: Directory path to check
            
        Returns:
            True if directory is writable
        """
        try:
            # Try to create a temporary file to test write access
            test_file = path / ".claude_write_test"
            test_file.touch()
            test_file.unlink()
            return True
        except (OSError, PermissionError):
            # Fall back to os.access check
            return os.access(path, os.W_OK)
    
    def _validate_platform_specific(self, path: Path) -> List[str]:
        """
        Perform platform-specific path validations.
        
        Args:
            path: Path to validate
            
        Returns:
            List of platform-specific error messages
        """
        errors = []
        
        if self.platform == "darwin":  # macOS
            # Check for case sensitivity issues
            if path.exists():
                # macOS can be case-insensitive, check for potential conflicts
                parent = path.parent
                if parent.exists():
                    existing_names = [p.name for p in parent.iterdir()]
                    path_name = path.name
                    case_conflicts = [name for name in existing_names 
                                    if name.lower() == path_name.lower() and name != path_name]
                    if case_conflicts:
                        errors.append(f"Case sensitivity conflict with existing: {case_conflicts}")
        
        elif self.platform == "linux":
            # Check for filesystem-specific limitations
            try:
                # Check if filesystem supports long filenames
                if path.exists():
                    stat_result = path.stat()
                    # Additional Linux-specific checks can be added here
            except OSError:
                pass
        
        elif self.platform == "windows":
            # Check path length (Windows has 260 character limit in many cases)
            if len(str(path)) > 260:
                errors.append("Path exceeds Windows 260 character limit")
            
            # Check for trailing dots or spaces (not allowed in Windows)
            for part in path.parts:
                if part.endswith('.') or part.endswith(' '):
                    errors.append(f"Path component '{part}' ends with dot or space (not allowed on Windows)")
        
        return errors
    
    def validate_installation_directory(self, directory: Union[str, Path], 
                                      purpose: str = "installation") -> Tuple[bool, List[str], Optional[Path]]:
        """
        Validate a user-specified installation directory with appropriate defaults.
        
        Args:
            directory: Directory path provided by user
            purpose: Purpose of the directory (for error messages)
            
        Returns:
            Tuple of (is_valid, error_messages, validated_path)
        """
        return self.validate_path(
            directory,
            check_exists=True,
            check_writable=True,
            create_if_missing=True,
            require_confirmation=True
        )
    
    def get_safe_directory_path(self, user_input: str, default_path: Path, 
                               purpose: str = "installation") -> Path:
        """
        Get a safe, validated directory path with fallback to default.
        
        Args:
            user_input: User-provided path
            default_path: Default path to use if validation fails
            purpose: Purpose of the directory (for messages)
            
        Returns:
            Validated Path object (either user input or safe default)
        """
        if not user_input.strip():
            return default_path
        
        is_valid, errors, validated_path = self.validate_installation_directory(user_input, purpose)
        
        if is_valid and validated_path:
            print(f"✅ {purpose.capitalize()} directory validated: {validated_path}")
            return validated_path
        else:
            print(f"❌ {purpose.capitalize()} directory validation failed:")
            for error in errors:
                print(f"   - {error}")
            print(f"   Using default instead: {default_path}")
            
            # Ensure default path exists and is writable
            default_path.mkdir(parents=True, exist_ok=True)
            return default_path