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
import fcntl

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
    config_file_hashes: Dict[str, str]  # Store content hashes instead of relying on mtime

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
        
        # Cache optimization settings
        self.session_timeout_hours = float(os.environ.get('CLAUDE_SESSION_TIMEOUT_HOURS', '8'))  # Extended from 2 to 8 hours
        self.max_session_lifetime_hours = float(os.environ.get('CLAUDE_MAX_SESSION_HOURS', '24'))  # Hard limit: 24 hours
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return hashlib.md5(f"{time.time()}_{os.getpid()}".encode()).hexdigest()[:12]
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get SHA-256 hash of file content for change detection"""
        try:
            if not file_path.exists():
                return "missing"
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return "error"
    
    def _safe_file_operation(self, operation: str, **kwargs):
        """Thread-safe file operations with locking"""
        lock_file = self.session_file.with_suffix('.lock')
        try:
            with open(lock_file, 'w') as lock:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
                
                if operation == 'read':
                    if not self.session_file.exists():
                        return None
                    with open(self.session_file, 'r') as f:
                        return json.load(f)
                        
                elif operation == 'write':
                    with open(self.session_file, 'w') as f:
                        json.dump(kwargs['data'], f, indent=2)
                        
        except Exception as e:
            if operation == 'read':
                return None
            print(f"⚠️ File operation failed: {e}")
        finally:
            try:
                lock_file.unlink()
            except:
                pass
    
    def is_session_active(self) -> bool:
        """
        Check if there's an active session that doesn't need reinitialization
        This is the KEY OPTIMIZATION that prevents redundant executions
        OPTIMIZED: Uses flexible timeout, content hashing, and thread-safe file operations
        """
        if not self.session_file.exists():
            return False
        
        data = self._safe_file_operation('read')
        if data is None:
            return False
            
        try:
            # Check sliding window timeout (activity-based)
            last_access = data.get('last_access', 0)
            age_hours = (time.time() - last_access) / 3600
            
            if age_hours > self.session_timeout_hours:
                return False
            
            # Check hard lifetime limit
            init_timestamp = data.get('initialization_timestamp', 0)
            lifetime_hours = (time.time() - init_timestamp) / 3600
            
            if lifetime_hours > self.max_session_lifetime_hours:
                return False
            
            # Check if configuration is loaded
            if not data.get('config_loaded', False):
                return False
                
            # Session is active and has config - populate state
            # Handle missing config_file_hashes for backward compatibility
            if 'config_file_hashes' not in data:
                data['config_file_hashes'] = {}
                
            self.state = SessionState(**data)
            return True
            
        except (TypeError, KeyError) as e:
            # Corrupted session data
            return False
    
    def get_cached_config(self) -> Optional[Dict[str, Any]]:
        """
        Get cached configuration if session is active
        This prevents re-running project_claude_loader.py
        OPTIMIZED: Thread-safe state updates
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
            access_count=1,
            config_file_hashes={}  # Initialize empty hash tracking
        )
        
        self._save_state()
        return self.state
    
    def mark_config_loaded(self, config: Dict[str, Any]):
        """
        Mark configuration as loaded and cache it
        This is called after project_claude_loader.py runs successfully
        OPTIMIZED: Stores content hashes for reliable change detection
        """
        if not self.state:
            self.initialize_session()
        
        # Store current file hashes for change detection
        config_files = self._get_config_files()
        self.state.config_file_hashes = {
            str(file_path): self._get_file_hash(file_path)
            for file_path in config_files
        }
        
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
        OPTIMIZED: More robust change detection
        """
        if not self.is_session_active():
            return True
        
        if not self.state.config_loaded:
            return True
            
        # Check if key files have changed since config load
        if self._config_files_changed():
            return True
            
        return False
    
    def _get_config_files(self) -> list[Path]:
        """Get list of configuration files to monitor for changes"""
        config_files = [
            self.project_root / "CLAUDE.md",
            # Add other config files that OptimizedProjectLoader might use
            self.project_root / "pyproject.toml",
            self.project_root / "package.json",
            self.project_root / ".env"
        ]
        return [f for f in config_files if f.exists()]
    
    def _config_files_changed(self) -> bool:
        """
        Check if TRUE configuration files changed since last load
        OPTIMIZED: Uses content hashing instead of mtime for accurate change detection
        """
        if not self.state or not self.state.config_loaded:
            return True
        
        # Get current files and their hashes
        current_files = self._get_config_files()
        current_hashes = {
            str(file_path): self._get_file_hash(file_path)
            for file_path in current_files
        }
        
        # Compare with stored hashes
        stored_hashes = self.state.config_file_hashes
        
        # Check if any files changed
        for file_path, current_hash in current_hashes.items():
            stored_hash = stored_hashes.get(file_path)
            if stored_hash != current_hash:
                print(f"🔄 Configuration file changed: {Path(file_path).name}")
                return True
        
        # Check if any files were removed
        for file_path in stored_hashes:
            if file_path not in current_hashes:
                print(f"🔄 Configuration file removed: {Path(file_path).name}")
                return True
        
        return False
    
    def _save_state(self):
        """Save session state to disk with thread safety"""
        try:
            self._safe_file_operation('write', data=asdict(self.state))
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
    
    def _log_side_effect(self, source: str, description: str, impact: str, 
                        files_affected: str, trigger: str):
        """Log side effect to side_effects_log.md"""
        try:
            side_effects_file = self.project_root / "memory" / "side_effects_log.md"
            
            if not side_effects_file.exists():
                return
            
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            side_effect_entry = f"""
### Side Effect - {timestamp}
**Source**: {source}
**Description**: {description}
**Impact**: {impact}
**Files Affected**: {files_affected}
**Trigger**: {trigger}
**Resolution**: pending
---

