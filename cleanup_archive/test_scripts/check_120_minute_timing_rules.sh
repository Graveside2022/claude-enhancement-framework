#\!/bin/bash

# Simplified 120-minute timing rule enforcement check
# Tests if timing rules trigger correctly without full procedure load

check_120_minute_timing_rules() {
    echo "⏰ MANDATORY 120-MINUTE TIMING RULE CHECK"
    echo "User: Christian"
    echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo ""
    
    local violations_found=false
    
    # CHECK 1: TODO.md age
    if [ -f "TODO.md" ]; then
        local last_modified=$(stat -c %Y TODO.md 2>/dev/null || stat -f %m TODO.md)
        local current_time=$(date +%s)
        local age_minutes=$(( (current_time - last_modified) / 60 ))
        
        echo "📝 TODO.md Check:"
        echo "   File age: $age_minutes minutes"
        
        if [ $age_minutes -gt 120 ]; then
            echo "   ⚠️  VIOLATION: TODO.md is $age_minutes minutes old (limit: 120)"
            echo "   🚨 ACTION: Update TODO.md IMMEDIATELY"
            violations_found=true
        else
            echo "   ✅ COMPLIANT: TODO.md is within 120-minute limit"
        fi
    else
        echo "📝 TODO.md Check:"
        echo "   ⚠️  VIOLATION: TODO.md does not exist"
        echo "   🚨 ACTION: Create TODO.md IMMEDIATELY"
        violations_found=true
    fi
    
    echo ""
    
    # CHECK 2: Backup system age
    if [ -f "backups/.last_scheduled_backup" ]; then
        local last_backup=$(stat -c %Y backups/.last_scheduled_backup 2>/dev/null || stat -f %m backups/.last_scheduled_backup)
        local current_time=$(date +%s)
        local backup_age_minutes=$(( (current_time - last_backup) / 60 ))
        
        echo "💾 Backup System Check:"
        echo "   Last backup: $backup_age_minutes minutes ago"
        
        if [ $backup_age_minutes -ge 120 ]; then
            echo "   ⚠️  VIOLATION: Backup is $backup_age_minutes minutes old (limit: 120)"
            echo "   🚨 ACTION: Create backup IMMEDIATELY"
            violations_found=true
        else
            echo "   ✅ COMPLIANT: Backup is within 120-minute limit"
        fi
    else
        echo "💾 Backup System Check:"
        echo "   ⚠️  VIOLATION: Backup system not initialized"
        echo "   🚨 ACTION: Initialize backup system IMMEDIATELY"
        violations_found=true
    fi
    
    echo ""
    
    # ENFORCEMENT SUMMARY
    if [ "$violations_found" = true ]; then
        echo "❌ TIMING RULE VIOLATIONS DETECTED"
        echo "⚡ These violations MUST be corrected before proceeding"
        echo "📋 Required actions listed above must execute immediately"
        return 1
    else
        echo "✅ ALL TIMING RULES COMPLIANT"
        echo "📋 No immediate actions required"
        return 0
    fi
}

# Execute the check
check_120_minute_timing_rules
