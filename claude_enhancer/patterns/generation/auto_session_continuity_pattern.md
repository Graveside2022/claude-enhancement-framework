# Pattern: Automatic Session Continuity on Boot

## Problem
When starting a new Claude session without formal handoff, there's no automatic continuity. Users must manually prompt Claude to read context files or use handoff prompts, creating friction.

## Solution
Implement an automatic session continuity system that updates a "latest state" file after every significant action and provides a boot sequence that Claude should execute automatically.

## Code Template

### 1. Auto-Update Function (Add to CLAUDE.md)
```bash
# Automatic session continuity updater
update_session_state() {
    local action="$1"
    local details="$2"
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Always update the latest state file
    cat > SESSION_LATEST_STATE.md << EOF
# LATEST SESSION STATE
Last Updated: ${timestamp}
User: {{USER_NAME}}
Project: $(basename "$(find_project_root)")

## CURRENT CONTEXT
Action Just Completed: ${action}
Details: ${details}

## NEXT ACTIONS
$(grep -A5 "^### Next step:" TODO.md 2>/dev/null | tail -n +2 || echo "- Check TODO.md for priorities")

## ACTIVE WORK
$(grep "in_progress" < <(echo "Check todo list") || echo "- Review TODO.md for current tasks")

## PROJECT STATUS
- Project Root: $(find_project_root)
- Session Continuity: Active
- Last Backup: $(stat -c %Y backups/.last_scheduled_backup 2>/dev/null | xargs -I {} date -d @{} '+%Y-%m-%d %H:%M' || echo "Unknown")

## QUICK START
1. Check timing rules (TODO.md age, backup status)
2. Read this file for immediate context  
3. Continue with "Next Actions" above
4. Apply all CLAUDE.md rules

## FILES TO CHECK
- TODO.md - Current task list
- SESSION_CONTINUITY.md - Detailed session history
- memory/learning_archive.md - Project learnings
- patterns/ - Reusable solutions
EOF
    
    # Also append to SESSION_CONTINUITY.md
    echo "" >> SESSION_CONTINUITY.md
    echo "### ${timestamp} - ${action}" >> SESSION_CONTINUITY.md
    echo "${details}" >> SESSION_CONTINUITY.md
}

# Hook this into all major operations
alias after_task='update_session_state'
```

### 2. Boot Sequence Pattern
```bash
# Add to start of CLAUDE.md or as first instruction
claude_boot_sequence() {
    echo "🚀 Claude Boot Sequence for {{USER_NAME}}"
    
    # 1. Detect project
    PROJECT_ROOT=$(find_project_root)
    echo "📁 Project: $PROJECT_ROOT"
    
    # 2. Check latest state
    if [ -f "$PROJECT_ROOT/SESSION_LATEST_STATE.md" ]; then
        echo "📊 Found latest state file"
        cat "$PROJECT_ROOT/SESSION_LATEST_STATE.md"
    else
        echo "⚠️ No latest state found - checking other continuity files"
        [ -f "$PROJECT_ROOT/SESSION_CONTINUITY.md" ] && head -50 "$PROJECT_ROOT/SESSION_CONTINUITY.md"
    fi
    
    # 3. Check timing rules
    echo ""
    echo "⏰ Checking timing rules..."
    check_timing_rules
    
    # 4. Load learning files
    echo ""
    load_learning_files
    
    echo ""
    echo "✅ Ready for instructions"
}
```

### 3. Integration Instructions
```markdown
## To Enable Auto-Continuity:

1. Add SESSION_LATEST_STATE.md to the files Claude checks on boot
2. Update all task completions to call update_session_state
3. Create instruction for Claude: "Always read SESSION_LATEST_STATE.md first"

## Usage Example:
# After completing any task
update_session_state "Completed documentation update" "Added 3 guides to docs/"

# On next session start
Claude automatically reads SESSION_LATEST_STATE.md and knows:
- Last action taken
- Current context  
- Next priorities
- No manual prompting needed
```

## Testing Requirements
- Complexity score: 3
- TDD used: No
- Test pattern: Create state, close session, verify continuity

## When to Use
- After every significant action
- Before potential session ends
- When context changes significantly
- After completing TODO items

## Time Saved
Estimated: 2-5 minutes per session start
Eliminates need for manual context loading

## Variations

### Minimal State Tracker
```bash
echo "Last: ${action} at ${timestamp}" > .last_action
echo "Next: ${next_action}" >> .last_action
```

### Detailed State with Diffs
```bash
update_session_state_with_diff() {
    # Include git diff summary
    echo "### Changed Files" >> SESSION_LATEST_STATE.md
    git status --short >> SESSION_LATEST_STATE.md 2>/dev/null
}
```

## Notes
- SESSION_LATEST_STATE.md is lightweight (always overwritten)
- SESSION_CONTINUITY.md remains for full history
- Provides "at a glance" context for immediate productivity
- Should be git-ignored (changes too frequently)