# INITIALIZATION TRIGGERS - CORE MODULE

## INITIALIZATION TRIGGER DETECTION

### TRIGGER PHRASES (HIGHEST PRIORITY)

```python
INITIALIZATION_TRIGGERS = [
    "i'm christian", "this is christian",
    "hi", "hello", "hey",
    "start", "setup", "boot", "startup",
    "ready", "bootup", "boot up",
    "whats up", "what's up"
]
```

### INITIALIZATION SEQUENCE

When trigger detected:

1. **IMMEDIATE ACTIONS**:
   ```bash
   # Load required modules
   LOAD modules/identity_verification.md
   LOAD modules/timing_enforcement.md
   LOAD functions/initialization.sh
   ```

2. **EXECUTE FUNCTIONS**:
   ```bash
   initialize_global_structure()
   load_learning_files()
   check_120_minute_timing_rules()
   ```

3. **PROJECT DISCOVERY**:
   - Detect project type
   - Check for CLAUDE.md
   - Initialize project structure

### OVERRIDE RULES

**CRITICAL**: Initialization triggers OVERRIDE:
- TodoRead requests
- Partial operations
- Cached responses

### MODULE DEPENDENCIES

Required modules for initialization:
- `identity_verification.md` (8KB)
- `timing_enforcement.md` (12KB)
- `functions/initialization.sh` (4KB)
- `functions/learning_files.sh` (3KB)

Total initialization load: ~27KB (vs 149KB full system)

**INITIALIZATION SYSTEM READY**