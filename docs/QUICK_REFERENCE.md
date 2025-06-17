# Quick Reference - Claude Enhanced Capabilities

## Key Functions

### Find Project Root
```bash
PROJECT_ROOT=$(find_project_root)
```
- Returns: Path to project root directory
- Fallback: Current directory if not found
- Works from: Any subdirectory

### Load Learning Files
```bash
load_learning_files
```
- Loads: Global + project learning files
- Silent: Missing files are OK
- Output: Status messages for loaded files

## Directory Structure

```
project-root/
├── CLAUDE.md           # Project configuration (primary marker)
├── SESSION_CONTINUITY.md
├── memory/             # Project learning files
│   ├── learning_archive.md
│   ├── error_patterns.md
│   └── side_effects_log.md
├── patterns/           # Reusable patterns
│   ├── generation/     # Including new detection patterns
│   └── ...
└── backups/           # Versioned backups
```

## Global Files Location

```
~/.claude/
├── CLAUDE.md          # Global configuration
├── LEARNED_CORRECTIONS.md
├── PYTHON_LEARNINGS.md
├── INFRASTRUCTURE_LEARNINGS.md
└── PROJECT_SPECIFIC_LEARNINGS.md
```

## Common Commands

### Test the System
```bash
# Test project detection
./test_project_detection.sh

# Test learning file loading  
./test_learning_file_loading.sh
```

### Work from Any Directory
```bash
# Old way (had to be in root)
cd /path/to/project
# Claude operations...

# New way (works from anywhere)
cd /path/to/project/src/deep/nested
# Claude operations work the same!
```

## Pattern Usage

### Apply Project Detection Pattern
```bash
# Pattern location
patterns/generation/project_detection_pattern.md

# Copy the template code
# Customize markers if needed
# Integrate into your scripts
```

### Initialize New Project
```bash
# Use the initialization pattern
patterns/generation/project_initialization_pattern.md

# Creates all required directories
# Sets up memory system
# Initializes backup markers
```

## Troubleshooting Checklist

- [ ] Project has `CLAUDE.md` file?
- [ ] Within 20 directories of root?
- [ ] File permissions OK?
- [ ] Global ~/.claude/ exists?
- [ ] Test scripts pass?

## Time Savings

- Project detection: 10-15 min/use
- Learning file loading: 5-10 min/session  
- Project initialization: 20-30 min/project
- **Total**: 35-55 minutes per project setup

---
Quick reference created by Christian
Last updated: 2025-06-16