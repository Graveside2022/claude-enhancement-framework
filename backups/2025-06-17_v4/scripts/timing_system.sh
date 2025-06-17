#!/bin/bash
# Minimal Timing Verification System for CLAUDE
# Preserves the mandatory 120-minute rule enforcement

# Core timing check function - MUST be called on every interaction
check_timing_rules() {
    echo "⏰ Checking 120-minute timing rules..."
    
    # 1. TODO.md Age Check (120-minute rule)
    if [ -f "TODO.md" ]; then
        last_modified=$(stat -c %Y TODO.md 2>/dev/null || stat -f %m TODO.md)
        current_time=$(date +%s)
        age_minutes=$(( (current_time - last_modified) / 60 ))
        
        if [ $age_minutes -gt 120 ]; then
            echo "⏰ TODO.md is ${age_minutes} minutes old - UPDATING NOW"
            echo -e "\n## Update - $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> TODO.md
            echo "User: Christian" >> TODO.md
            echo "Progress: [Active task status]" >> TODO.md
        fi
    else
        # Create TODO.md if missing
        create_todo_file
    fi
    
    # 2. Backup system (manual backup available)
    echo "💾 Manual backup system active"
    echo "    Run 'scripts/manual_backup.sh backup' for standard backup"
    echo "    Run 'scripts/manual_backup.sh full backup' for comprehensive backup"
}

# Minimal backup function
create_minimal_backup() {
    reason="${1:-routine}"
    date_stamp=$(date +%Y-%m-%d)
    version=1
    
    while [ -d "backups/${date_stamp}_v${version}" ]; do
        version=$((version + 1))
    done
    
    backup_dir="backups/${date_stamp}_v${version}"
    mkdir -p "$backup_dir"
    
    # Copy only critical files
    for file in TODO.md CLAUDE.md SESSION_CONTINUITY.md; do
        [ -f "$file" ] && cp "$file" "$backup_dir/"
    done
    
    # Minimal metadata
    echo "Backup: $(date -u +%Y-%m-%dT%H:%M:%SZ) - ${reason}" > "$backup_dir/backup_info.txt"
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ${backup_dir} - ${reason}" >> backups/backup_log.txt
}

# Create initial TODO.md
create_todo_file() {
    cat > TODO.md << 'EOF'
# TODO.md
Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## CURRENT SPRINT
- [ ] Active tasks

## COMPLETED THIS SESSION
- [x] Created TODO.md

## BACKLOG
- [ ] Pending tasks
EOF
}

# Export function for use in CLAUDE.md
export -f check_timing_rules
export -f create_minimal_backup

# If run directly, execute timing check
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    check_timing_rules
fi