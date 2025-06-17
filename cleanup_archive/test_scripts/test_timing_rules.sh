#\!/bin/bash

echo "=== TESTING 120-MINUTE TIMING RULES ==="
echo "User: Christian"
echo ""

# Test 1: TODO.md age check
echo "TEST 1: Checking TODO.md age (should be 180 minutes old)..."
if [ -f "TODO.md" ]; then
    last_modified=$(stat -c %Y TODO.md 2>/dev/null || stat -f %m TODO.md)
    current_time=$(date +%s)
    age_minutes=$(( (current_time - last_modified) / 60 ))
    
    echo "✓ TODO.md found"
    echo "  Age: $age_minutes minutes"
    
    if [ $age_minutes -gt 120 ]; then
        echo "  ⏰ TRIGGER: TODO.md is older than 120 minutes\!"
        echo "  ACTION REQUIRED: Update TODO.md immediately"
        
        # Test update would happen here
        echo -e "\n## Update Required - $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> TODO.md
        echo "User: Christian" >> TODO.md
        echo "Status: Timing rule triggered (was $age_minutes minutes old)" >> TODO.md
        
        echo "  ✓ TODO.md updated due to 120-minute rule"
    else
        echo "  ✓ TODO.md is current (less than 120 minutes old)"
    fi
else
    echo "  ✗ TODO.md not found - would create it"
fi

echo ""

# Test 2: Backup system check
echo "TEST 2: Checking backup system 120-minute rule..."
mkdir -p backups

if [ -f "backups/.last_scheduled_backup" ]; then
    last_backup=$(stat -c %Y backups/.last_scheduled_backup 2>/dev/null || stat -f %m backups/.last_scheduled_backup)
    current_time=$(date +%s)
    backup_age_minutes=$(( (current_time - last_backup) / 60 ))
    
    echo "✓ Backup marker found"
    echo "  Age: $backup_age_minutes minutes"
    
    if [ $backup_age_minutes -ge 120 ]; then
        echo "  ⏰ TRIGGER: Backup is older than 120 minutes\!"
        echo "  ACTION REQUIRED: Create new backup immediately"
        echo "  ✓ Backup would be created due to 120-minute rule"
    else
        echo "  ✓ Backup is current (less than 120 minutes old)"
    fi
else
    echo "  ✗ No backup system initialized"
    echo "  ACTION REQUIRED: Initialize backup system"
    touch backups/.last_scheduled_backup
    echo "  ✓ Backup system initialized"
fi

echo ""
echo "=== TIMING RULE TEST COMPLETE ==="
