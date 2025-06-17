# Claude Improvement Project Configuration

## Project Settings
- **Owner**: Christian
- **Type**: Claude optimization and memory improvement
- **Priority**: Pattern-first development, comprehensive testing

## Core Requirements
- Check patterns/ directory before new implementations
- Execute testing protocol for complex code
- Update SESSION_CONTINUITY.md after actions

---

# Development Workflow

## Project Structure
```
project-root/
├── CLAUDE.md (project config)
├── patterns/ (reusable code patterns)
├── memory/ (session persistence)
├── tests/ (test files)
└── SESSION_CONTINUITY.md (session state)
```

## Pattern-First Development

### Before Implementation
1. Search patterns/ directory (quick check)
2. **High match (>80%)**: Apply existing pattern
3. **Medium match (60-80%)**: Adapt existing pattern  
4. **Low match (<60%)**: Create new pattern, save for reuse

## Testing Decision Protocol

### Testing Requirements
- **Simple utilities**: Manual testing acceptable
- **Complex logic (>5 complexity)**: Write tests
- **Reusable components**: Test-driven development
- **Public APIs**: Comprehensive test coverage

### Validation Steps
1. Code review for over-engineering
2. Manual testing for basic functionality
3. All implementations must execute successfully

## ABSOLUTE BINDING AGENT EXECUTION RULES - PROJECT OVERRIDE

### MANDATORY PARALLEL EXECUTION - NEVER SEQUENTIAL
**PROJECT-SPECIFIC ABSOLUTE BINDING CONSTRAINTS:**

1. **SIMPLE TASKS**: 5 agents in parallel - SEQUENTIAL EXECUTION FORBIDDEN
2. **COMPLEX TASKS**: 10 agents in parallel - SEQUENTIAL EXECUTION FORBIDDEN
3. **ALL CONTEXTS**: Parallel execution mandatory - Never use sequential processing
4. **TASK DEPLOYMENT**: ALL agents must be deployed in ONE message
5. **COMPLIANCE REQUIRED**: Document parallel execution in every response

### BINDING AGENT ALLOCATION
- **Boot/Setup**: 5 parallel agents (ONE message with 5 Task invocations)
  - Session continuity check
  - Pattern library loading
  - Configuration verification
  - Cache system validation
  - Context detection setup

- **Investigation**: 5 parallel agents (ONE message with 5 Task invocations)
  - Component analysis
  - Environment setup
  - Integration points
  - Documentation review
  - Performance monitoring

- **Implementation**: 5-10 parallel agents (ONE message with 5-10 Task invocations)
  - Component development
  - Test implementation
  - Integration setup
  - Documentation updates
  - Performance validation

### SEQUENTIAL EXECUTION PROHIBITION
- **FORBIDDEN**: Using agents one after another
- **FORBIDDEN**: Single agent processing for multi-step tasks
- **REQUIRED**: All agents deployed simultaneously in parallel
- **REQUIRED**: Detailed report of each agent's achievements

## Memory Management

### Session Persistence
Update SESSION_CONTINUITY.md after:
- Code implementations
- Pattern applications
- Error resolutions
- Testing decisions

### Project Initialization
On setup command:
1. Check SESSION_CONTINUITY.md status
2. Load patterns/ if stale (>120 minutes)
3. Verify test environment
4. Begin work from saved state

## Command Reference

### For Christian
- **"setup"** or **"boot"**: Initialize project with 5 parallel agents
- **"investigate [area]"**: Parallel analysis with 5 agents
- **"implement [feature]"**: Parallel development with 5 agents
- **"use X agents"**: Override default agent count (supports 5-10 agents)
- **"handoff"**: Update SESSION_CONTINUITY.md with handoff information
- **"checkpoint"**: Update SESSION_CONTINUITY.md with checkpoint information

### Manual Backup System
- **`scripts/manual_backup.sh backup`**: Create standard backup
- **`scripts/manual_backup.sh full backup`**: Create comprehensive backup
- **`scripts/manual_backup.sh status`**: Check backup status

---

END PROJECT CLAUDE.md | USER: CHRISTIAN