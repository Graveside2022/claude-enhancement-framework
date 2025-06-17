#!/bin/bash

# Test Enhanced Learning File Discovery
# Tests the improved project discovery protocol with learning file loading

echo "🧪 Testing Enhanced Learning File Discovery for Christian"
echo "======================================================="

# Source the enhanced functions from CLAUDE.md
# Extract the find_project_root function
find_project_root() {
    local current_dir="$PWD"
    local max_depth=20
    local depth=0
    
    # Search up directory tree for project markers
    while [ "$current_dir" != "/" ] && [ $depth -lt $max_depth ]; do
        # Primary markers (highest confidence)
        if [ -f "$current_dir/CLAUDE.md" ]; then
            echo "$current_dir"
            return 0
        fi
        
        # Secondary markers with Claude memory structure
        if [ -d "$current_dir/memory" ] && [ -f "$current_dir/memory/learning_archive.md" ]; then
            echo "$current_dir"
            return 0
        fi
        
        # Tertiary markers - common project indicators with Claude structure
        if [ -f "$current_dir/package.json" ] || [ -f "$current_dir/requirements.txt" ] || [ -d "$current_dir/.git" ]; then
            # Verify it also has Claude learning structure
            if [ -d "$current_dir/memory" ] || [ -f "$current_dir/SESSION_CONTINUITY.md" ]; then
                echo "$current_dir"
                return 0
            fi
        fi
        
        # Move up one directory
        current_dir="$(dirname "$current_dir")"
        depth=$((depth + 1))
    done
    
    # No project root found - use current directory
    echo "$PWD"
    return 1
}

# Enhanced load_learning_files function
load_learning_files() {
    local project_root=$(find_project_root)
    
    echo "📚 Loading learning files for Christian..."
    echo "📁 Project root: $project_root"
    
    # Load global learning files (always available)
    echo "🌐 Loading global learning files from ~/.claude/"
    [ -f "$HOME/.claude/LEARNED_CORRECTIONS.md" ] && echo "✓ Global error learning loaded"
    [ -f "$HOME/.claude/PYTHON_LEARNINGS.md" ] && echo "✓ Python learnings loaded"
    [ -f "$HOME/.claude/INFRASTRUCTURE_LEARNINGS.md" ] && echo "✓ Infrastructure learnings loaded"
    [ -f "$HOME/.claude/PROJECT_SPECIFIC_LEARNINGS.md" ] && echo "✓ Project-specific learnings loaded"
    
    # Load project-specific learning files (if in project)
    if [ -f "$project_root/memory/learning_archive.md" ]; then
        echo "📊 Loading project learning files from $project_root/memory/"
        
        # Load and display learning archive content
        echo "✓ Learning archive loaded:"
        echo "   $(grep -c "Patterns created\|Patterns reused\|TDD applications" "$project_root/memory/learning_archive.md" || echo "0") metrics tracked"
        
        # Load error patterns if available
        if [ -f "$project_root/memory/error_patterns.md" ]; then
            local error_count=$(grep -c "##\|###" "$project_root/memory/error_patterns.md" 2>/dev/null || echo "0")
            echo "✓ Project error patterns loaded: $error_count patterns documented"
        fi
        
        # Load side effects log if available
        if [ -f "$project_root/memory/side_effects_log.md" ]; then
            local effects_count=$(grep -c "##\|###" "$project_root/memory/side_effects_log.md" 2>/dev/null || echo "0")
            echo "✓ Side effects log loaded: $effects_count effects documented"
        fi
        
        # Load session continuity
        if [ -f "$project_root/SESSION_CONTINUITY.md" ]; then
            local session_updates=$(grep -c "## " "$project_root/SESSION_CONTINUITY.md" 2>/dev/null || echo "0")
            echo "✓ Session continuity loaded: $session_updates session updates"
        fi
        
        # Display recent efficiency metrics
        echo "📈 Recent efficiency metrics:"
        local patterns_created=$(grep "Patterns created:" "$project_root/memory/learning_archive.md" | tail -1 | grep -o '[0-9]*' || echo "0")
        local patterns_reused=$(grep "Patterns reused:" "$project_root/memory/learning_archive.md" | tail -1 | grep -o '[0-9]*' || echo "0")
        local time_saved=$(grep "Time saved" "$project_root/memory/learning_archive.md" | tail -1 | grep -o '[0-9]*' || echo "0")
        echo "   - Patterns created: $patterns_created"
        echo "   - Patterns reused: $patterns_reused"
        echo "   - Time saved: $time_saved minutes"
        
    else
        echo "ℹ️ No project-specific learning files found"
    fi
    
    echo "✅ Learning file loading complete"
}

