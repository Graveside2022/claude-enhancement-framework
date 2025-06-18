# Pattern: Unified Learning File Loading

## Problem
Claude needs to load both global learning files (~/.claude/*.md) and project-specific learning files (./memory/*.md) regardless of the current working directory.

## Solution
Combine global file loading with project root detection to ensure all learning contexts are available from any location.

## Code Template

```bash
# Learning file loading implementation
load_learning_files() {
    local project_root=$(find_project_root)
    
    echo "📚 Loading learning files for {{USER_NAME}}..."
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
        echo "✓ Learning archive loaded"
        [ -f "$project_root/memory/error_patterns.md" ] && echo "✓ Project error patterns loaded"
        [ -f "$project_root/memory/side_effects_log.md" ] && echo "✓ Side effects log loaded"
        [ -f "$project_root/SESSION_CONTINUITY.md" ] && echo "✓ Session continuity loaded"
    else
        echo "ℹ️ No project-specific learning files found"
    fi
    
    echo "✅ Learning file loading complete"
}
```

## Testing Requirements
- Complexity score: 3 (multiple file checks)
- TDD used: No (configuration loading)
- Test pattern: Verify output messages match expected files

## When to Use
- At the beginning of each Claude session
- When switching between projects
- After error corrections are stored
- When loading context for decision making

## Time Saved
Estimated: 5-10 minutes per session (vs manual file navigation)
Actual uses: Every session initialization

## Variations

### Silent Loading Version
```bash
load_learning_files_silent() {
    local project_root=$(find_project_root)
    local files_loaded=0
    
    # Global files
    for file in LEARNED_CORRECTIONS.md PYTHON_LEARNINGS.md INFRASTRUCTURE_LEARNINGS.md PROJECT_SPECIFIC_LEARNINGS.md; do
        [ -f "$HOME/.claude/$file" ] && ((files_loaded++))
    done
    
    # Project files
    if [ -d "$project_root/memory" ]; then
        for file in learning_archive.md error_patterns.md side_effects_log.md; do
            [ -f "$project_root/memory/$file" ] && ((files_loaded++))
        done
    fi
    
    [ -f "$project_root/SESSION_CONTINUITY.md" ] && ((files_loaded++))
    
    return $files_loaded  # Return count for verification
}
```

### Selective Loading Version
```bash
load_learning_files_selective() {
    local file_type="$1"  # "global", "project", or "all"
    local project_root=$(find_project_root)
    
    case "$file_type" in
        "global")
            # Load only global files
            for file in "$HOME/.claude/"*.md; do
                [ -f "$file" ] && echo "Loaded: $(basename "$file")"
            done
            ;;
        "project")
            # Load only project files
            if [ -d "$project_root/memory" ]; then
                for file in "$project_root/memory/"*.md; do
                    [ -f "$file" ] && echo "Loaded: $(basename "$file")"
                done
            fi
            ;;
        *)
            # Load all files (default)
            load_learning_files
            ;;
    esac
}
```

## Integration Points
- Call from session initialization scripts
- Include in CLAUDE.md Section 2.6.1
- Use in error recovery procedures
- Integrate with handoff generation

## Dependencies
- Requires `find_project_root()` function
- Expects standard Claude directory structure
- Assumes learning files follow naming conventions

## Error Handling
```bash
load_learning_files_with_recovery() {
    # Ensure find_project_root exists
    if ! type find_project_root >/dev/null 2>&1; then
        echo "⚠️ Warning: find_project_root not available, using current directory"
        PROJECT_ROOT="$PWD"
    else
        PROJECT_ROOT=$(find_project_root)
    fi
    
    # Create missing directories if needed
    [ ! -d "$HOME/.claude" ] && mkdir -p "$HOME/.claude"
    [ ! -d "$PROJECT_ROOT/memory" ] && [ -f "$PROJECT_ROOT/CLAUDE.md" ] && mkdir -p "$PROJECT_ROOT/memory"
    
    # Continue with loading...
    load_learning_files
}
```

## Notes
- Global files are always loaded regardless of project context
- Project files only load when in a valid project directory
- Silent failures (missing files) are normal and expected
- Function provides visual feedback for user confidence