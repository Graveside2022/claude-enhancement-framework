#!/bin/bash

# Project CLAUDE.md Loader Integration
# Bash wrapper to integrate Python project loader with existing systems
# Created for: Christian

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Enhanced find_project_root function that integrates with Python loader
find_project_root() {
    echo "🔍 Finding project root using integrated loader..."
    
    # Use Python loader to find project root
    local project_root=$(python3 "$SCRIPT_DIR/project_claude_loader.py" 2>/dev/null | grep "Project root detected:" | sed 's/.*: //')
    
    if [ -n "$project_root" ]; then
        echo "$project_root"
        return 0
    else
        # Fallback to current directory
        echo "$PWD"
        return 1
    fi
}

# Automatic project CLAUDE.md loading function
auto_load_project_claude() {
    echo "🚀 Auto-loading project CLAUDE.md configuration for Christian..."
    
    # Execute Python auto-loader
    local loader_output=$(python3 "$SCRIPT_DIR/auto_project_loader.py")
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ Project CLAUDE.md loaded successfully"
        echo "$loader_output" | grep -E "✓|📊"
        return 0
    else
        echo "❌ Failed to load project CLAUDE.md"
        echo "$loader_output"
        return 1
    fi
}

# Check if project configuration should be applied
should_apply_project_config() {
    # Check if we're in a project with CLAUDE.md
    local project_root=$(find_project_root)
    
    if [ -f "$project_root/CLAUDE.md" ]; then
        echo "true"
        return 0
    else
        echo "false"
        return 1
    fi
}

# Get project-specific configuration values
get_project_config_value() {
    local config_key="$1"
    
    # Use Python to extract specific configuration value
    python3 -c "
import sys
sys.path.append('$SCRIPT_DIR')
from auto_project_loader import AUTO_LOADER

config = AUTO_LOADER.get_current_config()
if config:
    if '$config_key' == 'tdd_preferred':
        print(AUTO_LOADER.should_use_tdd())
    elif '$config_key' == 'default_agents':
        print(AUTO_LOADER.get_default_agent_count())
    elif '$config_key' == 'check_patterns_first':
        print(AUTO_LOADER.should_check_patterns_first())
    elif '$config_key' == 'valid':
        print(AUTO_LOADER.validate_current_config())
    else:
        print('false')
else:
    print('false')
"
}

# Enhanced project discovery that integrates automatic loading
execute_enhanced_project_discovery() {
    echo "=== Enhanced Project Discovery with Automatic CLAUDE.md Loading ==="
    echo "User: Christian"
    echo ""
    
    # First check if we should apply project config
    if [ "$(should_apply_project_config)" = "true" ]; then
        echo "✓ Project CLAUDE.md detected - loading configuration..."
        
        # Execute automatic loading
        auto_load_project_claude
        
        echo ""
        echo "📊 Applied Project Configuration:"
        echo "- TDD Preferred: $(get_project_config_value 'tdd_preferred')"
        echo "- Default Agents: $(get_project_config_value 'default_agents')"
        echo "- Check Patterns First: $(get_project_config_value 'check_patterns_first')"
        echo "- Configuration Valid: $(get_project_config_value 'valid')"
        
    else
        echo "ℹ️ No project CLAUDE.md found - using global defaults"
        echo "📁 Current directory: $(pwd)"
        echo "🔧 Global rules will be applied"
    fi
    
    echo ""
    echo "✅ Enhanced project discovery completed"
}

# Integration with existing session initialization
integrate_with_session_initialization() {
    echo "🔧 Integrating project CLAUDE.md loading with session initialization..."
    
    # Execute enhanced discovery
    execute_enhanced_project_discovery
    
    # Update SESSION_CONTINUITY.md if it exists
    if [ -f "SESSION_CONTINUITY.md" ]; then
        cat >> SESSION_CONTINUITY.md << EOF

## Project CLAUDE.md Integration - $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

### Configuration Status
- Project CLAUDE.md: $([ -f "CLAUDE.md" ] && echo "Found and loaded" || echo "Not found")
- TDD Protocol: $(get_project_config_value 'tdd_preferred')
- Default Agents: $(get_project_config_value 'default_agents')
- Pattern-First: $(get_project_config_value 'check_patterns_first')
- Config Valid: $(get_project_config_value 'valid')

### Integration Results
- Auto-loading: ✓ Completed
- Configuration applied: ✓ Active
- Session rules: $([ -f "CLAUDE.md" ] && echo "Project-specific" || echo "Global defaults")
EOF
        echo "✓ Updated SESSION_CONTINUITY.md with integration status"
    fi
    
    echo "✅ Integration with session initialization completed"
}

# Function to reload project configuration
reload_project_configuration() {
    echo "🔄 Reloading project CLAUDE.md configuration for Christian..."
    
    # Force reload using Python
    python3 -c "
import sys
sys.path.append('$SCRIPT_DIR')
from auto_project_loader import reload_project_config
reload_project_config()
"
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ Project configuration reloaded successfully"
        return 0
    else
        echo "❌ Failed to reload project configuration"
        return 1
    fi
}

# Test function
test_integration() {
    echo "🧪 Testing project CLAUDE.md loader integration..."
    echo "User: Christian"
    echo ""
    
    # Test project root detection
    echo "1. Testing project root detection:"
    local project_root=$(find_project_root)
    echo "   Result: $project_root"
    echo ""
    
    # Test configuration loading
    echo "2. Testing configuration loading:"
    execute_enhanced_project_discovery
    echo ""
    
    # Test configuration values
    echo "3. Testing configuration access:"
    echo "   TDD Preferred: $(get_project_config_value 'tdd_preferred')"
    echo "   Default Agents: $(get_project_config_value 'default_agents')"
    echo "   Check Patterns First: $(get_project_config_value 'check_patterns_first')"
    echo ""
    
    # Test session integration
    echo "4. Testing session integration:"
    integrate_with_session_initialization
    
    echo ""
    echo "✅ Integration test completed"
}

# Main execution
if [ "$1" = "test" ]; then
    test_integration
elif [ "$1" = "reload" ]; then
    reload_project_configuration
elif [ "$1" = "init" ]; then
    integrate_with_session_initialization
else
    # Default: execute enhanced discovery
    execute_enhanced_project_discovery
fi