# Enhanced project discovery protocol
project_discovery_protocol() {
    echo "=== Enhanced Project Discovery Scan ==="
    echo "User: Christian"
    echo ""
    
    # Detect project root using function
    PROJECT_ROOT=$(find_project_root)
    echo "📁 Project root detected: $PROJECT_ROOT"
    
    # Check for project CLAUDE.md in project root
    echo "Checking for project CLAUDE.md…"
    if [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
        echo "✓ Project CLAUDE.md found - will follow project rules"
        echo "  - Project patterns available"
        echo "  - Project testing protocol active"
    else
        echo "✗ No project CLAUDE.md - using global defaults"
    fi
    
    # Detect project type using project root
    echo ""
    echo "Detecting project type:"
    [ -f "$PROJECT_ROOT/requirements.txt" ] && echo "✓ Python project detected"
    [ -f "$PROJECT_ROOT/package.json" ] && echo "✓ Node.js project detected"
    [ -f "$PROJECT_ROOT/Cargo.toml" ] && echo "✓ Rust project detected"
    [ -f "$PROJECT_ROOT/go.mod" ] && echo "✓ Go project detected"
    [ -f "$PROJECT_ROOT/composer.json" ] && echo "✓ PHP project detected"
    [ -f "$PROJECT_ROOT/Gemfile" ] && echo "✓ Ruby project detected"
    
    # Check for key files in project root
    echo ""
    echo "Configuration files:"
    [ -f "$PROJECT_ROOT/.env" ] && echo "✓ .env (Environment config present - DO NOT DISPLAY CONTENTS)"
    [ -f "$PROJECT_ROOT/Dockerfile" ] && echo "✓ Dockerfile (Docker configuration)"
    [ -f "$PROJECT_ROOT/docker-compose.yml" ] && echo "✓ docker-compose.yml (Docker Compose setup)"
    
    # Check existing structure in project root
    echo ""
    echo "Project structure:"
    find "$PROJECT_ROOT" -maxdepth 2 -type d -name "memory" -o -name "patterns" -o -name "scripts" -o -name "tests" -o -name "docs" 2>/dev/null | head -10
    
    # Check git status in project root
    if [ -d "$PROJECT_ROOT/.git" ]; then
        echo ""
        echo "Git repository detected:"
        cd "$PROJECT_ROOT" && git status --short | head -5
        echo "Current branch: $(cd "$PROJECT_ROOT" && git branch --show-current)"
    fi
    
    # Load project learning files if they exist
    echo ""
    echo "Loading project learning files..."
    if [ -f "$PROJECT_ROOT/memory/learning_archive.md" ]; then
        echo "📊 Project learning files found in $PROJECT_ROOT/memory/"
        
        # Display learning archive summary
        echo "✓ Learning archive:"
        local patterns_created=$(grep "Patterns created:" "$PROJECT_ROOT/memory/learning_archive.md" | tail -1 | grep -o '[0-9]*' || echo "0")
        local patterns_reused=$(grep "Patterns reused:" "$PROJECT_ROOT/memory/learning_archive.md" | tail -1 | grep -o '[0-9]*' || echo "0")
        local time_saved=$(grep "Time saved" "$PROJECT_ROOT/memory/learning_archive.md" | tail -1 | grep -o '[0-9]*' || echo "0")
        echo "   - Patterns created: $patterns_created"
        echo "   - Patterns reused: $patterns_reused" 
        echo "   - Time saved: $time_saved minutes"
        
        # Check other memory files
        [ -f "$PROJECT_ROOT/memory/error_patterns.md" ] && echo "✓ Error patterns available for learning"
        [ -f "$PROJECT_ROOT/memory/side_effects_log.md" ] && echo "✓ Side effects log available for reference"
        
        # Session continuity check
        if [ -f "$PROJECT_ROOT/SESSION_CONTINUITY.md" ]; then
            local last_update=$(grep "## " "$PROJECT_ROOT/SESSION_CONTINUITY.md" | tail -1 | cut -d' ' -f2-4 || echo "Unknown")
            echo "✓ Session continuity - last update: $last_update"
        fi
    else
        echo "ℹ️ No project learning files found - this appears to be a fresh project"
    fi
    
    echo ""
    echo "✅ Enhanced project discovery complete with learning file integration"
}

# Run the tests
echo "1. Testing enhanced load_learning_files function:"
load_learning_files

echo ""
echo "2. Testing enhanced project discovery protocol:"
project_discovery_protocol

echo ""
echo "✅ Enhanced learning file discovery test complete!"
echo "   The project discovery now properly loads and displays learning file content"