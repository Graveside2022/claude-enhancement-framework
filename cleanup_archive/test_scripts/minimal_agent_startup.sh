#!/bin/bash
# Minimal Agent Startup Configuration
# Optimizes CLAUDE startup by deferring agent initialization

# Fast startup mode flag
export CLAUDE_FAST_STARTUP=true

# Agent registry without spawning
declare -A AGENT_REGISTRY
declare -A AGENT_STATUS

# Initialize minimal agent system
minimal_agent_init() {
    echo "⚡ Initializing minimal agent system for fast startup..."
    
    # Register agent types without creating them
    AGENT_REGISTRY[investigation]="not_loaded"
    AGENT_REGISTRY[development]="not_loaded"
    AGENT_REGISTRY[analysis]="not_loaded"
    
    # Set all agents to standby
    AGENT_STATUS[all]="standby"
    
    # Create deferred loading function
    export -f load_agents_on_demand
    
    echo "✓ Agent system ready (minimal mode - 0 agents loaded)"
    return 0
}

# Deferred agent loader
load_agents_on_demand() {
    local task_type="$1"
    local complexity="$2"
    
    # Only load if not already loaded
    if [ "${AGENT_REGISTRY[$task_type]}" = "not_loaded" ]; then
        echo "📊 Loading $task_type agents for complexity: $complexity"
        
        case "$complexity" in
            trivial)
                echo "→ No agents needed for trivial task"
                return 0
                ;;
            simple)
                echo "→ Loading 2 lightweight agents"
                AGENT_REGISTRY[$task_type]="2_agents"
                ;;
            moderate)
                echo "→ Loading 5 standard agents"
                AGENT_REGISTRY[$task_type]="5_agents"
                ;;
            complex)
                echo "→ Loading full 7-agent suite"
                AGENT_REGISTRY[$task_type]="7_agents"
                ;;
            *)
                echo "→ Loading 10 agents for system-wide work"
                AGENT_REGISTRY[$task_type]="10_agents"
                ;;
        esac
        
        AGENT_STATUS[$task_type]="active"
    else
        echo "✓ Agents already loaded for $task_type"
    fi
}

# Complexity assessment function
assess_task_complexity() {
    local file_count="$1"
    local operation_type="$2"
    
    if [ "$file_count" -lt 3 ]; then
        echo "trivial"
    elif [ "$file_count" -lt 6 ]; then
        echo "simple"
    elif [ "$file_count" -lt 11 ]; then
        echo "moderate"
    elif [ "$file_count" -lt 20 ]; then
        echo "complex"
    else
        echo "system"
    fi
}

# Fast execution path for simple operations
fast_execution_path() {
    local operation="$1"
    
    echo "⚡ Fast execution path activated"
    echo "→ Skipping parallel agent setup"
    echo "→ Direct execution mode"
    
    # Perform operation without agent overhead
    case "$operation" in
        init|startup|boot)
            echo "✓ Fast initialization complete"
            ;;
        simple_query)
            echo "✓ Query processed without agents"
            ;;
        *)
            echo "✓ Operation completed in fast mode"
            ;;
    esac
}

# Override for startup triggers
handle_startup_trigger() {
    echo "🚀 STARTUP TRIGGER DETECTED - Using fast mode"
    
    # Skip heavy initialization
    minimal_agent_init
    
    # Mark as startup mode
    export CLAUDE_STARTUP_COMPLETE=false
    
    # Defer heavy operations
    echo "✓ Heavy operations deferred until after startup"
    
    # Complete startup
    export CLAUDE_STARTUP_COMPLETE=true
    echo "✓ Startup completed in minimal mode"
}

# Check if we should use fast startup
should_use_fast_startup() {
    local trigger="$1"
    
    case "$trigger" in
        "hi"|"Hi"|"hello"|"Hello"|"ready"|"start"|"setup"|"boot"|"startup")
            return 0  # true - use fast startup
            ;;
        *)
            return 1  # false - normal mode
            ;;
    esac
}

# Export functions for use in CLAUDE.md
export -f minimal_agent_init
export -f load_agents_on_demand
export -f assess_task_complexity
export -f fast_execution_path
export -f handle_startup_trigger
export -f should_use_fast_startup

echo "✅ Minimal agent startup configuration loaded"
echo "⚡ Fast startup mode available for initialization triggers"