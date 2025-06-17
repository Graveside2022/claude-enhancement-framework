# PROJECT-SPECIFIC BINDING DIRECTIVE FOR CLAUDE IMPROVEMENT

## PROJECT BINDING ENFORCEMENT

**THIS PROJECT CONFIGURATION EXTENDS GLOBAL RULES WITH PROJECT-SPECIFIC REQUIREMENTS.**

### PROJECT BINDING STATEMENTS:

1. **PROJECT-SPECIFIC RULES OVERRIDE GLOBAL DEFAULTS (EXCEPT SECURITY)**
2. **PATTERN CHECKING BEFORE IMPLEMENTATION IS NON-NEGOTIABLE**
3. **THE 7-STEP TESTING DECISION PROTOCOL MUST BE EXECUTED**
4. **MEMORY PERSISTENCE (SESSION_CONTINUITY.md) IS MANDATORY**
5. **THIS PROJECT BELONGS TO CHRISTIAN**

### PROJECT ENFORCEMENT:

- **PATTERN LOCK**: Always check patterns/ before writing new code (10s limit)
- **TESTING LOCK**: Execute complete 7-step testing decision before ANY code
- **MEMORY LOCK**: Update SESSION_CONTINUITY.md after EVERY action
- **PARALLEL LOCK**: Context-aware agents (boot=3, work=5), Implementation = sequential

**BY PROCESSING THIS FILE, YOU ACKNOWLEDGE PROJECT-SPECIFIC BINDING.**

---

# PROJECT MODULE LOADER - MINIMAL

## PROJECT STRUCTURE REQUIRED

```
project-root/
├── CLAUDE_MINIMAL.md (this file)
├── patterns/
│   ├── bug_fixes/
│   ├── generation/
│   ├── refactoring/
│   └── architecture/
├── memory/
│   ├── learning_archive.md
│   ├── error_patterns.md
│   └── side_effects_log.md
├── tests/
├── scripts/
└── SESSION_CONTINUITY.md
```

## PATTERN-FIRST DEVELOPMENT

**BEFORE ANY CODE:**
1. Search patterns/ (10 second limit)
2. Match >80% → Apply pattern immediately
3. Match 60-80% → Adapt pattern
4. Match <60% → Create new, capture as pattern

## 7-STEP TESTING DECISION (MANDATORY)

```python
BEFORE WRITING CODE:
1. Quick utility/learning/throwaway? → Step 6
2. Complexity ≥ 7? → TDD REQUIRED
3. Reusable/public/complex? → TDD REQUIRED
4. AI-generated review → Verify no over-engineering
5. Test if complexity > 5
6. Direct implementation (with manual testing)
7. Final validation → All code must run
```

## CONTEXT-AWARE PROJECT AGENTS

### Boot Context (3 Agents)
**Used for**: Project initialization, session continuity, pattern loading
- Agent 1: SESSION_CONTINUITY.md check and project detection
- Agent 2: Pattern library loading and validation
- Agent 3: Configuration verification and status reporting

### Work Context (5+ Agents)
**Investigation (Parallel):**
- Component Discovery
- Style Analysis  
- Test Environment
- Type System
- Utility Functions
- Integration Points
- Documentation Status

**Implementation (Sequential):**
- Component → Styles → Tests → Types → Utilities → Integration → Docs

### Context Detection for Project
- **Boot triggers**: "setup", "boot", "startup", project initialization
- **Work triggers**: "implement", "create", "analyze", "design", "investigate"
- **Override**: Manual agent count specification takes precedence

## MEMORY PERSISTENCE RULES

**UPDATE SESSION_CONTINUITY.md AFTER:**
- Every code implementation
- Pattern application/creation
- Error encounters
- Testing decisions
- Agent deployments

## PROJECT INITIALIZATION

When entering project or Christian says "setup":
1. Read SESSION_CONTINUITY.md first
2. Only if file missing/stale (>120 minutes):
   - Check patterns/ directory
   - Load memory files
   - Verify testing protocols
3. Begin work based on SESSION_CONTINUITY.md state

## QUICK PROJECT DECISION MATRIX

```python
PROJECT REQUEST
    |
    ├─> Pattern exists? → APPLY (don't recreate)
    ├─> Testing needed? → 7-STEP PROTOCOL
    ├─> Investigation? → PARALLEL AGENTS
    ├─> Implementation? → SEQUENTIAL
    └─> Action complete? → UPDATE MEMORY
```

**PROJECT MODULES**: Load from project `modules/` if present, else use these rules.

---

END OF PROJECT MINIMAL CLAUDE.md | USER: CHRISTIAN | PATTERNS FIRST