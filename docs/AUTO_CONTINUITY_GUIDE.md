# Auto-Continuity System Guide

## Overview

The auto-continuity system eliminates the need for manual handoff procedures. Claude now automatically maintains and reads session state.

## How It Works

### 1. Automatic State Updates
After every significant action, Claude updates `SESSION_LATEST_STATE.md` with:
- What was just done
- Current context
- Next steps

### 2. Automatic State Reading
When you start a new session, Claude automatically:
- Detects project root
- Reads `SESSION_LATEST_STATE.md` if it exists
- Knows exactly where you left off

### 3. No Manual Steps Required
You can now:
- Close sessions without handoff procedures
- Start new sessions without prompt templates
- Just start giving instructions immediately

## File Structure

```
Only 2 continuity files now:
├── SESSION_LATEST_STATE.md  # Auto-updated, auto-read (lightweight)
└── SESSION_CONTINUITY.md     # Full history (for reference if needed)

Manual handoff files (only if explicitly requested):
├── HANDOFF_SUMMARY.md
└── NEXT_SESSION_HANDOFF_PROMPT.md
```

## Benefits

1. **Reduced Token Usage**: Only reads one lightweight file
2. **Zero Friction**: No manual steps between sessions
3. **Always Current**: Updates after every action
4. **Less Confusion**: Single source of truth for current state

## Testing

To test the system:
1. Close this session (no handoff needed)
2. Start a new session
3. Simply say "continue working"
4. Claude should know exactly where you left off

## Implementation Details

Added to global `~/.claude/CLAUDE.md`:
- Line 14: Binding statement #6 (mandatory updates)
- Lines 1050-1076: `update_session_state()` function
- Lines 1090-1096: Auto-read instruction

Total impact: Only 33 lines added, no existing code modified.

---
Created by: Christian
Date: 2025-06-16
Purpose: Document the new auto-continuity system