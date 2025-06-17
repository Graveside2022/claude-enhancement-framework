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
- **PARALLEL LOCK**: Investigation = parallel agents, Implementation = sequential

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

## PROJECT-SPECIFIC AGENTS

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

## MEMORY PERSISTENCE RULES

**UPDATE SESSION_CONTINUITY.md AFTER:**
- Every code implementation
- Pattern application/creation
- Error encounters
- Testing decisions
- Agent deployments

## PROJECT INITIALIZATION

When entering project or Christian says "setup":
1. Execute `initialize_project_structure()`
2. Check patterns/ directory
3. Load memory files
4. Verify testing protocols
5. Begin work with pattern search

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