"""
            
            with open(side_effects_file, 'a') as f:
                f.write(side_effect_entry)
                
        except Exception as e:
            # Don't fail execution due to logging issues
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
        OPTIMIZED: Properly populate learning_files and other cached data
        """
        # Import and run the optimized loader
        from optimized_project_loader import OptimizedProjectLoader
        
        loader = OptimizedProjectLoader(self.project_root)
        result = loader.quick_discovery()
        
        # Extract configuration with complete data
        config = {
            'project_root': str(self.project_root),
            'project_type': result.get('project_type', []),
            'has_claude_md': result.get('has_claude_md', False),
            'tdd_protocol_active': result.get('tdd_protocol_active', False),
            'default_agents': result.get('default_agents', 3),
            'pattern_first_active': result.get('pattern_first_active', True),
            'patterns_available': result.get('pattern_library', {}),
            'learning_files': result.get('learning_files', []),  # FIXED: Properly populate from result
            'memory_files': result.get('memory_files', []),  # Additional cached data
            'timing_rules': result.get('timing_rules', {}),  # Cache timing check results
            'load_timestamp': time.time(),
            'loader_time_ms': result.get('load_time_ms', 1)
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
    
    def get_learning_files(self) -> list:
        """Fast learning files access - no full reload"""
        config = self.get_project_configuration()
        return config.get('learning_files', [])
    
    def get_timing_rules(self) -> Dict[str, Any]:
        """Fast timing rules access - no full reload"""
        config = self.get_project_configuration()
        return config.get('timing_rules', {})
    
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

# OPTIMIZED: New helper functions for cache hit optimization
def timing_check(rule_name: str = None) -> Dict[str, Any]:
    """
    Fast timing rules check - uses cached config
    Replaces direct timing system calls to improve cache hit rate
    """
    manager = SmartConfigurationManager()
    timing_rules = manager.get_timing_rules()
    
    if rule_name:
        return timing_rules.get(rule_name, {})
    return timing_rules

def learning_access(file_type: str = None) -> list:
    """
    Fast learning files access - uses cached config  
    Replaces direct learning file discovery to improve cache hit rate
    """
    manager = SmartConfigurationManager()
    learning_files = manager.get_learning_files()
    
    if file_type:
        return [f for f in learning_files if file_type in f.get('type', '')]
    return learning_files

def main():
    """Test the optimized session state manager with cache performance validation"""
    print("🧪 Testing OPTIMIZED Session State Manager\n")
    
    # Test cache timeout configuration
    print(f"📊 Cache Configuration:")
    manager = SmartConfigurationManager()
    print(f"  Session timeout: {manager.session_manager.session_timeout_hours} hours")
    print(f"  Max lifetime: {manager.session_manager.max_session_lifetime_hours} hours")
    
    # Test cache performance
    operations = []
    
    # First call - should run full loader
    print("\n=== First Configuration Load ===")
    start_time = time.time()
    config1 = manager.get_project_configuration()
    load_time = (time.time() - start_time) * 1000
    operations.append(('full_load', False, load_time))
    
    # Rapid successive calls - should all use cache
    print("\n=== Cache Performance Test (15 operations) ===")
    for i in range(15):
        start_time = time.time()
        
        if i % 5 == 0:
            # Mix of operation types to simulate real usage
            result = timing_check("project_scan")
            op_type = "timing_check"
        elif i % 3 == 0:
            result = learning_access()
            op_type = "learning_access"
        else:
            result = manager.get_project_configuration()
            op_type = "config_access"
            
        access_time = (time.time() - start_time) * 1000
        cache_hit = access_time < 1.0  # Cache hits should be sub-millisecond
        operations.append((op_type, cache_hit, access_time))
        
        print(f"  {op_type}: {'HIT' if cache_hit else 'MISS'} ({access_time:.2f}ms)")
    
    # Calculate cache performance
    total_ops = len(operations) - 1  # Exclude first full load
    cache_hits = sum(1 for _, hit, _ in operations[1:] if hit)
    hit_rate = (cache_hits / total_ops) * 100
    
    print(f"\n📈 Cache Performance Summary:")
    print(f"  Total operations: {total_ops}")
    print(f"  Cache hits: {cache_hits}")
    print(f"  Hit rate: {hit_rate:.1f}%")
    print(f"  Target: 90%")
    print(f"  Target met: {'✅ YES' if hit_rate >= 90 else '❌ NO'}")
    
    # Session summary
    print("\n=== Session Details ===")
    summary = manager.get_session_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    return hit_rate >= 90

if __name__ == "__main__":
    main()