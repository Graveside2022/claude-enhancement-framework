#\!/bin/bash

# Test actual enforcement of 120-minute rules

echo "=== TESTING TIMING RULE ENFORCEMENT ==="
echo "User: Christian"
echo ""

# Function that enforces timing rules
enforce_timing_rules() {
    local enforced_actions=0
    
    # TODO.md enforcement
    if [ -f "TODO.md" ]; then
        local last_modified=$(stat -c %Y TODO.md 2>/dev/null || stat -f %m TODO.md)
        local current_time=$(date +%s)
        local age_minutes=$(( (current_time - last_modified) / 60 ))
        
        if [ $age_minutes -gt 120 ]; then
            echo "⏰ ENFORCING: TODO.md update (was $age_minutes minutes old)"
            echo -e "\n## Timing Rule Update - $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> TODO.md
            echo "User: Christian" >> TODO.md
            echo "Auto-updated due to 120-minute rule violation" >> TODO.md
            echo "✅ TODO.md updated"
            enforced_actions=$((enforced_actions + 1))
        fi
    else
        echo "⏰ ENFORCING: TODO.md creation"
        cat > TODO.md << EOFTODO
# TODO.md - Development Pipeline
Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## PROJECT TYPE
CLAUDE Improvement Testing

## CURRENT SPRINT
- [ ] Test timing rule enforcement

## AUTO-CREATED
This file was created by 120-minute rule enforcement
EOFTODO
        echo "✅ TODO.md created"
        enforced_actions=$((enforced_actions + 1))
    fi
    
    # Backup enforcement
    mkdir -p backups
    if [ -f "backups/.last_scheduled_backup" ]; then
        local last_backup=$(stat -c %Y backups/.last_scheduled_backup 2>/dev/null || stat -f %m backups/.last_scheduled_backup)
        local current_time=$(date +%s)
        local backup_age_minutes=$(( (current_time - last_backup) / 60 ))
        
        if [ $backup_age_minutes -ge 120 ]; then
            echo "⏰ ENFORCING: Backup creation (was $backup_age_minutes minutes old)"
            
            # Simple backup simulation
            date_stamp=$(date +%Y-%m-%d)
            version=1
            while [ -d "backups/${date_stamp}_v${version}" ]; do
                version=$((version + 1))
            done
            
            backup_dir="backups/${date_stamp}_v${version}"
            mkdir -p "$backup_dir"
            
            # Copy critical files
            [ -f "TODO.md" ] && cp TODO.md "$backup_dir/"
            [ -f "CLAUDE.md" ] && cp CLAUDE.md "$backup_dir/"
            
            # Update marker
            touch backups/.last_scheduled_backup
            echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Created backup: ${backup_dir} (120-minute rule)" >> backups/backup_log.txt
            
            echo "✅ Backup created: $backup_dir"
            enforced_actions=$((enforced_actions + 1))
        fi
    else
        echo "⏰ ENFORCING: Backup system initialization"
        touch backups/.last_scheduled_backup
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Backup system initialized (120-minute rule)" > backups/backup_log.txt
        echo "✅ Backup system initialized"
        enforced_actions=$((enforced_actions + 1))
    fi
    
    echo ""
    echo "📊 ENFORCEMENT SUMMARY:"
    echo "   Actions enforced: $enforced_actions"
    
    return $enforced_actions
}

# Run enforcement
echo "Before enforcement:"
./check_120_minute_timing_rules.sh

echo ""
echo "EXECUTING ENFORCEMENT..."
enforce_timing_rules

echo ""
echo "After enforcement:"
./check_120_minute_timing_rules.sh
