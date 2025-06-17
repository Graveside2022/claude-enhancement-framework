#!/usr/bin/env python3
"""
Session State Manager - Prevents Redundant CLAUDE Initialization
Solves the core issue of multiple full loading sequences per session

Key Features:
1. Session-level state tracking
2. Prevents redundant PROJECT_CLAUDE_LOADER executions
3. Caches configuration between multiple checks
4. Provides fast configuration access for TDD, agents, etc.

Created for: Christian
Purpose: Eliminate the 24.6k token overhead from repeated executions
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class SessionState:
    """Session state data structure"""
    session_id: str
    project_root: str
    initialized: bool
    initialization_timestamp: float
    config_loaded: bool
    config: Dict[str, Any]
    discovery_cached: bool
    discovery_timestamp: float
    last_access: float
    access_count: int

class SessionStateManager:
    """
    Manages session state to prevent redundant operations
    Core solution to the 24.6k token usage problem
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.session_file = self.project_root / ".claude_session_state.json"
        self.state: Optional[SessionState] = None
        self.session_id = self._generate_session_id()
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return hashlib.md5(f"{time.time()}_{os.getpid()}".encode()).hexdigest()[:12]
    
    def is_session_active(self) -> bool:
        """
        Check if there's an active session that doesn't need reinitialization
        This is the KEY OPTIMIZATION that prevents redundant executions
        """
        if not self.session_file.exists():
            return False
        
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)
            
            # Check if session is recent (within 2 hours)
            last_access = data.get('last_access', 0)
            age_minutes = (time.time() - last_access) / 60
            
            if age_minutes > 120:  # 2 hours
                return False
            
            # Check if configuration is loaded
            if not data.get('config_loaded', False):
                return False
                
            # Session is active and has config
            self.state = SessionState(**data)
            return True
            
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            # Corrupted session file
            return False
    
    def get_cached_config(self) -> Optional[Dict[str, Any]]:
        """
        Get cached configuration if session is active
        This prevents re-running project_claude_loader.py
        """
        if self.is_session_active() and self.state:
            self.state.last_access = time.time()
            self.state.access_count += 1
            self._save_state()
            return self.state.config
        return None
    
    def initialize_session(self, force: bool = False) -> SessionState:
        """
        Initialize new session or return existing active session
        """
        # Check for active session first
        if not force and self.is_session_active() and self.state:
            print(f"✅ Using active session {self.state.session_id} (age: {(time.time() - self.state.last_access)/60:.0f}m)")
            return self.state
        
        print(f"🚀 Initializing new session {self.session_id}")
        
        # Create new session state
        self.state = SessionState(
            session_id=self.session_id,
            project_root=str(self.project_root),
            initialized=False,
            initialization_timestamp=0,
            config_loaded=False,
            config={},
            discovery_cached=False,
            discovery_timestamp=0,
            last_access=time.time(),
            access_count=1
        )
        
        self._save_state()
        return self.state
    
    def mark_config_loaded(self, config: Dict[str, Any]):
        """
        Mark configuration as loaded and cache it
        This is called after project_claude_loader.py runs successfully
        """
        if not self.state:
            self.initialize_session()
        
        self.state.config_loaded = True
        self.state.config = config
        self.state.initialization_timestamp = time.time()
        self.state.initialized = True
        self.state.last_access = time.time()
        
        self._save_state()
        print(f"✅ Configuration cached for session {self.state.session_id}")
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Fast access to cached configuration values
        Used for TDD protocol, agent counts, etc.
        """
        if self.state and self.state.config_loaded:
            return self.state.config.get(key, default)
        return default
    
    def needs_initialization(self) -> bool:
        """
        Determine if full initialization is needed
        """
        if not self.is_session_active():
            return True
        
        if not self.state.config_loaded:
            return True
            
        # Check if key files have changed since config load
        if self._config_files_changed():
            return True
            
        return False
    
    def _config_files_changed(self) -> bool:
        """Check if configuration files changed since last load"""
        if not self.state or not self.state.config_loaded:
            return True
        
        config_files = [
            self.project_root / "CLAUDE.md",
            self.project_root / "SESSION_CONTINUITY.md"
        ]
        
        config_timestamp = self.state.initialization_timestamp
        
        for file_path in config_files:
            if file_path.exists():
                if file_path.stat().st_mtime > config_timestamp:
                    return True
        
        return False
    
    def _save_state(self):
        """Save session state to disk"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(asdict(self.state), f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save session state: {e}")
    
    def cleanup_old_sessions(self):
        """Remove old session files"""
        if self.session_file.exists():
            try:
                stat = self.session_file.stat()
                age_hours = (time.time() - stat.st_mtime) / 3600
                
                if age_hours > 24:  # Remove sessions older than 24 hours
                    self.session_file.unlink()
                    print("🧹 Cleaned up old session state")
            except Exception:
                pass

