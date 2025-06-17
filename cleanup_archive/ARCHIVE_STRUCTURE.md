# Cleanup Archive Structure

## Created: 2025-06-17

## Purpose
This directory serves as an archive for old analysis reports, performance logs, validation reports, and temporary files that were cluttering the project root.

## Directory Structure
```
cleanup_archive/
├── analysis_reports/      # Old comprehensive analysis and system reports
├── performance_logs/      # Performance tests, benchmarks, and optimization reports
├── validation_reports/    # Validation results, test reports, and verification files
├── integration_reports/   # Integration testing reports and coordination files
└── temp_files/           # Temporary files, cache files, and development artifacts
```

## What Gets Archived Here
- Old analysis reports (AGENT_*, COMPREHENSIVE_*, ANALYSIS_*)
- Performance logs and benchmark results
- Validation reports and test results  
- Integration test reports
- Temporary cache files
- Development artifacts and demo files
- Old optimization reports

## What Stays in Project Root
- `CLAUDE.md` - Current project configuration
- `SESSION_CONTINUITY.md` - Current session state  
- `TODO.md` - Current task list
- `README.md` - Project documentation
- `.claude_session_state.json` - Active session state

## What Is Never Moved Here
- Any files containing "SESSION_CONTINUITY" in the name
- Current operational configuration files
- Active memory files in `memory/` directory
- Patterns in `patterns/` directory  
- Scripts in `scripts/` directory
- Source code in `src/` directory
- Backup directories and their contents

## Maintenance
This archive can be periodically cleaned to remove very old files, but should preserve recent development history for debugging and reference purposes.