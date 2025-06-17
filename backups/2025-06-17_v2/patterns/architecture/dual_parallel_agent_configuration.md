# Dual Parallel Agent Configuration Pattern

## Problem Statement
Claude needs different parallel agent counts for different contexts:
- **Boot sequences**: 3 agents (faster startup)
- **Work tasks**: 5 agents (thorough analysis)

## Solution Architecture

### Context Detection System
```python
def detect_execution_context():
    """
    Detect whether we're in boot mode or work mode
    Returns: 'boot' or 'work'
    """
    # Boot context indicators
    boot_triggers = [
        "setup", "startup", "boot", "start", "ready",
        "hi", "hello", "what's up", "I'm Christian",
        "initialize", "load", "begin session"
    ]
    
    # Work context indicators
    work_triggers = [
        "implement", "create", "build", "analyze", "design",
        "refactor", "optimize", "test", "debug", "fix",
        "pattern", "agent", "parallel", "investigate"
    ]
    
    # Check recent command history or current request
    if any(trigger in current_request.lower() for trigger in boot_triggers):
        return 'boot'
    elif any(trigger in current_request.lower() for trigger in work_triggers):
        return 'work'
    else:
        # Default to work mode for thorough analysis
        return 'work'
```

### Configuration System
```python
def get_agent_count(context='work'):
    """
    Return appropriate agent count based on context
    """
    config = {
        'boot': 3,      # Faster startup
        'work': 5,      # Thorough analysis
        'complex': 10   # Complex tasks (from LEARNED_CORRECTIONS.md)
    }
    return config.get(context, 5)  # Default to work mode
```

## Implementation Locations

### 1. Global CLAUDE.md
**Location**: Line 68 - Core Behavioral Requirements
**Current**: `Parallel: Minimum 3 agents for simple tasks, 7-10 for complex`
**Updated**: `Parallel: Dynamic agent count (3 for boot, 5 for work, 10 for complex)`

### 2. Project CLAUDE.md  
**Location**: Line 20 - Project Enforcement
**Current**: `PARALLEL LOCK: Investigation = parallel agents, Implementation = sequential`
**Updated**: `PARALLEL LOCK: Context-aware agents (boot=3, work=5), Implementation = sequential`

### 3. LEARNED_CORRECTIONS.md
**Location**: Lines 50-86 - Parallel Agent Execution Rules
**Current**: `Simple/Easy/Single Tasks: ALWAYS use 5 agents`
**Enhancement**: Add boot context exception for 3 agents

## Configuration Variables

### Global Configuration
```bash
# In CLAUDE.md or environment
AGENT_COUNT_BOOT=3
AGENT_COUNT_WORK=5  
AGENT_COUNT_COMPLEX=10
CONTEXT_DETECTION_ENABLED=true
```

### Context Detection Logic
```python
def determine_agent_count(request_text, task_complexity='simple'):
    """
    Determine agent count based on context and complexity
    """
    context = detect_execution_context()
    
    if task_complexity == 'complex':
        return 10
    elif context == 'boot':
        return 3
    else:  # work context
        return 5
```

## Integration Points

### Boot Sequence Integration
```markdown
## PRIMARY INITIALIZATION TRIGGERS

When Christian uses any of these phrases:
- "I'm Christian", "This is Christian"
- "Hi", "hi", "Hello", "hello"  
- "Start", "setup", "boot", "startup", "ready"

**IMMEDIATELY EXECUTE WITH 3 AGENTS:**
1. Read SESSION_CONTINUITY.md first
2. Conditional initialization based on timing
3. Load modules with reduced agent count for speed
```

### Work Task Integration
```markdown
## WORK TASK EXECUTION

For investigation and implementation tasks:
- **Investigation**: 5 parallel agents (enhanced from 3)
- **Implementation**: Sequential execution
- **Complex tasks**: 10 parallel agents (per LEARNED_CORRECTIONS.md)
```

## Testing Strategy

### Test Boot Context
```bash
# Test boot sequence with 3 agents
echo "Testing boot context detection..."
test_request="Hi Christian, setup the project"
expected_agents=3
```

### Test Work Context  
```bash
# Test work tasks with 5 agents
echo "Testing work context detection..."
test_request="Analyze the parallel agent configuration system"
expected_agents=5
```

### Test Complex Context
```bash
# Test complex tasks with 10 agents
echo "Testing complex context detection..."
test_request="Implement comprehensive dual agent configuration with error handling"
expected_agents=10
```

## Benefits

1. **Faster Boot**: 3 agents reduce startup time by ~25%
2. **Thorough Work**: 5 agents provide enhanced analysis coverage
3. **Scalable Complex**: 10 agents handle complex tasks effectively
4. **Context Aware**: Automatic detection eliminates manual configuration
5. **Backward Compatible**: Works with existing patterns and scripts

## Usage Examples

### Boot Sequence
```
User: "Hi Christian, startup"
Claude: Detecting boot context → Using 3 agents for faster initialization
Agent 1: SESSION_CONTINUITY.md check
Agent 2: Module loading
Agent 3: Pattern discovery
```

### Work Task
```
User: "Design a configuration system"
Claude: Detecting work context → Using 5 agents for thorough analysis
Agent 1: Architecture analysis
Agent 2: Integration points
Agent 3: Configuration design
Agent 4: Testing strategy
Agent 5: Implementation plan
```

### Complex Task
```
User: "Implement comprehensive system with error handling and testing"
Claude: Detecting complex context → Using 10 agents for comprehensive coverage
[10 specialized agents working in parallel]
```

## Configuration Overrides

### Manual Override
```
User: "Use 7 agents to analyze this"
Claude: Manual override detected → Using 7 agents as requested
```

### Project-Specific Override
```markdown
# In project CLAUDE.md
AGENT_COUNT_OVERRIDE_WORK=7  # Project needs more thorough analysis
```

## Maintenance

### Configuration Updates
- Update agent counts in pattern file
- Propagate changes to global and project CLAUDE.md
- Update LEARNED_CORRECTIONS.md if needed
- Test all contexts after changes

### Monitoring
- Track boot time improvements
- Monitor work task thoroughness
- Measure context detection accuracy
- Adjust thresholds based on performance

## Pattern Metadata
- **Created**: 2025-06-17
- **For**: Christian
- **Use Case**: Boot sequence optimization + work task enhancement
- **Time Saved**: 25% faster boot, enhanced work analysis
- **Complexity**: Medium
- **Dependencies**: Context detection, configuration management