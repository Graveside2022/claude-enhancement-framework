#!/usr/bin/env python3
"""
Automatic Project CLAUDE.md Loader Integration
Automatically executes project loading when project is detected

Created for: Christian
Integrates with existing project initialization systems
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from project_claude_loader import ProjectCLAUDELoader

class AutoProjectLoader:
    """
    Automatic integration of project CLAUDE.md loading
    Executes on session start or project context switch
    """
    
    def __init__(self):
        self.loader = None
        self.current_project_root = None
        self.loaded_config = None
        
    def detect_project_context_change(self, current_dir: str = ".") -> bool:
        """
        Detect if we've switched to a different project context
        """
        abs_dir = str(Path(current_dir).resolve())
        
        if self.current_project_root != abs_dir:
            print(f"🔄 Project context change detected")
            print(f"   Previous: {self.current_project_root}")
            print(f"   Current:  {abs_dir}")
            return True
        
        return False
    
    def auto_load_project_config(self, force_reload: bool = False) -> dict:
        """
        Automatically load project configuration if needed
        """
        current_dir = str(Path().resolve())
        
        # Check if we need to load/reload
        if (force_reload or 
            self.loaded_config is None or 
            self.detect_project_context_change(current_dir)):
            
            print("🚀 Auto-loading project CLAUDE.md configuration...")
            
            # Create new loader for current context
            self.loader = ProjectCLAUDELoader(current_dir)
            
            # Execute complete loading sequence
            results = self.loader.execute_complete_loading_sequence()
            
            # Store results
            self.loaded_config = results
            self.current_project_root = current_dir
            
            # Apply configuration
            self.apply_loaded_configuration(results)
            
            return results
        else:
            print("ℹ️ Project configuration already loaded for current context")
            return self.loaded_config
    
    def apply_loaded_configuration(self, config_results: dict):
        """
        Apply the loaded configuration to current session
        """
        print("⚙️ Applying loaded project configuration...")
        
        config = config_results.get("configuration", {})
        
        # Apply testing protocol
        testing_config = config.get("testing_protocol", {})
        if testing_config.get("tdd_preferred"):
            print("✓ TDD protocol activated")
        
        # Apply parallel execution settings
        parallel_config = config.get("parallel_execution", {})
        if "default_agents" in parallel_config:
            agents = parallel_config["default_agents"]
            print(f"✓ Default agent count set to: {agents}")
        
        # Apply pattern library settings
        pattern_config = config.get("pattern_library", {})
        if pattern_config.get("check_patterns_first"):
            print("✓ Pattern-first development activated")
        
        # Apply coding standards
        standards = config.get("coding_standards", {})
        if "directive_count" in standards:
            count = standards["directive_count"]
            print(f"✓ {count} coding directives active")
        
        # Report project-specific rules
        rules = config.get("project_specific_rules", [])
        if rules:
            print(f"✓ {len(rules)} project-specific binding rules loaded")
        
        print("✅ Project configuration applied successfully")
    
    def get_current_config(self) -> dict:
        """
        Get current loaded configuration
        """
        if self.loaded_config is None:
            return self.auto_load_project_config()
        return self.loaded_config
    
    def get_pattern_library(self) -> dict:
        """
        Get current pattern library
        """
        config = self.get_current_config()
        return config.get("patterns", {})
    
    def get_testing_protocol(self) -> dict:
        """
        Get current testing protocol
        """
        config = self.get_current_config()
        return config.get("configuration", {}).get("testing_protocol", {})
    
    def get_parallel_config(self) -> dict:
        """
        Get current parallel execution configuration
        """
        config = self.get_current_config()
        return config.get("configuration", {}).get("parallel_execution", {})
    
    def should_use_tdd(self) -> bool:
        """
        Check if TDD should be used based on project configuration
        """
        testing_config = self.get_testing_protocol()
        return testing_config.get("tdd_preferred", False)
    
    def get_default_agent_count(self) -> int:
        """
        Get default agent count for parallel execution
        """
        parallel_config = self.get_parallel_config()
        return parallel_config.get("default_agents", 7)  # Global default from CLAUDE.md
    
    def should_check_patterns_first(self) -> bool:
        """
        Check if patterns should be checked before implementation
        """
        config = self.get_current_config()
        pattern_config = config.get("configuration", {}).get("pattern_library", {})
        return pattern_config.get("check_patterns_first", False)
    
    def validate_current_config(self) -> bool:
        """
        Validate that current configuration is properly loaded
        """
        if self.loaded_config is None:
            return False
        
        validation = self.loaded_config.get("validation", {})
        return validation.get("valid", False)

# Global instance for session-wide use
AUTO_LOADER = AutoProjectLoader()

def initialize_project_for_session():
    """
    Initialize project loading for current session
    Called automatically when script is imported
    """
    print("🔧 Initializing automatic project CLAUDE.md loading for Christian...")
    
    # Auto-load configuration for current context
    AUTO_LOADER.auto_load_project_config()
    
    print("✅ Automatic project loading initialized")

def get_project_config():
    """
    Public interface to get current project configuration
    """
    return AUTO_LOADER.get_current_config()

def get_project_patterns():
    """
    Public interface to get current pattern library
    """
    return AUTO_LOADER.get_pattern_library()

def should_use_project_tdd():
    """
    Public interface to check TDD preference
    """
    return AUTO_LOADER.should_use_tdd()

def get_project_agent_count():
    """
    Public interface to get default agent count
    """
    return AUTO_LOADER.get_default_agent_count()

def check_patterns_first():
    """
    Public interface to check if patterns should be checked first
    """
    return AUTO_LOADER.should_check_patterns_first()

def reload_project_config():
    """
    Public interface to force reload project configuration
    """
    return AUTO_LOADER.auto_load_project_config(force_reload=True)

if __name__ == "__main__":
    # Test the auto-loader
    print("Testing automatic project CLAUDE.md loader...")
    
    initialize_project_for_session()
    
    print("\n📊 Current Configuration Summary:")
    print(f"- TDD Preferred: {should_use_project_tdd()}")
    print(f"- Default Agents: {get_project_agent_count()}")
    print(f"- Check Patterns First: {check_patterns_first()}")
    
    patterns = get_project_patterns()
    print(f"- Pattern Categories: {list(patterns.keys())}")
    
    config = get_project_config()
    print(f"- Configuration Valid: {AUTO_LOADER.validate_current_config()}")
    
    print("\n✅ Auto-loader test completed")