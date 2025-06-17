#!/bin/bash
# Full Backup System for CLAUDE Projects
# Implements the complete backup functionality from CLAUDE.md

# Full backup function with all features
create_backup() {
    reason="${1:-routine}"
    date_stamp=$(date +%Y-%m-%d)

    # Find next version number for today
    version=1
    while [ -d "backups/${date_stamp}_v${version}" ]; do
        version=$((version + 1))
    done

    backup_dir="backups/${date_stamp}_v${version}"
    mkdir -p "$backup_dir"

    # Copy all critical files
    for file in TODO.md CLAUDE.md HANDOFF_SUMMARY.md NEXT_SESSION_HANDOFF_PROMPT.md .project_context; do
        [ -f "$file" ] && cp "$file" "$backup_dir/"
    done

    # Create backup metadata
    cat > "$backup_dir/backup_info.txt" << EOF
Backup Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Reason: ${reason}
Version: ${date_stamp}_v${version}
Project State:
- Files in root: $(ls -1 | wc -l)
- TODO.md lines: $(wc -l < TODO.md 2>/dev/null || echo "0")
- Git status: $(git status --short 2>/dev/null | wc -l) uncommitted changes
EOF

    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ${date_stamp}_v${version} - ${reason}" >> backups/backup_log.txt

    # PRUNING: Keep the last 5 backups
    echo "🧹 Pruning old backups (keeping last 5)..."
    ls -1dr backups/20*_v* 2>/dev/null | tail -n +6 | xargs -r rm -rf 2>/dev/null || true
    echo "✓ Kept last 5 backups"

    echo "✓ Backup created: ${backup_dir}"
}

# Project-specific backup with patterns and memory
create_project_backup() {
    reason="${1:-routine}"
    
    # Call base backup function
    create_backup "$reason"
    
    # Get the backup directory that was just created
    date_stamp=$(date +%Y-%m-%d)
    version=$(ls -d backups/${date_stamp}_v* 2>/dev/null | wc -l)
    backup_dir="backups/${date_stamp}_v${version}"
    
    # Additionally backup patterns and memory
    [ -d "patterns" ] && cp -r "patterns" "$backup_dir/"
    [ -d "memory" ] && cp -r "memory" "$backup_dir/"
    [ -f "SESSION_CONTINUITY.md" ] && cp "SESSION_CONTINUITY.md" "$backup_dir/"
    
    # Update backup info with pattern stats
    echo "Patterns captured: $(find patterns -name "*.md" 2>/dev/null | wc -l)" >> "$backup_dir/backup_info.txt"
    echo "Memory files: $(find memory -name "*.md" 2>/dev/null | wc -l)" >> "$backup_dir/backup_info.txt"
}

# Scheduled backup check (disabled - use manual backup system)
check_scheduled_backup() {
    echo "⚠️ Automatic backup scheduling has been disabled."
    echo "💾 Use manual backup system instead:"
    echo "    scripts/manual_backup.sh backup           - Standard backup"
    echo "    scripts/manual_backup.sh full backup      - Comprehensive backup"
    echo "    scripts/manual_backup.sh status           - Check backup status"
    
    # Ensure backup directory exists for manual backups
    if [ ! -d "backups" ]; then
        mkdir -p backups
        echo "✓ Created backups directory for manual backup system"
    fi
    
    return 1  # Always return failure to prevent automatic execution
}

# Backup integrity verification
verify_backup_integrity() {
    local backup_dir="$1"
    
    if [ -z "$backup_dir" ] || [ ! -d "$backup_dir" ]; then
        echo "❌ Error: Invalid backup directory"
        return 1
    fi
    
    echo "🔍 Verifying backup integrity: $backup_dir"
    
    local verification_passed=true
    local critical_files=("TODO.md" "CLAUDE.md")
    
    for file in "${critical_files[@]}"; do
        if [ -f "$backup_dir/$file" ]; then
            # Compare file sizes
            if [ -f "$file" ]; then
                local orig_size=$(stat -c %s "$file" 2>/dev/null || stat -f %z "$file")
                local backup_size=$(stat -c %s "$backup_dir/$file" 2>/dev/null || stat -f %z "$backup_dir/$file")
                
                if [ "$orig_size" -eq "$backup_size" ]; then
                    echo "✓ $file - Size matches"
                else
                    echo "✗ $file - Size mismatch"
                    verification_passed=false
                fi
            fi
        else
            echo "✗ $file - Missing from backup"
            verification_passed=false
        fi
    done
    
    if [ "$verification_passed" = true ]; then
        echo "✅ Backup verification passed"
        return 0
    else
        echo "❌ Backup verification failed"
        return 1
    fi
}

# Export functions
export -f create_backup
export -f create_project_backup
export -f check_scheduled_backup
export -f verify_backup_integrity

# If run directly, show usage
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    echo "Backup System Functions Available:"
    echo "  create_backup [reason] - Create basic backup"
    echo "  create_project_backup [reason] - Create full project backup"
    echo "  check_scheduled_backup - Check if 120-minute backup is due"
    echo "  verify_backup_integrity [backup_dir] - Verify backup integrity"
fi