class SmartConfigurationManager:
    """
    High-level manager that coordinates session state and configuration loading
    This is the main interface that replaces direct project_claude_loader calls
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.session_manager = SessionStateManager(project_root)
        self._config_cache = {}
    
    def get_project_configuration(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        Get project configuration with smart caching
        This is the MAIN METHOD that prevents redundant executions
        """
        # Check for cached config first
        if not force_reload:
            cached_config = self.session_manager.get_cached_config()
            if cached_config:
                return cached_config
        
        # If no cache or force reload, run full loading
        print("⚙️ Loading project configuration (required)")
        return self._load_configuration_once()
    
    def _load_configuration_once(self) -> Dict[str, Any]:
        """
        Run project_claude_loader.py once and cache results
        """
        # Import and run the optimized loader
        from optimized_project_loader import OptimizedProjectLoader
        
        loader = OptimizedProjectLoader(self.project_root, verbose=False)
        result = loader.execute_optimized_loading()
        
        # Extract configuration
        config = {
            'project_root': str(self.project_root),
            'project_type': result['session_config']['project_type'],
            'has_claude_md': result['session_config']['has_claude_md'],
            'tdd_protocol_active': result['session_config'].get('tdd_protocol_active', False),
            'default_agents': result['session_config'].get('default_agents', 3),
            'pattern_first_active': result['session_config'].get('pattern_first_active', True),
            'patterns_available': result['patterns_indexed'],
            'learning_files': result['learning_files_available'],
            'load_timestamp': time.time(),
            'loader_time_ms': result['total_time_ms']
        }
        
        # Cache the configuration
        self.session_manager.mark_config_loaded(config)
        
        return config
    
    def is_tdd_protocol_active(self) -> bool:
        """Fast TDD protocol check - no full reload"""
        config = self.get_project_configuration()
        return config.get('tdd_protocol_active', False)
    
    def get_default_agent_count(self) -> int:
        """Fast agent count check - no full reload"""
        config = self.get_project_configuration()
        return config.get('default_agents', 3)
    
    def is_pattern_first_active(self) -> bool:
        """Fast pattern-first check - no full reload"""
        config = self.get_project_configuration()
        return config.get('pattern_first_active', True)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get lightweight session summary"""
        config = self.get_project_configuration()
        
        return {
            'session_active': self.session_manager.is_session_active(),
            'project_type': config.get('project_type', 'unknown'),
            'has_claude_md': config.get('has_claude_md', False),
            'configuration_age_minutes': (time.time() - config.get('load_timestamp', 0)) / 60,
            'last_load_time_ms': config.get('loader_time_ms', 0),
            'cache_status': 'active' if self.session_manager.state else 'fresh'
        }

# Integration helper functions for existing CLAUDE.md
def check_tdd_protocol() -> bool:
    """
    Replacement for TDD protocol check that uses cached config
    Use this instead of running full project_claude_loader
    """
    manager = SmartConfigurationManager()
    return manager.is_tdd_protocol_active()

def get_project_agent_count() -> int:
    """
    Replacement for agent count check that uses cached config
    Use this instead of running full project_claude_loader
    """
    manager = SmartConfigurationManager()
    return manager.get_default_agent_count()

def verify_pattern_first() -> bool:
    """
    Replacement for pattern-first check that uses cached config
    Use this instead of running full project_claude_loader
    """
    manager = SmartConfigurationManager()
    return manager.is_pattern_first_active()

def get_optimized_session_status() -> Dict[str, Any]:
    """
    Get complete session status with minimal overhead
    Use this for all configuration checks
    """
    manager = SmartConfigurationManager()
    return manager.get_session_summary()

def main():
    """Test the session state manager"""
    print("🧪 Testing Session State Manager\n")
    
    manager = SmartConfigurationManager()
    
    # First call - should run full loader
    print("=== First Configuration Load ===")
    config1 = manager.get_project_configuration()
    
    # Second call - should use cache
    print("\n=== Second Configuration Load (should be cached) ===")
    config2 = manager.get_project_configuration()
    
    # Test individual checks
    print("\n=== Individual Configuration Checks ===")
    print(f"TDD Protocol: {manager.is_tdd_protocol_active()}")
    print(f"Default Agents: {manager.get_default_agent_count()}")
    print(f"Pattern First: {manager.is_pattern_first_active()}")
    
    # Session summary
    print("\n=== Session Summary ===")
    summary = manager.get_session_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()