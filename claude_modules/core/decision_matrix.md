# DECISION MATRIX - CORE MODULE

## MASTER DECISION MATRIX - PRIMARY ROUTER

When Christian provides ANY input, follow this sequence:

### LEVEL 0: MODULE LOADING DECISION

```python
INPUT RECEIVED FROM CHRISTIAN
    |
    ├─> Check MODULE_INDEX.md for task mapping
    ├─> Identify required modules
    ├─> Load modules in dependency order
    └─> Continue to LEVEL 1
```

### LEVEL 1: INITIALIZATION CHECK

```python
Is this an INITIALIZATION TRIGGER?
    ├─> Triggers: "Hi", "start", "setup", "ready", etc.
    ├─> YES: Load modules/initialization_triggers.md
    └─> NO: Continue to LEVEL 2
```

### LEVEL 2: ERROR DETECTION

```python
Does this indicate an error?
    ├─> YES: Load modules/error_learning_system.md
    └─> NO: Continue to LEVEL 3
```

### LEVEL 3: TIMING CHECKS

```python
Are timing rules due?
    ├─> YES: Load modules/timing_enforcement.md
    └─> NO: Continue to LEVEL 4
```

### LEVEL 4: TASK ROUTING

```python
What type of request is this?
    ├─> Technical/Code: Load coding_directives.md
    ├─> Investigation: Load parallel_execution.md
    ├─> Project Work: Load project_hierarchy.md
    └─> General: Load behavioral_framework.md
```

### MODULE LOADING RULES:

1. **Lazy Loading**: Only load modules needed for current task
2. **Dependency Order**: Load dependencies before dependent modules
3. **Caching**: Keep frequently used modules in memory
4. **Efficiency**: Minimize total modules loaded per request

**ROUTING MATRIX ACTIVE**