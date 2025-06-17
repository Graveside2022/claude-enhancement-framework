# File Organization Enforcement Pattern

## Problem
Files being created directly in project root instead of organized directory structure, causing clutter and making project navigation difficult.

## Solution
**MANDATORY ENFORCEMENT**: Always use the organized directory structure and NEVER create files directly in project root except for the 4 core files.

## Core Files ONLY in Root Directory
**ONLY these 4 files belong in project root:**
1. `CLAUDE.md` - Project configuration
2. `TODO.md` - Task tracking  
3. `SESSION_CONTINUITY.md` - Session memory
4. `README.md` - Project documentation

## Organized Directory Structure

### reports/ - All Reports and Documentation
- `reports/analysis/` - Analysis, investigation, research reports
- `reports/implementation/` - Implementation and integration reports  
- `reports/handoff/` - Session handoff and transition files
- `reports/session/` - Session checkpoints and continuity
- `reports/backup/` - Backup status and verification reports
- `reports/completion/` - Task completion and summary reports
- `reports/archive/` - Historical reports (30+ days old)

### Other Organized Directories
- `tests/` - All test scripts (test_*.sh, test_*.py)
- `scripts/` - All Python scripts and utilities
- `config/` - Configuration files (*.json, *requirements.txt)
- `logs/` - Log files (*.log)
- `patterns/` - Reusable patterns and templates
- `memory/` - Learning and memory files
- `docs/` - Additional documentation
- `backups/` - Backup files and corrupted file quarantine

## Implementation

### MANDATORY File Creation Check:
```bash
# BEFORE creating ANY file, determine proper location
determine_file_location() {
    local filename="$1"
    local target_dir
    
    case "$filename" in
        # Core files - ONLY these stay in root
        "CLAUDE.md"|"TODO.md"|"SESSION_CONTINUITY.md"|"README.md")
            target_dir="./"
            ;;
        # Reports - MUST go in reports/ subdirectories
        *REPORT*.md|*ANALYSIS*.md|*INVESTIGATION*.md|*RESEARCH*.md)
            target_dir="reports/analysis/"
            ;;
        *IMPLEMENTATION*.md|*INTEGRATION*.md)
            target_dir="reports/implementation/"
            ;;
        *HANDOFF*.md|*SESSION_END*.md|*EMERGENCY*.md|*TRANSITION*.md)
            target_dir="reports/handoff/"
            ;;
        *CHECKPOINT*.md|*SESSION*.md|*CONTINUITY*.md)
            target_dir="reports/session/"
            ;;
        *BACKUP*.md|*RESTORE*.md|*VERIFICATION*.md)
            target_dir="reports/backup/"
            ;;
        *COMPLETION*.md|*SUMMARY*.md|*FINISHED*.md)
            target_dir="reports/completion/"
            ;;
        # Scripts and tests
        test_*.sh|test_*.py|*_test.*)
            target_dir="tests/"
            ;;
        *.py)
            target_dir="scripts/"
            ;;
        # Configuration
        *.json|*requirements*.txt|*config*.*)
            target_dir="config/"
            ;;
        # Logs
        *.log)
            target_dir="logs/"
            ;;
        # Backup/corrupted files  
        *.backup.*|*.bak|*.corrupted)
            target_dir="backups/corrupted_files/"
            ;;
        *)
            echo "⚠️ UNKNOWN FILE TYPE: $filename - defaulting to appropriate category"
            target_dir="reports/misc/"
            ;;
    esac
    
    echo "$target_dir"
}

# MANDATORY enforcement function
enforce_file_organization() {
    local filename="$1"
    local content="$2"
    local target_dir=$(determine_file_location "$filename")
    
    # Create directory if needed
    mkdir -p "$target_dir"
    
    # Place file in proper location
    local full_path="${target_dir}${filename}"
    echo "$content" > "$full_path"
    
    echo "✅ File created: $full_path"
    return 0
}
```

### MANDATORY Usage:
```bash
# Instead of: cat > SOME_REPORT.md
# Use: enforce_file_organization "ANALYSIS_REPORT.md" "$content"

# Instead of: echo "content" > test_script.py  
# Use: enforce_file_organization "test_script.py" "$content"
```

## Auto-Cleanup Function
```bash
# Run this if files end up in wrong locations
organize_misplaced_files() {
    echo "🧹 Organizing misplaced files..."
    
    # Move by file patterns
    for file in test_*.sh test_*.py *_test.*; do [ -f "$file" ] && mv "$file" tests/; done
    for file in *.json *requirements*.txt; do [ -f "$file" ] && mv "$file" config/; done  
    for file in *.log; do [ -f "$file" ] && mv "$file" logs/; done
    for file in *.py; do [ -f "$file" ] && [[ "$file" != "tests/"* ]] && mv "$file" scripts/; done
    for file in *.backup.* *.bak *.corrupted; do [ -f "$file" ] && mkdir -p backups/corrupted_files && mv "$file" backups/corrupted_files/; done
    
    # Move reports by content/name patterns
    for file in *REPORT*.md *ANALYSIS*.md *INVESTIGATION*.md; do [ -f "$file" ] && mv "$file" reports/analysis/; done
    for file in *IMPLEMENTATION*.md *INTEGRATION*.md; do [ -f "$file" ] && mv "$file" reports/implementation/; done
    for file in *HANDOFF*.md *SESSION_END*.md *EMERGENCY*.md; do [ -f "$file" ] && mv "$file" reports/handoff/; done
    for file in *CHECKPOINT*.md *SESSION*.md; do [ -f "$file" ] && [[ "$file" != "SESSION_CONTINUITY.md" ]] && mv "$file" reports/session/; done
    for file in *BACKUP*.md *RESTORE*.md; do [ -f "$file" ] && mv "$file" reports/backup/; done
    for file in *COMPLETION*.md *SUMMARY*.md; do [ -f "$file" ] && mv "$file" reports/completion/; done
    
    echo "✅ Files organized into proper directories"
}
```

## Enforcement Rules (MANDATORY)
1. **NEVER create files directly in project root** except core files
2. **ALWAYS use `enforce_file_organization()` function** for file creation  
3. **AUTO-CLEANUP**: Run `organize_misplaced_files()` if violations detected
4. **BOOT CHECK**: Verify root directory only has 4 core files on session start
5. **PATTERN FIRST**: Check this pattern before any file creation

## Detection and Prevention
- **Boot Sequence**: Check root directory file count (should be ≤ 4)
- **File Creation**: Use organized functions instead of direct creation
- **Auto-Organization**: Automatically move misplaced files to proper locations
- **Warning System**: Alert when files are created in wrong locations

## Time Saved  
- **File organization**: 5-10 minutes per session
- **Project navigation**: 2-3 minutes per search  
- **Maintenance cleanup**: 15-20 minutes per cleanup
- **Total efficiency gain**: 22-33 minutes per session

## Success Metrics
- ✅ Root directory contains exactly 4 files
- ✅ All reports in organized subdirectories  
- ✅ All tests in tests/ directory
- ✅ All scripts in scripts/ directory
- ✅ All config in config/ directory
- ✅ Zero cleanup time needed