"""
Config: Configuration management for Claude Enhancement Framework
Part of Claude Enhancement Framework by Christian

Handles:
- Global CLAUDE.md configuration loading and validation
- Project-specific configuration overlays
- Performance optimization settings
- Cross-platform configuration normalization
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from .path_manager import PathManager


@dataclass
class PerformanceConfig:
    """Performance optimization configuration."""
    boot_optimization_enabled: bool = True
    cache_hit_target: float = 0.90
    session_continuity_lines: int = 750
    pattern_search_timeout: int = 10
    auto_pruning_enabled: bool = True
    parallel_agent_limit: int = 10


@dataclass
class MemoryConfig:
    """Memory system configuration."""
    auto_learning_enabled: bool = True
    side_effects_tracking: bool = True
    error_pattern_capture: bool = True
    solution_candidate_promotion: bool = True
    memory_unification_enabled: bool = True


@dataclass
class PatternConfig:
    """Pattern system configuration."""
    pattern_first_development: bool = True
    auto_pattern_indexing: bool = True
    pattern_safety_enabled: bool = True
    seven_step_testing: bool = True
    pattern_match_threshold: float = 0.80


@dataclass
class AgentConfig:
    """Agent execution configuration."""
    boot_agents: int = 3
    work_agents: int = 5
    complex_task_agents: int = 10
    parallel_execution: bool = True
    sequential_forbidden: bool = True


class Config:
    """Central configuration manager for Claude Enhancement Framework."""
    
    def __init__(self, path_manager: Optional[PathManager] = None):
        """
        Initialize configuration manager.
        
        Args:
            path_manager: PathManager instance (creates new if not provided)
        """
        self.path_manager = path_manager or PathManager()
        
        # Default configurations
        self.performance = PerformanceConfig()
        self.memory = MemoryConfig()
        self.patterns = PatternConfig()
        self.agents = AgentConfig()
        
        # Runtime state
        self._global_config_loaded = False
        self._project_config_loaded = False
        self._custom_settings: Dict[str, Any] = {}
    
    def load_global_config(self) -> bool:
        """
        Load global CLAUDE.md configuration.
        
        Returns:
            True if global config loaded successfully
        """
        global_claude_path = self.path_manager.get_global_claude_dir() / "CLAUDE.md"
        
        if not global_claude_path.exists():
            return False
        
        try:
            with open(global_claude_path, 'r', encoding='utf-8') as f:
                global_content = f.read()
            
            # Parse global configuration
            self._parse_claude_md_content(global_content, is_global=True)
            self._global_config_loaded = True
            return True
            
        except Exception as e:
            print(f"Warning: Failed to load global config: {e}")
            return False
    
    def load_project_config(self, project_root: Optional[Path] = None) -> bool:
        """
        Load project-specific CLAUDE.md configuration.
        
        Args:
            project_root: Project root path (auto-detected if not provided)
            
        Returns:
            True if project config loaded successfully
        """
        root = project_root or self.path_manager.find_project_root()
        if not root:
            return False
        
        project_claude_path = root / "CLAUDE.md"
        if not project_claude_path.exists():
            return False
        
        try:
            with open(project_claude_path, 'r', encoding='utf-8') as f:
                project_content = f.read()
            
            # Parse project configuration (overrides global)
            self._parse_claude_md_content(project_content, is_global=False)
            self._project_config_loaded = True
            return True
            
        except Exception as e:
            print(f"Warning: Failed to load project config: {e}")
            return False
    
    def _parse_claude_md_content(self, content: str, is_global: bool = False):
        """
        Parse CLAUDE.md content and update configurations.
        
        Args:
            content: CLAUDE.md file content
            is_global: True if parsing global config
        """
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Performance settings
            if "session_continuity_lines" in line.lower():
                try:
                    value = int(line.split(':')[-1].strip())
                    self.performance.session_continuity_lines = value
                except ValueError:
                    pass
            
            # Agent settings
            elif "boot_agents" in line.lower():
                try:
                    value = int(line.split(':')[-1].strip())
                    self.agents.boot_agents = value
                except ValueError:
                    pass
            
            elif "work_agents" in line.lower():
                try:
                    value = int(line.split(':')[-1].strip())
                    self.agents.work_agents = value
                except ValueError:
                    pass
            
            # Pattern settings
            elif "pattern_match_threshold" in line.lower():
                try:
                    value = float(line.split(':')[-1].strip())
                    self.patterns.pattern_match_threshold = value
                except ValueError:
                    pass
            
            # Memory settings
            elif "auto_learning" in line.lower() and "enabled" in line.lower():
                self.memory.auto_learning_enabled = "true" in line.lower()
    
    def get_effective_config(self) -> Dict[str, Any]:
        """
        Get effective configuration (merged global + project + custom).
        
        Returns:
            Dictionary of all configuration values
        """
        config_dict = {
            "performance": asdict(self.performance),
            "memory": asdict(self.memory),
            "patterns": asdict(self.patterns),
            "agents": asdict(self.agents),
            "custom": self._custom_settings
        }
        
        config_dict["_meta"] = {
            "global_config_loaded": self._global_config_loaded,
            "project_config_loaded": self._project_config_loaded,
            "username": self.path_manager.username,
            "platform": self.path_manager.platform
        }
        
        return config_dict
    
    def set_custom_setting(self, key: str, value: Any):
        """
        Set custom configuration setting.
        
        Args:
            key: Setting key
            value: Setting value
        """
        self._custom_settings[key] = value
    
    def get_custom_setting(self, key: str, default: Any = None) -> Any:
        """
        Get custom configuration setting.
        
        Args:
            key: Setting key
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        return self._custom_settings.get(key, default)
    
    def save_config_to_file(self, file_path: Path):
        """
        Save current configuration to JSON file.
        
        Args:
            file_path: Output file path
        """
        config_dict = self.get_effective_config()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2)
    
    def get_agent_count(self, context: str) -> int:
        """
        Get appropriate agent count for given context.
        
        Args:
            context: Context type ("boot", "work", "complex")
            
        Returns:
            Number of agents to use
        """
        context_lower = context.lower()
        
        if "boot" in context_lower or "init" in context_lower:
            return self.agents.boot_agents
        elif "complex" in context_lower or "analysis" in context_lower:
            return self.agents.complex_task_agents
        else:
            return self.agents.work_agents
    
    def validate_config(self) -> List[str]:
        """
        Validate configuration settings.
        
        Returns:
            List of validation warnings/errors
        """
        warnings = []
        
        # Performance validation
        if self.performance.session_continuity_lines < 100:
            warnings.append("Session continuity lines very low (< 100)")
        elif self.performance.session_continuity_lines > 1000:
            warnings.append("Session continuity lines very high (> 1000)")
        
        if self.performance.cache_hit_target > 1.0:
            warnings.append("Cache hit target > 100% is impossible")
        
        # Agent validation
        if self.agents.boot_agents < 1:
            warnings.append("Boot agents must be >= 1")
        
        if self.agents.work_agents < 1:
            warnings.append("Work agents must be >= 1")
        
        # Pattern validation
        if not (0.0 <= self.patterns.pattern_match_threshold <= 1.0):
            warnings.append("Pattern match threshold must be between 0.0 and 1.0")
        
        return warnings
    
    def initialize_framework_defaults(self):
        """Initialize with Claude Enhancement Framework optimized defaults."""
        # Optimized performance settings
        self.performance.boot_optimization_enabled = True
        self.performance.cache_hit_target = 0.90
        self.performance.session_continuity_lines = 750
        self.performance.pattern_search_timeout = 10
        
        # Enhanced memory settings
        self.memory.auto_learning_enabled = True
        self.memory.side_effects_tracking = True
        self.memory.error_pattern_capture = True
        self.memory.solution_candidate_promotion = True
        
        # Pattern-first development
        self.patterns.pattern_first_development = True
        self.patterns.auto_pattern_indexing = True
        self.patterns.pattern_safety_enabled = True
        self.patterns.seven_step_testing = True
        
        # Optimized agent configuration
        self.agents.boot_agents = 3
        self.agents.work_agents = 5
        self.agents.complex_task_agents = 10
        self.agents.parallel_execution = True