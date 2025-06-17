#!/bin/bash
# Manual Backup System for CLAUDE Projects
# Replaces automatic 120-minute backup daemon with manual commands
# User: Christian

set -e  # Exit on any error

# Function: Create standard backup
backup() {
    reason="${1:-manual}"
    date_stamp=$(date +%Y-%m-%d)

    # Find next version number for today
    version=1
    while [ -d "backups/${date_stamp}_v${version}" ]; do
        version=$((version + 1))
    done

    backup_dir="backups/${date_stamp}_v${version}"
    mkdir -p "$backup_dir"

    echo "📦 Creating standard backup: $backup_dir"

    # Copy all critical files
    for file in TODO.md CLAUDE.md HANDOFF_SUMMARY.md NEXT_SESSION_HANDOFF_PROMPT.md .project_context; do
        if [ -f "$file" ]; then
            cp "$file" "$backup_dir/"
            echo "  ✓ Copied $file"
        fi
    done

    # Create backup metadata
    {
        echo "Backup Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "User: Christian"
        echo "Project: CLAUDE Improvement"  
        echo "Backup Type: Standard Manual Backup"
        echo "Reason: ${reason}"
        echo "Version: ${date_stamp}_v${version}"
        echo "Project State:"
        echo "- Files in root: $(ls -1 | wc -l)"
        echo "- TODO.md lines: $(wc -l < TODO.md 2>/dev/null || echo "0")"
        echo "- Git status: $(git status --short 2>/dev/null | wc -l) uncommitted changes"
    } > "$backup_dir/backup_info.txt"

    # Log backup creation
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ${date_stamp}_v${version} - MANUAL STANDARD - ${reason}" >> backups/backup_log.txt

    # Prune old backups (keep last 5)
    echo "🧹 Pruning old backups (keeping last 5)..."
    ls -1dr backups/20*_v* 2>/dev/null | tail -n +6 | xargs -r rm -rf 2>/dev/null || true
    echo "✓ Kept last 5 backups"

    echo "✅ Standard backup created successfully: ${backup_dir}"
}

# Function: Create comprehensive full backup
full_backup() {
    reason="${1:-manual_full}"
    date_stamp=$(date +%Y-%m-%d)

    # Find next version number for today
    version=1
    while [ -d "backups/${date_stamp}_v${version}" ]; do
        version=$((version + 1))
    done

    backup_dir="backups/${date_stamp}_v${version}"
    mkdir -p "$backup_dir"

    echo "📦 Creating comprehensive full backup: $backup_dir"

    # Copy all critical files
    for file in TODO.md CLAUDE.md HANDOFF_SUMMARY.md NEXT_SESSION_HANDOFF_PROMPT.md .project_context; do
        if [ -f "$file" ]; then
            cp "$file" "$backup_dir/"
            echo "  ✓ Copied $file"
        fi
    done

    # Copy SESSION_CONTINUITY.md
    if [ -f SESSION_CONTINUITY.md ]; then
        cp SESSION_CONTINUITY.md "$backup_dir/"
        echo "  ✓ Copied SESSION_CONTINUITY.md"
    fi

    # Copy patterns directory
    if [ -d patterns ]; then
        cp -r patterns "$backup_dir/"
        echo "  ✓ Copied patterns/ directory ($(find patterns -name "*.md" 2>/dev/null | wc -l) patterns)"
    fi

    # Copy memory directory  
    if [ -d memory ]; then
        cp -r memory "$backup_dir/"
        echo "  ✓ Copied memory/ directory ($(find memory -name "*.md" 2>/dev/null | wc -l) memory files)"
    fi

    # Copy scripts directory
    if [ -d scripts ]; then
        cp -r scripts "$backup_dir/"
        echo "  ✓ Copied scripts/ directory"
    fi

    # Create comprehensive backup metadata
    {
        echo "Backup Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "User: Christian"
        echo "Project: CLAUDE Improvement"
        echo "Backup Type: Comprehensive Full Backup"
        echo "Reason: ${reason}"
        echo "Version: ${date_stamp}_v${version}"
        echo "Project State:"
        echo "- Files in root: $(ls -1 | wc -l)"
        echo "- TODO.md lines: $(wc -l < TODO.md 2>/dev/null || echo "0")"
        echo "- Git status: $(git status --short 2>/dev/null | wc -l) uncommitted changes"
        echo "- Patterns captured: $(find patterns -name "*.md" 2>/dev/null | wc -l)"
        echo "- Memory files: $(find memory -name "*.md" 2>/dev/null | wc -l)"
        echo "- Scripts included: $(find scripts -name "*.sh" -o -name "*.py" 2>/dev/null | wc -l)"
    } > "$backup_dir/backup_info.txt"

    # Log backup creation
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ${date_stamp}_v${version} - MANUAL FULL - ${reason}" >> backups/backup_log.txt

    # Prune old backups (keep last 5)
    echo "🧹 Pruning old backups (keeping last 5)..."
    ls -1dr backups/20*_v* 2>/dev/null | tail -n +6 | xargs -r rm -rf 2>/dev/null || true
    echo "✓ Kept last 5 backups"

    echo "✅ Comprehensive full backup created successfully: ${backup_dir}"
}

# Function: Show backup status
status() {
    echo "=== MANUAL BACKUP SYSTEM STATUS ==="
    echo "User: Christian"
    echo "Project: CLAUDE Improvement"
    echo "Backup Directory: backups/"
    echo ""
    
    if [ -d backups ]; then
        backup_count=$(ls -1d backups/20*_v* 2>/dev/null | wc -l)
        echo "📊 Total backups: $backup_count"
        
        if [ $backup_count -gt 0 ]; then
            echo "📋 Recent backups:"
            ls -1dt backups/20*_v* 2>/dev/null | head -3 | while read backup; do
                backup_name=$(basename "$backup")
                backup_size=$(du -sh "$backup" 2>/dev/null | cut -f1)
                echo "  - $backup_name ($backup_size)"
            done
        fi
        
        if [ -f backups/backup_log.txt ]; then
            echo ""
            echo "📝 Recent backup log entries:"
            tail -3 backups/backup_log.txt | sed 's/^/  /'
        fi
    else
        echo "⚠️ No backup directory found"
    fi
    
    echo ""
    echo "🔧 Available commands:"
    echo "  $0 backup [reason]       - Create standard backup"
    echo "  $0 full backup [reason]  - Create comprehensive full backup"
    echo "  $0 status               - Show backup status (this command)"
}

# Main command handling
case "${1:-}" in
    "backup")
        backup "${2:-manual}"
        ;;
    "full")
        if [ "${2:-}" = "backup" ]; then
            full_backup "${3:-manual_full}"
        else
            echo "❌ Error: Use 'full backup' for comprehensive backup"
            echo "Usage: $0 full backup [reason]"
            exit 1
        fi
        ;;
    "status")
        status
        ;;
    "")
        echo "=== MANUAL BACKUP SYSTEM ==="
        echo "User: Christian"
        echo ""
        echo "Usage:"
        echo "  $0 backup [reason]       - Create standard backup in /backups"
        echo "  $0 full backup [reason]  - Create comprehensive backup in /backups"
        echo "  $0 status               - Show backup system status"
        echo ""
        echo "Examples:"
        echo "  $0 backup"
        echo "  $0 backup 'before major changes'"
        echo "  $0 full backup"
        echo "  $0 full backup 'weekly comprehensive backup'"
        ;;
    *)
        echo "❌ Error: Unknown command '$1'"
        echo "Use '$0' without arguments to see usage information"
        exit 1
        ;;
esac